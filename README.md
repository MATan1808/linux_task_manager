# Linux Task Manager (Windows 11 Modern Desktop Style)

Ứng dụng quản trị tác vụ, theo dõi tiến trình và giám sát hiệu năng hệ thống Linux theo phong cách Windows 11 Task Manager. Được xây dựng bằng Python, PyQt5 và psutil.

---

## 🌟 Tính Năng Nổi Bật

1. **📋 Quản Lý Tiến Trình (Processes)**:
   - Theo dõi chi tiết: Tên tiến trình, PID, Trạng thái, **CPU %**, **RAM (MB & %)**, Người dùng.
   - **Heatmap màu sắc**: Tự động tô màu vàng/cam/đỏ cho các tiến trình ngốn nhiều CPU / RAM giống Windows Task Manager.
   - **Chức năng End Task**: Nút `[ Kết thúc tác vụ (End Task) ]` ở góc dưới phải và Menu chuột phải (`End Task`, `Force Kill`, `Mở vị trí file`, `Tra cứu trên Web`).
   - Tìm kiếm nhanh tức thì theo tên ứng dụng hoặc PID.

2. **📈 Biểu Đồ Hiệu Năng Thời Gian Thực (Performance Graphs)**:
   - Vẽ biểu đồ sóng thời gian thực mượt mà (60 giây gần nhất) bằng `QPainter` với hiệu ứng Gradient Wave.
   - Giám sát 5 thành phần phần cứng:
     - **CPU**: % Sử dụng tổng thể, Tốc độ xung nhịp (GHz), Số Core/Threads, Uptime.
     - **Bộ nhớ (RAM)**: Đã dùng, Còn trống, Tổng RAM, Bộ nhớ ảo Swap.
     - **Ổ đĩa (Disk)**: Tốc độ đọc/ghi (Read/Write MB/s), Dung lượng các phân vùng.
     - **Mạng (Network)**: Tốc độ tải xuống (Download) và tải lên (Upload).
     - **Card Đồ Họa (GPU)**: Thông tin GPU Intel Iris Xe / Nvidia / AMD.

3. **🏥 Sức Khỏe Phần Cứng & Trung Tâm Tối Ưu 1-Click (AIaC Boost)**:
   - **Đo sức khỏe toàn diện**: Điểm số sức khỏe phần cứng (/100), độ chai pin laptop (Battery Wear %), nhiệt độ CPU/NVMe/Wi-Fi, áp lực RAM và ổ SSD.
   - **⚡ Giải phóng Cache RAM (1-Click)**: Tự động thu hồi bộ đệm buffers/cache, trả lại dung lượng RAM thực sự cho ứng dụng mà **không cần nhập mật khẩu sudo**.
   - **🗑️ Dọn dẹp File Rác (1-Click)**: Quét và dọn sạch APT cache, thumbnails, Google Chrome browser cache, user logs và rác hệ thống tức thì.
   - **🔥 AIaC Boost (Chống Lag ASUS ZenBook)**: Thiết lập Swappiness = 10 (ưu tiên 8GB RAM vật lý, chống nghẽn I/O ổ cứng), dừng các dịch vụ ngầm nặng (như Waydroid container) và dọn sạch RAM chỉ bằng 1 cú nhấp chuột.
   - **🔪 Kill Lag (Diệt Tiến Trình Lag)**: Tự động quét và kill các tiến trình ngốn CPU > 15% hoặc RAM > 500MB gây lag máy. Bao gồm: kill Chrome tabs nặng (giữ main process), stop Headroom AI service, stop Docker demo containers, sau đó dọn RAM cache. Hiển thị báo cáo chi tiết số tiến trình đã diệt và RAM giải phóng.

4. **🚀 Quản Lý Khởi Động (Startup Apps)**:
   - Liệt kê các ứng dụng tự động chạy khi khởi động Linux.
   - Bật / Tắt trạng thái khởi động với 1-click.

4. **ℹ️ Chi Tiết Hệ Thống (System Info)**:
   - Thông tin chi tiết phần cứng, bản phân phối OS, Kernel, Uptime.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Yêu cầu hệ thống:
```bash
sudo apt update
sudo apt install -y python3-pyqt5 python3-psutil
```

### 2. Khởi chạy ứng dụng:
*   **Cách 1 (Từ Terminal)**:
    ```bash
    python3 /media/tanma/DATA/terminal/task_manager_gui.py
    ```
*   **Cách 2 (Từ Desktop)**: Double-click vào icon **Linux Task Manager** ngoài màn hình Desktop.
*   **Cách 3 (Từ Menu ứng dụng)**: Tìm kiếm **Linux Task Manager** trong Application Menu của Linux Mint.

---

## 🛠️ Tác Giả & Bản Quyền
*   **Chủ sở hữu**: Anh Tân (MATan1808)
*   **Được xây dựng bởi**: AIaC (360 CORP)
*   **Git Commit Attribution**: `Authored-By: 360org <support@360.org.vn>`
