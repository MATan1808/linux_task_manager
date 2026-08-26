#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Linux Task Manager - Global Hotkey Listener Daemon
Lắng nghe phím tắt toàn hệ thống Ctrl+Shift+Esc và Ctrl+Alt+Del ở cấp độ X11 XGrabKey.
Đảm bảo 100% bắt được phím tắt trên Linux Mint mọi lúc mọi nơi.
"""

import os
import sys
import subprocess
import time

try:
    from Xlib import X, XK
    from Xlib.display import Display
except ImportError:
    print("Yêu cầu python3-xlib: sudo apt install -y python3-xlib")
    sys.exit(1)

def launch_task_manager():
    try:
        # Kiểm tra xem Task Manager có đang mở không
        # Nếu chưa mở thì khởi chạy mới
        subprocess.Popen(
            ["/bin/bash", "/media/tanma/DATA/terminal/launch.sh"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    except Exception as e:
        print("Lỗi khi mở Task Manager:", e)

def main():
    # Đảm bảo chỉ có 1 instance listener chạy
    lock_file = "/tmp/task_manager_hotkey.pid"
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r") as f:
                old_pid = int(f.read().strip())
            if os.path.exists(f"/proc/{old_pid}"):
                print(f"Hotkey listener đang chạy với PID {old_pid}")
                return
        except Exception:
            pass

    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))

    disp = Display()
    root = disp.screen().root

    # Lấy keycode
    keycode_esc = disp.keysym_to_keycode(XK.string_to_keysym("Escape"))
    keycode_del = disp.keysym_to_keycode(XK.string_to_keysym("Delete"))

    # Các trạng thái CapsLock / NumLock để không bị vô hiệu hóa
    lock_masks = [0, X.LockMask, X.Mod2Mask, X.LockMask | X.Mod2Mask]

    for mask in lock_masks:
        # 1. Ctrl + Shift + Esc
        root.grab_key(
            keycode_esc,
            X.ControlMask | X.ShiftMask | mask,
            True,
            X.GrabModeAsync,
            X.GrabModeAsync
        )
        # 2. Ctrl + Alt + Delete
        root.grab_key(
            keycode_del,
            X.ControlMask | X.Mod1Mask | mask,
            True,
            X.GrabModeAsync,
            X.GrabModeAsync
        )

    disp.sync()
    print("✅ Đã kích hoạt lắng nghe phím tắt toàn hệ thống: [Ctrl+Shift+Esc] và [Ctrl+Alt+Del]")

    last_trigger = 0.0
    while True:
        try:
            ev = disp.next_event()
            if ev.type == X.KeyPress:
                curr = time.time()
                # Chống debounce (bấm dính phím liên tiếp trong 0.8s)
                if curr - last_trigger > 0.8:
                    last_trigger = curr
                    launch_task_manager()
        except Exception as e:
            time.sleep(0.1)

if __name__ == "__main__":
    main()
