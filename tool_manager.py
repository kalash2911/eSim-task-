import shutil
import subprocess
import platform
import os

#log file to save everything (checks/errors etc)
LOG_FILE = "tool_manager.log"

def log(message):
    #Logs message to both console and log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

#Check if tool is in PATH
def check_tool(tool_name):
    return shutil.which(tool_name) is not None

#try installing tool (Windows = choco & Linux = apt)
def install_tool(tool_name):
    system = platform.system()
    try:
        if system == "Windows":
            log(f"Installing {tool_name} using Chocolatey...")
            subprocess.run(["choco", "install", tool_name, "-y"], check=True)
        elif system == "Linux":
            log(f"Installing {tool_name} using apt...")
            subprocess.run(["sudo", "apt", "install", "-y", tool_name], check=True)
        else:
            log(f"Unsupported system: {system}")
    except Exception as e:
        log(f"Error installing {tool_name}: {e}")

#get version of tool
def check_version(tool_name):
    try:
        result = subprocess.run([tool_name, "-v"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "ngspice-" in line:   # filter only version line
                    log(f"{tool_name} version: {line.strip()}")
                    break
        else:
            log(f"Could not fetch version for {tool_name}")
    except FileNotFoundError:
        log(f"{tool_name} not installed.")


if __name__ == "__main__":
    tool = "ngspice"

    log(f"Checking {tool}...")
    if check_tool(tool):
        log(f"{tool} is already installed")
        check_version(tool)
    else:
        log(f"{tool} not found")
        install_tool(tool)
        if check_tool(tool):
            check_version(tool)
import subprocess

result = subprocess.run(['ngspice', '-v'], capture_output=True, text=True)
print(result.stdout)
