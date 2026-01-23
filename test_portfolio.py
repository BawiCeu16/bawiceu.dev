import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def absolute_path(file_path):
    return f"file://{os.path.abspath(file_path)}"

def test_placeholder_visibility_and_desktop_hover(page):
    """
    Verify that the placeholder text is visible on initial load and that the hover
    effect works as expected on desktop.
    """
    page.goto(absolute_path("index.html"))

    # Verify placeholder is visible initially
    placeholder = page.locator(".placeholder-text")
    expect(placeholder).to_be_visible()

    # Verify screenshot src is initially empty
    screenshot = page.locator("#appScreenshot")
    expect(screenshot).to_have_attribute("src", "")

    # Simulate hover over the first app icon
    first_icon = page.locator(".app-icon").first
    first_icon.hover()

    # Verify screenshot becomes visible and placeholder is hidden
    expect(screenshot).to_be_visible()
    expect(placeholder).not_to_be_visible()

    # Verify the screenshot source is correct
    expected_src = first_icon.get_attribute("data-screenshot")
    expect(screenshot).to_have_attribute("src", expected_src)

def test_mobile_tap_to_preview_and_navigate(browser):
    """
    Verify that the tap-to-preview and tap-to-navigate functionality works as
    expected on a touch-enabled device.
    """
    # Simulate a touch device
    context = browser.new_context(has_touch=True)
    page = context.new_page()
    page.goto(absolute_path("index.html"))

    first_icon = page.locator(".app-icon").first
    screenshot = page.locator("#appScreenshot")
    placeholder = page.locator(".placeholder-text")

    # First tap: Preview
    first_icon.tap()
    expect(screenshot).to_be_visible()
    expect(placeholder).not_to_be_visible()

    # Second tap: Navigate
    with context.expect_page() as new_page_info:
        first_icon.tap()
    new_page = new_page_info.value
    assert "github.com" in new_page.url

    context.close()
