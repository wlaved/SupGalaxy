import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Abort network requests to external services to prevent hanging
        await page.route("**/*.png", lambda route: route.abort())
        await page.route("**/*.jpg", lambda route: route.abort())
        await page.route("**/p2fk.io/**", lambda route: route.abort())
        await page.route("**/ipfs.io/**", lambda route: route.abort())
        await page.route("**/google.com/**", lambda route: route.abort())

        # Start the game
        await page.goto(f"file://{os.getcwd()}/index.html")

        # Enter world and user names
        await page.fill("#worldNameInput", "test")
        await page.fill("#userInput", "jules")
        await page.click("#startBtn")

        # Wait for the game to load
        await page.wait_for_selector("#hud", state="visible")

        # Move the player to trigger mob kiting behavior
        await page.keyboard.down("w")
        await asyncio.sleep(1)
        await page.keyboard.up("w")

        # Wait for the mob to initiate a laser attack
        await asyncio.sleep(5)

        # Take a final screenshot to show the laser attack
        await page.screenshot(path="jules-scratch/verification/mob_final.png")

        await browser.close()

if __name__ == "__main__":
    import os
    asyncio.run(main())