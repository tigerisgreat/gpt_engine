import json
import os
import re
import random
import time
from contextlib import suppress
from seleniumbase import SB
from utils import *
from access_keys import * 
from is_pop_ups import *

def is_chat_ui_visible(sb):
    # Try current page first
    popups=is_popups_visible(sb)
    sel = wait_for_textarea(sb, timeout=12)
    if sel:
        print(f"[CHAT-UI] Textarea found ({sel}) without redirect")
        return True

    print("[CHAT-UI] Opening https://chatgpt.com/ after password Continue")
    with suppress(Exception):
        sb.open("https://chatgpt.com/")
    sleep_dbg(sb, a=6, b=10, label="after chatgpt.com open")

    sel = wait_for_textarea(sb, timeout=15)
    if sel:
        print(f"[CHAT-UI] Textarea found ({sel}) after chatgpt.com open")
        return True

    print("[CHAT-UI] Opening https://chatgpt.com/?oai-dm=1 as fallback")
    with suppress(Exception):
        sb.open("https://chatgpt.com/?oai-dm=1")
    sleep_dbg(sb, a=6, b=10, label="after dm fallback")

    sel = wait_for_textarea(sb, timeout=15)
    if sel:
        print(f"[CHAT-UI] Textarea found ({sel}) after dm fallback")
        return True

    save_ss(sb, "login_after_password_failed")
    return False
