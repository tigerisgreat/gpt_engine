from utils import *

PROMPT_DISMISS_SELECTORS = [
    'button.btn-secondary:contains("Not now")',
    '//button[contains(text(), "Not now")]',
    '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div[2]/button/div',
    'button.btn-secondary:contains("Maybe later")',
    'button[type="button"]:contains("Maybe later")',
    'div:contains("Not now")',
    'div:contains("Close")',  # Add this
    'div:contains("Dismiss")',
    'div:contains("Maybe later")',
    'button:contains("Maybe later")',
    'button:contains("Not now")',
    'button[type="button"]:contains("Maybe later")', 
    '//button[contains(text(), "Maybe later")]',
    'button:contains("Open")',  # Add this
    'button:contains("Close")',  # Add this
    'button:contains("Dismiss")',  # Add this
    'button[aria-label="Close"]',
    'button[aria-label="Dismiss"]',
    'button[aria-label="Not now"]',
]

# 'div[role="dialog"] button',  # Any button in a dialog
#     '[role="dialog"] [aria-label="Close"]',
# 'button.close',
#     'button.dismiss',
#     '.modal-close',
#     '.popup-close',
#     'svg[aria-label="Close"]',  # SVG close icons
#     'button:nth-of-type(1)',  # First button (often close)

def is_popups_visible(sb, timeout=4, screenshot_name="closed_prompt"):
    """Try to detect and close popup prompts/buttons on the page."""
    sb.sleep(2)
    save_ss(sb,"Checking for a Pop up")
    import time
    import random
    t0 = time.time()
    closed_any = False
    while time.time() - t0 < timeout:
        for sel in PROMPT_DISMISS_SELECTORS:
            try:
                # visible() and click() are SeleniumBase builtins
                if sb.is_element_visible(sel):
                    
                    sb.highlight(sel)
                    sb.cdp.click(sel)
                    closed_any = True
                    save_ss(sb,"Pop closed")
                    print(f"::warning::[POP UP] Closed popup/button using selector: {sel}")
                    # sb.save_screenshot(screenshot_name)
                    sb.sleep(3)  # Pause after closing
                      
            except Exception:
                continue
        sb.sleep(random.uniform(0.4, 0.8))
        if closed_any==True:
            save_ss(sb,"Closed_any variable is true so a Pop was closed")
    return closed_any
