import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Self-correcting code agent - generates and fixes Python code until it works"
    )
    
    parser.add_argument(
        "--task", 
        required=True, 
        help="The programming task to solve (describe what the code should do)"
    )
    
    parser.add_argument(
        "--expected", 
        default=None, 
        help="Expected output string to validate against (optional)"
    )
    
    parser.add_argument(
        "--max-iterations", 
        type=int, 
        default=5, 
        help="Maximum number of attempts (default: 5)"
    )
    
    return parser.parse_args()