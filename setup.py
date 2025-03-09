import os
import sys
import subprocess
import time

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def run_command(command, silent=True):
    """Runs a shell command silently in the background unless there's an error."""
    stdout_dest = subprocess.DEVNULL if silent else None
    stderr_dest = subprocess.DEVNULL if silent else None

    result = subprocess.run(command, shell=True, stdout=stdout_dest, stderr=stderr_dest)
    if result.returncode != 0:
        print(f"\n{RED}Error running command: {command}{RESET}")
        sys.exit(1)


def progress_bar(task_name, duration=5):
    """Displays a loading bar for the given task."""
    bar_length = 50
    print(f"{task_name} [", end="", flush=True)

    for _ in range(bar_length):
        time.sleep(duration / 100)  # Faster but still visible progress
        print("=", end="", flush=True)

    print(f"] {GREEN}Success{RESET}")  # End progress bar


# Create virtual environment
if not os.path.exists("venv"):
    progress_bar("Creating virtual environment")
    run_command("python -m venv venv")

# Install Python dependencies inside venv silently
progress_bar("Installing Python dependencies")
run_command(
    "venv/bin/python -m pip install --upgrade pip pyqt6 pyqtgraph markdown2 || venv\\Scripts\\python.exe -m pip install --upgrade pip pyqt6 pyqtgraph markdown2"
)

# Get the list of installed libraries
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
print("   For Linux/macOS (bash/zsh):")
print("     source venv/bin/activate\n")
print("   For Windows (Command Prompt - CMD):")
print("     venv\\Scripts\\activate\n")
print("   For Windows (PowerShell):")
print("     venv\\Scripts\\Activate.ps1\n")
print("   For Fish Shell:")
print("     source venv/bin/activate.fish\n")
