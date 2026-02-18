# MediaPipe Model Setup

## BlazeFace Short Range Model

This service requires the MediaPipe BlazeFace Short Range model for face detection.

### Automatic Download (Recommended)

The model is automatically downloaded during Docker build using the `download_models.py` script.

**In Dockerfile:**
```dockerfile
RUN python3 download_models.py
```

This downloads `blaze_face_short_range.tflite` to `/app/app/ml/` during the build process.

### Manual Download (Development)

If you're running locally and the automatic download fails:

1. **Option 1: Run the download script**
   ```bash
   cd server/ml-service
   python3 download_models.py
   ```

2. **Option 2: Manual download from MediaPipe**
   - Visit: https://developers.google.com/mediapipe/solutions/vision/face_detector
   - Or: https://github.com/google/mediapipe
   - Download `blaze_face_short_range.tflite`
   - Place it in `server/ml-service/app/ml/`

3. **Option 3: Use wget/curl**
   ```bash
   cd server/ml-service/app/ml/
   wget https://storage.googleapis.com/mediapipe-assets/blaze_face_short_range.tflite
   ```

### Verification

After downloading, verify the model file exists:
```bash
ls -lh server/ml-service/app/ml/*.tflite
```

You should see:
```
blaze_face_short_range.tflite  (~200-300 KB)
```

### Troubleshooting

**FileNotFoundError in Docker:**
- Ensure the download script runs successfully during build
- Check Docker build logs for any download errors
- Verify `.dockerignore` doesn't exclude `.tflite` files

**403 Forbidden errors:**
- This is normal in restricted network environments
- The script tries multiple mirror URLs automatically
- In production (Render), downloads should work fine
- For local development, use manual download option

**Model file missing after build:**
- Check if `.gitignore` excludes `.tflite` files (it shouldn't)
- Ensure Dockerfile includes `RUN python3 download_models.py`
- Rebuild the Docker image: `docker build --no-cache .`

### Why Not Commit the Model?

The model file (~300KB) could be committed to git, but:
- Keeps repository size smaller
- Allows easy model updates
- Follows MediaPipe best practices
- Model is downloaded once during build, then cached in Docker layers

If you prefer to commit it, add the file to git and the Dockerfile will use it automatically (the download script checks if file exists first).
