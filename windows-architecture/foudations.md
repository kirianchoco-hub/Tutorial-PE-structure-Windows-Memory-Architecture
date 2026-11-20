
# Phần 1: Nền tảng
## 01 — Introduction
Tổng quan về kiến trúc phân lớp của Windows. Hệ điều hành Windows là một môi trường phức tạp và phân lớp. Với hầu hết người dùng, nó là một "hộp đen" — bạn click icon, chương trình chạy. Nhưng với developer, security researcher, hoặc system administrator, hiểu cơ chế bên dưới là điều thiết yếu để xây dựng phần mềm vững chắc, phân tích mã độc, và troubleshoot các vấn đề hệ thống phức tạp.

Series này sẽ là hướng dẫn bước vào thế giới đó, bóc tách các lớp của OS để lộ ra các thành phần và hành vi cốt lõi. Trong phần đầu tiên, chúng ta sẽ thiết lập bản đồ nền tảng của kiến trúc Windows. Bắt đầu với khái niệm quan trọng nhất: **sự phân tách giữa User Mode và Kernel Mode**.

## 02 — Kernel vs User Mode
Thiết kế nền tảng của Windows, thiết yếu cho tính ổn định và bảo mật, là sự phân tách thành hai chế độ truy cập processor: **user mode** và **kernel mode**. Sự phân chia này quy định code nào được làm gì và truy cập tài nguyên hệ thống nào.
- **User application code** chạy trong user mode.
- **OS code** (system services, device drivers) chạy trong kernel mode.
**Kernel mode** là chế độ thực thi trong processor cấp quyền truy cập toàn bộ bộ nhớ hệ thống và mọi lệnh CPU. Một số processor gọi đây là **code privilege level** hoặc **ring level**, số khác gọi là **supervisor mode** và **application mode**.

Windows chỉ dùng **2 mức** vì một số kiến trúc phần cứng (ARM hiện nay, MIPS/Alpha trước đây) chỉ hỗ trợ 2 mức đặc quyền. Chọn mức tối thiểu thấp nhất cho phép kiến trúc hiệu quả và portable hơn.

## 03 — System Architecture
https://drive.google.com/file/d/1cAJK2b-k-MQ1MkUiwG1Z2hv0gslCe7lv/view?usp=sharing
Windows chia thành hai chế độ chính: **User Mode** và **Kernel Mode**.
### User Mode
Môi trường hạn chế, nơi hầu hết ứng dụng thực thi. Bao gồm:
- **Applications**: Chương trình người dùng (trình duyệt, word processor, game). Chạy trong không gian địa chỉ ảo riêng.
- **Subsystems**: Cầu nối giữa ứng dụng và kernel-mode services:
  - **Win32 Subsystem (`csrss.exe`)**: Quản lý cửa sổ, đồ họa, sự kiện nhập liệu.
  - **NT Subsystem (`ntdll.dll`)**: Giao diện giữa ứng dụng và kernel, chứa system call stubs.
- **DLLs**: Thư viện liên kết động, chia sẻ code giữa các tiến trình (ví dụ: `kernel32.dll`).
### Kernel Mode
Chế độ đặc quyền, truy cập trực tiếp phần cứng và bộ nhớ. Bao gồm:
- **Executive**: Object Manager, VMM, Process Manager, SRM, I/O Manager, Cache Manager, PnP, Power Manager.
- **Kernel**: Lập lịch thread, xử lý ngắt, điều phối ngoại lệ.
- **Device Drivers**: Giao tiếp phần cứng.
- **HAL**: Trừu tượng phần cứng.
> **Lưu ý**: Bộ nhớ Kernel Mode **không phụ thuộc tiến trình** (process-relative). Đây là "system space" dùng chung cho mọi tiến trình.
