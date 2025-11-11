#!/usr/bin/env python3
"""
venom_console_windows_full.py
Windows-only, ANSI colors, all commands implemented (best-effort).
No external libs required. Ctrl+C stops loops.
"""
def cmd_uptime(args=""):
    """
    Show system uptime.
    Tries psutil for a clean uptime; otherwise prints Windows 'net stats workstation'
    output (which includes 'Statistics since' line) as a fallback.
    """
    try:
        # Preferred: psutil gives precise uptime
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
        # fallback for Windows: show net stats workstation which contains 'Statistics since'
        try:
            if IS_WINDOWS:
                out, err, rc = run_quiet("net stats workstation", timeout=5)
                if out:
                    print(out)
                    # Try to parse "Statistics since ..." to show a nicer uptime
                    for line in out.splitlines():
                        if "Statistics since" in line or "Statistics Since" in line:
                            svc = line.strip()
                            print("Found:", svc)
                            break
                    return
            # On non-Windows fallback to 'uptime' command if available
            out, err, rc = run_quiet("uptime", timeout=5)
            if out:
                print(out)
                return
        except Exception:
            pass
    print("Uptime information not available (install 'psutil' for better output).")

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
from pathlib import Path

# ---------------- ANSI Colors ----------------
BLUE = "\033[94m"
ORANGE = "\033[93m"
WHITE = "\033[97m"
RED = "\033[91m"
RESET = "\033[0m"

IS_WINDOWS = os.name == "nt"
VERSION = "venom.console v1.6-windows"
HIST_PATH = os.path.join(tempfile.gettempdir(), "venom_history.txt")

# ---------------- Helpers ----------------
def save_history(entry: str):
    try:
        with open(HIST_PATH, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat()} {entry}\n")
    except Exception:
        pass

def set_title(s):
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(s)
    except Exception:
        pass

def clear_screen():
    os.system("cls")

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

def cmd_help(args=""):
    print(BLUE + "Available Commands (categorized):" + RESET)
    print(BLUE + "\n[Core]" + RESET)
    print("  help/h, cls, exit/q, version, about")
    print(BLUE + "\n[System]" + RESET)
    print("  sysinfo, uptime, whoami, whereami, env, path, processes, kill, storage, battery")
    print(BLUE + "\n[Network]" + RESET)
    print("  ping, fastping, pingpayload, pinginline, tracert, ns, netinfo, saveinfo, myip/netip, wifi, speedtest, dnsflush, hostname, netstat, arp, ports, users")
    print(BLUE + "\n[Internet]" + RESET)
    print("  http, download, open")
    print(BLUE + "\n[Files]" + RESET)
    print("  ls/dir, cd, cat/type, copy, del/rm, rename/mv, mkdir, rmdir")
    print(BLUE + "\n[Utilities]" + RESET)
    print("  calc, time, date, randtitle, sleep, echo, history, savehistory, remind, timer, clock")
    print(BLUE + "\n[Help Tools]" + RESET)
    print("  explain, hexplain")
    print(BLUE + "\n[Fun]" + RESET)
    print("  say, typewriter, matrix")
    print(WHITE + "\nUse 'explain <command>' or '<command> explain' for details.")
    print("Press Ctrl+C to stop long-running commands (ping -t, fastping, matrix, etc.)." + RESET)
    print()

def cmd_cls(args=""):
    clear_screen()

def cmd_exit(args=""):
    print("Exiting...")
    sys.exit(0)

def cmd_version(args=""):
    print(VERSION)

def cmd_about(args=""):
    print("venom.console — Windows ANSI full version. Use 'help' and 'explain <command>'.")

def cmd_echo(args=""):
    print(args)

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

# --- ping/network variants ---
def cmd_ping(args=""):
    if not args.strip():
        args = input("Host/IP to ping (flags allowed): ").strip()
        if not args:
            return
    run_and_print(f"ping {args}")

def cmd_pingpayload(args=""):
    print("Pingpayload — interactive.")
    target = input("Target (default 127.0.0.1): ").strip() or "127.0.0.1"
    cnt = input("Count (default 4): ").strip() or "4"
    size = input("Payload size bytes (default 32): ").strip() or "32"
    run_and_print(f"ping -n {cnt} -l {size} {target}")

def cmd_pinginline(args=""):
    if not args.strip():
        args = input("Host + flags: ").strip()
        if not args: return
    run_and_print(f"ping {args}")

def cmd_fastping(args=""):
    target = args.strip() or input("Target for fastping: ").strip()
    if not target:
        return
    cnt_text = input("Number of pings (0=infinite, default 0): ").strip() or "0"
    interval_text = input("Interval seconds (e.g. 0.1, default 0.2): ").strip() or "0.2"
    try:
        cnt = int(cnt_text)
    except:
        cnt = 0
    try:
        interval = float(interval_text)
    except:
        interval = 0.2
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

