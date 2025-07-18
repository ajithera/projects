from playwright.sync_api import sync_playwright
import time

def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.eduarena.ai/")

        # Click age group
        page.click("text=18-20")
        time.sleep(1)

        # Click login with Google
        page.click("text=Continue with Google")

        # --- NOW WAIT FOR YOU TO LOGIN MANUALLY IN THE BROWSER ---
        print("Please log in manually. You have 60 seconds...")
        time.sleep(60)

        # Save the authenticated session to a file
        context.storage_state(path="auth.json")
        print("✅ Session saved to auth.json")
        browser.close()

if __name__ == "__main__":
    save_login_session()