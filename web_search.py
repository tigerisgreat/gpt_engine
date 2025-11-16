from utils import *

def make_web_search_on(sb):
    save_ss(sb)
    print("[SEARCH BUTTON CLICK PREPARINGS]")
    sb.cdp.type("#prompt-textarea", "/")
    sb.sleep(2)
    sb.cdp.type("#prompt-textarea", "s")
    sb.sleep(1)
    sb.cdp.type("#prompt-textarea", "e")
    sb.sleep(1)
    sb.cdp.type("#prompt-textarea", "a")
    sb.sleep(1)
    sb.cdp.type("#prompt-textarea", "r")
    sb.sleep(1)
    sb.cdp.type("#prompt-textarea", "c")
    sb.sleep(1)
    sb.cdp.type("#prompt-textarea", "h")
    
    sb.sleep(1)
    sb.cdp.send_keys("#prompt-textarea", "\n")
    # # Clicking the "+" button
    # click_first(sb, ['button[data-testid="composer-plus-btn"]'], label="Add files button")
    
    # sb.sleep(2)
    # # Clicking on "... More" text
    # click_first(sb, ['div:contains("More")'], label="More menu option")
    # sb.sleep(2)
    
    # # Clicking on web search option emoji
    # click_first(sb, ['div:contains("Web search")'], label="Web search")
    sb.sleep(2)
    
    sb.cdp.type("#prompt-textarea", " ")
    sb.sleep(1)
    #is search emoji finding search button
    sb.sleep(3)