def cmd_myip(args=""):
    hostname = socket.gethostname()
    local = get_local_outbound_ip() or "Unavailable"
    public = get_public_ip() or "Unavailable"
    print(f"Hostname: {hostname}\nLocal IP: {local}\nPublic IP: {public}")

def cmd_wifi(args=""):
    try:
        run_and_print("netsh wlan show interfaces")
    except Exception as e:
        print("wifi failed:", e)

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

# --- Files ---
def cmd_ls(args=""):
    path = args.strip() or "."
    try:
        for e in sorted(os.listdir(path)):
            full = os.path.join(path, e)
            if os.path.isdir(full):
                print(f"<DIR> {e}")
            else:
                print(f"      {e} ({os.path.getsize(full)} bytes)")
    except Exception as e:
        print("ls failed:", e)

def cmd_cd(args=""):
    target = args.strip() or input("Change dir to: ").strip()
    if not target: return
    try:
        os.chdir(os.path.expanduser(target))
        print("CWD:", os.getcwd())
    except Exception as e:
        print("cd failed:", e)

def cmd_cat(args=""):
    fname = args.strip() or input("File to show: ").strip()
    if not fname: return
    try:
        with open(fname, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
    except Exception as e:
        print("cat failed:", e)

def cmd_copy(args=""):
    parts = args.split()
    if len(parts) >= 2:
        src, dst = parts[0], parts[1]
    else:
        src = input("Source file: ").strip()
        dst = input("Destination: ").strip()
    try:
        shutil.copy2(src, dst)
        print("Copied.")
    except Exception as e:
        print("copy failed:", e)

def cmd_del(args=""):
    target = args.strip() or input("File(s) to delete (glob supported): ").strip()
    if not target: return
    matches = glob.glob(target)
    if not matches:
        print("No matches.")
        return
    print("Matches:", matches)
    confirm = input("Type YES to delete all matches: ").strip()
    if confirm.upper() != "YES":
        print("Aborted.")
        return
    for m in matches:
        try:
            if os.path.isdir(m):
                shutil.rmtree(m)
            else:
                os.remove(m)
            print("Deleted", m)
        except Exception as e:
            print("delete failed for", m, e)

def cmd_rename(args=""):
    parts = args.split()
    if len(parts) >= 2:
        src, dst = parts[0], parts[1]
    else:
        src = input("Source: ").strip()
        dst = input("New name: ").strip()
    try:
        os.rename(src, dst)
        print("Renamed.")
    except Exception as e:
        print("rename failed:", e)

def cmd_mkdir(args=""):
    d = args.strip() or input("Directory to create: ").strip()
    if not d: return
    try:
        os.makedirs(d, exist_ok=True)
        print("Created.")
    except Exception as e:
        print("mkdir failed:", e)

def cmd_rmdir(args=""):
    d = args.strip() or input("Directory to remove: ").strip()
    if not d: return
    try:
        shutil.rmtree(d)
        print("Removed.")
    except Exception as e:
        print("rmdir failed:", e)

# --- System extras ---
def cmd_sysinfo(args=""):
    try:
        import platform
        print(platform.platform())
        print("Processor:", platform.processor())
        try:
            import psutil
            vm = psutil.virtual_memory()
            print(f"Memory: {vm.total//(1024**2)}MB available={vm.available//(1024**2)}MB")
            print("CPU logical count:", psutil.cpu_count(logical=True))
        except Exception:
            print("(install 'psutil' for richer info)")
    except Exception as e:
        print("sysinfo failed:", e)

def cmd_battery(args=""):
    run_and_print("wmic path Win32_Battery get EstimatedChargeRemaining,BatteryStatus /format:list")

def cmd_storage(args=""):
    run_and_print("wmic logicaldisk get name,size,freespace,description /format:list")

def cmd_processes(args=""):
    run_and_print("tasklist")

def cmd_kill(args=""):
    tgt = args.strip() or input("PID or process name to kill: ").strip()
    if not tgt: return
    confirm = input(f"Type YES to kill {tgt}: ").strip()
    if confirm.upper() != "YES":
        print("Aborted.")
        return
    if tgt.isdigit():
        run_and_print(f"taskkill /PID {tgt} /F")
    else:
        run_and_print(f"taskkill /IM \"{tgt}\" /F")
    print("Kill attempted.")

def cmd_whoami(args=""):
    try:
        print("User:", os.getlogin())
    except:
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

# --- Fun & utilities ---
def cmd_say(args=""):
    text = args.strip() or input("Text to say: ").strip()
    if not text: return
    try:
        # Use PowerShell System.Speech
        safe = text.replace("'", "''")
        ps = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe}')"
        subprocess.run(["powershell", "-Command", ps], shell=False)
    except Exception as e:
        print("say failed:", e)

