from utils import *
from is_verification_page import *
from is_chat_ui import *
from is_incorrect_page import *


def handle_login(sb, email, password):
    print("(handle login) Navigating to https://chatgpt.com/auth/login")
    try:
        sb.cdp.open("https://chatgpt.com/auth/login")
    except Exception as e:
        print("(handle login)[ERROR] Could not open /auth/login:", str(e)[:200])
        save_ss(sb, "login_open_error")
        return "reopen"

    sleep_dbg(sb, a=8, b=15, label="after /auth/login open")
    save_ss(sb, "login_page")

    login_button_selectors = [
        'button[data-testid="login-button"]',
        'button[data-testid="log-in-button"]',
        'button:has(span:contains("Log in"))',
        'button:contains("Log in")',
    ]
    clicked_login_btn = click_first(sb, login_button_selectors, label="login button")
    if clicked_login_btn:
        print(f"[(handle login)LOGIN] Clicked login button: {clicked_login_btn}")
        sleep_dbg(sb, a=1, b=3, label="post login-button click")
        save_ss(sb, "after_login_btn")

    email_selectors = [
        'div[role="dialog"] input#email',
        'div[role="dialog"] input[name="email"]',
        'div[role="dialog"] input[type="email"]',
        'div[role="dialog"] input[placeholder="Email address"]',
        'div[role="dialog"] input[aria-label="Email address"]',
        'input#email',
        'input[name="email"]',
        'input[type="email"]',
        'input[placeholder="Email address"]',
        'input[aria-label="Email address"]',
    ]
    email_input = None
    for _ in range(30):
        for sel in email_selectors:
            if visible(sb, sel):
                email_input = sel
                break
        if email_input:
            break
        sb.sleep(0.5)

    if not email_input:
        print("[ERROR]: [ERROR] Email input not found in login dialog")
        save_ss(sb, "email_input_not_found")
        return "reopen"

    print(f"(handle login) Email input found: {email_input}")
    try:
        sb.cdp.click(email_input)
        short_sleep_dbg(sb, label="before typing email")
        sb.cdp.type(email_input, email)
        short_sleep_dbg(sb, label="after typing email")
        save_ss(sb, "email_typed")
    except Exception as e:
        print("(handle login)[ERROR] Typing email failed:", str(e)[:200])
        save_ss(sb, "email_type_error")
        return "reopen"

    continue_btn_selectors = [
        'div[role="dialog"] button[type="submit"]',
        'div[role="dialog"] button:contains("Continue")',
        'button[type="submit"]',
        'button:contains("Continue")',
    ]
    cont_sel = click_first(sb, continue_btn_selectors, label="continue-after-email")
    if not cont_sel:
        print("(handle login)[ERROR] Continue button after email not found/clickable")
        save_ss(sb, "continue_button_missing")
        return "reopen"

    sleep_dbg(sb, a=8, b=15, label="after Continue (email)")

    # If email verification page appears here, report and stop login flow
    if is_verification_page_visible(sb, timeout=8, screenshot_name="verification_after_email"):
        print("(handle login) Verification code required after email step")
        return "verification"

    # Password input on auth.openai.com
    pwd_selectors = [
        'input[type="password"]',
        'input[autocomplete="current-password"]',
        'input[id*="current-password"]',
        'input[name="password"]',
        'input[placeholder*="Password" i]',
    ]
    pwd_input = None
    for _ in range(40):
        for sel in pwd_selectors:
            if visible(sb, sel):
                pwd_input = sel
                break
        if pwd_input:
            break
        sb.sleep(0.5)

    if not pwd_input:
        print("[ERROR] Password input not found")
        save_ss(sb, "password_input_not_found")
        return "reopen"

    print(f"(handle login) Password input found: {pwd_input}")
    try:
        sb.cdp.click(pwd_input)
        short_sleep_dbg(sb, label="before typing password")
        sb_password=get_password(email)
        sb.cdp.type(pwd_input, sb_password)
        short_sleep_dbg(sb, label="after typing password")
        save_ss(sb, "password_typed")
    except Exception as e:
        print("[handle login][ERROR] Typing password failed:", str(e)[:200])
        save_ss(sb, "password_type_error")
        return "reopen"

    continue_button_selectors = [
        'button[type="submit"]',
        'button:contains("Continue")',
    ]
    pw_sel = click_first(sb, continue_button_selectors, label="password-continue")
    if not pw_sel:
        print("[ERROR] Password submit button not found/clickable")
        save_ss(sb, "password_continue_missing")
        return "reopen"

    sleep_dbg(sb, a=8, b=15, label="after Continue (password)")
    save_ss(sb, "after_password_continue")
    try:
        sb.sleep(3)
        cookies_verification = sb.cdp.get_all_cookies()  # ✅ Correct
        print(f"(handle login) [COOKIES] Saved {len(cookies_verification)} cookies")
    except Exception as e:
        print(f"(handle login) [COOKIES] Error saving cookies: {e}")
    
    # If verification page appears after password, report and stop login flow
    if is_verification_page_visible(sb, timeout=8, screenshot_name="verification_after_password"):
        print("(handle login) Verification code required after password step")
        error_page="verification"
        return "verification"
    
    
    if is_incorrect_credentials_page_visible(sb):  
        print("(handle login) Incorrect credentials detected! Need to reset password now!")
        error_page="password incorrect"
        return "password_incorrect"
    
    if is_chat_ui_visible(sb):
        save_ss(sb, "chat_ui_ready")
        popups=is_popups_visible(sb)
        print("(handle login) Login successful, chat UI visible")
        sb.sleep(10)
        popups=is_popups_visible(sb)
        error_page="we_passed"
        return True
    
    # Handle error: retry with another account or abort

    print("[ERROR] After login, #prompt-textarea not visible")
    return "reopen"
