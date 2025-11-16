from utils import *
from is_incorrect_page import *
from is_chat_ui import *
from is_login_page import *
from is_verification_page import *
from get_boomlify_code import *
from scrape_chatgpt_responses import *
from submit_chatgpt_code import *
from handle_login import *
from password_reset_chatgpt import *
from sanatizing_prompt import *
from prompt_sending import *
from web_search import *

def scrape_chatgpt_responses(prompts,email,password):
    debug()
    results = []
    total = len(prompts)
    i = 0
    max_retries = 2
    force_login_on_reopen = False
    debug()
    while i < total:
        tries = 0
        debug()
        while tries < max_retries and i < total:
            trigger_reopen = False
            debug()
            try:
                debug()
                with SB(uc=True, test=True, ad_block=True, locale="en") as sb:
                    url = "https://chatgpt.com/"
                    print("\n" + "=" * 80)
                    print("Opening ChatGPT:", url)
                    print("=" * 80 + "\n")
                    debug()

                    sb.activate_cdp_mode(url)
                    sleep_dbg(sb, a=8, b=15, label="after initial open")
                    debug()

                    if force_login_on_reopen:
                        # Fetch OTP from SEPARATE Boomlify browser session
                        print("[INFO] Fetching OTP from separate Boomlify session...")
                        debug()
                        lr=handle_login()
                        
                        
                        debug()
                        
                        if lr=="verification":
                            debug()
                            code = fetch_chatgpt_code_from_boomlify_separate(email)
                            print(f"[INFO] Got OTP code: {code}, submitting to ChatGPT...")
                            if submit_chatgpt_verification_code(sb, code):
                                debug()
                                lr = True
                            else:
                                debug()
                                trigger_reopen = True
                        if lr=="password_incorrect":
                                debug()
                                new_password=reset_password(email, sb_password)
                                debug()
                                print("(Scrape chatgpt responses)Passwrod RESET done")
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
                                debug()
                                sb.cdp.clear_input(pwd_input)
                                sb.cdp.click(pwd_input)
                                sb.cdp.type(pwd_input,new_password)
                                if not click_first(sb, ['button:contains("Continue")', 'button[type="submit"]'], label="otp-continue"):
                                    print("[RESET PASSWORD][WARN] Continue button not found; trying Enter")
                                    debug()
                                    save_ss(sb,"Continue button not found")
                                    with suppress(Exception):
                                        sb.cdp.press_keys(sel, "Enter")
                                        short_sleep_dbg(sb, "after Enter on OTP")
                                if is_verification_page_visible:
                                    debug()
                                    code = fetch_chatgpt_code_from_boomlify_separate(email)
                                    debug()
                                    if code and submit_chatgpt_verification_code(sb, code):
                                        debug()
                                        lr = True
                                    else:
                                        debug()
                                        trigger_reopen = True
                                if is_chat_ui_visible(sb):
                                    debug()
                                    save_ss(sb, "chat_ui_ready")
                                    print("(handle login) Login successful, chat UI visible")
                                    error_page="we_passed"
                                    #is pop ups visible?
                                    popups=is_popups_visible(sb)
                                    lr= True
                        else:
                            debug()
                            print("[ERROR] Failed to get OTP code")
                            trigger_reopen = True
                        if lr == "reopen" or not lr:
                            debug()
                            print("Error:  Login failed -> reopen")
                            trigger_reopen = True
                        else:
                            debug()
                            sleep_dbg(sb, a=8, b=15, label="post-login settle")
                            force_login_on_reopen = False
                    else:
                        debug()
                        if is_login_page_visible(sb):
                            debug()
                            print("[Scrape chatgpt responses] Login page detected -> /auth/login flow")
                            sb_password=  get_password(email)
                            debug()
                            print(sb_password)
                            lr = handle_login(sb, email, sb_password)
                            if lr == "verification":
                                debug()
                                code = fetch_chatgpt_code_from_boomlify_separate(email)
                                debug()
                                if code and submit_chatgpt_verification_code(sb, code):
                                    lr = True
                                    debug()
                                else:
                                    trigger_reopen = True
                                    debug()
                            if lr=="password_incorrect":
                                debug()
                                new_password=reset_password(email, sb_password)
                                debug()
                                print("(Scrape chatgpt responses)Passwrod RESET done")
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
                                debug()
                                sb.cdp.clear_input(pwd_input)
                                sb.cdp.click(pwd_input)
                                sb.cdp.type(pwd_input,new_password)
                                if not click_first(sb, ['button:contains("Continue")', 'button[type="submit"]'], label="otp-continue"):
                                    print("[RESET PASSWORD][WARN] Continue button not found; trying Enter")
                                    debug()
                                    save_ss(sb,"Continue button not found")
                                    with suppress(Exception):
                                        sb.cdp.press_keys(sel, "Enter")
                                        short_sleep_dbg(sb, "after Enter on OTP")
                                if is_verification_page_visible:
                                    debug()
                                    code = fetch_chatgpt_code_from_boomlify_separate(email)
                                    debug()
                                    if code and submit_chatgpt_verification_code(sb, code):
                                        debug()
                                        lr = True
                                    else:
                                        debug()
                                        trigger_reopen = True
                                if is_chat_ui_visible(sb):
                                    debug()
                                    save_ss(sb, "chat_ui_ready")
                                    print("(handle login) Login successful, chat UI visible")
                                    error_page="we_passed"
                                    #is pop ups visible?
                                    popups=is_popups_visible(sb)
                                    lr= True
                                lr=True
                                debug()
                            if lr == "reopen" or not lr:
                                debug()
                                print("Error:  Login failed -> reopen")
                                trigger_reopen = True
                            else:
                                debug()
                                sleep_dbg(sb, a=8, b=15, label="post-login settle")
                        else:
                            debug()
                            print("[DEBUG] No login required")

                    if not trigger_reopen:
                        debug()
                        sb.click_if_visible('button[aria-label="Close dialog"]')
                        sb.click_if_visible('button[data-testid="close-button"]')
                        short_sleep_dbg(sb, label="after closing dialogs")
                        sel = wait_for_textarea(sb, timeout=40)
                        if not sel:
                            debug()
                            print("[ERROR] Textarea not found on load")
                            save_ss(sb, "textarea_not_found_on_load")
                            trigger_reopen = True
                            force_login_on_reopen = True
                    #Search emoji variable
                    is_search_true=False
                    prompts_until_new_chat=5
                    debug()
                    #This is the main loop of chats
                    while not trigger_reopen and i < total:
                        debug()
                        prompt_raw = prompts[i]
                        prompt = sanitize_prompt(prompt_raw)
                        debug()
                        print("[%d/%d] Sanitized prompt: %s" % (i + 1, total, (prompt[:100] if prompt else "")))
                        print("-" * 80)
                        if prompts_until_new_chat==0:
                            debug()
                            is_search_true=False
                            prompts_until_new_chat=5
                            sb.sleep(2)
                            save_ss(sb, "Before clicking New chat button")
                            sb.cdp.click('//div[contains(text(), "New chat")]')
                            sb.sleep(9)
                            save_ss(sb,"After clicking New chat button")
                            
                        if not prompt:
                            debug()
                            print("[WARN] Empty prompt after cleaning; skipping")
                            save_ss(sb,"Empty prompt after cleaning")
                            results.append({
                                "prompt": prompt_raw,
                                "response": "Error: Empty prompt after cleaning",
                                "screenshot": None,
                                "captcha_type": None,
                            })
                            i += 1
                            continue

                        try:
                            debug()
                            # Dismiss “Stay logged out” modal if appears
                            login_modal_selectors = [
                                'a[href="#"][class*="text-secondary"]',
                                'a[href="#"]:contains("Stay logged out")',
                                '[role="dialog"] a[href="#"]',
                                'div[role="dialog"] a',
                            ]
                            for sel in login_modal_selectors:
                                debug()
                                if visible(sb, sel):
                                    debug()
                                    print("[WARNING] LOGIN MODAL detected -> dismissing")
                                    save_ss(sb, "Login Modal detected")
                                    sb.cdp.click(sel)
                                    short_sleep_dbg(sb, label="after dismiss click")
                                    print("[DEBUG] Modal dismissed")
                                    break

                            if not visible(sb, "#prompt-textarea"):
                                debug()
                                print("[ERROR] Textarea missing -> reopen & force login")
                                save_ss(sb, "textarea_missing_midrun")
                                trigger_reopen = True
                                force_login_on_reopen = True
                                continue
                            if_links_appear=False
                            if_links_do_not_appear_retry=3
                            count=0
                            while count<if_links_do_not_appear_retry and if_links_appear==False:
                                # Type prompt
                                debug()
                                sb.scroll_into_view("#prompt-textarea")
                                short_sleep_dbg(sb, label="after scroll to textarea")
                                sb.cdp.click("#prompt-textarea")
                                short_sleep_dbg(sb, label="after click textarea")
                                sb.cdp.select_all("#prompt-textarea")
                                sb.cdp.press_keys("#prompt-textarea", "")
                                if(is_search_true==False):
                                    debug()
                                    #is search emoji finding search button
                                    make_web_search_on(sb)
                                    is_search_true=True
                                short_sleep_dbg(sb, label="after clear textarea")
                                debug()
                                sb.sleep(1)
                                sb.cdp.type("#prompt-textarea", "/search ")
                                sb.sleep(3)
                                sb.cdp.type("#prompt-textarea", prompt)
                                short_sleep_dbg(sb, label="after typing prompt")
                                sb.sleep(3)
                                debug()
                                is_prompt_sending_successful=send_prompt(sb)
                                debug()
                                # Send errors
                                if is_prompt_sending_successful==False:
                                    debug()
                                    print("Error:  Send failed -> reopen")
                                    screenshot_path = save_ss(sb, f"send_failed_{i+1}")
                                    results.append({
                                        "prompt": prompt_raw,
                                        "response": "Error: Send failed",
                                        "screenshot": screenshot_path,
                                        "captcha_type": None,
                                    })
                                    trigger_reopen = True
                                    force_login_on_reopen = True
                                    continue
                                else:
                                    debug()
                                    prompts_until_new_chat-=1
                            
                                # Wait finished + extra
                                try:
                                    debug()                                  
                                    sb.cdp.wait_for_element_not_visible('button[data-testid="stop-button"]', timeout=90)
                                except Exception as e:
                                    debug()
                                    print(f"::warning::Exception: {e}") 
                                sleep_dbg(sb, a=10, b=15, label="extra wait after streaming")
                                sb.sleep(10)
                                debug()
                                # Extract last assistant message
                                response_selectors = [
                                    '[data-message-author-role="assistant"] .markdown',
                                    '[data-message-author-role="assistant"] article',
                                    'div[data-message-author-role="assistant"]',
                                    '[class*="message"] [class*="markdown"]',
                                    '[role="article"] .markdown',
                                ]
                                debug()
                                sb.sleep(10)
                                elems = []
                                for sel in response_selectors:
                                    debug()
                                    try:
                                        debug()
                                        elems = sb.cdp.find_all(sel, timeout=60)
                                        if elems:
                                            break
                                    except Exception:
                                        debug()
                                        pass
                                debug()
                                if not elems:
                                    debug()
                                    print("::error::[ERROR] No response found")
                                    screenshot_path = save_ss(sb, f"no_response_{i+1}")
                                    results.append({
                                        "prompt": prompt_raw,
                                        "response": "Error: No response",
                                        "screenshot": screenshot_path,
                                        "captcha_type": None,
                                    })
                                    i += 1
                                    sleep_dbg(sb, a=8, b=15, label="between prompts (no response)")
                                    continue
                                debug()
                                #extraction
                                hrefs=[]
                                try:
                                    debug()
                                    sb.sleep(6)
                                    latest_elem = elems[-1]               # This is the SeleniumBase element object
                                    latest_html = latest_elem.get_html()  # HTML string for text extraction

                                    # Extract plain text from the HTML
                                    text = sb.get_beautiful_soup(latest_html).text.strip().replace("\n\n\n", "\n\n")
                                    debug()
                                    # Extract links from the Selenium element object
                                    # links variable will contain the list of anchor element objects (<a> tags) from Selenium.
                                    # hrefs variable will contain just the URLs (strings) extracted from those anchor elements.
                                    links = latest_elem.query_selector_all("a")
                                    debug()
                                    hrefs = [link.get_attribute("href") for link in links]
                                    debug()
                                except Exception as e:
                                    debug()
                                    print("[WARNING] Extract failed:", str(e)[:200])
                                    screenshot_path = save_ss(sb, f"extract_failed_{i+1}")
                                    results.append({
                                        "prompt": prompt_raw,
                                        "appeared_links": hrefs,
                                        "response": "Error: Extract failed",
                                        "screenshot": screenshot_path,
                                        "captcha_type": None,
                                    })
                                    i += 1
                                    sleep_dbg(sb, a=8, b=15, label="between prompts (extract failed)")
                                    continue
                                
                                debug()
                                if not text or len(text) < 10:
                                    debug()
                                    print("[WARNING] Response too short")
                                    screenshot_path = save_ss(sb, f"empty_response_{i+1}")
                                    results.append({
                                        "prompt": prompt_raw,
                                        "response": "Error: Empty response",
                                        "screenshot": screenshot_path,
                                        "captcha_type": None,
                                    })
                                    i += 1
                                    sleep_dbg(sb, a=8, b=15, label="between prompts (short response)")
                                    debug()
                                    continue

                                screenshot_path = save_ss(sb, f"success_{i+1}")
                                debug()
                                print(f"📌Appeared_links: {len(hrefs)}")                               
                                sleep_dbg(sb, a=8, b=15, label="between prompts")
                                if len(hrefs)==0:
                                    debug()
                                    if_links_appear=False
                                    count+=1
                                    save_ss(sb, "Before clicking New chat since links appeared are zero.")
                                    sb.sleep(2)
                                    sb.cdp.click('//div[contains(text(), "New chat")]')
                                    sb.sleep(9)
                                    save_ss(sb, "After clicking New chat since links appeared are zero.")
                                    is_search_true=False
                                    print(f"[⚠️RETRYING] Since there are zero links which appeared in the response.")
                                    if count==if_links_do_not_appear_retry:
                                        print(f"[✅SUCCESS] Response {i+1} received (%d chars)\n" % len(text))
                                        results.append({
                                        "prompt": prompt_raw,
                                        "appeared_links":hrefs,
                                        "response": text,
                                        "screenshot": screenshot_path,
                                        "captcha_type": None,
                                    })
                                        i += 1
                                    debug()
                                else:
                                    debug()
                                    if_links_appear=True
                                    print(f"[✅SUCCESS] Response {i+1} received (%d chars)\n" % len(text))
                                    results.append({
                                    "prompt": prompt_raw,
                                    "appeared_links":hrefs,
                                    "response": text,
                                    "screenshot": screenshot_path,
                                    "captcha_type": None,
                                })
                                    i += 1
                                debug()

                        except Exception as e:
                            debug()
                            print("[ERROR] Unexpected exception -> reopen & force login:", str(e)[:200])
                            screenshot_path = save_ss(sb, f"general_exception_{i+1}")
                            results.append({
                                "prompt": prompt_raw,
                                "response": f"Error: {str(e)[:150]}",
                                "screenshot": screenshot_path,
                                "captcha_type": None,
                            })
                            trigger_reopen = True
                            force_login_on_reopen = True
                            debug()
                            continue

                if trigger_reopen:
                    debug()
                    tries += 1
                    print(f"[INFO] Will reopen browser for prompt index {i} (try {tries}/{max_retries})")
                    continue
                else:
                    debug()
                    break

            except Exception as e:
                debug()
                print("\n[FATAL] Browser creation/use failed -> will force login next try:", str(e)[:200])
                tries += 1
                force_login_on_reopen = True
                continue

        if i < total and tries >= max_retries:
            debug()
            results.append({
                "prompt": prompts[i],
                "response": "Error: Could not complete prompt after retries",
                "screenshot": None,
                "captcha_type": None,
            })
            i += 1

    print("\n" + "=" * 80)
    release_account(email)
    print("All prompts processed!")
    print("=" * 80 + "\n")
    debug()
    return results
