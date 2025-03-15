import os
import sys
import subprocess
import time

# Define ANSI color codes for colored terminal output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run_command(command, silent=True):
    """
    Runs a shell command silently in the background unless there's an error.

    Parameters:
    - command (str): The shell command to execute.
    - silent (bool): If True, suppresses output unless an error occurs.
    """
    stdout_dest = subprocess.DEVNULL if silent else None
    stderr_dest = subprocess.DEVNULL if silent else None

    result = subprocess.run(command, shell=True, stdout=stdout_dest, stderr=stderr_dest)
    if result.returncode != 0:
        print(f"\n{RED}Error running command: {command}{RESET}")
        sys.exit(1)


def progress_bar(task_name, duration=5):
    """
    Displays a loading bar for the given task.

    Parameters:
    - task_name (str): The name of the task being executed.
    - duration (int): Time in seconds for the progress bar animation.
    """
    bar_length = 50
    print(f"{YELLOW}{task_name}{RESET} [", end="", flush=True)

    for _ in range(bar_length):
        time.sleep(duration / 100)  # Faster but still visible progress
        print("=", end="", flush=True)

    print(f"] {GREEN}Success{RESET}")  # End progress bar


# Check if virtual environment exists, if not, create one
if not os.path.exists("venv"):
    progress_bar("Creating virtual environment      ", duration=2)
    run_command("python -m venv venv")

# Install required dependencies inside the virtual environment (including Jinja2)
run_command(
    "venv/bin/python -m pip install --upgrade pip pyqt6 pyqtgraph markdown2 jinja2 || "
    "venv\\Scripts\\python.exe -m pip install --upgrade pip pyqt6 pyqtgraph markdown2 jinja2"
)

# Display progress bar for dependency installation
progress_bar("Installing Python dependencies    ")

# Get the list of installed libraries in the virtual environment
installed_libraries = subprocess.run(
    "venv/bin/python -m pip freeze || venv\\Scripts\\python.exe -m pip freeze",
    shell=True,
    capture_output=True,
    text=True,
).stdout.splitlines()

# Print installed libraries
print(f"\n{GREEN}Installed Libraries:{RESET}")
for lib in installed_libraries:
    print(f"  - {lib}")

# Print virtual environment activation instructions
print(
    f"\n{GREEN}Setup complete! You can now start developing your note-taking app!{RESET}"
)

print(
    "\nTo activate the virtual environment, use the appropriate command for your OS:\n"
)
print(f"   {BLUE}For Linux/macOS (bash/zsh):{RESET}")
print("     source venv/bin/activate\n")
print(f"   {BLUE}For Windows (Command Prompt - CMD):{RESET}")
print("     venv\\Scripts\\activate\n")
print(f"   {BLUE}For Windows (PowerShell):{RESET}")
print("     venv\\Scripts\\Activate.ps1\n")
print(f"   {BLUE}For Fish Shell:{RESET}")
print("     source venv/bin/activate.fish\n")
