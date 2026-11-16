#!/usr/bin/env python3
"""无线 ADB 一键重连（Android 11+ / 含 Android 14）。

用法:
    python tools/adb_reconnect.py                 # 自动发现并连接
    python tools/adb_reconnect.py --list          # 只列出当前 adb 设备
    python tools/adb_reconnect.py --serial ip:port

连接顺序:
    1. 已有网络设备(ip:port)
    2. adb mDNS 发现 _adb-tls-connect._tcp
    3. USB 设备在场时, 自动 adb tcpip 5555 后无线连接
    4. 上次成功地址缓存 (tools/.adb_last_endpoint)

注意: Android 14 休眠/重启后无线调试会自动关闭, 此时需先在手机上重新打开
「设置 > 开发者选项 > 无线调试」, 否则任何脚本都无法凭空重连。
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

ADB = shutil.which("adb") or "adb"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".adb_last_endpoint")
MDNS_CONNECT = "_adb-tls-connect._tcp"


def adb(args, timeout=20):
    return subprocess.run([ADB, *args], capture_output=True, text=True, timeout=timeout)


def devices():
    """返回 [(serial, state)]。"""
    rows = []
    for line in adb(["devices"]).stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            rows.append((parts[0], parts[1]))
    return rows


def is_network(serial):
    return ":" in serial and not serial.startswith("emulator-")


def current_network():
    for serial, state in devices():
        if is_network(serial) and state == "device":
            return serial
    return None


def mdns_endpoints():
    eps = []
    for line in adb(["mdns", "services"]).stdout.splitlines():
        if MDNS_CONNECT in line:
            token = line.split()[-1]
            if ":" in token:
                eps.append(token)
    return eps


def connect(endpoint):
    r = adb(["connect", endpoint])
    msg = (r.stdout + r.stderr).strip()
    print(f"  {msg}" if msg else "")
    return "connected to" in msg or "already connected" in msg


def save(endpoint):
    try:
        with open(CACHE, "w", encoding="utf-8") as f:
            f.write(endpoint)
    except OSError:
        pass


def load():
    try:
        with open(CACHE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return None


def bootstrap_from_usb():
    usb = [s for s, st in devices() if st == "device" and not is_network(s) and not s.startswith("emulator-")]
    if not usb:
        return None
    serial = usb[0]
    print(f"发现 USB 设备 {serial}, 尝试开 tcpip 5555…")
    out = adb(["-s", serial, "shell", "ip", "-f", "inet", "addr", "show", "wlan0"]).stdout
    m = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", out)
    if not m:
        print("  读不到 wlan0 地址, 跳过。")
        return None
    endpoint = f"{m.group(1)}:5555"
    adb(["-s", serial, "tcpip", "5555"])
    import time
    time.sleep(1)
    print(f"  adb connect {endpoint}")
    if connect(endpoint):
        save(endpoint)
        return endpoint
    return None


def ensure_connected(serial=None):
    """供其它脚本复用。返回可用的网络 serial 或 None。"""
    if serial and is_network(serial) and any(s == serial and st == "device" for s, st in devices()):
        print(f"已连接: {serial}")
        return serial

    cur = current_network()
    if cur:
        print(f"已连接: {cur}")
        return cur

    print("未发现已连接的无线设备, 尝试重新发现…")
    for endpoint in mdns_endpoints():
        print(f"mDNS 发现 {endpoint}, 尝试连接…")
        if connect(endpoint):
            save(endpoint)
            print(f"连接成功: {endpoint}")
            return endpoint

    boot = bootstrap_from_usb()
    if boot:
        print(f"连接成功: {boot}")
        return boot

    last = load()
    if last:
        print(f"尝试上次地址 {last}…")
        if connect(last):
            print(f"连接成功: {last}")
            return last

    print("重连失败。请确认:")
    print("  1) 手机与电脑在同一 WiFi 网段;")
    print("  2) 设置 > 开发者选项 > 无线调试 已打开 (Android 14 休眠后会自动关闭);")
    print("  3) 或插一次数据线, 本脚本会自动 adb tcpip 5555 后无线连接。")
    return None


def main():
    ap = argparse.ArgumentParser(description="无线 ADB 一键重连")
    ap.add_argument("--list", action="store_true", help="只列出当前 adb 设备")
    ap.add_argument("--serial", help="指定网络设备序列号 ip:port")
    args = ap.parse_args()

    if args.list:
        for serial, state in devices():
            print(f"{serial}\t{state}")
        return 0

    endpoint = ensure_connected(args.serial)
    return 0 if endpoint else 1


if __name__ == "__main__":
    sys.exit(main())
