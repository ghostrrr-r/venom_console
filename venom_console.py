#!/usr/bin/env python3
"""
venom_console.py — Windows-only, native colors, full-featured console
Includes: system, network, internet, files, utilities, fun, explain, history.
No external libraries required (uses ctypes for console colors).
Ctrl+C stops long-running commands. Pauses on exit for Explorer launches.
"""

import os
import sys
import time
import datetime
import subprocess
import socket
import shutil
import tempfile
import glob
import webbrowser
import zipfile
from pathlib import Path

# ---- extra AI stuff ----
#!/usr/bin/env python3
import base64

# --- put your encoded string here ---
encoded_string = "3031313030303031303130303031313130313031313031303031313030313130303130313130303130313031303131303031303130303130303130313031303030313130303031313031313031313030303130303031313030313030313030313031303130313131303130313130303030313031303131303030313130313030303131303030313130313130313130313031313030313030303131313031313030313031303131303031303030313131303131313031303030313031313031303031313030303131303131303131303130313130313030303031313031303031303130313031303030313030303131313031303030313130303130313030303030313130303030313031303130313131303130303130313030303131303031303031313030303031303031313030313030303131303030313030313130303130303130313030303130313130313130313031313030313030303130303130313030313130303130303030313130303130303130313031313030303131303031303031303130303130303131303031313130303131313130313030313131313031"

# --- Step 1: decode hex to binary string ---
binary_string = bytes.fromhex(encoded_string).decode('utf-8')

# --- Step 2: decode binary string to base64 string ---
b64_bytes = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
b64_string = b64_bytes.decode('utf-8')

# --- Step 3: decode base64 to final key ---
key = base64.b64decode(b64_string).decode('utf-8')




# ---------------- Windows native color (ctypes) ----------------
IS_WINDOWS = os.name == "nt"
if not IS_WINDOWS:
    print("This script targets Windows only.")
    # We will still try to run, but color functions will be no-ops.

if IS_WINDOWS:
    import ctypes
    STD_OUTPUT_HANDLE = -11
    hConsole = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    # color constants
    FOREGROUND_BLUE = 0x01
    FOREGROUND_GREEN = 0x02
    FOREGROUND_RED = 0x04
    FOREGROUND_INTENSITY = 0x08

    BG_BLUE = 0x10
    BG_GREEN = 0x20
    BG_RED = 0x40
    BG_INTENSITY = 0x80

    DEFAULT_COLOR = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

    def set_color(attr):
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(hConsole, int(attr))
        except Exception:
            pass

    def reset_color():
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(hConsole, DEFAULT_COLOR)
        except Exception:
            pass
else:
    def set_color(attr): pass
    def reset_color(): pass

# convenient named colors (Windows attributes)
BLUE = FOREGROUND_BLUE | FOREGROUND_INTENSITY if IS_WINDOWS else None
ORANGE = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY if IS_WINDOWS else None
WHITE = DEFAULT_COLOR if IS_WINDOWS else None
RED = FOREGROUND_RED | FOREGROUND_INTENSITY if IS_WINDOWS else None
CYAN = FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY if IS_WINDOWS else None
YELLOW = ORANGE

# ---------------- Globals ----------------
VERSION = "venom.console v1.6-windows-full"
HIST_PATH = os.path.join(tempfile.gettempdir(), "venom_history.txt")

def save_history(entry: str):
    try:
        with open(HIST_PATH, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat()} {entry}\n")
    except Exception:
        pass

def set_title(s):
    if IS_WINDOWS:
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(s)
        except Exception:
            pass
    else:
        sys.stdout.write(f"\x1b]0;{s}\x07")

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")

def run_and_print(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nInterrupted (Ctrl+C).")
    except Exception as e:
        print("Command failed:", e)

def run_quiet(cmd, timeout=None):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout or "").strip(), (r.stderr or "").strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", -1
    except Exception as e:
        return "", str(e), -1

def get_local_outbound_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def get_public_ip():
    services = ["https://api.ipify.org?format=text", "https://ifconfig.co/ip", "https://icanhazip.com"]
    for url in services:
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=5) as r:
                txt = r.read(128).decode("utf-8", errors="replace").strip()
                if txt:
                    return txt
        except Exception:
            continue
    return None

# ---------------- Commands ----------------
import os
import shutil

# ==== AI ====

