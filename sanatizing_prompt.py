from utils import *
import re

def sanitize_prompt(p):
    debug()
    """Extract prompt text from tuple format: (index, 'text')"""
    if isinstance(p, tuple) and len(p) >= 2:
        return p[1]
    return p


# def main():
#     s=sanitize_prompt((61, 'How do I handle model serving with varying request latencies?'))
#     print(s)
#     debug()

# if __name__ == "__main__":
#     main()