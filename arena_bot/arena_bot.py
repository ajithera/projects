from playwright.sync_api import sync_playwright, expect
import random
import json
import time

def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

def main():
    questions = load_questions()
    random.shuffle(questions)  # Shuffle once to avoid repeats

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        page.goto("https://www.eduarena.ai/")

        # Define a specific locator for the main question input area.
        # This is important to distinguish it from the feedback textarea.
        # You may need to adjust this selector by inspecting the page.
        main_question_input_selector = "textarea[placeholder='Ask Anything']"

        for i, q in enumerate(questions[:75]):
            # Use the specific selector to ensure we're filling the correct box
            page.fill(main_question_input_selector, q['question'])
            page.keyboard.press("Enter")

            # Wait for answers to load
            # page.wait_for_selector("text=Left is better", timeout=150000)
            # page.reload()
            # page.wait_for_selector("text=Left is better", timeout=75000)

            page.wait_for_selector("text=A is better", timeout=150000)
            page.reload()
            page.wait_for_selector("text=A is better", timeout=75000)


            # Select answer randomly
            option = random.choice(["Left", "Right", "Tie", "BothBad"])
            # option_map = {
            #     "Left": "text=Left is better",
            #     "Right": "text=Right is better",
            #     "Tie": "text=It's a tie",
            #     "BothBad": "text=Both are bad"
            # }
            option_map = {
                "Left": "text=A is better",
                "Right": "text=B is better",
                "Tie": "text=Tie",
                "BothBad": "text=Both are bad"
            }
            page.click(option_map[option])

            page.wait_for_timeout(2000)

            # Select reason
            reason = random.choice(["Correctness", "Clarity", "Completeness", "Style"])
            page.wait_for_timeout(2000)
            
            page.click(f"text={reason}")

            page.wait_for_timeout(2000)
            # Tab clicks to reach feedback box depending on reason
            reason_tab_map = {
                "Correctness": 4,
                "Clarity": 3,
                "Completeness": 2,
                "Style": 1
            }

            for _ in range(reason_tab_map[reason]):
                page.keyboard.press("Tab")
            
            page.wait_for_timeout(1000)

            # Optional feedback
            if True:
                feedback = random.choice(q["feedback"])
                page.keyboard.type(feedback)

            # --- START OF ROBUST SUBMISSION LOGIC ---

            # 1. Use a direct locator to click the submit button. This is far more
            #    reliable than tabbing and pressing Enter.
            #    You may need to inspect the page to get the correct selector.
            #    A common selector is a button that contains the text "Submit".
            page.wait_for_timeout(2000)
            page.click("button:has-text('Submit')")
            page.keyboard.press("Enter")
            page.keyboard.press("Enter")
            page.keyboard.press("Enter")
            page.keyboard.press("Enter")


            # 2. CRITICAL: Wait for the page to reset and the main question box
            #    to be visible again. This SYNCHRONIZES the script with the browser,
            #    guaranteeing it's ready for the next loop iteration.
            # page.wait_for_selector(main_question_input_selector, state="visible", timeout=60000)

            # You can still add a small random delay to appear more human.
            time.sleep(random.randint(2, 5))

            # --- END OF ROBUST SUBMISSION LOGIC ---

        browser.close()


if __name__ == "__main__":
    main()
