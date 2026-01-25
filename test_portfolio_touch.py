import os
import pytest
from playwright.sync_api import Page, expect

def test_touch_interaction(page: Page, browser):
    # Simulate a touch-enabled device
    context = browser.new_context(has_touch=True)
    page = context.new_page()

    # Navigate to the local HTML file
    file_path = os.path.abspath('index.html')
    page.goto(f'file://{file_path}')

    # Get the first project icon
    first_icon = page.locator('.app-icon').first
    screenshot_image = page.locator('#appScreenshot')

    expected_screenshot_src = first_icon.get_attribute('data-screenshot')
    expected_href = first_icon.get_attribute('href')

    # --- First Tap: Preview ---
    first_icon.click()

    # Wait for the image src to be updated
    expect(screenshot_image).to_have_attribute('src', expected_screenshot_src)

    # --- Second Tap: Navigate ---
    # Start waiting for the new page before clicking
    with context.expect_page() as new_page_info:
        first_icon.click()  # Second click should trigger navigation

    new_page = new_page_info.value
    # Wait for the new page to load
    new_page.wait_for_load_state()

    # Assert that the new page has the correct URL
    assert new_page.url == expected_href

    # Clean up
    context.close()
