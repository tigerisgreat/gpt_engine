from utils import *


def submit_chatgpt_verification_code(sb, code):
    code_selectors = [
        'input[name="code"]',
        'input[autocomplete="one-time-code"]',
        'input[id*="code"]',
        'input[placeholder*="Code" i]',
    ]
    sel = None
    for s in code_selectors:
        if visible(sb, s):
            sel = s
            break
    if not sel:
        print("[OTP][ERROR] Code input not visible on ChatGPT page")
        save_ss(sb, "otp_input_missing")
        return False

    sb.cdp.click(sel)
    sb.cdp.type(sel, str(code))
    short_sleep_dbg(sb, "after typing OTP")

    if not click_first(sb, ['button:contains("Continue")', 'button[type="submit"]'], label="otp-continue"):
        print("[OTP][WARN] Continue button not found; trying Enter")
        save_ss(sb,"Continue button not found")
        with suppress(Exception):
            sb.cdp.press_keys(sel, "Enter")
            short_sleep_dbg(sb, "after Enter on OTP")

    if wait_for_textarea(sb, timeout=20):
        print("[OTP][INFO] OTP accepted; chat textarea visible")
        save_ss(sb, "Verification OTP accepted")
        return True

    print("[OTP][WARN] OTP submission did not reveal textarea yet")
    save_ss(sb, "otp_submit_unclear")
    return False
