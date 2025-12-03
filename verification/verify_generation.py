
from playwright.sync_api import sync_playwright
import time

def verify_generation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a user agent to ensure we are not treated as a bot
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        # Attach console listener to catch worker errors
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page error: {err.message}"))

        print("Navigating to game...")
        try:
            page.goto("http://localhost:8000")
        except Exception as e:
            print(f"Navigation failed: {e}")
            return

        # Login flow
        print("Logging in...")
        try:
            page.wait_for_selector("#worldNameInput", state="visible")
            page.fill("#worldNameInput", "Earth")
            page.fill("#userInput", "Tester")

            # Wait for playBtn to be potentially hidden by autocomplete, then force click
            page.wait_for_selector("#startBtn", state="visible") # ID confirmed from index.html
            page.evaluate("document.getElementById(\"startBtn\").click()")
        except Exception as e:
            print(f"Login failed: {e}")
            page.screenshot(path="verification/login_failed.png")
            return

        # Wait for game to load (HUD visible)
        print("Waiting for game HUD...")
        try:
            # wait for #hud to be attached to dom, display might still be none initially
            page.wait_for_selector("#hud", state="attached", timeout=60000)

            # Wait until login overlay is hidden
            page.wait_for_function("document.getElementById(\"loginOverlay\").style.display === \"none\"", timeout=60000)
        except Exception as e:
            print(f"HUD did not appear or Login Overlay did not hide: {e}")
            page.screenshot(path="verification/failed_load.png")
            return

        print("Game loaded. Waiting for chunks to generate...")
        # Wait a bit for chunks to render
        time.sleep(15)

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/terrain_generation.png")
        print("Screenshot saved to verification/terrain_generation.png")

        browser.close()

if __name__ == "__main__":
    verify_generation()
