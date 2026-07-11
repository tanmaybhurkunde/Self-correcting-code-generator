import re
from llm_utils import extract_code , ask_model_with_history, execute_code


def output_matches(expected, actual):
    """Check if actual output matches expected value (robustly)."""
    expected_clean = expected.strip()
    actual_clean = actual.strip()
    
    # Exact match (ignoring trailing whitespace)
    if actual_clean == expected_clean:
        return True
    
    # Check last line (common for print statements)
    lines = actual_clean.split('\n')
    if lines and lines[-1].strip() == expected_clean:
        return True
    
    # Check if expected appears as a whole word/number in the output
    # Using regex to avoid substring false positives
    pattern = r'\b' + re.escape(expected_clean) + r'\b'
    if re.search(pattern, actual_clean):
        return True
    
    return False

def build_execution_error_message(result):
    error_parts = []
    if result["exit_code"] is not None and result["exit_code"] != 0:
        error_parts.append(f"Exit code: {result['exit_code']}")
    if result["stderr"]:
        error_parts.append(f"Error output: {result['stderr'][:500]}")
    if result["timed_out"]:
        error_parts.append("Timed out after 10 seconds")
    if result["stdout"] and not result["stderr"]:
        error_parts.append(f"Unexpected output: {result['stdout'][:200]}")
    
    return " | ".join(error_parts) if error_parts else "Execution failed with no error details"

def build_wrong_output_message(actual):
    """Builds a message for when code runs but output doesn't match.
    Does NOT include the expected output - the model should figure it out."""
    actual_clean = actual.strip()[:200]
    return f"Your code ran without errors, but the output was '{actual_clean}' which was incorrect. The logic needs to be fixed."

def run_loop(task, expected_output=None, max_iterations=5):
    # Initialize conversation history - DON'T include expected output
    messages = [
        {"role": "system", "content": "You are a Python expert. Write clean, working Python code to solve the given task. Only respond with code in markdown code blocks."},
        {"role": "user", "content": task}
    ]
    
    for attempt in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"Attempt {attempt + 1}/{max_iterations}")
        print('='*60)
        
        response = ask_model_with_history(messages)
        print("🤖 Model response received")
        
        code = extract_code(response)
        
        if not code:
            print("❌ No code block found in response")
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": "Your response didn't include a code block with the solution. Please provide the complete Python code in a ```python ... ``` block."})
            continue
        
        print(f"📝 Code extracted ({len(code)} characters)")
        
        result = execute_code(code)
        
        ran_cleanly = result["exit_code"] == 0 and not result["stderr"]
        success = False
        failure_reason = None
        
        if not ran_cleanly:
            failure_reason = build_execution_error_message(result)
            print(f"❌ Execution failed (attempt {attempt + 1})")
            print(f"Error details: {failure_reason}")
            
        elif expected_output is not None:
            if output_matches(expected_output, result["stdout"]):
                success = True
                print("✅ Success! Code executed cleanly with correct output.")
            else:
                failure_reason = build_wrong_output_message(result["stdout"])
                print(f"❌ Output mismatch (attempt {attempt + 1})")
                print(f"Expected something matching: '{expected_output[:50]}...'")
                print(f"Got: '{result['stdout'][:100]}...'" if len(result['stdout']) > 100 else f"Got: '{result['stdout']}'")
        else:
            success = True
            print("✅ Success! Code executed without errors.")
        
        if success:
            output_preview = result["stdout"][:200] + "..." if len(result["stdout"]) > 200 else result["stdout"]
            print(f"Output: {output_preview}")
            
            return {
                "success": True,
                "code": code,
                "output": result["stdout"],
                "attempts": attempt + 1
            }
        else:
            messages.append({"role": "assistant", "content": response})
            
            feedback = f"The code execution failed. {failure_reason}\n\n"
            feedback += "Please fix the code and try again. Make sure to:\n"
            feedback += "- Include proper error handling\n"
            feedback += "- Make sure all imports are included\n"
            feedback += "- Print the output so we can verify it works\n"
            feedback += "- Check your logic for edge cases\n\n"
            feedback += f"Here's the code that failed:\n```python\n{code}\n```"
            
            messages.append({"role": "user", "content": feedback})
    
    print(f"\n❌ Failed after {max_iterations} attempts")
    return {
        "success": False,
        "attempts": max_iterations,
        "last_code": code if 'code' in locals() else None,
        "last_error": result if 'result' in locals() else "No execution result"
    }

if __name__ == "__main__":
    print("TEST 1: Median")
    print("="*60)
    
    result = run_loop(
        "Write a Python function that takes a list of numbers and returns the median. Print the median for [1, 3, 2, 4, 5]",
        expected_output="3",
        max_iterations=3
    )
    
    if result["success"]:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(result["code"])
        print("\nOutput:")
        print(result["output"])
    
    print("\n" + "\n" + "="*60)
    print("TEST 2: Second Largest")
    print("="*60)
    
    result2 = run_loop(
        "Write a function that returns the second largest number in a list. Print the result for [3, 1, 4, 1, 5, 9, 2, 6, 5]",
        expected_output="6",
        max_iterations=3
    )
    
    if result2["success"]:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(result2["code"])
        print("\nOutput:")
        print(result2["output"])