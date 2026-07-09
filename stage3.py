import subprocess
import sys
from pathlib import Path

def execute_code(code: str) -> dict:
    """
    Execute Python code as a separate subprocess using pathlib.
    """
    # 1. Write code to file using pathlib
    filepath = Path("generated.py")
    filepath.write_text(code)
    
    # 2. Run the file
    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False
        }
        
    except subprocess.TimeoutExpired:
        return {
            # "exit_code": -1,
            "stdout": "",
            "stderr": "Process timed out after 10 seconds",
            "timed_out": True
        }
    
    # finally:
    #     # Optional: clean up the file after execution
    #     if filepath.exists():
    #         filepath.unlink()