def cmd_typewriter(args=""):
    text = args or input("Text to type: ")
    try:
        d = float(input("Delay per char (s, default 0.05): ").strip() or "0.05")
    except:
        d = 0.05
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
    "help":"Show categorized help. Use 'explain <command>' for details.",
    "ping":"ping — test reachability. Use Ctrl+C to stop continuous ping.",
    "fastping":"fastping — repeated single pings with interval (sub-second possible).",
    "pingpayload":"pingpayload — interactive ping with payload size.",
    "pinginline":"pinginline — ping with flags inline.",
    "tracert":"tracert — trace route to host.",
    "ns":"ns — run nslookup for host.",
    "netinfo":"netinfo — show network interfaces, ARP, routes, Wi-Fi info, user.",
    "saveinfo":"saveinfo — saves netinfo output to temp file.",
    "myip":"myip — show local outbound and public IP.",
    "wifi":"wifi — show Wi-Fi interface info via netsh.",
    "speedtest":"speedtest — run speedtest-cli or speedtest if installed.",
    "dnsflush":"dnsflush — flush DNS cache (ipconfig /flushdns).",
    "hostname":"hostname — print hostname.",
    "netstat":"netstat — show active connections.",
    "arp":"arp — show ARP table.",
    "ports":"ports — alias to netstat.",
    "users":"users — list local user accounts.",
    "http":"http — HTTP HEAD request.",
    "download":"download — download URL to temp folder.",
    "open":"open — open URL/file with default handler.",
    "ls":"ls — list directory entries.",
    "cd":"cd — change directory.",
    "cat":"cat — show file contents.",
    "copy":"copy — copy files.",
    "del":"del — delete files (supports glob).",
    "rename":"rename — rename files.",
    "mkdir":"mkdir — make directory.",
    "rmdir":"rmdir — remove directory.",
    "sysinfo":"sysinfo — show OS/CPU/memory info (psutil optional).",
    "battery":"battery — print battery info (WMIC).",
    "storage":"storage — list drives and free space.",
    "processes":"processes — list running processes.",
    "kill":"kill — terminate a process by PID or name.",
    "whoami":"whoami — current username and hostname.",
    "whereami":"whereami — show current working directory.",
    "env":"env — print environment variables.",
    "path":"path — print PATH entries.",
    "say":"say — text-to-speech via PowerShell.",
    "typewriter":"typewriter — print text slowly.",
    "matrix":"matrix — animation (Ctrl+C to stop).",
    "clock":"clock — live clock (Ctrl+C to stop).",
    "timer":"timer — countdown timer.",
    "remind":"remind — delayed reminder.",
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
    "http": cmd_http, "download": cmd_download, "open": cmd_open,
    # files
    "ls": cmd_ls, "dir": cmd_ls, "cd": cmd_cd, "cat": cmd_cat, "type": cmd_cat,
    "copy": cmd_copy, "del": cmd_del, "rm": cmd_del, "rename": cmd_rename, "mv": cmd_rename,
    "mkdir": cmd_mkdir, "rmdir": cmd_rmdir,
    # system extras
    "sysinfo": cmd_sysinfo, "battery": cmd_battery, "storage": cmd_storage,
    "processes": cmd_processes, "kill": cmd_kill, "whoami": cmd_whoami, "whereami": cmd_whereami,
    "env": cmd_env, "path": cmd_path, "uptime": cmd_uptime,
    # fun / utilities
    "calc": lambda a="": run_and_print("start calc" if IS_WINDOWS else "gnome-calculator"),
    "echo": cmd_echo,
    "say": cmd_say, "typewriter": cmd_typewriter, "matrix": cmd_matrix, "clock": cmd_clock,
    "timer": cmd_timer, "remind": cmd_remind,
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
            print(BLUE + "venom.console >" + RESET)
            # input (orange)
            raw = input(ORANGE + "> " + RESET).strip()
            if not raw:
                continue
            save_history(raw)
            # support "<cmd> explain"
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
                    print(RED + "Error:" + RESET, e)
            else:
                print(RED + f"'{raw}' is not a recognized command." + RESET)
        except KeyboardInterrupt:
            print("\nOperation stopped (Ctrl+C).")
        except EOFError:
            print("\nEOF — exiting.")
            break
        except Exception as e:
            print("Main loop error:", e)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Show the traceback so you can see what went wrong if something crashes.
        import traceback
        print("Fatal error (stack trace):")
        traceback.print_exc()
    finally:
        # Ensure the console waits so a double-clicked window doesn't vanish.
        try:
            sys.stdout.flush()
        except Exception:
            pass
        if os.name == "nt":
            # Windows 'pause' reliably waits for a keypress in Explorer-launched consoles.
            try:
                os.system("pause")
            except Exception:
                # fallback to input if pause fails for some reason
                try:
                    input("Press Enter to exit...")
                except Exception:
                    pass
        else:
            # Non-windows fallback
            try:
                input("Press Enter to exit...")
            except Exception:
                pass
                
            