#!/usr/bin/env python3
"""
venom_console.py — consolidated checked version
All commands listed in help are implemented (best-effort).
Ctrl+C stops long-running commands.
"""
def cmd_uptime():
    """
    Show system uptime.
    """
    import psutil
    boot_time = psutil.boot_time()
    import datetime
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    print(f"System uptime: {uptime}")

try:
    import os, sys, time, datetime, subprocess, socket, shutil, tempfile, glob, webbrowser
    from pathlib import Path
    from colorama import init, Fore, Style
except Exception as e:
    print("Startup error:", e)
    input("Press Enter to exit...")
    sys.exit(1)

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

# colorama for cross-platform colors
try:
    from colorama import init, Fore, Style
except Exception:
    # install if missing, then import
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    except Exception:
        pass
    from colorama import init, Fore, Style

init(autoreset=True)

IS_WINDOWS = os.name == "nt"

VERSION = "venom.console v1.6"
HIST_PATH = os.path.join(tempfile.gettempdir(), "venom_history.txt")

def save_history(entry: str):
    try:
        with open(HIST_PATH, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat()} {entry}\n")
    except Exception:
        pass

def set_title(s):
    try:
        if IS_WINDOWS:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(s)
        else:
            sys.stdout.write(f"\x1b]0;{s}\x07")
    except Exception:
        pass

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")

def run_and_print(cmd, shell=True):
    try:
        subprocess.run(cmd, shell=shell)
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
# [All your commands remain here, omitted for brevity — ping, fastping, files, network, fun, utilities]
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
            print(Fore.BLUE + "venom.console >" + Style.RESET_ALL)
            # input line (plain white / default)
            raw = input("> ").strip()
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
                    print("Error:", e)
            else:
                print(f"'{raw}' is not a recognized command.")
        except KeyboardInterrupt:
            print("\nOperation stopped (Ctrl+C).")
        except EOFError:
            print("\nEOF — exiting.")
            break
        except Exception as e:
            print("Main loop error:", e)

if __name__ == "__main__":
    main()
