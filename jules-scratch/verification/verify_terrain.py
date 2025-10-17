from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Increase timeout to handle potentially slow loading of the game
    page.set_default_timeout(60000)

    try:
        # Block external network calls that can hang the game
        page.route("**/*", lambda route: route.abort() if "p2fk.io" in route.request.url or "ipfs.io" in route.request.url else route.continue_())

        # Navigate to the game
        page.goto("http://localhost:8000", wait_until="domcontentloaded")

        # Enter world and user name
        page.fill("#worldNameInput", "VolcanoTest")
        page.fill("#userInput", "Jules")

        # Click the start button
        page.click("#startBtn")

        # The external calls are blocked, so the loading overlay might not hide automatically.
        # We'll manually hide it and show the game HUD.
        page.evaluate("document.getElementById('loginOverlay').style.display = 'none';")
        page.evaluate("document.getElementById('hud').style.display = 'block';")
        page.evaluate("document.getElementById('hotbar').style.display = 'flex';")
        page.evaluate("document.getElementById('rightPanel').style.display = 'flex';")

        # Wait a few seconds for the terrain to generate and render
        page.wait_for_timeout(8000) # Increased wait time for complex terrain

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot even if there's an error to help with debugging
        page.screenshot(path="jules-scratch/verification/error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)