def cmd_chatbot(self=None, arg=None):
    """
    Interactive MiniMax AI chat session.
    Normal venom.console commands work if prefixed with 'venom.console'.
    """
    import json, urllib.request, urllib.error

    api_key = key
    if not api_key.startswith("hf_"):
        print("Invalid or missing Hugging Face API key.")
        return

    print("Starting MiniMax AI chat. Type 'venom.console <command>' to run console commands. Ctrl+C to exit.\n")
    history = []

    try:
        while True:
            user_input = input("MiniMax AI> ").strip()
            if not user_input:
                continue

            # --- Check for venom.console command ---
            if user_input.lower().startswith("venom.console "):
                cmd_text = user_input[len("venom.console "):].strip()
                parts = cmd_text.split(" ", 1)
                verb = parts[0].lower()
                rest = parts[1] if len(parts) > 1 else ""
                func = COMMANDS.get(verb)
                if func:
                    try:
                        func(rest)  # run the command
                    except Exception as e:
                        print("Error:", e)
                else:
                    print(f"'{cmd_text}' is not a recognized command.")
                continue  # back to chatbot prompt

            # --- Otherwise, send to AI ---
            history.append({"role": "user", "content": user_input})
            body = json.dumps({"model": "MiniMaxAI/MiniMax-M2", "messages": history}).encode("utf-8")
            req = urllib.request.Request(
                "https://router.huggingface.co/v1/chat/completions",
                data=body,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                method="POST"
            )

            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    print("\nMiniMax:", message, "\n")
                    history.append({"role": "assistant", "content": message})
            except urllib.error.HTTPError as e:
                print("HTTP error:", e.code, e.reason)
            except urllib.error.URLError as e:
                print("Connection error:", e.reason)
    except KeyboardInterrupt:
        print("\nReturning to venom.console prompt...")



# ----- FILE COMMANDS -----
import shutil
import zipfile
import glob
import os

# ===== File Commands =====

import os, shutil, time

# === COPY ===
def cmd_copy(src=None, dst=None):
    """Copy a file interactively or with arguments (Windows-safe)."""
    try:
        if not src:
            src = input("Source file: ").strip()
        if not dst:
            dst = input("Destination (file or folder): ").strip()

        if not os.path.exists(src):
            print(f"Source '{src}' not found.")
            return
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        for attempt in range(3):
            try:
                with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst)
                print(f"Copied: {os.path.abspath(src)} -> {os.path.abspath(dst)}")
                return
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 32 and attempt < 2:
                    print(f"File in use... retrying ({attempt+1}/3)")
                    time.sleep(0.5)
                    continue
                raise
    except Exception as e:
        print(f"Copy error: {e}")

# === MOVE ===
def cmd_move(src=None, dst=None):
    """Move a file interactively or with arguments (Windows-safe)."""
    try:
        if not src:
            src = input("Source file: ").strip()
        if not dst:
            dst = input("Destination (file or folder): ").strip()

        if not os.path.exists(src):
            print(f"Source '{src}' not found.")
            return
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        for attempt in range(3):
            try:
                shutil.move(src, dst)
                print(f"Moved: {os.path.abspath(src)} -> {os.path.abspath(dst)}")
                return
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 32 and attempt < 2:
                    print(f"File in use... retrying ({attempt+1}/3)")
                    time.sleep(0.5)
                    continue
                raise
    except Exception as e:
        print(f"Move error: {e}")

# === DELETE ===
def cmd_delete(target=None):
    """Delete file or folder interactively or with argument."""
    try:
        if not target:
            target = input("File or folder to delete: ").strip()

        if not os.path.exists(target):
            print(f"'{target}' not found.")
            return

        confirm = input(f"Are you sure you want to delete '{target}'? (y/n): ").lower()
        if confirm != "y":
            print("Cancelled.")
            return

        for attempt in range(3):
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                print(f"Deleted: {os.path.abspath(target)}")
                return
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 32 and attempt < 2:
                    print(f"File in use... retrying ({attempt+1}/3)")
                    time.sleep(0.5)
                    continue
                raise
    except Exception as e:
        print(f"Delete error: {e}")

# === RENAME ===
def cmd_rename(src=None, dst=None):
    """Rename or move a file interactively or by arguments (Windows-safe)."""
    try:
        if not src:
            src = input("Source file: ").strip()
        if not dst:
            dst = input("New name or destination: ").strip()

        if not os.path.exists(src):
            print(f"Source '{src}' not found.")
            return

        for attempt in range(3):
            try:
                os.rename(src, dst)
                print(f"Renamed: {os.path.abspath(src)} -> {os.path.abspath(dst)}")
                return
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 32 and attempt < 2:
                    print(f"File in use... retrying ({attempt+1}/3)")
                    time.sleep(0.5)
                    continue
                raise
    except Exception as e:
        print(f"Rename error: {e}")


def cmd_ls(path="."):
    """Lists files and folders in the current directory."""
    try:
        items = os.listdir(path)
        for item in items:
            print(item)
    except Exception as e:
        print(f"Error listing directory: {e}")

def cmd_cd(path):
    """Changes the current working directory."""
    try:
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
    except Exception as e:
        print(f"Error changing directory: {e}")

