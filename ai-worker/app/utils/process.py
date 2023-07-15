import subprocess


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Read from stdout and stderr
    stdout, stderr = p.communicate()

    exit_code = p.wait()
    # Convert byte stream to string
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")

    return stdout, stderr, exit_code
