import sys
debug_flag = False
def dprint(msg):
    if debug_flag and msg and len(msg) > 1 and msg[0] == "*":
        msg = f"DEBUG: {msg}\n"
        sys.stderr.write(msg)

if __name__ == "__main__":
    dprint("this is an error")
