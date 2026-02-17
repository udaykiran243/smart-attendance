from unittest.mock import patch, MagicMock

from app.core.scheduler import start_scheduler, shutdown_scheduler, scheduler


def test_scheduler_starts_and_shuts_down():
    """Verify the scheduler can start and shut down without errors."""
    with patch.object(scheduler, "start") as mock_start:
        start_scheduler()
        mock_start.assert_called_once()
    shutdown_scheduler()


def test_scheduler_double_shutdown():
    """Shutting down an already stopped scheduler should not error."""
    shutdown_scheduler()
