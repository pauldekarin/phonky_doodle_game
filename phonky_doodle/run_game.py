import subprocess
import sys

def main():
    script_path = './phonky_doodle/main.py'
    
    result = subprocess.run(['pgzrun', script_path], check=True)
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())