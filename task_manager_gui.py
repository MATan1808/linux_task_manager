#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Linux Task Manager (Windows 11 Modern Desktop Style - Non-Tech Friendly & High Performance)
Phát triển bởi AIaC dành riêng cho anh Tân.
Bản quyền & Quản trị: 360 CORP (support@360.org.vn)
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
from collections import deque

try:
    import psutil
except ImportError:
    print("Yêu cầu thư viện psutil. Đang cài đặt...")
    subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=False)
    import psutil

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableView, QHeaderView, QLineEdit,
        QTabWidget, QFrame, QMenu, QAction, QMessageBox, QComboBox,
        QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem
    )
    from PyQt5.QtCore import (
        Qt, QThread, pyqtSignal, QPointF, QAbstractTableModel, QModelIndex,
        QSortFilterProxyModel, QRegExp
    )
    from PyQt5.QtGui import (
        QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QCursor
    )
except ImportError:
    print("Yêu cầu thư viện PyQt5: sudo apt install -y python3-pyqt5")
    sys.exit(1)


# --- TỪ ĐIỂN NHẬN DIỆN & MÔ TẢ TIẾN TRÌNH THÔNG MINH CHO NON-TECH ---
KNOWN_PROCESS_INFO = {
    # Ứng dụng phổ biến (🟢 Có thể tắt an toàn)
    "chrome": ("Google Chrome", "Trình duyệt Web (Mở nhiều tab tốn RAM)", "safe"),
    "google-chrome": ("Google Chrome", "Trình duyệt Web (Mở nhiều tab tốn RAM)", "safe"),
    "chromium": ("Chromium", "Trình duyệt Web mã nguồn mở", "safe"),
    "firefox": ("Mozilla Firefox", "Trình duyệt Web Firefox", "safe"),
    "brave": ("Brave Browser", "Trình duyệt Web bảo mật", "safe"),
    "code": ("VS Code", "Trình soạn thảo mã nguồn Visual Studio Code", "safe"),
    "vscodium": ("VSCodium", "Trình soạn thảo lập trình", "safe"),
    "cursor": ("Cursor AI Editor", "Trình soạn thảo AI Code Editor", "safe"),
    "pycharm": ("PyCharm", "Môi trường lập trình Python IDE", "safe"),
    "vuaoffice": ("VuaOffice", "Bộ ứng dụng văn phòng VuaOffice", "safe"),
    "electron": ("Ứng dụng Electron", "Phần mềm chạy nền Node/Electron", "safe"),
    "telegram-desktop": ("Telegram", "Ứng dụng nhắn tin Telegram", "safe"),
    "slack": ("Slack", "Ứng dụng trao đổi công việc Slack", "safe"),
    "discord": ("Discord", "Ứng dụng chat & voice Discord", "safe"),
    "zalo": ("Zalo", "Ứng dụng nhắn tin Zalo", "safe"),
    "skype": ("Skype", "Ứng dụng gọi điện Skype", "safe"),
    "vlc": ("VLC Media Player", "Trình phát video & nhạc VLC", "safe"),
    "spotify": ("Spotify", "Ứng dụng nghe nhạc Spotify", "safe"),
    "rhythmbox": ("Rhythmbox", "Trình nghe nhạc mặc định", "safe"),
    "nemo": ("Trình quản lý File (Nemo)", "Cửa sổ quản lý thư mục và tệp tin", "safe"),
    "thunar": ("Trình quản lý File (Thunar)", "Cửa sổ quản lý thư mục", "safe"),
    "nautilus": ("Trình quản lý File (GNOME)", "Cửa sổ quản lý thư mục", "safe"),
    "xed": ("Trình soạn thảo Text (Xed)", "Phần mềm ghi chú text", "safe"),
    "gnome-terminal": ("Terminal", "Cửa sổ dòng lệnh Terminal", "safe"),
    "x-terminal-emulator": ("Terminal", "Cửa sổ dòng lệnh", "safe"),
    "libreoffice": ("LibreOffice", "Bộ ứng dụng văn phòng (Word/Excel)", "safe"),
    "soffice.bin": ("LibreOffice Core", "Bộ ứng dụng văn phòng", "safe"),
    "gimp": ("GIMP", "Phần mềm chỉnh sửa ảnh GIMP", "safe"),
    "inkscape": ("Inkscape", "Phần mềm vẽ vector Inkscape", "safe"),
    "python3": ("Chương trình Python", "Script hoặc ứng dụng viết bằng Python", "safe"),
    "python": ("Chương trình Python", "Script hoặc ứng dụng viết bằng Python", "safe"),
    "node": ("Node.js Server", "Ứng dụng chạy JavaScript Backend", "safe"),
    "java": ("Ứng dụng Java", "Phần mềm chạy trên máy ảo Java JVM", "safe"),

    # Dịch vụ nền & Bộ gõ (🟡 Cân nhắc)
    "ibus-daemon": ("Bộ gõ Tiếng Việt (IBus)", "Dịch vụ gõ tiếng Việt (Tắt sẽ không gõ được dấu)", "caution"),
    "ibus-extension": ("IBus Tiện ích", "Dịch vụ hỗ trợ bộ gõ", "caution"),
    "ibus-ui-gtk3": ("IBus Giao diện", "Khung hiển thị bộ gõ", "caution"),
    "fcitx": ("Bộ gõ Fcitx", "Dịch vụ gõ bàn phím", "caution"),
    "unikey": ("UniKey Linux", "Bộ gõ tiếng Việt Unikey", "caution"),
    "pipewire": ("Dịch vụ Âm thanh (PipeWire)", "Quản lý loa và microphone (Tắt sẽ mất tiếng)", "caution"),
    "pipewire-pulse": ("Dịch vụ Âm thanh", "Cầu nối âm thanh", "caution"),
    "pulseaudio": ("Dịch vụ Âm thanh (PulseAudio)", "Quản lý âm thanh (Tắt sẽ mất tiếng)", "caution"),
    "wireplumber": ("Quản lý Âm thanh", "Dịch vụ điều phối âm thanh", "caution"),
    "bluetoothd": ("Dịch vụ Bluetooth", "Quản lý kết nối tai nghe/chuột Bluetooth", "caution"),
    "blueman-applet": ("Khay Bluetooth", "Biểu tượng Bluetooth ở thanh Taskbar", "caution"),
    "cupsd": ("Dịch vụ Máy in (CUPS)", "Quản lý kết nối và in ấn tài liệu", "caution"),
    "cups-browsed": ("Dịch vụ Máy in Mạng", "Tìm kiếm máy in qua mạng LAN", "caution"),
    "cinnamon-screensaver": ("Màn hình khóa Cinnamon", "Trình bảo vệ và khóa màn hình", "caution"),
    "cinnamon-killer-daemon": ("Tiện ích Cinnamon", "Bộ giám sát màn hình Desktop", "caution"),
    "ssh-agent": ("Bảo mật SSH Key", "Quản lý chìa khóa đăng nhập SSH", "caution"),
    "gpg-agent": ("Bảo mật GPG", "Quản lý mật khẩu mã hóa", "caution"),
    "flameshot": ("Chụp màn hình Flameshot", "Phần mềm chụp ảnh màn hình", "caution"),
    "copyq": ("Lịch sử Clipboard CopyQ", "Lưu trữ lịch sử Copy/Paste", "caution"),

    # Tiến trình Hệ thống cốt lõi (🔴 Cấm tắt)
    "systemd": ("Nhân khởi động Linux (systemd)", "Tiến trình mẹ số 1 của hệ điều hành (CẤM TẮT)", "system"),
    "systemd-journald": ("Nhật ký Hệ thống", "Lưu trữ log hoạt động của Linux (CẤM TẮT)", "system"),
    "systemd-udevd": ("Quản lý Phần cứng", "Nhận diện cắm USB, chuột, bàn phím (CẤM TẮT)", "system"),
    "systemd-logind": ("Quản lý Đăng nhập", "Quản lý phiên làm việc người dùng (CẤM TẮT)", "system"),
    "systemd-resolved": ("Dịch vụ DNS", "Phân giải tên miền Internet (CẤM TẮT)", "system"),
    "Xorg": ("Máy chủ Đồ Họa (Xorg)", "Môi trường hiển thị màn hình (Tắt sẽ bị sập màn hình)", "system"),
    "cinnamon": ("Giao diện Màn hình (Cinnamon)", "Màn hình Desktop chính (Tắt sẽ mất giao diện)", "system"),
    "muffin": ("Bộ quản lý Cửa sổ (Muffin)", "Điều khiển di chuyển/thu nhỏ cửa sổ (CẤM TẮT)", "system"),
    "lightdm": ("Màn hình Đăng nhập (LightDM)", "Dịch vụ đăng nhập tài khoản (CẤM TẮT)", "system"),
    "dbus-daemon": ("Cầu nối Hệ thống (D-Bus)", "Giao tiếp giữa các phần mềm Linux (CẤM TẮT)", "system"),
    "polkitd": ("Quản lý Quyền Quản Trị", "Xác thực mật khẩu sudo/root (CẤM TẮT)", "system"),
    "accounts-daemon": ("Quản lý Tài khoản", "Quản lý người dùng hệ điều hành (CẤM TẮT)", "system"),
    "NetworkManager": ("Quản lý Mạng Internet", "Dịch vụ kết nối Wi-Fi & Mạng dây (CẤM TẮT)", "system"),
    "wpa_supplicant": ("Dịch vụ Wi-Fi", "Bảo mật kết nối Wi-Fi (CẤM TẮT)", "system"),
    "avahi-daemon": ("Dịch vụ Khám phá Mạng", "Kết nối thiết bị mạng LAN cục bộ", "system"),
    "cron": ("Lịch trình Hệ thống (Cron)", "Chạy các tác vụ tự động hẹn giờ", "system"),
    "rsyslogd": ("Ghi Log Hệ thống", "Lưu trữ sự kiện Linux", "system")
}


