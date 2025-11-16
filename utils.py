import os
import random
import time
from contextlib import suppress
from seleniumbase import SB
import inspect
ss_number=1
debug_number=1

#sleep command with debug statement
def sleep_dbg(sb, secs=None, a=None, b=None, label=""):
    if secs is None:
        secs = random.randint(a, b)
    print(f"---{secs:.1f}s---")
    # print(f"[SLEEP] {label} sleeping {secs:.1f}s")
    sb.sleep(secs)
    return secs

#short sleep command with debug statement
def short_sleep_dbg(sb, label=""):
    secs = random.randint(8, 45) / 10.0  # 0.8–1.5s
    print(f"---{secs:.1f}s---")
    # print(f"[SLEEP] {label} short sleep {secs:.1f}s")
    sb.sleep(secs)
    return secs

#Visibility checking function to check if an element is present in "sb" instance
def visible(sb, sel):
    try:
        return sb.cdp.is_element_visible(sel)
    except Exception:
        return False

#To click a selector function in present "sb" instance
def click_first(sb, selectors, label=""):
    for sel in selectors:
        try:
            if sb.cdp.is_element_visible(sel):
                print("Element now visible to click!")
                sb.cdp.click(sel)
                short_sleep_dbg(sb, label=f"after click {label or sel}")
                print(f"[CLICK BUTTON] {label or sel}")
                return sel
        except Exception as e:
            print(f"::warning::[WARN] click fail {sel}: {e}")
    return None

#Screenshot taking function
def save_ss(sb, name=None):
    global ss_number
    path = f"screenshots/{ss_number}_{name}_{int(time.time())}.png"
    with suppress(Exception):
        sb.save_screenshot(path)
        print(f"SCREENSHOT {ss_number}")
        ss_number=ss_number+1
        # print(f"[SCREENSHOT] {path}")
    return path

def debug():
    global debug_number
    
    # Get the calling file and line number
    caller_frame = inspect.currentframe().f_back
    caller_file = os.path.basename(caller_frame.f_code.co_filename)
    caller_line = caller_frame.f_lineno
    
    print(f"____________{caller_file}______________{caller_line}___________________{debug_number}")
    debug_number += 1

def _env_int(name, default):
    try:
        v = os.environ.get(name, "")
        return int(v) if str(v).strip() else default
    except Exception:
        return default
    

def wait_for_textarea(sb, timeout=40):
    TEXTAREA_SELECTORS = [
    "#prompt-textarea",
    "textarea#prompt-textarea",
    'textarea[placeholder*="Message" i]',
]
    t0 = time.time()
    while time.time() - t0 < timeout:
        for sel in TEXTAREA_SELECTORS:
            if visible(sb, sel):
                return sel
        sb.sleep(0.5)
    return None