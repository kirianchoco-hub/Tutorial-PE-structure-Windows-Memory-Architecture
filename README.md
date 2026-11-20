# Tutorial-PE-structure-Windows-Memory-Architecture
### Mở đầu

Khi bạn double-click một file ```.exe```, Windows không đơn thuần "đọc" file đó từ ổ cứng. Nó thực hiện một quá trình ánh xạ phức tạp: các section trên đĩa được căn chỉnh lại theo đơn vị bộ nhớ (thường là 0x1000 thay vì 0x200), các địa chỉ tương đối (RVA) được cộng thêm ImageBase để trở thành địa chỉ ảo tuyệt đối. Sự khác biệt giữa File Offset và RVA chính là nguồn gốc của vô số lỗi trong reverse engineering và phân tích malware.

Tutorial này được thiết kế cho những ai đã có kiến thức cơ bản về C/Assembly nhưng muốn hiểu tường tận cách Windows tổ chức bộ nhớ cho một tiến trình. Chúng ta sẽ không chỉ dừng ở việc đọc cấu trúc PE trên giấy, mà sẽ đi sâu vào Windows Memory Architecture: cách loader tạo ra Image Buffer, cách các section được bảo vệ bằng quyền truy cập (Read/Write/Execute), và cách tính toán địa chỉ thực thi từ cấu trúc file.

### Bạn sẽ nắm được:
- Cấu trúc chuẩn của một file PE32/PE32+ (DOS Header → NT Headers → Section Table).
- Sự khác biệt cốt lõi giữa File Alignment và Section Alignment.
- Cách Windows ánh xạ file PE vào bộ nhớ ảo và cơ chế Relocation
