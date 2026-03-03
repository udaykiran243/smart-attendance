import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.api.routes import attendance

# Standard synchronous client for WebSocket testing
@pytest.fixture
def client_sync(app):
    return TestClient(app)

def test_attendance_websocket_flow(client_sync):
    """
    Test the full WebSocket flow:
    1. Connect with token
    2. Send image frame
    3. Receive status updates (processing -> detected -> match -> complete)
    """
    
    with patch("app.api.routes.attendance.decode_jwt") as mock_decode, \
         patch("app.api.routes.attendance.ml_client") as mock_ml, \
         patch("app.api.routes.attendance.db") as mock_db:

        # Mock JWT
        mock_decode.return_value = {
            "user_id": "507f1f77bcf86cd799439011", 
            "role": "teacher" # Role must be teacher/admin
        }
        
        # Mock ML detect
        mock_ml.detect_faces = AsyncMock(return_value={
            "success": True,
            "faces": [{
                "embedding": [0.1] * 128, 
                "location": {"top": 10, "right": 100, "bottom": 100, "left": 10},
                "is_live": True
            }]
        })
        
        # Mock ML match
        mock_ml.match_faces = AsyncMock(return_value={
            "success": True,
            "match": {"student_id": "507f1f77bcf86cd799439033", "distance": 0.1, "status": "present"}
        })
        mock_ml.batch_match = AsyncMock(return_value={
            "success": True, 
            "matches": [{
                "student_id": "507f1f77bcf86cd799439033", 
                "distance": 0.1, 
                "status": "present"
            }]
        })
        
        # Mock DB Subject
        mock_db.subjects.find_one = AsyncMock(return_value={
            "_id": "507f1f77bcf86cd799439022",
            "students": [
                {"student_id": "507f1f77bcf86cd799439033", "verified": True}
            ]
        })
        
        # Mock DB Students
        student_obj = {
             "userId": "507f1f77bcf86cd799439033",
             "name": "Test Student",
             "face_embeddings": [[0.1]*128],
             "_id": "507f1f77bcf86cd799439033",
             "roll_number": "123"
        }
        
        mock_cursor = AsyncMock()
        mock_cursor.to_list = AsyncMock(return_value=[student_obj])
        mock_db.students.find.return_value = mock_cursor

        # Test
        # Token is required
        token = "valid_token"
        
        # We need to use `client_sync` from fixture
        # Note: `attendance` router prefix is `/attendance`
        with client_sync as client:
            with client.websocket_connect(f"/attendance/ws/session_123?token={token}") as websocket:
                websocket.send_json({
                    "command": "process_frame",
                    "image": "data:image/jpeg;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
                    "subject_id": "507f1f77bcf86cd799439022"
                })
                
                # 1. Processing
                data = websocket.receive_json()
                assert data["status"] == "processing"
                
                # 2. Detected
                data = websocket.receive_json()
                assert data["status"] == "detected"
                assert data["count"] == 1
                
                # 3. Match Update
                data = websocket.receive_json()
                assert data["status"] == "match_update"
                assert data["match"]["student"]["name"] == "Test Student"
                assert data["match"]["status"] == "present"
                
                # 4. Complete
                data = websocket.receive_json()
                assert data["status"] == "complete"
                assert data["count"] == 1
