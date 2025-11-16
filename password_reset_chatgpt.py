from utils import * 
from is_incorrect_page import *
from get_boomlify_code import *
from access_keys import *

reset_password_code="Katana@23030091"
def reset_password(email, password):
    print("[PASSWROD RESET] Starting password reset in separate session...")
    with SB(uc=True, test=True, ad_block=True, locale="en") as password_reset_sb:
            password_reset_sb.activate_cdp_mode("https://platform.openai.com/docs/overview")
            short_sleep_dbg(password_reset_sb, "Chatgpt password change page")
            
            password_reset_sb.sleep(3)
            
            # Fill login form
            password_reset_sb.cdp.wait_for_element_visible('button:contains("Log in")', timeout=20)
            short_sleep_dbg(password_reset_sb, "Log in button visible")
            save_ss(password_reset_sb,"Password change page")
            password_reset_sb.cdp.click('button:contains("Log in")')
            short_sleep_dbg(password_reset_sb, "Log in button clicked")
            password_reset_sb.sleep(3)
            
            password_reset_sb.cdp.wait_for_element_visible('input[type="email"]', timeout=20)
            password_reset_sb.cdp.click('input[type="email"]')
            password_reset_sb.cdp.type('input[type="email"]', email)
            short_sleep_dbg(password_reset_sb,"Email filled")
            save_ss(password_reset_sb, "Email filled")
            
            password_reset_sb.sleep(2)
            password_reset_sb.cdp.click('button:contains("Continue")')
            password_reset_sb.cdp.wait_for_element_visible('input[type="password"]', timeout=20)
            password_reset_sb.cdp.click('input[type="password"]')
            sb_password=  get_password(email)
            password_reset_sb.cdp.type('input[type="password"]', sb_password)
            save_ss(password_reset_sb, "typed login password")
            
            short_sleep_dbg(password_reset_sb, "typed login password")
            password_reset_sb.cdp.click('button:contains("Continue")')
            password_reset_sb.sleep(3)
            check=is_incorrect_credentials_page_visible(password_reset_sb)
            print(f'is incorrect credentials page: {check}')
            password_reset_sb.sleep(1)
            
            # Wait for it to be visible and then click
            password_reset_sb.cdp.wait_for_element_visible("a[href='/reset-password']", timeout=10)
            password_reset_sb.cdp.click("a[href='/reset-password']")
            password_reset_sb.sleep(5)
            password_reset_sb.cdp.wait_for_element_visible('button:contains("Continue")', timeout=10)
            password_reset_sb.cdp.click('button:contains("Continue")')
            password_reset_sb.sleep(2)
            
            code=fetch_chatgpt_code_from_boomlify_separate(email)
            password_reset_sb.sleep(2)
            password_reset_sb.cdp.wait_for_element_visible('div:contains("Code")', timeout=10)
            password_reset_sb.cdp.type('div:contains("Code")', code)
            password_reset_sb.sleep(2)
            
            password_reset_sb.cdp.wait_for_element_visible('button:contains("Continue")', timeout=10)
            password_reset_sb.cdp.click('button:contains("Continue")')
            password_reset_sb.sleep(2)
            
            password_reset_sb.cdp.wait_for_element_visible('div:contains("New password")', timeout=10)
            password_reset_sb.cdp.click('div:contains("New password")')
            password_reset_sb.cdp.type('div:contains("New password")', reset_password_code)
            password_reset_sb.sleep(2)
            
            # New password must contain atleast 12 characters
            password_reset_sb.cdp.wait_for_element_visible('div:contains("Re-enter new password")', timeout=10)
            password_reset_sb.cdp.click('input[placeholder="Re-enter new password"]')
            password_reset_sb.cdp.type('input[placeholder="Re-enter new password"]', reset_password_code)
            password_reset_sb.sleep(2)
            save_ss(password_reset_sb,"Before password reset continue button")
            
            password_reset_sb.cdp.wait_for_element_visible('button:contains("Continue")', timeout=10)
            password_reset_sb.cdp.click('button:contains("Continue")')
            
            password_reset=True
            save_ss(password_reset_sb,"After password reset continue button")
            update_password(email, reset_password_code)
            return reset_password_code
