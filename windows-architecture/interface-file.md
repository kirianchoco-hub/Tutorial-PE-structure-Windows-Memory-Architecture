# Phần 3: Giao diện & Hệ thống

> Các lớp giao diện lập trình mà ứng dụng dùng để tương tác với Windows, cùng các file hệ thống cốt lõi hiện thực hóa kiến trúc bên dưới.

## 10 — Programming Interfaces
Windows cung cấp nhiều lớp **Application Programming Interfaces (APIs)** để developer tương tác với core OS objects và services. Qua nhiều thập kỷ, các API này tiến hóa phản ánh thay đổi trong paradigm lập trình và nhu cầu về kiến trúc component-based. Hành trình bắt đầu với API kiểu C nền tảng.
### Windows API
**Windows API** là user-mode system programming interface đến Windows OS family. Thuật ngữ "Windows API" hoặc "Win32 API" chỉ cả giao diện lập trình 32-bit và 64-bit đến Windows.
### Component Object Model (COM)
Để giải quyết hạn chế của API kiểu C, Microsoft giới thiệu **Component Object Model (COM)** năm 1993. Ban đầu phát triển để cho phép các ứng dụng Microsoft Office chia sẻ dữ liệu — ví dụ: nhúng biểu đồ Excel vào tài liệu Word. Khả năng này, gọi là **Object Linking and Embedding (OLE)**, ban đầu xây trên cơ chế cũ hơn là **Dynamic Data Exchange (DDE)**, nhưng hạn chế của DDE đã thúc đẩy việc tạo ra COM. Thực tế, COM ban đầu được phát hành với tên **OLE 2**.
COM xây trên 2 nguyên tắc cốt lõi:
| Nguyên tắc | Mô tả |
|------------|-------|
| **Interfaces** | Client applications tương tác với COM objects (đôi khi gọi là COM servers) qua các contract được định nghĩa rõ ràng gọi là interfaces. Các interface này nhóm các hàm liên quan, tạo chuẩn binary-compatible, tránh vấn đề name mangling đặc thù của từng compiler. Điều này cho phép developer dùng COM objects từ nhiều ngôn ngữ: C, C++, Visual Basic, .NET. |
| **Dynamic Loading** | Thay vì được liên kết tĩnh (statically linked) vào client application, COM components được nạp động (dynamically loaded) lúc runtime. Các component này thường nằm trong DLLs hoặc executable files (EXEs). |

COM cũng giới thiệu các tính năng quan trọng để quản lý security, data transfer giữa các process (marshalling), và threading models. Nhiều công nghệ Windows quen thuộc xây trên COM, bao gồm **DirectX**, **Windows Media Foundation**, và **Windows Shell**.

### The Windows Runtime (WinRT)

Với bản phát hành Windows 8, Microsoft ra mắt API và runtime environment mới gọi là **Windows Runtime (WinRT)**. Cần phân biệt WinRT với **Windows RT** — phiên bản Windows cho thiết bị ARM đã ngừng phát triển.

WinRT được thiết kế làm nền tảng cho một lớp ứng dụng mới, ban đầu gọi là **Metro Apps**, nay gọi là **Universal Windows Platform (UWP) apps**. Các ứng dụng này chạy trên nhiều loại thiết bị: IoT, phones, tablets, desktops, thậm chí Xbox và HoloLens.

Về mặt kỹ thuật, WinRT xây trên COM, mở rộng infrastructure cốt lõi. Nó giới thiệu các tính năng như **type metadata toàn diện** lưu trong file `.winmd` — nâng cấp từ khái niệm tương tự trong COM gọi là type libraries. Điều này dẫn đến API nhất quán hơn với namespace hierarchy rõ ràng.

> **Quan trọng**: WinRT **không phải** là sự thay thế hoàn toàn cho Windows API truyền thống. Nó song song với Windows API. Desktop applications có thể truy cập một subset của WinRT APIs, và ngược lại, UWP apps có thể dùng limited set của Win32 và COM APIs cổ điển. Về cốt lõi, WinRT API vẫn dựa trên các binary và API Windows legacy.