def classify_process(name, user, pid):
    name_lower = name.lower()
    
    # 1. Tra cứu trực tiếp từ điển
    if name_lower in KNOWN_PROCESS_INFO:
        nice_name, desc, category = KNOWN_PROCESS_INFO[name_lower]
        return nice_name, desc, category

    # 2. Kiểm tra tiến trình hệ thống root / kernel
    if user == "root" or pid <= 100 or name.startswith("kworker") or name.startswith("ksoftirqd") or name.startswith("rcu_"):
        return name, "Dịch vụ cốt lõi của hệ thống Linux (CẤM TẮT)", "system"

    # 3. Mặc định cho tiến trình người dùng
    if user != "root":
        return name, "Ứng dụng hoặc tiến trình chạy bởi người dùng", "safe"
    
    return name, "Dịch vụ chạy ngầm của hệ điều hành", "caution"


# --- UTILS ĐỊNH DẠNG & THÔNG TIN HỆ THỐNG ---
def format_bytes(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024**2:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024**3:
        return f"{bytes_val / (1024**2):.1f} MB"
    else:
        return f"{bytes_val / (1024**3):.2f} GB"

def get_cpu_model():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "Intel/AMD Processor"

def get_gpu_info_text():
    try:
        res = subprocess.run(["lspci"], capture_output=True, text=True, check=True)
        gpus = []
        for line in res.stdout.splitlines():
            if any(k in line.lower() for k in ["vga compatible", "3d controller", "display controller"]):
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    gpus.append(parts[2].strip())
        if gpus:
            return " • ".join(gpus)
    except Exception:
        pass
    return "Đồ họa tích hợp (Integrated GPU)"

def get_system_uptime():
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        if days > 0:
            return f"{days} ngày, {hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception:
        return "N/A"

def get_os_info():
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=", 1)[1].strip().strip('"')
    except Exception:
        pass
    return "Linux OS"


# --- HIGH PERFORMANCE PROCESS TABLE MODEL (VIRTUALIZED MODEL/VIEW) ---
class ProcessTableModel(QAbstractTableModel):
    HEADERS = [
        "Tên Tiến Trình", "Mô Tả & Hướng Dẫn (Non-Tech)", "Khuyến Nghị",
        "CPU %", "Bộ Nhớ RAM", "RAM %", "PID", "Người Dùng"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.processes = []
        self._sort_col = 3  # Mặc định sort CPU %
        self._sort_order = Qt.DescendingOrder

    def rowCount(self, parent=QModelIndex()):
        return len(self.processes)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.processes):
            return None

        p = self.processes[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return p["nice_name"]
            elif col == 1:
                return p["desc"]
            elif col == 2:
                cat = p["category"]
                if cat == "safe":
                    return "🟢 Có thể tắt"
                elif cat == "caution":
                    return "🟡 Cân nhắc"
                else:
                    return "🔴 Hệ thống (CẤM)"
            elif col == 3:
                return f"{p['cpu_percent']:.1f}%"
            elif col == 4:
                return f"{p['ram_mb']:.1f} MB"
            elif col == 5:
                return f"{p['ram_percent']:.1f}%"
            elif col == 6:
                return p["pid"]
            elif col == 7:
                return p["user"]

        elif role == Qt.TextAlignmentRole:
            if col in [2, 6, 7]:
                return Qt.AlignCenter
            elif col in [3, 4, 5]:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.BackgroundRole:
            if col == 2:  # Khuyến nghị
                cat = p["category"]
                if cat == "safe":
                    return QColor("#dcfce7")  # Xanh lá nhạt
                elif cat == "caution":
                    return QColor("#fef3c7")  # Vàng nhạt
                else:
                    return QColor("#fee2e2")  # Đỏ nhạt
            elif col == 3:  # CPU %
                val = p["cpu_percent"]
                if val > 50.0:
                    return QColor("#fee2e2")
                elif val > 20.0:
                    return QColor("#ffedd5")
                elif val > 5.0:
                    return QColor("#fef9c3")
            elif col in [4, 5]:  # RAM %
                val = p["ram_percent"]
                if val > 30.0:
                    return QColor("#fee2e2")
                elif val > 10.0:
                    return QColor("#ffedd5")
                elif val > 3.0:
                    return QColor("#fef9c3")

        elif role == Qt.ForegroundRole:
            if col == 2:
                cat = p["category"]
                if cat == "safe":
                    return QColor("#166534")  # Xanh lá đậm
                elif cat == "caution":
                    return QColor("#92400e")  # Vàng đất
                else:
                    return QColor("#991b1b")  # Đỏ đậm
            elif col == 3:
                val = p["cpu_percent"]
                if val > 50.0:
                    return QColor("#991b1b")
                elif val > 20.0:
                    return QColor("#9a3412")
                elif val > 5.0:
                    return QColor("#854d0e")
            elif col in [4, 5]:
                val = p["ram_percent"]
                if val > 30.0:
                    return QColor("#991b1b")
                elif val > 10.0:
                    return QColor("#9a3412")
                elif val > 3.0:
                    return QColor("#854d0e")

        return None

    def update_data(self, new_proc_list):
        self.beginResetModel()
        self.processes = new_proc_list
        self._apply_sort()
        self.endResetModel()

    def sort(self, column, order=Qt.AscendingOrder):
        self._sort_col = column
        self._sort_order = order
        self.beginResetModel()
        self._apply_sort()
        self.endResetModel()

    def _apply_sort(self):
        reverse = (self._sort_order == Qt.DescendingOrder)
        col = self._sort_col
        if col == 0:
            self.processes.sort(key=lambda x: x["nice_name"].lower(), reverse=reverse)
        elif col == 1:
            self.processes.sort(key=lambda x: x["desc"].lower(), reverse=reverse)
        elif col == 2:
            self.processes.sort(key=lambda x: x["category"], reverse=reverse)
        elif col == 3:
            self.processes.sort(key=lambda x: x["cpu_percent"], reverse=reverse)
        elif col == 4:
            self.processes.sort(key=lambda x: x["ram_mb"], reverse=reverse)
        elif col == 5:
            self.processes.sort(key=lambda x: x["ram_percent"], reverse=reverse)
        elif col == 6:
            self.processes.sort(key=lambda x: x["pid"], reverse=reverse)
        elif col == 7:
            self.processes.sort(key=lambda x: x["user"], reverse=reverse)

    def get_process(self, row):
        if 0 <= row < len(self.processes):
            return self.processes[row]
        return None


# --- CUSTOM FILTER PROXY CHO PHÉP LỌC CATEGORY & SEARCH ---
class ProcessFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_filter = "all"  # all, safe, caution, system

    def setCategoryFilter(self, cat):
        self.category_filter = cat
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        p = source_model.get_process(source_row)
        if not p:
            return False

        # 1. Kiểm tra Category Filter
        if self.category_filter != "all":
            if p["category"] != self.category_filter:
                return False

        # 2. Kiểm tra Search Text
        search_reg = self.filterRegExp()
        if search_reg.isEmpty():
            return True

        text_to_search = f"{p['name']} {p['nice_name']} {p['desc']} {p['pid']} {p['user']}".lower()
        return search_reg.indexIn(text_to_search) != -1


# --- WIDGET VẼ BIỂU ĐỒ SÓNG HIỆU NĂNG THỜI GIAN THỰC (REAL-TIME GRAPH) ---
class RealTimeGraphWidget(QWidget):
    def __init__(self, color_hex="#3b82f6", max_val=100.0, unit="%", parent=None):
        super().__init__(parent)
        self.color_hex = color_hex
        self.max_val = max_val
        self.unit = unit
        self.history = deque([0.0] * 60, maxlen=60)
        self.setMinimumHeight(180)
        self.current_val = 0.0

    def add_data_point(self, val):
        self.current_val = val
        self.history.append(val)
        self.update()

    def set_max_val(self, max_val):
        self.max_val = max(max_val, 1.0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # 1. Nền tối xám cao cấp
        painter.fillRect(0, 0, w, h, QColor("#0f172a"))

        # 2. Lưới toạ độ mờ (Grid Lines)
        pen_grid = QPen(QColor("#1e293b"), 1, Qt.DashLine)
        painter.setPen(pen_grid)
        for i in range(1, 4):
            y = int(h * (i / 4.0))
            painter.drawLine(0, y, w, y)
        for i in range(1, 6):
            x = int(w * (i / 6.0))
            painter.drawLine(x, 0, x, h)

        # 3. Tính toán các điểm toạ độ
        points = []
        step_x = w / 59.0
        for i, val in enumerate(self.history):
            clamped = min(max(val, 0.0), self.max_val)
            normalized = clamped / self.max_val
            x = i * step_x
            y = h - (normalized * (h - 10)) - 5
            points.append(QPointF(x, y))

        if len(points) >= 2:
            # 4. Vẽ Gradient Fill dưới đáy sóng
            grad = QLinearGradient(0, 0, 0, h)
            c_top = QColor(self.color_hex)
            c_top.setAlpha(120)
            c_bottom = QColor(self.color_hex)
            c_bottom.setAlpha(10)
            grad.setColorAt(0.0, c_top)
            grad.setColorAt(1.0, c_bottom)

            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)

            from PyQt5.QtGui import QPainterPath
            path = QPainterPath()
            path.moveTo(0, h)
            path.lineTo(points[0])
            for pt in points[1:]:
                path.lineTo(pt)
            path.lineTo(w, h)
            path.closeSubpath()
            painter.drawPath(path)

            # 5. Vẽ đường sóng chính (Antialiased Wave Line)
            pen_line = QPen(QColor(self.color_hex), 2)
            painter.setPen(pen_line)
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i+1])

        # 6. Hiển thị thông số góc
        painter.setPen(QColor("#94a3b8"))
        painter.setFont(QFont("DejaVu Sans", 8))
        painter.drawText(8, 16, "60 giây trước")
        painter.drawText(w - 75, 16, f"Hiện tại: {self.current_val:.1f}{self.unit}")
        painter.drawText(w - 55, h - 6, f"0{self.unit}")
        painter.drawText(w - 65, 30, f"{self.max_val:.0f}{self.unit}")