def cmd_cat(file_path):
    """Displays the contents of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")


def cmd_mkdir(folder_name):
    """Creates a directory."""
    try:
        os.mkdir(folder_name)
        print(f"Directory created: {folder_name}")
    except Exception as e:
        print(f"Error creating directory: {e}")

def cmd_rmdir(folder_name):
    """Deletes a directory."""
    try:
        os.rmdir(folder_name)
        print(f"Directory removed: {folder_name}")
    except Exception as e:
        print(f"Error removing directory: {e}")


# HELP / META
def cmd_help(args=""):
    set_color(CYAN)
    print("Available Commands (categorized):")
    reset_color()

    set_color(BLUE); print("\n[Core]"); reset_color()
    print("  help/h, cls, exit/q, version, about")

    set_color(BLUE); print("\n[System]"); reset_color()
    print("  sysinfo, uptime, whoami, whereami, env, path, processes, kill, storage, battery")

    set_color(BLUE); print("\n[Network]"); reset_color()
    print("  ping, fastping, pingpayload, pinginline, tracert, ns, netinfo, saveinfo, myip/netip, wifi, speedtest, dnsflush, hostname, netstat, arp, ports, users")

    set_color(BLUE); print("\n[Internet]"); reset_color()
    print("  http, download, open")

    set_color(BLUE); print("\n[Files]"); reset_color()
    print("  ls/dir, cd, cat/type, copy, del/rm, rename/mv, mkdir, rmdir, find, search, copyfile, movefile, deletefile, compress, extract, filesize, recent")

    set_color(BLUE); print("\n[Utilities]"); reset_color()
    print("  calc, time, date, randtitle, sleep, echo, history, savehistory, remind, timer, clock")

    set_color(BLUE); print("\n[Help Tools]"); reset_color()
    print("  explain, hexplain")

    set_color(BLUE); print("\n[Fun]"); reset_color()
    print("  say, typewriter, matrix, freeminecraft")
    
    set_color(BLUE); print("\n[AI]"); reset_color()
    print("  chatbot")

    set_color(WHITE)
    print("\nUse 'explain <command>' or '<command> explain' for details.")
    print("Press Ctrl+C to stop long-running commands (ping -t, fastping, matrix, etc.).")
    reset_color()
    print()

def cmd_cls(args=""):
    clear_screen()

def cmd_exit(args=""):
    print("Exiting...")
    raise SystemExit

def cmd_version(args=""):
    print(VERSION)

def cmd_about(args=""):
    print("venom.console — Windows ANSI native color full edition. See README for notes.")

def cmd_echo(args=""):
    print(args)

# Time/date/title
def cmd_time(args=""):
    print(datetime.datetime.now().strftime("%H:%M:%S"))

def cmd_date(args=""):
    print(datetime.datetime.now().strftime("%Y-%m-%d"))

def cmd_randtitle(args=""):
    set_title("venom.console " + str(int(time.time()) % 100000))

def cmd_sleep(args=""):
    try:
        s = float(args.strip()) if args.strip() else float(input("Seconds to sleep: ").strip() or "1")
        time.sleep(s)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print("sleep failed:", e)

# --- System ---
def cmd_uptime(args=""):
    try:
        import psutil
        boot_ts = psutil.boot_time()
        boot_dt = datetime.datetime.fromtimestamp(boot_ts)
        uptime = datetime.datetime.now() - boot_dt
        days = uptime.days
        hours, rem = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Boot time: {boot_dt}")
        print(f"Uptime: {days}d {hours}h {minutes}m {seconds}s")
        return
    except Exception:
        # fallback to net stats
        out, err, rc = run_quiet("net stats workstation", timeout=3)
        if out:
            for line in out.splitlines():
                if "Statistics since" in line or "Statistics Since" in line:
                    print(line.strip())
                    return
        print("Uptime not available (install 'psutil' for precise uptime).")

def cmd_sysinfo(args=""):
    try:
        import platform
        print(platform.platform())
        print("Processor:", platform.processor())
        try:
            import psutil
            vm = psutil.virtual_memory()
            print(f"Memory: total={vm.total//(1024**2)}MB available={vm.available//(1024**2)}MB")
            print("CPU logical count:", psutil.cpu_count(logical=True))
        except Exception:
            print("(install 'psutil' for richer info)")
    except Exception as e:
        print("sysinfo failed:", e)

def cmd_whoami(args=""):
    try:
        print("User:", os.getlogin())
    except Exception:
        import getpass
        print("User:", getpass.getuser())
    print("Host:", socket.gethostname())

def cmd_whereami(args=""):
    print("CWD:", os.getcwd())

def cmd_env(args=""):
    for k, v in os.environ.items():
        print(f"{k}={v}")

def cmd_path(args=""):
    for item in os.environ.get("PATH", "").split(os.pathsep):
        print(item)

def cmd_processes(args=""):
    run_and_print("tasklist")

def cmd_kill(args=""):
    tgt = args.strip() or input("PID or process name to kill: ").strip()
    if not tgt:
        return
    confirm = input(f"Type YES to kill {tgt}: ").strip()
    if confirm.upper() != "YES":
        print("Aborted.")
        return
    try:
        if tgt.isdigit():
            run_and_print(f"taskkill /PID {tgt} /F")
        else:
            run_and_print(f"taskkill /IM \"{tgt}\" /F")
        print("Kill attempted.")
    except Exception as e:
        print("kill failed:", e)

def cmd_storage(args=""):
    run_and_print("wmic logicaldisk get name,size,freespace,description /format:list")

def cmd_battery(args=""):
    run_and_print("wmic path Win32_Battery get EstimatedChargeRemaining,BatteryStatus /format:list")

# --- Network ---
def cmd_myip():
    """Displays hostname, local IP, and public IP (if available)."""
    import socket, urllib.request

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        hostname, local_ip = "Unavailable", "Unavailable"

    try:
        public_ip = urllib.request.urlopen("https://api.ipify.org").read().decode()
    except Exception:
        public_ip = "Unavailable"

    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")
    print(f"Public IP: {public_ip}")

def cmd_ping(args=""):
    if not args.strip():
        args = input("Host/IP to ping (flags allowed): ").strip()
        if not args:
            return
    run_and_print(f"ping {args}")

def cmd_pingpayload(args=""):
    target = input("Target (default 127.0.0.1): ").strip() or "127.0.0.1"
    cnt = input("Count (default 4): ").strip() or "4"
    size = input("Payload size in bytes (default 32): ").strip() or "32"
    run_and_print(f"ping -n {cnt} -l {size} {target}")

def cmd_pinginline(args=""):
    if not args.strip():
        args = input("Enter host + flags: ").strip()
        if not args:
            return
    run_and_print(f"ping {args}")

def cmd_fastping(args=""):
    target = args.strip() or input("Target for fastping: ").strip()
    if not target: return
    cnt_text = input("Number of pings (0=infinite, default 0): ").strip() or "0"
    interval_text = input("Interval seconds (default 0.2): ").strip() or "0.2"
    try: cnt = int(cnt_text)
    except: cnt = 0
    try: interval = float(interval_text)
    except: interval = 0.2
    print(f"Pinging {target} every {interval}s. Press Ctrl+C to stop.")
    n = 0
    try:
        while cnt == 0 or n < cnt:
            subprocess.run(f"ping -n 1 {target}", shell=True)
            n += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nFastping stopped.")

def cmd_tracert(args=""):
    host = args.strip() or input("Host for tracert: ").strip()
    if not host: return
    run_and_print(f"tracert {host}")

def cmd_ns(args=""):
    target = args.strip() or input("Host for nslookup: ").strip()
    if not target: return
    run_and_print(f"nslookup {target}")

def cmd_netinfo(args=""):
    print("Showing network info (no passwords).")
    cmds = ["ipconfig /all", "netsh wlan show interfaces", "netsh wlan show profiles", "arp -a", "route print", "ipconfig /displaydns", "whoami"]
    try:
        for c in cmds:
            print("\n=== ", c, " ===")
            run_and_print(c)
    except KeyboardInterrupt:
        print("\nInterrupted.")

def cmd_saveinfo(args=""):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(tempfile.gettempdir(), f"venom_netinfo_{ts}.txt")
    try:
        with open(out, "w", encoding="utf-8", errors="replace") as f:
            cmds = ["ipconfig /all", "netsh wlan show interfaces", "netsh wlan show profiles", "arp -a", "route print", "ipconfig /displaydns", "whoami"]
            for c in cmds:
                f.write(f"=== {c} ===\n")
                outp, err, rc = run_quiet(c, timeout=20)
                f.write((outp or err) + "\n\n")
        print("Saved to", out)
    except Exception as e:
        print("saveinfo failed:", e)

def cmd_wifi(args=""):
    run_and_print("netsh wlan show interfaces")

def cmd_speedtest(args=""):
    if shutil.which("speedtest-cli"):
        run_and_print("speedtest-cli")
    elif shutil.which("speedtest"):
        run_and_print("speedtest")
    else:
        print("No speedtest CLI installed. Install 'speedtest-cli' or 'speedtest'.")

def cmd_dnsflush(args=""):
    run_and_print("ipconfig /flushdns")

def cmd_hostname(args=""):
    print(socket.gethostname())

def cmd_netstat(args=""):
    run_and_print("netstat -ano")

def cmd_arp(args=""):
    run_and_print("arp -a")

def cmd_ports(args=""):
    cmd_netstat(args)

def cmd_users(args=""):
    run_and_print("net user")

# --- Internet helpers ---
def cmd_freeminecraft(args):
    print("https://eaglercraft.com/mc/1.12.2")

def cmd_http(args=""):
    url = args.strip() or input("URL (e.g. https://example.com): ").strip()
    if not url: return
    if "://" not in url: url = "http://" + url
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("Status:", resp.status)
            for k, v in resp.getheaders():
                print(f"{k}: {v}")
    except Exception as e:
        print("http failed:", e)

def cmd_download(args=""):
    url = args.strip() or input("URL to download: ").strip()
    if not url: return
    if "://" not in url: url = "http://" + url
    fname = os.path.basename(url.split("?", 1)[0]) or "download"
    out = os.path.join(tempfile.gettempdir(), f"venom_download_{int(time.time())}_{fname}")
    try:
        import urllib.request
        urllib.request.urlretrieve(url, out)
        print("Saved to", out)
    except Exception as e:
        print("download failed:", e)

def cmd_open(args=""):
    target = args.strip() or input("URL/file to open: ").strip()
    if not target: return
    try:
        webbrowser.open(target)
        print("Opened:", target)
    except Exception as e:
        print("open failed:", e)

# --- File management (NEW commands added) ---
def resolve_path(p):
    """Return absolute path; allow ~ and variables."""
    if not p:
        return p
    p = os.path.expanduser(p)
    p = os.path.expandvars(p)
    return os.path.abspath(p)

def cmd_find(args=""):
    """find <pattern> — find files by name pattern (supports glob, searches recursively)."""
    pattern = args.strip() or input("Filename or pattern to find (e.g. '*.txt' or report.docx): ").strip()
    if not pattern:
        return
    start = "."
    # allow specifying path: "pattern path"
    parts = pattern.split(" ", 1)
    if len(parts) == 2 and os.path.exists(parts[1]):
        pattern, start = parts[0], parts[1]
    start = resolve_path(start)
    matches = []
    for root, dirs, files in os.walk(start):
        # check files and dirs
        for name in files + dirs:
            if glob.fnmatch.fnmatch(name, pattern):
                matches.append(os.path.join(root, name))
    if matches:
        for m in matches:
            print(m)
    else:
        print("No matches found.")

def cmd_search(args=""):
    """search <text> <path> — search for text inside files. Prompts if missing."""
    parts = args.strip().split(" ", 1)
    if len(parts) == 2:
        text, path = parts[0], parts[1]
    else:
        text = args.strip() or input("Text to search for: ").strip()
        path = input("Path to search in (default .): ").strip() or "."
    if not text:
        return
    start = resolve_path(path)
    matches = []
    for root, dirs, files in os.walk(start):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if text in line:
                            print(f"{fpath}:{i}: {line.strip()}")
                            matches.append(fpath)
                            break
            except Exception:
                continue
    if not matches:
        print("No occurrences found.")

def cmd_copyfile(args=""):
    parts = args.strip().split(" ", 1)
    if len(parts) >= 2:
        src, dst = parts[0], parts[1]
    else:
        src = input("Source file: ").strip()
        dst = input("Destination (file or folder): ").strip()
    if not src or not dst:
        return
    src = resolve_path(src); dst = resolve_path(dst)
    try:
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.copy2(src, dst)
        print("Copied:", src, "->", dst)
    except Exception as e:
        print("copyfile failed:", e)

def cmd_movefile(args=""):
    parts = args.strip().split(" ", 1)
    if len(parts) >= 2:
        src, dst = parts[0], parts[1]
    else:
        src = input("Source file: ").strip()
        dst = input("Destination (file or folder): ").strip()
    if not src or not dst:
        return
    src = resolve_path(src); dst = resolve_path(dst)
    try:
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.move(src, dst)
        print("Moved:", src, "->", dst)
    except Exception as e:
        print("movefile failed:", e)

def cmd_deletefile(args=""):
    target = args.strip() or input("File to delete: ").strip()
    if not target:
        return
    target = resolve_path(target)
    if not os.path.exists(target):
        print("Not found:", target); return
    confirm = input(f"Type YES to delete {target}: ").strip()
    if confirm.upper() != "YES":
        print("Aborted."); return
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        print("Deleted:", target)
    except Exception as e:
        print("deletefile failed:", e)

def cmd_compress(args=""):
    """compress <path> -> creates path.zip in current dir (or specified dest if provided)"""
    parts = args.strip().split(" ", 1)
    if not parts[0]:
        p = input("Folder/file to compress: ").strip()
    else:
        p = parts[0]
    p = resolve_path(p)
    if not os.path.exists(p):
        print("Not found:", p); return
    base = os.path.basename(p.rstrip(os.sep))
    dest = parts[1].strip() if len(parts) > 1 and parts[1].strip() else f"{base}.zip"
    dest = resolve_path(dest)
    try:
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
            if os.path.isdir(p):
                for root, dirs, files in os.walk(p):
                    for fname in files:
                        fpath = os.path.join(root, fname)
                        arcname = os.path.relpath(fpath, os.path.dirname(p))
                        z.write(fpath, arcname)
            else:
                z.write(p, os.path.basename(p))
        print("Created zip:", dest)
    except Exception as e:
        print("compress failed:", e)

def cmd_extract(args=""):
    zfile = args.strip() or input("Zip file to extract: ").strip()
    if not zfile:
        return
    zfile = resolve_path(zfile)
    if not os.path.exists(zfile):
        print("Not found:", zfile); return
    dest = input("Destination folder (default current): ").strip() or "."
    dest = resolve_path(dest)
    try:
        with zipfile.ZipFile(zfile, "r") as z:
            z.extractall(dest)
        print("Extracted to:", dest)
    except Exception as e:
        print("extract failed:", e)

def cmd_filesize(args=""):
    f = args.strip() or input("File to show size: ").strip()
    if not f: return
    f = resolve_path(f)
    if not os.path.exists(f):
        print("Not found:", f); return
    size = os.path.getsize(f)
    units = ["B","KB","MB","GB","TB"]
    i = 0
    while size >= 1024 and i < len(units)-1:
        size /= 1024.0
        i += 1
    print(f"{f}: {size:.2f} {units[i]}")

def cmd_recent(args=""):
    path = args.strip() or "."
    path = resolve_path(path)
    if not os.path.isdir(path):
        print("Not a directory:", path); return
    items = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                mtime = os.path.getmtime(fpath)
                items.append((mtime, fpath))
            except Exception:
                continue
    items.sort(reverse=True)
    for mtime, fpath in items[:50]:
        print(datetime.datetime.fromtimestamp(mtime).isoformat(), fpath)

# --- Fun & misc ---
def cmd_say(args=""):
    text = args.strip() or input("Text to say: ").strip()
    if not text: return
    try:
        safe = text.replace("'", "''")
        ps = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe}')"
        subprocess.run(["powershell", "-Command", ps], shell=False)
    except Exception as e:
        print("say failed:", e)

def cmd_typewriter(args=""):
    text = args or input("Text: ")
    try: d = float(input("Delay per char (s, default 0.05): ").strip() or "0.05")
    except: d = 0.05
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(d)
    print()

def cmd_matrix(args=""):
    import random
    cols = shutil.get_terminal_size((80,20)).columns
    try:
        while True:
            print("".join(random.choice("01 ") for _ in range(cols)))
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nMatrix stopped.")

def cmd_clock(args=""):
    try:
        while True:
            print("\r" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nClock stopped.")

def cmd_timer(args=""):
    try:
        s = int(args.strip()) if args.strip() else int(input("Seconds: ").strip() or "0")
    except:
        print("Invalid number."); return
    try:
        for i in range(s, -1, -1):
            print(f"\r{i} seconds remaining", end="")
            time.sleep(1)
        print("\nTimer finished.")
    except KeyboardInterrupt:
        print("\nTimer stopped.")

def cmd_remind(args=""):
    try:
        secs = int(input("Remind in how many seconds? ").strip())
    except:
        print("Invalid."); return
    msg = input("Message: ").strip()
    print(f"Reminder set for {secs} seconds.")
    try:
        time.sleep(secs)
        print("\nREMINDER:", msg)
    except KeyboardInterrupt:
        print("\nReminder cancelled.")

# --- hexplain / history ---
def cmd_hexplain(args=""):
    s = args.strip() or input("Filename or ':s <text>': ").strip()
    if s.startswith(":s "):
        b = s[3:].encode("utf-8", errors="replace")
        width = 16
        for i in range(0, len(b), width):
            chunk = b[i:i+width]
            hex_bytes = " ".join(f"{bb:02X}" for bb in chunk)
            ascii_repr = "".join(chr(bb) if 32 <= bb < 127 else "." for bb in chunk)
            print(f"{i:08X}  {hex_bytes:<48}  {ascii_repr}")
        return
    if not os.path.exists(s):
        print("File not found:", s)
        return
    data = Path(s).read_bytes()
    width = 16
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_bytes = " ".join(f"{bb:02X}" for bb in chunk)
        ascii_repr = "".join(chr(bb) if 32 <= bb < 127 else "." for bb in chunk)
        print(f"{i:08X}  {hex_bytes:<48}  {ascii_repr}")

def cmd_history(args=""):
    print("History file:", HIST_PATH)
    if os.path.exists(HIST_PATH):
        with open(HIST_PATH, "r", encoding="utf-8", errors="replace") as f:
            print(f.read(), end="")
    else:
        print("(no history yet)")

def cmd_savehistory(args=""):
    save_history(args or "")
    print("Saved history entry.")

# --- explanations ---
EXPLAINS = {
    "freeminecraft":"get a link to free minecraft",
    "chatbot":"connect to a ai chatbot",
    "help":"Show categorized help. Use 'explain <command>' for details.",
    "ping":"ping — test reachability. Use Ctrl+C to stop continuous ping.",
    "fastping":"fastping — repeated single pings with interval (sub-second possible).",
    "pingpayload":"pingpayload — interactive: set count and payload size.",
    "pinginline":"pinginline — ping with flags inline.",
    "tracert":"tracert — trace route to host.",
    "ns":"ns — run nslookup for host.",
    "netinfo":"netinfo — show network interfaces, ARP, routes, Wi-Fi info, user.",
    "saveinfo":"saveinfo — saves netinfo output to temp file.",
    "myip":"myip — show local outbound and public IP.",
    "wifi":"wifi — show connected Wi-Fi info via netsh.",
    "speedtest":"speedtest — runs speedtest-cli or speedtest if installed.",
    "dnsflush":"dnsflush — flush DNS cache (ipconfig /flushdns).",
    "hostname":"hostname — print hostname.",
    "netstat":"netstat — lists active network connections.",
    "arp":"arp — show ARP table.",
    "ports":"ports — alias to netstat listing.",
    "users":"users — list user accounts or logged-in users.",
    "http":"http — HTTP HEAD request, shows status and headers.",
    "download":"download — download a URL to temp folder.",
    "open":"open — open URL/file with default handler.",
    "ls":"ls/dir — list directory entries.",
    "cd":"cd — change directory.",
    "cat":"cat/type — print file contents.",
    "copy":"copy — copy files.",
    "del":"del/rm — delete files (supports glob).",
    "rename":"rename/mv — rename files.",
    "mkdir":"mkdir — make directory.",
    "rmdir":"rmdir — remove directory recursively.",
    "find":"find — search files by name (supports glob).",
    "search":"search — search text inside files.",
    "copyfile":"copyfile — copy file (handles folders as dest).",
    "movefile":"movefile — move/rename file or folder.",
    "deletefile":"deletefile — delete file or folder (confirmation).",
    "compress":"compress — create zip from folder/file.",
    "extract":"extract — extract zip file.",
    "filesize":"filesize — show human-readable size.",
    "recent":"recent — list recently modified files.",
    "sysinfo":"sysinfo — print OS/CPU/memory info (psutil improves output).",
    "battery":"battery — show battery status (WMIC).",
    "storage":"storage — show mounted drives and free space.",
    "processes":"processes — list running processes.",
    "kill":"kill — terminate a process by PID or name.",
    "whoami":"whoami — current username and hostname.",
    "whereami":"whereami — prints current working directory.",
    "env":"env — print environment variables.",
    "path":"path — print PATH entries.",
    "say":"say — text-to-speech via PowerShell.",
    "typewriter":"typewriter — print text slowly.",
    "matrix":"matrix — matrix-like animation (Ctrl+C to stop).",
    "clock":"clock — live clock (Ctrl+C stops).",
    "timer":"timer — countdown timer.",
    "remind":"remind — set a delayed reminder.",
    "hexplain":"hexplain — hex dump of file or string.",
    "history":"history — show saved command history file.",
    "savehistory":"savehistory — save custom entry to history."
}

def cmd_explain(args=""):
    key = (args or "").strip().lower()
    if not key:
        print("Usage: explain <command>")
        return
    print(EXPLAINS.get(key, f"No explanation for '{key}'. Try 'help'."))

# ---------------- Command map ----------------
COMMANDS = {
    # Core
    "help": cmd_help, "h": cmd_help,
    "cls": cmd_cls,
    "exit": cmd_exit, "q": cmd_exit,
    "version": cmd_version, "about": cmd_about,
    # time/date/util
    "time": cmd_time, "date": cmd_date, "randtitle": cmd_randtitle, "sleep": cmd_sleep,
    # ping/network
    "ping": cmd_ping, "pingpayload": cmd_pingpayload, "pinginline": cmd_pinginline,
    "fastping": cmd_fastping, "tracert": cmd_tracert, "ns": cmd_ns,
    "netinfo": cmd_netinfo, "saveinfo": cmd_saveinfo, "myip": cmd_myip, "netip": cmd_myip,
    "wifi": cmd_wifi, "speedtest": cmd_speedtest, "dnsflush": cmd_dnsflush, "hostname": cmd_hostname,
    "netstat": cmd_netstat, "arp": cmd_arp, "ports": cmd_ports, "users": cmd_users,
    # internet
    "http": cmd_http, "download": cmd_download, "open": cmd_open,"freeminecraft":cmd_freeminecraft,
    # files
    "ls": cmd_ls, "dir": cmd_ls, "cd": cmd_cd, "cat": cmd_cat, "type": cmd_cat,
    "copy": cmd_copyfile, "copyfile": cmd_copyfile, "movefile": cmd_movefile, "deletefile": cmd_deletefile,
    "del": cmd_deletefile, "rm": cmd_deletefile, "rename": cmd_rename, "mv": cmd_rename,
    "mkdir": cmd_mkdir, "rmdir": cmd_rmdir,
    "find": cmd_find, "search": cmd_search, "compress": cmd_compress, "extract": cmd_extract,
    "filesize": cmd_filesize, "recent": cmd_recent,
    # system extras
    "sysinfo": cmd_sysinfo, "battery": cmd_battery, "storage": cmd_storage,
    "processes": cmd_processes, "kill": cmd_kill, "whoami": cmd_whoami, "whereami": cmd_whereami,
    "env": cmd_env, "path": cmd_path, "uptime": cmd_uptime,
    # fun / utilities
    "calc": lambda a="": run_and_print("start calc" if IS_WINDOWS else "gnome-calculator"),
    "echo": cmd_echo,
    "say": cmd_say, "typewriter": cmd_typewriter, "matrix": cmd_matrix, "clock": cmd_clock,
    "timer": cmd_timer, "remind": cmd_remind,
    #ai
    "chatbot":cmd_chatbot,
    # help/tools
    "hexplain": cmd_hexplain, "history": cmd_history, "savehistory": cmd_savehistory, "explain": cmd_explain
}

# ---------------- Main loop ----------------
def main():
    set_title("venom.console")
    clear_screen()
    while True:
        try:
            # label line (blue)
            if IS_WINDOWS: set_color(BLUE)
            sys.stdout.write("venom.console >\n")
            if IS_WINDOWS: reset_color()
            # input line (plain default)
            raw = input("> ").strip()
            if not raw:
                continue
            save_history(raw)
            # "<cmd> explain" support
            if raw.endswith(" explain"):
                key = raw[:-8].strip()
                cmd_explain(key)
                continue
            parts = raw.split(" ", 1)
            verb = parts[0].lower()
            rest = parts[1] if len(parts) > 1 else ""
            func = COMMANDS.get(verb)
            if func:
                try:
                    func(rest)
                except KeyboardInterrupt:
                    print("\nOperation interrupted (Ctrl+C).")
                except Exception as e:
                    if IS_WINDOWS: set_color(RED)
                    print("Error:", e)
                    if IS_WINDOWS: reset_color()
            else:
                if IS_WINDOWS: set_color(RED)
                print(f"'{raw}' is not a recognized command.")
                if IS_WINDOWS: reset_color()
        except KeyboardInterrupt:
            print("\nOperation stopped (Ctrl+C).")
        except EOFError:
            print("\nEOF — exiting.")
            break
        except Exception as e:
            print("Main loop error:", e)

# ---------------- Safe exit for double-click (pause) ----------------
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except Exception:
        import traceback
        print("Fatal error (stack trace):")
        traceback.print_exc()
    finally:
        try:
            sys.stdout.flush()
        except Exception:
            pass
        if os.name == "nt":
            try:
                os.system("pause")
            except Exception:
                try:
                    input("Press Enter to exit...")
                except Exception:
                    pass
        else:
            try:
                input("Press Enter to exit...")
            except Exception:
                pass

# ----- Replace the final block with this (safe crash catcher) -----
if __name__ == "__main__":
    import traceback, pathlib
    log_path = pathlib.Path(__file__).with_name("venom_crash.log")
    try:
        main()
    except SystemExit:
        # normal exit
        pass
    except Exception:
        # write full traceback to venom_crash.log
        with open(log_path, "w", encoding="utf-8") as fh:
            fh.write("Fatal error - full traceback:\n\n")
            traceback.print_exc(file=fh)
        # also print a short message to console so Explorer shows something
        print("A fatal error occurred. See file:", log_path)
        print("The full traceback was written to", log_path)
    finally:
        # ensure console pauses on exit so it won't immediately close
        try:
            sys.stdout.flush()
        except Exception:
            pass
        if os.name == "nt":
            try:
                os.system("pause")
            except Exception:
                try:
                    input("Press Enter to exit...")
                except Exception:
                    pass
        else:
            try:
                input("Press Enter to exit...")
            except Exception:
                pass
