import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        # Launch a browser with touch simulation
        browser = await p.chromium.launch()
        context = await browser.new_context(has_touch=True)
        page = await context.new_page()

        # Navigate to the local index.html file
        await page.goto(f"file://{os.path.abspath('index.html')}")

        # Get the first app icon
        app_icon = page.locator(".app-icon").first
        screenshot_image = page.locator("#appScreenshot")

        # First tap: Check if the screenshot is displayed
        await app_icon.tap()
        await expect(screenshot_image).to_have_attribute("src", "assets/app_screenshots/nix_screenshot.png")

        # Second tap: Check if a new page is opened (navigation)
        async with context.expect_page() as new_page_info:
            await app_icon.tap()
        new_page = await new_page_info.value
        await expect(new_page).to_have_url("https://github.com/BawiCeu16/nix")

        await browser.close()

asyncio.run(main())
