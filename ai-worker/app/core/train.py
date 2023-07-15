import os
import subprocess
from app.utils.process import run_command


def write_training_file(file_contents: str):
    script_path = "/app/builder_train.py"
    file = os.open(
        script_path,
        flags=(
            os.O_RDWR
            | os.O_CREAT  # create if not exists
            | os.O_TRUNC  # truncate the file to zero
        ),
        mode=0o777,
    )

    with open(script_path, "w") as file:
        file.write(file_contents)
    return script_path


def start_training_file(script_path: str):
    command = ["python", script_path]

    return run_command(command)
