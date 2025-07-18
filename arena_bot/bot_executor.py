import subprocess

MAX_ITERATIONS = 30
MAX_CONSECUTIVE_FAILURES = 10
TARGET_SCRIPT = "arena_bot.py"  # Replace with the name of your script

def run_target_script():
    try:
        result = subprocess.run(["python", TARGET_SCRIPT], check=True)
        return True  # Success
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}")
        return False  # Failure

def main():
    consecutive_failures = 0

    for i in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {i} ---")

        success = run_target_script()

        if success:
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            print(f"Consecutive failures: {consecutive_failures}")

            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print("❌ Execution failed 3 times in a row. Stopping program.")
                break

if __name__ == "__main__":
    main()
