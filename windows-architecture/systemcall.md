# 05 — System Calls

## Tóm tắt
User-mode applications không thể truy cập trực tiếp tài nguyên kernel-mode. Thay vào đó, chúng phải sử dụng **system calls** (còn gọi là syscall hoặc service call) để yêu cầu kernel thực hiện dịch vụ. Đây là cơ chế chuyển đổi (transition) từ User Mode sang Kernel Mode một cách an toàn và có kiểm soát.
## 1. Tại sao cần System Call?
Trong kiến trúc phân lớp của Windows:
- **User Mode** bị hạn chế quyền truy cập: không thể đọc/ghi trực tiếp vào bộ nhớ kernel, không thể thực thi lệnh đặc quyền (privileged instructions).
- **Kernel Mode** có toàn quyền truy cập phần cứng và bộ nhớ.
Do đó, khi ứng dụng cần một dịch vụ từ kernel (tạo file, cấp phát bộ nhớ, tạo process, v.v.), nó phải "nhờ" kernel thông qua một cơ chế được kiểm soát — đó chính là **system call**.
## 2. Quy trình System Call (4 bước)

https://drive.google.com/file/d/1uXRqVW-4nRbPG3wnuK2rBxivcADWwQpx/view?usp=sharing
