# 03 — System Architecture (Kiến trúc hệ thống)
https://drive.google.com/file/d/1cAJK2b-k-MQ1MkUiwG1Z2hv0gslCe7lv/view?usp=sharing
## Tóm tắt

Windows được chia thành hai chế độ chính: **User Mode** và **Kernel Mode**. Sự phân tách này là nền tảng cho tính ổn định và bảo mật của hệ thống.

## 1. User Mode

User Mode là môi trường hạn chế, nơi hầu hết các ứng dụng thực thi. Nó cung cấp không gian an toàn và biệt lập, ngăn chương trình truy cập trực tiếp vào tài nguyên hệ thống hoặc can thiệp vào ứng dụng khác.

### Các thành phần chính:

- **Applications**: Các chương trình người dùng tương tác (trình duyệt, word processor, game). Chúng chạy trong không gian địa chỉ ảo riêng, biệt lập với nhau.

- **Subsystems**: Cầu nối giữa ứng dụng User Mode và các dịch vụ Kernel Mode. Các subsystem chính bao gồm:
  - **Win32 Subsystem (`csrss.exe`)**: Quản lý cửa sổ, đồ họa và sự kiện nhập liệu. Đây là subsystem chính cho hầu hết ứng dụng desktop.
  - **NT Subsystem (`ntdll.dll`)**: Cung cấp giao diện giữa ứng dụng User Mode và Windows kernel. Nó chứa các system call stub để chuyển execution sang Kernel Mode.
  - **Các subsystem khác**: Windows cũng hỗ trợ POSIX subsystem (ít dùng) để tương thích với hệ điều hành khác.

- **DLLs (Dynamic Link Libraries)**: Các subsystem trên được hiện thực trong các file `.dll`. DLL là file chứa code và dữ liệu dùng chung cho nhiều chương trình cùng lúc. Thay vì biên dịch các hàm phổ biến (tạo cửa sổ, mở file) vào từng ứng dụng, Windows đặt chúng trong DLL. Khi cần, ứng dụng nạp DLL vào không gian địa chỉ của mình lúc runtime. **Lợi ích chính**: Tiết kiệm bộ nhớ — nếu 10 chương trình cùng dùng `kernel32.dll`, Windows chỉ giữ một bản copy trong RAM và chia sẻ cho cả 10 tiến trình.

## 2. Kernel Mode

Kernel Mode là chế độ đặc quyền, nơi các thành phần cốt lõi của hệ điều hành trú ngụ. Nó có quyền truy cập trực tiếp vào phần cứng và bộ nhớ, chịu trách nhiệm quản lý tài nguyên, thực thi chính sách bảo mật và cung cấp dịch vụ cho ứng dụng User Mode.

### Các thành phần chính:

- **Executive**: Lõi của Windows kernel, chứa các dịch vụ nền tảng:
  - **Object Manager**: Quản lý mọi tài nguyên hệ thống dưới dạng object (file, process, thread, synchronization primitive).
  - **Virtual Memory Manager (VMM)**: Quản lý bộ nhớ ảo, cấp không gian địa chỉ riêng cho từng tiến trình, xử lý cấp phát, phân trang và bảo vệ.
  - **Process Manager**: Tạo, quản lý và kết thúc process và thread.
  - **Security Reference Monitor (SRM)**: Thực thi chính sách bảo mật và kiểm soát truy cập. Kiểm tra quyền của process khi truy cập object.
  - **I/O Manager**: Xử lý mọi thao tác input/output, cung cấp giao diện thống nhất cho device driver.
  - **Cache Manager**: Cải thiện hiệu năng bằng cách cache dữ liệu thường xuyên truy cập trong bộ nhớ.
  - **Plug and Play (PnP) Manager**: Phát hiện và cấu hình thiết bị phần cứng.
  - **Power Manager**: Quản lý tiêu thụ điện năng của hệ thống.

- **Kernel**: Cấp thấp nhất của Kernel Mode, chịu trách nhiệm cho các chức năng hệ thống cơ bản như lập lịch thread, xử lý ngắt và điều phối ngoại lệ. Nó là nền tảng để Executive xây dựng lên.

- **Device Drivers**: Thành phần phần mềm cho phép hệ điều hành giao tiếp với thiết bị phần cứng. Chúng hoạt động trong Kernel Mode, dịch các yêu cầu I/O chung thành lệnh cụ thể cho thiết bị.

- **Hardware Abstraction Layer (HAL)**: Cung cấp lớp trừu tượng giữa kernel và phần cứng bên dưới. Cho phép Windows chạy trên nhiều nền tảng phần cứng khác nhau mà không cần sửa đổi kernel.

> **Đặc điểm quan trọng**: Bộ nhớ của Kernel Mode **không phụ thuộc tiến trình** (process-relative). Đây là "system space" dùng chung cho mọi tiến trình, nơi kernel, HAL và driver trú ngụ sau khi nạp. Điều này tạo bảo vệ tự động khỏi truy cập trực tiếp từ User Mode, đồng thời có nghĩa là lỗi trong kernel component (vd: memory leak trong driver) sẽ ảnh hưởng toàn hệ thống và không được giải phóng cho đến khi reboot.

## 3. Hypervisor Layer

Trong các phiên bản Windows hiện đại, có thêm một lớp kiến trúc nằm **bên dưới kernel**, cung cấp ranh giới tin cậy nền tảng cho toàn hệ thống. Đây là **hypervisor layer**.

- Thành phần duy nhất: **Hypervisor** (không có driver hay module khác trong môi trường này).
- Bản thân hypervisor gồm nhiều lớp và dịch vụ nội bộ: memory manager riêng, virtual processor scheduler, quản lý ngắt và timer, synchronization routines, quản lý partition (virtual machine instance) và inter-partition communication (IPC).
