from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Abort network requests to external services that can hang tests.
        page.route("**/*.{png,jpg,jpeg,mp3,ico}", lambda route: route.abort())
        page.route(
            lambda url: "p2fk.io" in url or "ipfs.io" in url,
            lambda route: route.abort()
        )

        try:
            # Navigate to the local game file.
            page.goto("http://localhost:8000/index.html", timeout=60000)

            # Wait for the login screen to be visible.
            expect(page.locator("#loginOverlay")).to_be_visible(timeout=30000)

            # If the login UI is still obscured, force it visible.
            if page.locator("#loginCard").is_hidden():
                page.evaluate("document.getElementById('loginOverlay').style.display = 'none'")
                page.evaluate("document.getElementById('hud').style.display = 'block'")

            # Enter world and username.
            page.fill("#worldNameInput", "test_world")
            page.fill("#userInput", "test_user")

            # Click the start button.
            page.click("#startBtn")

            # Force the HUD to be visible for the screenshot.
            page.evaluate("document.getElementById('loginOverlay').style.display = 'none'")
            page.evaluate("document.getElementById('hud').style.display = 'block'")
            page.evaluate("document.getElementById('rightPanel').style.display = 'flex'")

            # Wait for a moment to ensure the game loop starts and mobs can spawn.
            page.wait_for_timeout(2000)

            # Press 'g' to spawn a mob, which should also ensure the world is rendered.
            page.keyboard.press('g')

            # Wait for the mob to appear.
            page.wait_for_timeout(10000)

            # Take a screenshot to verify mobs have spawned.
            page.screenshot(path="jules-scratch/verification/mobs_spawned.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error_screenshot.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()