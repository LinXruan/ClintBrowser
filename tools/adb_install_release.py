#!/usr/bin/env python3
"""无线 ADB 重连 + 安装正式版 (release) APK。

用法:
    python tools/adb_install_release.py                # 用已构建的 release 包装机
    python tools/adb_install_release.py --build        # 先 assembleGithubRelease 再装
    python tools/adb_install_release.py --flavor foss --build
    python tools/adb_install_release.py --serial ip:port

说明:
    release 包名是 com.jhaiian.clint, debug 是 com.jhaiian.clint.debug, 两者可共存。
    未配置签名 (local.properties 缺 signingConfig.*) 时只会产出 unsigned 包,
    本脚本会检测并拒绝安装, 因为 adbd 不接受未签名 APK。
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adb_reconnect as ar  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADB = ar.ADB


def device_abi(serial):
    out = subprocess.run(
        [ADB, "-s", serial, "shell", "getprop", "ro.product.cpu.abi"],
        capture_output=True, text=True,
    ).stdout.strip()
    return out or None


def gradle_build(flavor):
    gradle = os.path.join(ROOT, "gradlew.bat" if os.name == "nt" else "gradlew")
    task = f":app:assemble{flavor.capitalize()}Release"
    print(f"构建 {task} …")
    if subprocess.run([gradle, task], cwd=ROOT).returncode != 0:
        print("构建失败。")
        return False
    return True


def find_apk(flavor, abi):
    """返回 (apk_path, signed)。优先设备 ABI 的已签名包。"""
    out_dir = os.path.join(ROOT, "app", "build", "outputs", "apk", flavor, "release")
    preferred = os.path.join(out_dir, f"app-{flavor}-{abi}-release.apk")
    if os.path.isfile(preferred):
        return preferred, True

    all_apks = glob.glob(os.path.join(out_dir, "*.apk"))
    signed = [p for p in all_apks if not p.endswith("-unsigned.apk")]
    if signed:
        return signed[0], True
    unsigned = [p for p in all_apks if p.endswith("-unsigned.apk")]
    if unsigned:
        return unsigned[0], False
    return None, False


def main():
    ap = argparse.ArgumentParser(description="无线 ADB 重连 + 安装正式版 APK")
    ap.add_argument("--build", action="store_true", help="安装前先构建 release")
    ap.add_argument("--flavor", default="github", choices=["github", "foss"])
    ap.add_argument("--serial", help="指定网络设备序列号 ip:port")
    args = ap.parse_args()

    endpoint = ar.ensure_connected(args.serial)
    if not endpoint:
        return 1

    abi = device_abi(endpoint)
    if not abi:
        print(f"无法读取 {endpoint} 的 ABI。")
        return 1
    print(f"设备 ABI: {abi}")

    if args.build and not gradle_build(args.flavor):
        return 1

    apk, signed = find_apk(args.flavor, abi)
    if not apk:
        print(f"未找到 release APK: app/build/outputs/apk/{args.flavor}/release/")
        print(f"先构建: ./gradlew :app:assemble{args.flavor.capitalize()}Release  (或加 --build)")
        return 1
    if not signed:
        print(f"找到的是未签名包: {os.path.basename(apk)}")
        print("adbd 无法安装未签名 APK。请在 local.properties 配置签名后重新构建:")
        print("  signingConfig.storeFile / storePassword / keyAlias / keyPassword")
        return 1

    print(f"安装 {os.path.basename(apk)} …")
    r = subprocess.run([ADB, "-s", endpoint, "install", "-r", apk], capture_output=True, text=True)
    msg = (r.stdout + r.stderr).strip()
    print(msg)
    return 0 if "Success" in msg else 1


if __name__ == "__main__":
    sys.exit(main())
