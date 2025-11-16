from utils import *

def pass_turnstile_if_present(sb, timeout=25):
    """
    Use SeleniumBase helpers to solve Cloudflare Turnstile.
    1) Try sb.solve_captcha() (UC/CDP helper).
    2) If still present, attempt a GUI click on the parent above the shadow-root.
    3) Confirm success by waiting for 'Verified'/'Success' text or the widget to disappear.
    Docs/examples: SeleniumBase CDP Mode + raw_cdp_turnstile.  (See notes above.)
    """
    print("[Turnstile] Checking for Turnstile...")
    turnstile_locs = [
        'iframe[src*="turnstile"]',
        'div[class*="cf-turnstile"]',
        'div:contains("Verify you are human")',
        'div[aria-label*="Verify you are human" i]',
    ]

    detected = False
    with suppress(Exception):
        for sel in turnstile_locs:
            if sb.is_element_present(sel):
                detected = True
                break

    if not detected:
        print("[Turnstile] Not detected.")
        return True

    # 1) Built-in solver
    try:
        print("[Turnstile] Trying SeleniumBase solver: solve_captcha()")
        sb.solve_captcha()  # per docs; no args needed
        short_sleep_dbg(sb, "after solve_captcha()")
    except Exception as e:
        print(f"[Turnstile][WARN] solve_captcha() failed: {e}")

    # 2) If still there, try GUI click on parents often used by CF widgets
    still_there = False
    with suppress(Exception):
        still_there = sb.is_element_present('iframe[src*="turnstile"]')

    if still_there:
        print("[Turnstile] Still present, attempting GUI click on widget parent")
        parents = [
            '#turnstile-widget div',
            'div[id*="turnstile"] div',
            'div[aria-label*="Verify you are human" i]',
        ]
        for sel in parents:
            with suppress(Exception):
                sb.cdp.gui_click_element(sel)
                short_sleep_dbg(sb, f"gui-click {sel}")
                break

    # 3) Success check
    ok = False
    with suppress(Exception):
        sb.wait_for_text("Verified", timeout=timeout)
        ok = True
    if not ok:
        with suppress(Exception):
            sb.wait_for_text("Success", timeout=timeout)
            ok = True
    if not ok:
        # Or the iframe becomes absent (token accepted)
        with suppress(Exception):
            sb.wait_for_element_absent('iframe[src*="turnstile"]', timeout=timeout)
            ok = True

    if ok:
        print("[Turnstile] Challenge cleared.")
        return True

    print("Error: [Turnstile][ERROR] Could not confirm Turnstile success")
    save_ss(sb, "boomlify_turnstile")
    return False
