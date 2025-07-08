import subprocess
import sys
import os


def send_broadcast_by_id(mailing_id: int) -> None:
    python_path = sys.executable
    command_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../management/run_broadcast.py"
        )
    )

    subprocess.Popen([python_path, command_path, str(mailing_id)])
