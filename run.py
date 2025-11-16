import json
import os
import re
import random
import time
from contextlib import suppress
from seleniumbase import SB
from utils import *
from access_keys import * 
from scrape_chatgpt_responses import *

def _env_int(name, default):
    try:
        v = os.environ.get(name, "")
        return int(v) if str(v).strip() else default
    except Exception:
        return default

batch_number   = _env_int("BATCH_NUMBER", 1)
total_batches  = _env_int("TOTAL_BATCHES", 10)
MAX_PROMPTS    = _env_int("MAX_PROMPTS", 30)
# batch_number   = 1
# total_batches  = 1
# MAX_PROMPTS    = 1
ACCOUNT        = get_available_account()
account=ACCOUNT['email']
password=ACCOUNT['password']
cookies_verification=None
is_password_reset_required=False
with open("prompts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Get prompts with their indices
all_prompts = [(int(item["Index"]), sanitize_prompt(item["Prompt"])) for item in data]

prompts_per_batch = max(1, len(all_prompts) // max(1, total_batches))
start_idx = (batch_number - 1) * prompts_per_batch
end_idx   = len(all_prompts) if batch_number == total_batches else min(len(all_prompts), start_idx + prompts_per_batch)
batch_prompts = all_prompts[start_idx:end_idx][:MAX_PROMPTS]
error_page=""
os.makedirs("screenshots", exist_ok=True)

print("\n" + "=" * 80)
print(f"BATCH {batch_number}/{total_batches}")
print(f"Processing prompts {start_idx} to {start_idx + len(batch_prompts) - 1} ({len(batch_prompts)} total)")
print("=" * 80 + "\n")


def main():
    print("\n" + "=" * 80)
    print(f"Starting ChatGPT scraping for batch {batch_number}")
    print(f"Processing {len(batch_prompts)} prompts (max {MAX_PROMPTS})")
    print("=" * 80 + "\n")
    debug()
    results = scrape_chatgpt_responses(batch_prompts,account,password)

    for idx, result in enumerate(results):
        qi = start_idx + idx
        result["batch_id"] = batch_number
        result["query_index"] = qi
        try:
            result["prompt_id"] = data["queries"][qi].get("id", qi)
        except Exception:
            result["prompt_id"] = qi

    out_file = f"results_batch_{batch_number}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    success = sum(1 for r in results if not str(r.get("response", "")).startswith("Error"))
    print("\n" + "=" * 80)
    print(f"[✓] Batch {batch_number}: {success}/{len(batch_prompts)} successful")
    print(f"[✓] Results saved to {out_file}")
    print("=" * 80 + "\n")
    return results

if __name__ == "__main__":
    main()
