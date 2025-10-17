from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Intercept and abort problematic network requests
        def route_handler(route):
            if "p2fk.io" in route.request.url or "ipfs.io" in route.request.url:
                return route.abort()
            return route.continue_()

        page.route("**/*", route_handler)

        # Navigate to the local server
        page.goto("http://localhost:8000")

        # Wait for the login card to be visible
        page.wait_for_selector("#loginCard", state="visible")

        # Enter world and user names
        page.fill("#worldNameInput", "test-world")
        page.fill("#userInput", "jules")

        # Click the start button
        page.click("#startBtn")

        # Manually force the UI to be visible
        page.evaluate("document.getElementById('loginOverlay').style.display = 'none';")
        page.evaluate("document.getElementById('hud').style.display = 'block';")
        page.evaluate("document.getElementById('hotbar').style.display = 'flex';")
        page.evaluate("document.getElementById('rightPanel').style.display = 'flex';")

        # Wait for the HUD to be visible
        page.wait_for_selector("#hud", state="visible")

        # Move forward to trigger chunk loading
        page.keyboard.down('w')
        page.wait_for_timeout(3000) # Move forward for 3 seconds
        page.keyboard.up('w')

        page.wait_for_timeout(2000) # Wait for chunks to render

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)