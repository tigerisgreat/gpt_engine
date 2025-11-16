from utils import * 
from is_pop_ups import *

SEND_SELECTORS = [
    'button[data-testid="send-button"]',
    'button[aria-label="Send message"]',
    'button[aria-label="Send"]',
    'button:has(svg[aria-label="Send"])',
]

def send_prompt(sb):
    popups=is_popups_visible(sb)
    print("I am here")
    for sel in SEND_SELECTORS:
        try:
            sb.sleep(2)
            popups=is_popups_visible(sb)
            sb.cdp.wait_for_element_visible(sel, timeout=7)
            sb.scroll_into_view(sel)
            short_sleep_dbg(sb, label=f"after scroll to {sel}")
            sb.cdp.click(sel)
            short_sleep_dbg(sb, label=f"after click {sel}")
            print(f"[DEBUG] Send clicked via {sel}")
            return True
        except Exception as e:
            print(f"[SEND][WARN] {sel} not clickable/visible yet: {e}")
            save_ss(sb, "Not visible")

    # Fallback: Enter
    try:
        sb.cdp.click("#prompt-textarea")
        short_sleep_dbg(sb, label="before Enter fallback")
        sb.cdp.press_keys("#prompt-textarea", "Enter")
        short_sleep_dbg(sb, label="after Enter fallback")
        print("[DEBUG] Send via Enter fallback")
        return True
    except Exception as e:
        print(f"[SEND][ERROR] Enter fallback failed: {str(e)[:200]}")
        return False
