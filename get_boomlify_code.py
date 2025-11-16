from utils import *
import re


def fetch_chatgpt_code_from_boomlify_separate(
    search_email,
    login_email="staywhizzy2023@gmail.com",
    login_password="Katana@23033",
    total_timeout=60,
):
    """
    SEPARATE SB session for Boomlify only!
    Opens its own browser, logs in, gets the OTP code, then closes.
    Does NOT switch tabs or interact with ChatGPT session.
    """
    print("[BOOMLIFY SERVER] Starting separate Boomlify browser session...")
    
    
    with SB(uc=True, test=True, ad_block=True, locale="en") as boom_sb:
        boom_sb.activate_cdp_mode("https://boomlify.com/en/login")
        short_sleep_dbg(boom_sb, "boomlify login page")
        boom_sb.sleep(3)
        
        # Fill login form
        boom_sb.cdp.wait_for_element_visible('input[type="email"]', timeout=20)
        boom_sb.cdp.click('input[type="email"]')
        boom_sb.cdp.type('input[type="email"]', login_email)
        save_ss(boom_sb, "boomlify_email_filled")
        short_sleep_dbg(boom_sb, "typed login email")

        boom_sb.cdp.wait_for_element_visible('input[type="password"]', timeout=20)
        boom_sb.cdp.click('input[type="password"]')
        boom_sb.cdp.type('input[type="password"]', login_password)
        save_ss(boom_sb, "boomlify_password_filled")
        short_sleep_dbg(boom_sb, "typed login password")
        
        boom_sb.sleep(2)
        boom_sb.cdp.solve_captcha()
        boom_sb.cdp.wait_for_element_absent("input[disabled]")
        boom_sb.sleep(10)
        boom_sb.cdp.scroll_down(30)
        boom_sb.sleep(8)

        # Submit login
        click_first(
            boom_sb,
            [
                'button:contains("Access Your Secure Inbox")',
                'button[type="submit"]',
            ],
            label="boomlify-login-submit",
        )
        print("[OTP] Access your inbox button clicked")
        sleep_dbg(boom_sb, a=3, b=5, label="after submit login")

        # Ensure dashboard
        with suppress(Exception):
            if not re.search(r"/dashboard", boom_sb.cdp.get_current_url() or "", re.I):
                boom_sb.cdp.open("https://boomlify.com/en/dashboard")
                sleep_dbg(boom_sb, a=2, b=4, label="ensure dashboard")

        save_ss(boom_sb, "boomlify_dashboard_check")

        # Search the email
        search_selectors = [
            'input[placeholder*="Search" i]',
            'input[type="search"]',
            'input[aria-label*="Search" i]',
        ]
        ssel = click_first(boom_sb, search_selectors, label="boomlify-search")
        if not ssel:
            print("[BOOMLIFY][ERROR] Search input not found on Boomlify dashboard")
            save_ss(boom_sb, "boomlify_search_missing")
            return None

        boom_sb.cdp.select_all(ssel)
        boom_sb.cdp.type(ssel, search_email)
        short_sleep_dbg(boom_sb, "after typing search email")
        boom_sb.cdp.sleep(3)
        # Scrape the 6-digit code
        code = None
        t0 = time.time()
        while time.time() - t0 < total_timeout:
            try:
                html = boom_sb.cdp.get_page_source()
                m = re.search(r"Your\s+(?:ChatGPT|OpenAI)\s+(?:code\s+is|password\s+reset\s+code\s+is)\s+(\d{6})", html, re.I)
                
                if m:
                    code = m.group(1)
                    break
            except Exception:
                pass
            boom_sb.sleep(1.0)

        if not code:
            print(f"[BOOMLIFY][ERROR] Could not find ChatGPT code for {search_email}")
            save_ss(boom_sb, "boomlify_code_not_found")
            return None

        print(f"[BOOMLIFY][SUCCESS] Found verification code: {code}")
        save_ss(boom_sb, f"boomlify_code_{code}")
        return code
        
    