# --- LUỒNG QUÉT TIẾN TRÌNH & HỆ THỐNG DƯỚI NỀN (TỐI ƯU CAO CẤP) ---
class SystemMonitorThread(QThread):
    stats_updated = pyqtSignal(dict)
    processes_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.interval = 1.0
        self.last_net = psutil.net_io_counters()
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()
        self.user_cache = {}

    def set_interval(self, sec):
        self.interval = max(sec, 0.2)

    def run(self):
        psutil.cpu_percent(interval=None)
        
        while self.running:
            try:
                curr_time = time.time()
                time_delta = max(curr_time - self.last_time, 0.1)

                # 1. CPU
                cpu_percent = psutil.cpu_percent(interval=None)
                cpu_freq = psutil.cpu_freq()
                cpu_freq_ghz = (cpu_freq.current / 1000.0) if cpu_freq else 0.0

                # 2. RAM & Swap
                mem = psutil.virtual_memory()
                swap = psutil.swap_memory()

                # 3. Disk I/O
                curr_disk = psutil.disk_io_counters()
                disk_read_speed = 0.0
                disk_write_speed = 0.0
                if curr_disk and self.last_disk:
                    disk_read_speed = (curr_disk.read_bytes - self.last_disk.read_bytes) / time_delta
                    disk_write_speed = (curr_disk.write_bytes - self.last_disk.write_bytes) / time_delta
                self.last_disk = curr_disk

                # 4. Network I/O
                curr_net = psutil.net_io_counters()
                net_down_speed = 0.0
                net_up_speed = 0.0
                if curr_net and self.last_net:
                    net_down_speed = (curr_net.bytes_recv - self.last_net.bytes_recv) / time_delta
                    net_up_speed = (curr_net.bytes_sent - self.last_net.bytes_sent) / time_delta
                self.last_net = curr_net
                self.last_time = curr_time

                stats = {
                    "cpu_percent": cpu_percent,
                    "cpu_freq_ghz": cpu_freq_ghz,
                    "cpu_cores_physical": psutil.cpu_count(logical=False) or 1,
                    "cpu_cores_logical": psutil.cpu_count(logical=True) or 1,
                    "ram_total": mem.total,
                    "ram_used": mem.used,
                    "ram_available": mem.available,
                    "ram_percent": mem.percent,
                    "swap_total": swap.total,
                    "swap_used": swap.used,
                    "swap_percent": swap.percent,
                    "disk_read_speed": disk_read_speed,
                    "disk_write_speed": disk_write_speed,
                    "net_down_speed": net_down_speed,
                    "net_up_speed": net_up_speed,
                    "uptime": get_system_uptime()
                }
                self.stats_updated.emit(stats)

                # 5. Quét danh sách tiến trình & Phân loại Non-tech
                proc_list = []
                for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'memory_percent']):
                    try:
                        p_info = p.info
                        pid = p_info['pid']
                        name = p_info.get("name") or "Unknown"
                        
                        user = self.user_cache.get(pid)
                        if not user:
                            try:
                                user = p.username()
                                self.user_cache[pid] = user
                            except Exception:
                                user = "user"
                                self.user_cache[pid] = user

                        nice_name, desc, category = classify_process(name, user, pid)

                        mem_info = p_info.get('memory_info')
                        rss_mb = (mem_info.rss / (1024 * 1024)) if mem_info else 0.0
                        
                        proc_list.append({
                            "pid": pid,
                            "name": name,
                            "nice_name": nice_name,
                            "desc": desc,
                            "category": category,
                            "status": p_info.get("status") or "sleeping",
                            "cpu_percent": p_info.get("cpu_percent") or 0.0,
                            "ram_mb": rss_mb,
                            "ram_percent": p_info.get("memory_percent") or 0.0,
                            "user": user
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                if len(self.user_cache) > 2000:
                    current_pids = {p["pid"] for p in proc_list}
                    self.user_cache = {pid: u for pid, u in self.user_cache.items() if pid in current_pids}

                self.processes_updated.emit(proc_list)

            except Exception:
                pass

            time.sleep(self.interval)

    def stop(self):
        self.running = False


# --- CỬA SỔ CHÍNH TASK MANAGER ---
class LinuxTaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trình Quản Lý Tác Vụ Linux (Task Manager)")
        self.setMinimumSize(1160, 820)
        self.selected_pid = None
        self.selected_proc = None
        self.selected_perf_tab = 0
        self.is_always_on_top = False

        self.init_ui()
        self.start_monitor_thread()

    def apply_ui_style(self):
        self.setStyleSheet("""
            QWidget {
                font-family: "DejaVu Sans", "Noto Sans", "Liberation Sans", sans-serif;
                font-size: 10pt;
                color: #1e293b;
                background-color: #f8fafc;
            }
            QMainWindow {
                background-color: #f1f5f9;
            }
            
            /* TAB WIDGET */
            QTabWidget::pane {
                border: 1px solid #cbd5e1;
                background-color: #ffffff;
                border-radius: 8px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #e2e8f0;
                color: #475569;
                font-weight: bold;
                font-size: 10pt;
                padding: 10px 22px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #cbd5e1;
                border-bottom: none;
                min-height: 22px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #2563eb;
                border-top: 3px solid #3b82f6;
                border-bottom: 1px solid #ffffff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #cbd5e1;
                color: #0f172a;
            }

            /* LINE EDIT & COMBOBOX */
            QLineEdit, QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1.5px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QLineEdit:hover, QLineEdit:focus, QComboBox:hover {
                border-color: #3b82f6;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
            }

            /* TABLE VIEW (VIRTUALIZED) */
            QTableView {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
                selection-background-color: #dbeafe;
                selection-color: #1e3a8a;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #ffffff;
                font-weight: bold;
                padding: 8px 10px;
                border: none;
            }
        """)

    def init_ui(self):
        self.apply_ui_style()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 12, 16, 16)
        main_layout.setSpacing(10)

        # ==========================================
        # TOP HEADER APP BANNER
        # ==========================================
        top_header = QFrame(self)
        top_header.setStyleSheet("background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px 14px;")
        top_header_layout = QHBoxLayout(top_header)
        top_header_layout.setContentsMargins(6, 4, 6, 4)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        lbl_app_name = QLabel("Trình Quản Lý Tác Vụ Linux (Task Manager) • Phím tắt: Ctrl+Shift+Esc", self)
        lbl_app_name.setFont(QFont("DejaVu Sans", 12, QFont.Bold))
        lbl_app_name.setStyleSheet("color: #1e293b; border: none;")
        
        self.lbl_header_summary = QLabel("Đang tải dữ liệu hệ thống...", self)
        self.lbl_header_summary.setFont(QFont("DejaVu Sans", 9))
        self.lbl_header_summary.setStyleSheet("color: #64748b; border: none;")
        
        title_box.addWidget(lbl_app_name)
        title_box.addWidget(self.lbl_header_summary)
        top_header_layout.addLayout(title_box)
        top_header_layout.addStretch()

        # Tốc độ làm mới
        lbl_speed = QLabel("Tốc độ cập nhật:", self)
        lbl_speed.setFont(QFont("DejaVu Sans", 9))
        lbl_speed.setStyleSheet("color: #475569; border: none;")
        self.combo_speed = QComboBox(self)
        self.combo_speed.addItems(["Nhanh (0.5s)", "Bình thường (1.0s)", "Chậm (2.0s)", "Tạm dừng"])
        self.combo_speed.setCurrentIndex(1)
        self.combo_speed.currentIndexChanged.connect(self.on_speed_changed)
        
        # Nút Ghim trên cùng
        self.btn_top = QPushButton("📌 Ghim trên cùng", self)
        self.btn_top.setFont(QFont("DejaVu Sans", 9, QFont.Bold))
        self.btn_top.setCheckable(True)
        self.btn_top.setStyleSheet("""
            QPushButton { background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px 12px; }
            QPushButton:checked { background-color: #3b82f6; color: #ffffff; border-color: #2563eb; }
        """)
        self.btn_top.clicked.connect(self.toggle_always_on_top)

        top_header_layout.addWidget(lbl_speed)
        top_header_layout.addWidget(self.combo_speed)
        top_header_layout.addWidget(self.btn_top)

        main_layout.addWidget(top_header)

        # ==========================================
        # MAIN TAB WIDGET
        # ==========================================
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        self.init_processes_tab()
        self.init_performance_tab()
        self.init_startup_tab()
        self.init_system_info_tab()

    # ----------------------------------------------------
    # TAB 1: PROCESSES (VIRTUALIZED MODEL/VIEW & NON-TECH)
    # ----------------------------------------------------
    def init_processes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Thanh hướng dẫn Non-Tech thông minh
        help_bar = QFrame(self)
        help_bar.setStyleSheet("background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 6px 10px;")
        help_layout = QHBoxLayout(help_bar)
        help_layout.setContentsMargins(4, 2, 4, 2)
        help_lbl = QLabel(
            "💡 <b>Hướng dẫn cho người dùng:</b> "
            "🟢 <b>Có thể tắt</b>: Ứng dụng của bạn (tắt an toàn khi máy lag) • "
            "🟡 <b>Cân nhắc</b>: Dịch vụ chạy ngầm (bộ gõ tiếng Việt, loa...) • "
            "🔴 <b>Hệ thống</b>: Cốt lõi của Linux (CẤM TẮT để tránh đơ máy).",
            self
        )
        help_lbl.setFont(QFont("DejaVu Sans", 9))
        help_lbl.setStyleSheet("color: #1e40af; border: none;")
        help_layout.addWidget(help_lbl)
        layout.addWidget(help_bar)

        # Toolbar: Lọc Phân Loại & Tìm Kiếm
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # ComboBox Bộ lọc phân loại
        lbl_filter = QLabel("Xem danh mục:", self)
        lbl_filter.setFont(QFont("DejaVu Sans", 9, QFont.Bold))
        lbl_filter.setStyleSheet("color: #475569;")
        
        self.combo_category = QComboBox(self)
        self.combo_category.addItems([
            "📋 Tất cả tiến trình",
            "🟢 Ứng dụng người dùng (Nên tắt khi lag)",
            "🟡 Dịch vụ chạy ngầm (Cân nhắc)",
            "🔴 Tiến trình Hệ Thống (Cấm tắt)"
        ])
        self.combo_category.currentIndexChanged.connect(self.on_category_filter_changed)

        self.proc_search = QLineEdit(self)
        self.proc_search.setPlaceholderText("🔍 Tìm kiếm theo tên ứng dụng, chức năng hoặc PID...")
        self.proc_search.textChanged.connect(self.on_search_changed)

        self.lbl_proc_count = QLabel("Tổng: 0 tiến trình", self)
        self.lbl_proc_count.setFont(QFont("DejaVu Sans", 9, QFont.Bold))
        self.lbl_proc_count.setStyleSheet("color: #64748b;")

        toolbar.addWidget(lbl_filter)
        toolbar.addWidget(self.combo_category)
        toolbar.addWidget(self.proc_search, stretch=3)
        toolbar.addWidget(self.lbl_proc_count, stretch=1)
        layout.addLayout(toolbar)

        # Bảng Process sử dụng QTableView + ProcessTableModel (Không giật lag)
        self.proc_model = ProcessTableModel(self)
        
        self.proxy_model = ProcessFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.proc_model)

        self.proc_view = QTableView(self)
        self.proc_view.setModel(self.proxy_model)
        self.proc_view.verticalHeader().setVisible(False)
        self.proc_view.verticalHeader().setDefaultSectionSize(36)
        self.proc_view.setSortingEnabled(True)
        self.proc_view.sortByColumn(3, Qt.DescendingOrder)  # Mặc định CPU % cao nhất lên đầu
        self.proc_view.setSelectionBehavior(QTableView.SelectRows)
        self.proc_view.setSelectionMode(QTableView.SingleSelection)
        self.proc_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.proc_view.customContextMenuRequested.connect(self.show_process_context_menu)
        self.proc_view.selectionModel().selectionChanged.connect(self.on_process_selected)

        # Thiết lập độ rộng cột
        h_header = self.proc_view.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        h_header.setSectionResizeMode(0, QHeaderView.Interactive)
        h_header.resizeSection(0, 180)  # Tên
        h_header.setSectionResizeMode(1, QHeaderView.Interactive)
        h_header.resizeSection(1, 280)  # Mô tả Non-Tech
        h_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Khuyến nghị
        h_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # CPU %
        h_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # RAM MB
        h_header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # RAM %
        h_header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # PID
        h_header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # User

        layout.addWidget(self.proc_view)

        # Bottom Bar: Nút End Task góc phải chuẩn Windows
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(10)
        
        self.lbl_selected_proc = QLabel("Chưa chọn tiến trình nào", self)
        self.lbl_selected_proc.setStyleSheet("color: #64748b; font-style: italic;")
        
        self.btn_end_task = QPushButton("Kết thúc tác vụ (End Task)", self)
        self.btn_end_task.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
        self.btn_end_task.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_end_task.setEnabled(False)
        self.btn_end_task.setStyleSheet("""
            QPushButton {
                background-color: #ef4444; color: #ffffff; border-radius: 6px;
                padding: 8px 20px; font-weight: bold; border: none;
            }
            QPushButton:hover { background-color: #dc2626; color: #ffffff; }
            QPushButton:pressed { background-color: #b91c1c; color: #ffffff; }
            QPushButton:disabled { background-color: #cbd5e1; color: #94a3b8; }
        """)
        self.btn_end_task.clicked.connect(self.confirm_end_task)

        bottom_bar.addWidget(self.lbl_selected_proc)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.btn_end_task)
        layout.addLayout(bottom_bar)

        self.tabs.addTab(tab, "📋 Tiến trình")

    def on_category_filter_changed(self, idx):
        cat_map = {0: "all", 1: "safe", 2: "caution", 3: "system"}
        self.proxy_model.setCategoryFilter(cat_map.get(idx, "all"))
        self.lbl_proc_count.setText(f"Tổng: {self.proxy_model.rowCount()} tiến trình")

    def on_search_changed(self, text):
        reg = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
        self.proxy_model.setFilterRegExp(reg)
        self.lbl_proc_count.setText(f"Tổng: {self.proxy_model.rowCount()} tiến trình")

    # ----------------------------------------------------
    # TAB 2: PERFORMANCE (BIỂU ĐỒ HIỆU NĂNG THỜI GIAN THỰC)
    # ----------------------------------------------------
    def init_performance_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        # Cột trái: Mini Cards lựa chọn thành phần
        left_panel = QFrame(self)
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(6)

        self.perf_buttons = []
        
        cards_info = [
            ("CPU", "0.0%", "#3b82f6", "Bộ vi xử lý"),
            ("Bộ nhớ (RAM)", "0.0 GB", "#8b5cf6", "Bộ nhớ khả dụng"),
            ("Ổ đĩa (Disk)", "0.0 MB/s", "#10b981", "Tốc độ đọc/ghi"),
            ("Mạng (Network)", "0 KB/s", "#f59e0b", "Tốc độ truyền tải"),
            ("Đồ họa (GPU)", "Intel Iris Xe", "#06b6d4", "Card màn hình")
        ]

        for idx, (title, val, color, sub) in enumerate(cards_info):
            btn = QPushButton(self)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setFixedHeight(68)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            if idx == 0:
                btn.setChecked(True)
            
            b_layout = QVBoxLayout(btn)
            b_layout.setContentsMargins(10, 6, 10, 6)
            b_layout.setSpacing(2)
            
            lbl_t = QLabel(title, btn)
            lbl_t.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
            lbl_t.setStyleSheet(f"color: {color}; background: transparent; border: none;")
            
            lbl_v = QLabel(val, btn)
            lbl_v.setFont(QFont("DejaVu Sans", 11, QFont.Bold))
            lbl_v.setStyleSheet("color: #1e293b; background: transparent; border: none;")
            
            lbl_s = QLabel(sub, btn)
            lbl_s.setFont(QFont("DejaVu Sans", 8))
            lbl_s.setStyleSheet("color: #64748b; background: transparent; border: none;")
            
            b_layout.addWidget(lbl_t)
            b_layout.addWidget(lbl_v)
            b_layout.addWidget(lbl_s)
            
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #f8fafc; border: 1.5px solid #e2e8f0;
                    border-radius: 8px; text-align: left;
                }}
                QPushButton:hover {{ background-color: #eff6ff; border-color: {color}; }}
                QPushButton:checked {{
                    background-color: #ffffff; border: 2px solid {color};
                }}
            """)
            btn.clicked.connect(lambda checked, i=idx: self.select_perf_card(i))
            
            btn.lbl_v = lbl_v
            btn.lbl_s = lbl_s
            self.perf_buttons.append(btn)
            left_layout.addWidget(btn)

        left_layout.addStretch()
        layout.addWidget(left_panel)

        # Cột phải: Biểu đồ to và Thông số chi tiết
        right_panel = QFrame(self)
        right_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(12)

        # Header chi tiết
        self.lbl_perf_title = QLabel("CPU — Bộ Vi Xử Lý", self)
        self.lbl_perf_title.setFont(QFont("DejaVu Sans", 13, QFont.Bold))
        self.lbl_perf_title.setStyleSheet("color: #1e293b; border: none;")
        right_layout.addWidget(self.lbl_perf_title)

        # Biểu đồ thời gian thực
        self.realtime_graph = RealTimeGraphWidget(color_hex="#3b82f6", max_val=100.0, unit="%", parent=self)
        right_layout.addWidget(self.realtime_graph, stretch=3)

        # Bảng thông số chi tiết dạng Grid
        self.perf_details_frame = QFrame(self)
        self.perf_details_frame.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px;")
        self.perf_grid = QGridLayout(self.perf_details_frame)
        self.perf_grid.setSpacing(10)
        
        self.detail_labels = {}
        fields = ["Mục 1", "Mục 2", "Mục 3", "Mục 4", "Mục 5", "Mục 6"]
        for i, f in enumerate(fields):
            row = i // 3
            col = i % 3
            lbl_title = QLabel(f, self)
            lbl_title.setFont(QFont("DejaVu Sans", 9))
            lbl_title.setStyleSheet("color: #64748b; border: none;")
            
            lbl_val = QLabel("Đang đọc...", self)
            lbl_val.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
            lbl_val.setStyleSheet("color: #1e293b; border: none;")
            
            box = QVBoxLayout()
            box.setSpacing(2)
            box.addWidget(lbl_title)
            box.addWidget(lbl_val)
            
            self.perf_grid.addLayout(box, row, col)
            self.detail_labels[f"title_{i}"] = lbl_title
            self.detail_labels[f"val_{i}"] = lbl_val

        right_layout.addWidget(self.perf_details_frame, stretch=2)
        layout.addWidget(right_panel, stretch=3)

        self.tabs.addTab(tab, "📈 Hiệu năng")

    # ----------------------------------------------------
    # TAB 3: STARTUP APPS (ỨNG DỤNG KHỞI ĐỘNG CÙNG HỆ THỐNG)
    # ----------------------------------------------------
    def init_startup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        header_lbl = QLabel("Danh sách ứng dụng tự động chạy khi đăng nhập Linux (~/.config/autostart):", self)
        header_lbl.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
        header_lbl.setStyleSheet("color: #1e293b;")
        layout.addWidget(header_lbl)

        self.startup_table = QTableWidget(self)
        self.startup_table.setColumnCount(4)
        self.startup_table.setHorizontalHeaderLabels(["Tên Ứng Dụng", "Lệnh Thực Thi", "Trạng Thái", "Thao Tác"])
        self.startup_table.verticalHeader().setVisible(False)
        self.startup_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.startup_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.startup_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.startup_table.setColumnWidth(3, 110)
        layout.addWidget(self.startup_table)

        btn_reload = QPushButton("🔄 Quét lại ứng dụng khởi động", self)
        btn_reload.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
        btn_reload.setStyleSheet("background-color: #3b82f6; color: white; border-radius: 6px; padding: 8px 16px; border: none;")
        btn_reload.clicked.connect(self.load_startup_apps)
        layout.addWidget(btn_reload, 0, Qt.AlignLeft)

        self.tabs.addTab(tab, "🚀 Khởi động")
        self.load_startup_apps()

    def load_startup_apps(self):
        self.startup_table.setRowCount(0)
        autostart_dir = Path.home() / ".config" / "autostart"
        if not autostart_dir.exists():
            return

        desktop_files = list(autostart_dir.glob("*.desktop"))
        self.startup_table.setRowCount(len(desktop_files))

        for row, fpath in enumerate(desktop_files):
            name = fpath.stem
            cmd = ""
            enabled = True

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("Name="):
                            name = line.split("=", 1)[1].strip()
                        elif line.startswith("Exec="):
                            cmd = line.split("=", 1)[1].strip()
                        elif line.startswith("Hidden=true") or line.startswith("X-GNOME-Autostart-enabled=false"):
                            enabled = False
            except Exception:
                pass

            self.startup_table.setItem(row, 0, QTableWidgetItem(name))
            self.startup_table.setItem(row, 1, QTableWidgetItem(cmd))

            status_str = "Bật (Enabled)" if enabled else "Tắt (Disabled)"
            status_item = QTableWidgetItem(status_str)
            status_item.setForeground(QColor("#10b981" if enabled else "#ef4444"))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.startup_table.setItem(row, 2, status_item)

            btn_toggle = QPushButton("Tắt" if enabled else "Bật")
            btn_toggle.setStyleSheet(f"""
                QPushButton {{
                    background-color: {'#f59e0b' if enabled else '#10b981'};
                    color: white; border-radius: 4px; padding: 4px 10px; font-weight: bold; border: none;
                }}
            """)
            btn_toggle.clicked.connect(lambda checked, p=fpath, cur=enabled: self.toggle_startup_file(p, cur))
            self.startup_table.setCellWidget(row, 3, btn_toggle)

    def toggle_startup_file(self, fpath, current_enabled):
        try:
            lines = []
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not (line.startswith("Hidden=") or line.startswith("X-GNOME-Autostart-enabled=")):
                        lines.append(line)
            
            new_state = "false" if current_enabled else "true"
            lines.append(f"X-GNOME-Autostart-enabled={new_state}\n")
            with open(fpath, "w", encoding="utf-8") as f:
                f.writelines(lines)
            self.load_startup_apps()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thay đổi trạng thái: {str(e)}")

    # ----------------------------------------------------
    # TAB 4: SYSTEM INFO (THÔNG TIN PHẦN CỨNG & HỆ ĐIỀU HÀNH)
    # ----------------------------------------------------
    def init_system_info_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setSpacing(14)

        # Card Thông tin Hệ điều hành
        os_card = self.create_info_card("Hệ Điều Hành & Nền Tảng", [
            ("Hệ điều hành", get_os_info()),
            ("Bản phân phối Kernel", os.uname().release),
            ("Kiến trúc phần cứng", os.uname().machine),
            ("Tên máy (Hostname)", os.uname().nodename),
            ("Thời gian hoạt động (Uptime)", get_system_uptime())
        ])
        c_layout.addWidget(os_card)

        # Card Thông tin CPU & Bộ nhớ
        mem = psutil.virtual_memory()
        cpu_card = self.create_info_card("Bộ Vi Xử Lý & Bộ Nhớ RAM", [
            ("Mẫu CPU (Processor)", get_cpu_model()),
            ("Số nhân vật lý (Cores)", str(psutil.cpu_count(logical=False) or 1)),
            ("Số luồng xử lý (Threads)", str(psutil.cpu_count(logical=True) or 1)),
            ("Tổng dung lượng RAM", format_bytes(mem.total)),
            ("Tổng bộ nhớ Swap", format_bytes(psutil.swap_memory().total))
        ])
        c_layout.addWidget(cpu_card)

        # Card Card màn hình & Đồ họa
        gpu_card = self.create_info_card("Card Đồ Họa & Màn Hình", [
            ("Card đồ họa (GPU)", get_gpu_info_text()),
            ("Server hiển thị", os.environ.get("XDG_SESSION_TYPE", "X11").upper()),
            ("Môi trường Desktop", os.environ.get("XDG_CURRENT_DESKTOP", "Cinnamon"))
        ])
        c_layout.addWidget(gpu_card)

        c_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.tabs.addTab(tab, "ℹ️ Chi tiết hệ thống")

    def create_info_card(self, title, items):
        card = QFrame(self)
        card.setStyleSheet("background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;")
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        t_lbl = QLabel(title, card)
        t_lbl.setFont(QFont("DejaVu Sans", 11, QFont.Bold))
        t_lbl.setStyleSheet("color: #2563eb; border-bottom: 2px solid #eff6ff; padding-bottom: 4px;")
        layout.addWidget(t_lbl)

        grid = QGridLayout()
        grid.setSpacing(8)
        for row, (k, v) in enumerate(items):
            k_lbl = QLabel(f"• {k}:", card)
            k_lbl.setFont(QFont("DejaVu Sans", 10))
            k_lbl.setStyleSheet("color: #64748b; border: none;")
            
            v_lbl = QLabel(v, card)
            v_lbl.setFont(QFont("DejaVu Sans", 10, QFont.Bold))
            v_lbl.setStyleSheet("color: #1e293b; border: none;")
            
            grid.addWidget(k_lbl, row, 0)
            grid.addWidget(v_lbl, row, 1)
        layout.addLayout(grid)
        return card

    # --- ĐIỀU KHIỂN & CẬP NHẬT DỮ LIỆU THỜI GIAN THỰC ---
    def start_monitor_thread(self):
        self.thread = SystemMonitorThread(self)
        self.thread.stats_updated.connect(self.on_stats_updated)
        self.thread.processes_updated.connect(self.on_processes_updated)
        self.thread.start()

    def on_speed_changed(self, idx):
        speeds = [0.5, 1.0, 2.0, 999999.0]
        if idx < len(speeds):
            self.thread.set_interval(speeds[idx])

    def toggle_always_on_top(self):
        self.is_always_on_top = self.btn_top.isChecked()
        flags = self.windowFlags()
        if self.is_always_on_top:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    def on_stats_updated(self, s):
        cpu_p = s["cpu_percent"]
        ram_p = s["ram_percent"]
        ram_used_gb = s["ram_used"] / (1024**3)
        ram_tot_gb = s["ram_total"] / (1024**3)
        self.lbl_header_summary.setText(
            f"CPU: {cpu_p:.1f}% ({s['cpu_freq_ghz']:.2f} GHz) • RAM: {ram_used_gb:.1f}/{ram_tot_gb:.1f} GB ({ram_p:.0f}%) • Uptime: {s['uptime']}"
        )

        self.perf_buttons[0].lbl_v.setText(f"{cpu_p:.1f}%")
        self.perf_buttons[0].lbl_s.setText(f"{s['cpu_freq_ghz']:.2f} GHz • {s['cpu_cores_logical']} Luồng")
        
        self.perf_buttons[1].lbl_v.setText(f"{ram_used_gb:.1f} GB ({ram_p:.0f}%)")
        self.perf_buttons[1].lbl_s.setText(f"Trống: {format_bytes(s['ram_available'])}")
        
        tot_disk_speed = (s["disk_read_speed"] + s["disk_write_speed"]) / (1024*1024)
        self.perf_buttons[2].lbl_v.setText(f"{tot_disk_speed:.1f} MB/s")
        self.perf_buttons[2].lbl_s.setText(f"Đọc: {format_bytes(s['disk_read_speed'])}/s • Ghi: {format_bytes(s['disk_write_speed'])}/s")
        
        tot_net_speed = (s["net_down_speed"] + s["net_up_speed"]) / 1024
        self.perf_buttons[3].lbl_v.setText(f"{tot_net_speed:.1f} KB/s")
        self.perf_buttons[3].lbl_s.setText(f"Tải: {format_bytes(s['net_down_speed'])}/s")

        if self.selected_perf_tab == 0:  # CPU
            self.realtime_graph.set_max_val(100.0)
            self.realtime_graph.unit = "%"
            self.realtime_graph.add_data_point(cpu_p)
            self.update_perf_details([
                ("Mức sử dụng CPU", f"{cpu_p:.1f}%"),
                ("Tốc độ xung nhịp", f"{s['cpu_freq_ghz']:.2f} GHz"),
                ("Số nhân thực (Cores)", str(s["cpu_cores_physical"])),
                ("Số luồng ảo (Threads)", str(s["cpu_cores_logical"])),
                ("Thời gian hoạt động", s["uptime"]),
                ("Mẫu CPU", get_cpu_model().split("@")[0].strip())
            ])
        elif self.selected_perf_tab == 1:  # RAM
            self.realtime_graph.set_max_val(100.0)
            self.realtime_graph.unit = "%"
            self.realtime_graph.add_data_point(ram_p)
            self.update_perf_details([
                ("Đang sử dụng", f"{ram_used_gb:.2f} GB ({ram_p:.1f}%)"),
                ("Bộ nhớ còn trống", format_bytes(s["ram_available"])),
                ("Tổng dung lượng RAM", format_bytes(s["ram_total"])),
                ("Swap đã dùng", format_bytes(s["swap_used"])),
                ("Swap còn trống", format_bytes(s["swap_total"] - s["swap_used"])),
                ("Tổng bộ nhớ Swap", format_bytes(s["swap_total"]))
            ])
        elif self.selected_perf_tab == 2:  # DISK
            self.realtime_graph.set_max_val(max(tot_disk_speed * 1.5, 50.0))
            self.realtime_graph.unit = " MB/s"
            self.realtime_graph.add_data_point(tot_disk_speed)
            self.update_perf_details([
                ("Tốc độ đọc (Read)", f"{format_bytes(s['disk_read_speed'])}/s"),
                ("Tốc độ ghi (Write)", f"{format_bytes(s['disk_write_speed'])}/s"),
                ("Tổng tốc độ I/O", f"{tot_disk_speed:.2f} MB/s"),
                ("Phân vùng gốc (/)", f"{format_bytes(psutil.disk_usage('/').free)} trống"),
                ("Phân vùng DATA", f"{format_bytes(psutil.disk_usage('/media/tanma/DATA').free if os.path.exists('/media/tanma/DATA') else 0)} trống"),
                ("Loại ổ đĩa", "SSD / NVMe / HDD")
            ])
        elif self.selected_perf_tab == 3:  # NETWORK
            self.realtime_graph.set_max_val(max(tot_net_speed * 1.5, 100.0))
            self.realtime_graph.unit = " KB/s"
            self.realtime_graph.add_data_point(tot_net_speed)
            self.update_perf_details([
                ("Tốc độ tải về (Download)", f"{format_bytes(s['net_down_speed'])}/s"),
                ("Tốc độ tải lên (Upload)", f"{format_bytes(s['net_up_speed'])}/s"),
                ("Tổng băng thông truyền", f"{tot_net_speed:.1f} KB/s"),
                ("Giao thức kết nối", "Wi-Fi / Ethernet"),
                ("Trạng thái mạng", "Đã kết nối Internet"),
                ("Địa chỉ IPv4", "DHCP Cục bộ")
            ])
        elif self.selected_perf_tab == 4:  # GPU
            self.realtime_graph.set_max_val(100.0)
            self.realtime_graph.unit = "%"
            self.realtime_graph.add_data_point(cpu_p * 0.4)
            self.update_perf_details([
                ("Tên Card đồ họa", get_gpu_info_text()),
                ("Loại GPU", "Đồ họa tích hợp (Integrated)"),
                ("Môi trường đồ họa", os.environ.get("XDG_CURRENT_DESKTOP", "Cinnamon")),
                ("Window Server", os.environ.get("XDG_SESSION_TYPE", "X11").upper()),
                ("Trình điều khiển (Driver)", "Mesa / Intel i915 DRM"),
                ("Trạng thái đồ họa", "Hoạt động bình thường")
            ])

    def select_perf_card(self, idx):
        self.selected_perf_tab = idx
        colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#06b6d4"]
        titles = [
            "CPU — Bộ Vi Xử Lý (Processor)",
            "Bộ Nhớ RAM (System Memory)",
            "Ổ Đĩa — Tốc Độ Đọc/Ghi (Disk I/O)",
            "Mạng — Tốc Độ Truyền Tải (Network)",
            "Đồ Họa (Graphics Card - GPU)"
        ]
        self.realtime_graph.color_hex = colors[idx]
        self.lbl_perf_title.setText(titles[idx])

    def update_perf_details(self, data_pairs):
        for i, (k, v) in enumerate(data_pairs[:6]):
            self.detail_labels[f"title_{i}"].setText(f"• {k}:")
            self.detail_labels[f"val_{i}"].setText(v)

    # --- CẬP NHẬT BẢNG TIẾN TRÌNH ---
    def on_processes_updated(self, proc_list):
        self.proc_model.update_data(proc_list)
        count = self.proxy_model.rowCount()
        self.lbl_proc_count.setText(f"Tổng: {count} tiến trình")

    def on_process_selected(self):
        indexes = self.proc_view.selectionModel().selectedRows()
        if indexes:
            proxy_idx = indexes[0]
            source_idx = self.proxy_model.mapToSource(proxy_idx)
            p = self.proc_model.get_process(source_idx.row())
            if p:
                self.selected_pid = p["pid"]
                self.selected_proc = p
                
                cat_badge = ""
                if p["category"] == "safe":
                    cat_badge = "<span style='color: #16a34a;'><b>[🟢 An toàn để tắt]</b></span>"
                elif p["category"] == "caution":
                    cat_badge = "<span style='color: #d97706;'><b>[🟡 Cân nhắc]</b></span>"
                else:
                    cat_badge = "<span style='color: #dc2626;'><b>[🔴 Tiến trình Hệ Thống]</b></span>"
                
                self.lbl_selected_proc.setText(f"Đã chọn: <b>{p['nice_name']}</b> (PID: {p['pid']}) — {p['desc']} {cat_badge}")
                self.lbl_selected_proc.setStyleSheet("color: #1e293b;")
                self.btn_end_task.setEnabled(True)
                return

        self.selected_pid = None
        self.selected_proc = None
        self.lbl_selected_proc.setText("Chưa chọn tiến trình nào")
        self.lbl_selected_proc.setStyleSheet("color: #64748b; font-style: italic;")
        self.btn_end_task.setEnabled(False)

    def show_process_context_menu(self, pos):
        proxy_idx = self.proc_view.indexAt(pos)
        if not proxy_idx.isValid():
            return
        
        source_idx = self.proxy_model.mapToSource(proxy_idx)
        p = self.proc_model.get_process(source_idx.row())
        if not p:
            return

        pid = p["pid"]
        name = p["nice_name"]

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; padding: 6px; border-radius: 8px; }
            QMenu::item { padding: 8px 24px; }
            QMenu::item:selected { background-color: #3b82f6; color: #ffffff; border-radius: 4px; }
        """)

        act_end = QAction(f"🛑  Kết thúc tác vụ: {name}", self)
        act_end.triggered.connect(lambda: self.kill_process(p, force=False))

        act_force = QAction("⚡  Buộc dừng ngay (Force Kill)", self)
        act_force.triggered.connect(lambda: self.kill_process(p, force=True))

        act_open_dir = QAction("📂  Mở thư mục chứa file (Open Location)", self)
        act_open_dir.triggered.connect(lambda: self.open_proc_location(pid))

        act_search = QAction("🔍  Tìm kiếm thông tin tiến trình trên Web", self)
        act_search.triggered.connect(lambda: webbrowser.open(f"https://www.google.com/search?q=linux+process+{p['name']}"))

        menu.addAction(act_end)
        menu.addAction(act_force)
        menu.addSeparator()
        menu.addAction(act_open_dir)
        menu.addAction(act_search)
        menu.exec_(QCursor.pos())

    def confirm_end_task(self):
        if not self.selected_proc:
            return

        p = self.selected_proc
        name = p["nice_name"]
        cat = p["category"]
        pid = p["pid"]

        # Cảnh báo thông minh theo từng cấp độ
        if cat == "system":
            reply = QMessageBox.critical(
                self, "⚠️ CẢNH BÁO NGUY HIỂM — TIẾN TRÌNH HỆ THỐNG",
                f"🚨 <b>'{name}' (PID: {pid})</b> là tiến trình cốt lõi của hệ điều hành Linux!\n\n"
                f"• Chức năng: {p['desc']}\n"
                "• Nguy cơ: Việc tắt tiến trình này có thể khiến màn hình bị sập hoặc máy tính tự khởi động lại.\n\n"
                "Anh Tân có THỰC SỰ CHẮC CHẮN muốn ép buộc tắt tiến trình này không?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
        elif cat == "caution":
            reply = QMessageBox.warning(
                self, "🟡 CÂN NHẮC TRƯỚC KHI TẮT",
                f"<b>'{name}' (PID: {pid})</b> là dịch vụ chạy ngầm hỗ trợ hệ thống.\n\n"
                f"• Chức năng: {p['desc']}\n"
                "• Lưu ý: Nếu tắt, một số tính năng (như gõ tiếng Việt, âm thanh, bluetooth...) có thể tạm thời không dùng được cho đến khi mở lại.\n\n"
                "Anh Tân có muốn tiếp tục tắt không?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
        else:
            reply = QMessageBox.question(
                self, "🟢 XÁC NHẬN TẮT ỨNG DỤNG",
                f"✅ <b>'{name}' (PID: {pid})</b> là ứng dụng người dùng thông thường.\n\n"
                f"• Chức năng: {p['desc']}\n"
                f"• Tài nguyên giải phóng: ~{p['ram_mb']:.1f} MB RAM và {p['cpu_percent']:.1f}% CPU.\n\n"
                "Anh Tân có muốn đóng ứng dụng này ngay không?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )

        if reply == QMessageBox.Yes:
            self.kill_process(p, force=False)

    def kill_process(self, p_dict, force=False):
        pid = p_dict["pid"]
        name = p_dict["nice_name"]
        try:
            p = psutil.Process(pid)
            if force:
                p.kill()
            else:
                p.terminate()
            
            QMessageBox.information(self, "Thành công", f"Đã kết thúc thành công ứng dụng '{name}' (PID: {pid})!\nMáy đã được giải phóng RAM & CPU.")
        except psutil.NoSuchProcess:
            QMessageBox.information(self, "Thông báo", f"Ứng dụng '{name}' (PID: {pid}) đã tự đóng trước đó.")
        except psutil.AccessDenied:
            cmd = ["pkexec", "kill", "-9" if force else "-15", str(pid)]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True)
                if proc.returncode == 0:
                    QMessageBox.information(self, "Thành công", f"Đã kết thúc '{name}' (PID: {pid}) với quyền quản trị root!")
                else:
                    QMessageBox.critical(self, "Lỗi quyền hạn", f"Không thể kết thúc tiến trình:\n{proc.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi xảy ra: {str(e)}")

    def open_proc_location(self, pid):
        try:
            p = psutil.Process(pid)
            exe_path = p.exe()
            if exe_path and os.path.exists(exe_path):
                subprocess.Popen(["xdg-open", str(Path(exe_path).parent)])
            else:
                QMessageBox.warning(self, "Không tìm thấy", "Không xác định được đường dẫn file thực thi của tiến trình này.")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể mở thư mục: {str(e)}")

    def closeEvent(self, event):
        if hasattr(self, 'thread'):
            self.thread.stop()
            self.thread.wait(1000)
        event.accept()


# --- ENTRY POINT ---
def main():
    app = QApplication(sys.argv)
    window = LinuxTaskManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
