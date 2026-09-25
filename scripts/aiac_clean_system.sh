#!/usr/bin/env bash
# AIaC System Cleanup & Optimization Script for ASUS ZenBook (tanma)
# Authored-By: 360org <support@360.org.vn>

set -e

ACTION="${1:-all}"

case "$ACTION" in
    ram)
        # 1. Thu hồi bộ đệm RAM (Buffer/Cache)
        sync
        echo 3 > /proc/sys/vm/drop_caches
        # Nén swap thừa nếu còn đủ RAM
        swapoff -a 2>/dev/null && swapon -a 2>/dev/null || true
        echo "CLEAN_RAM_OK"
        ;;
    disk)
        # 2. Dọn file rác, APT cache, thumbnails & nhật ký journal cũ
        apt-get clean -y 2>/dev/null || true
        apt-get autoremove -y 2>/dev/null || true
        journalctl --vacuum-time=2d >/dev/null 2>&1 || true
        rm -rf /home/*/.cache/thumbnails/* 2>/dev/null || true
        rm -rf /home/*/.local/share/Trash/* 2>/dev/null || true
        rm -rf /home/*/.cache/google-chrome/Default/Cache/* 2>/dev/null || true
        rm -rf /home/*/.cache/google-chrome/Profile*/Cache/* 2>/dev/null || true
        rm -rf /home/*/.cache/uv/* 2>/dev/null || true
        rm -rf /home/*/.npm/_cacache/* 2>/dev/null || true
        rm -rf /var/tmp/* 2>/dev/null || true
        echo "CLEAN_DISK_OK"
        ;;
    optimize)
        # 3. Tối ưu độ nhạy ZenBook & giải phóng dịch vụ ngầm
        # Giảm swappiness để ưu tiên RAM vật lý 8GB
        sysctl -w vm.swappiness=10 >/dev/null 2>&1 || true
        sysctl -w vm.vfs_cache_pressure=50 >/dev/null 2>&1 || true

        # Dừng dịch vụ giả lập Android Waydroid nếu đang chạy chiếm tài nguyên
        if systemctl is-active --quiet waydroid-container 2>/dev/null; then
            systemctl stop waydroid-container 2>/dev/null || true
        fi

        # Dọn RAM cache
        sync
        echo 3 > /proc/sys/vm/drop_caches

        # Dọn rác
        journalctl --vacuum-time=2d >/dev/null 2>&1 || true
        apt-get clean -y 2>/dev/null || true
        rm -rf /home/*/.cache/thumbnails/* 2>/dev/null || true
        echo "OPTIMIZE_OK"
        ;;
    all)
        sync
        echo 3 > /proc/sys/vm/drop_caches
        apt-get clean -y 2>/dev/null || true
        journalctl --vacuum-time=2d >/dev/null 2>&1 || true
        rm -rf /home/*/.cache/thumbnails/* 2>/dev/null || true
        rm -rf /home/*/.local/share/Trash/* 2>/dev/null || true
        echo "ALL_OK"
        ;;
    *)
        echo "Unknown action: $ACTION"
        exit 1
        ;;
esac
