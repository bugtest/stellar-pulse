"""StellarPulse - Task Runner."""

import asyncio
import subprocess
import shlex
from datetime import datetime
from typing import Optional


class TaskRunner:
    """Task execution engine."""

    def __init__(self):
        self.running_tasks = {}

    async def run_script(
        self,
        script: str,
        script_type: str = "bash",
        timeout: int = 300,
        env: dict = None
    ) -> dict:
        """Run a script."""

        cmd = None
        if script_type == "bash":
            cmd = ["bash", "-c", script]
        elif script_type == "python":
            cmd = ["python3", "-c", script]
        elif script_type == "shell":
            cmd = shlex.split(script)

        if not cmd:
            return {
                "status": "failed",
                "stdout": "",
                "stderr": f"Unsupported script type: {script_type}",
                "exit_code": 1,
                "duration": 0
            }

        start_time = datetime.utcnow()

        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(
                    subprocess.run,
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env or {}
                ),
                timeout=timeout
            )

            duration = (datetime.utcnow() - start_time).total_seconds()

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "duration": duration
            }

        except asyncio.TimeoutError:
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {
                "status": "failed",
                "stdout": "",
                "stderr": f"Task timeout after {timeout} seconds",
                "exit_code": 124,
                "duration": duration
            }
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {
                "status": "failed",
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1,
                "duration": duration
            }


# Global runner
_task_runner = None


def get_task_runner() -> TaskRunner:
    """Get task runner instance."""
    global _task_runner
    if _task_runner is None:
        _task_runner = TaskRunner()
    return _task_runner
