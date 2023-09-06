
import subprocess

def is_docker_installed():
    try:
        subprocess.check_output(["docker", "--version"])
        return True
    except FileNotFoundError:
        return False
