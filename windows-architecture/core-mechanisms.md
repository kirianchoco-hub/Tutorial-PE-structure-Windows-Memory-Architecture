# Phần 2: Cơ chế cốt lõi
> Các cơ chế nền tảng mà Windows kernel sử dụng để quản lý tài nguyên và thực thi mã: system call, object, process, thread, và bộ nhớ ảo.
## 05 — System Calls
https://drive.google.com/file/d/1uXRqVW-4nRbPG3wnuK2rBxivcADWwQpx/view?usp=sharing
User-mode applications không thể truy cập trực tiếp tài nguyên kernel-mode. Thay vào đó, chúng sử dụng **system calls** (còn gọi là syscall hoặc service call) để yêu cầu kernel thực hiện dịch vụ.
### Quy trình 4 bước
1. **Application** gọi hàm high-level trong `kernel32.dll` (ví dụ: `CreateFileW`).
2. **`ntdll.dll`** chuẩn bị tham số, đặt syscall number vào `EAX`/`RAX`, thực thi lệnh `SYSENTER`/`SYSCALL` → chuyển từ Ring 3 sang Ring 0.
3. **Kernel** nhận syscall, tra **SSDT (System Service Dispatch Table)**, gọi hàm kernel tương ứng (ví dụ: `NtCreateFile`), validate tham số, thực hiện thao tác.
4. **Kernel** thực thi `SYSRETURN`/`SYSRET` → trở về Ring 3, trả kết quả cho ứng dụng.

### Bảng lệnh chuyển đổi

| Kiến trúc | Vào Kernel | Về User |
|-----------|------------|---------|
| x86 (32-bit) | `SYSENTER` | `SYSEXIT` |
| x64 (64-bit) | `SYSCALL` | `SYSRET` |
| ARM | `SVC` | `ERET` |

## 06 — Objects & Handles

Windows sử dụng **kiến trúc hướng đối tượng (object-based architecture)**: mọi tài nguyên hệ thống đều được biểu diễn dưới dạng **object**. Mỗi object có **type**, **thuộc tính (attributes)** và **phương thức (methods)**. Cách tiếp cận này cung cấp cơ chế quản lý tài nguyên thống nhất, an toàn và có thể mở rộng.

### Object là gì?

**Object** là cấu trúc dữ liệu đại diện cho tài nguyên hệ thống, ví dụ:

- File
- Process
- Thread
- Mutex, Semaphore, Event
- Graphic image (cửa sổ, bitmap)

Ứng dụng **không thể truy cập trực tiếp** dữ liệu object hoặc tài nguyên mà object đại diện. Thay vào đó, ứng dụng phải lấy **object handle** — một định danh (identifier) không trong suốt (opaque) đại diện cho object cụ thể.

### Object Type

Mỗi object thuộc về một **object type** (loại đối tượng). Object type bao gồm:

- **Kiểu dữ liệu do hệ thống định nghĩa** (system-defined data type).
- **Các hàm thao tác trên instance** của kiểu dữ liệu đó.
- **Tập thuộc tính object** (object attributes).

Ví dụ về object type:

| Object Type | Đại diện cho |
|-------------|--------------|
| `Process` | Tiến trình đang chạy |
| `Thread` | Luồng thực thi |
| `File` | Tệp tin hoặc thiết bị I/O |
| `Event` | Sự kiện đồng bộ hóa |
| `Mutex` | Mutex (loại trừ tương hỗ) |
| `Semaphore` | Semaphore (đếm tín hiệu) |
| `Key` | Registry key |
| `Section` | Vùng bộ nhớ chia sẻ (memory-mapped file) |

### Object Handle

**Handle** là một giá trị (thường là số nguyên) do hệ thống cấp cho ứng dụng khi nó tạo hoặc mở một object. Handle này là **opaque** — ứng dụng không thể biết nó trỏ đến đâu, chỉ có thể dùng nó để yêu cầu hệ thống thực hiện thao tác trên object.

#### Cơ chế hoạt động
- Mỗi tiến trình có một **bảng handle riêng** (private handle table).
- Khi ứng dụng nhận được handle, hệ thống ghi một entry vào bảng này.
- Entry chứa **địa chỉ của tài nguyên** và **cách xác định loại tài nguyên**.
- Khi ứng dụng gọi hàm API với handle, kernel tra bảng để tìm object tương ứng.

## 07 — Processes

**Program** là chuỗi lệnh tĩnh. **Process** là container chứa tập tài nguyên dùng khi thực thi instance của chương trình.
Process = program + execution context (processor state + memory map).
### Định nghĩa
**Process** là một **containment and management object** đại diện cho một instance đang chạy của chương trình. Thuật ngữ "process runs" (process chạy) được dùng khá phổ biến nhưng **không chính xác**. Process **không chạy** — process **quản lý**. Thread mới là thứ thực thi code và thực sự "chạy".

### Memory map của Process

Memory map của process bao gồm các vùng:

| Vùng | Mô tả |
|------|-------|
| **Text** | Machine instructions (chương trình đã biên dịch). |
| **Data** | Initialized static và global data. |
| **Bss** | Uninitialized static data (global uninitialized strings, numbers, structures). Kích thước vùng này nằm trong chương trình. |
| **Heap** | Bộ nhớ cấp phát động (thông qua `malloc`, `new`, hoặc memory allocation requests). |
| **Stack** | Call stack — chứa return addresses, local variables, temporary data, saved registers. |

### Process sở hữu những gì?
Từ góc nhìn high-level, một process sở hữu:
#### 1. Executable program
Chứa initial code và data dùng để thực thi code trong process. Điều này đúng với hầu hết process, nhưng một số process đặc biệt không có executable image (được kernel tạo trực tiếp).
#### 2. Private virtual address space
Dùng để cấp phát bộ nhớ cho bất kỳ mục đích nào mà code trong process cần.
#### 3. Access token (primary token)
Là object lưu **security context** của process, được dùng bởi các thread thực thi trong process (trừ khi thread giả định token khác bằng impersonation), và được dùng cho mọi access check mặc định.
#### 4. Private handle table
Bảng handle riêng đến các executive objects (events, semaphores, files, ...).
#### 5. Một hoặc nhiều thread thực thi
Process user-mode thông thường được tạo với **một thread** (thực thi hàm `main`/`WinMain` cổ điển). Process user-mode không có thread hầu như vô dụng, và trong điều kiện bình thường sẽ bị kernel hủy.

## 08 — Threads

**Thread** là thực thể thực sự thực thi code, nằm trong process, dùng tài nguyên do process cung cấp (virtual memory, handles). Nếu process là "container quản lý", thì thread là "đơn vị lao động" thực sự.

### Định nghĩa

Một **thread** là một thực thể trong process mà hệ điều hành lập lịch để thực thi. Mỗi thread có:
- Ngữ cảnh thực thi (execution context) riêng.
- Stack riêng.
- Trạng thái riêng.

### Thông tin quan trọng của Thread

Mỗi thread sở hữu các thông tin sau:

| Thành phần | Mô tả |
|------------|-------|
| **Current access mode** | User hoặc kernel. |
| **Execution context** | Processor registers và execution state (bao gồm program counter). |
| **Stack(s)** | Một hoặc hai stack: kernel stack và user stack. |
| **TLS array** | Thread Local Storage — lưu dữ liệu riêng của thread với uniform access semantics. |
| **Base priority** | Độ ưu tiên cơ bản (do lập trình viên hoặc hệ thống đặt). |
| **Current (dynamic) priority** | Độ ưu tiên hiện tại (có thể thay đổi bởi scheduler). |
| **Processor affinity** | Tập hợp các processor mà thread được phép chạy trên đó. |
| **State** | Running, Ready, hoặc Waiting. |

### Trạng thái Thread

Thread trong Windows có thể ở một trong các trạng thái chính sau:

| Trạng thái | Mô tả |
|------------|-------|
| **Running** | Thread đang thực thi code trên một logical processor. |
| **Ready** | Thread đang chờ được lập lịch để thực thi vì tất cả các processor liên quan đang bận hoặc không khả dụng. |
| **Waiting** | Thread đang chờ một sự kiện xảy ra trước khi tiếp tục. Khi sự kiện xảy ra, thread chuyển sang trạng thái Ready. |

## 09 — Virtual Memory

Mỗi process có **không gian địa chỉ ảo riêng, private, linear** (private virtual address space). Không gian này bắt đầu gần như trống — executable image và `ntdll.dll` được map đầu tiên, sau đó là các subsystem DLLs. Khi thread chính bắt đầu thực thi, bộ nhớ được cấp phát, nhiều DLLs được nạp, v.v.

### Đặc điểm của Virtual Address Space

- **Private**: Không gian địa chỉ này là riêng của process. Process khác **không thể truy cập trực tiếp**.
- **Range**: Bắt đầu từ 0 (thực tế 64KB đầu và cuối không thể commit) đến mức tối đa phụ thuộc vào "bitness" của process (32-bit hoặc 64-bit) và "bitness" của hệ điều hành.
- **Virtual**: Có mối quan hệ **gián tiếp** giữa một dải địa chỉ và vị trí chính xác của nó trong bộ nhớ vật lý (RAM). Từ góc nhìn thực thi, không cần biết bộ nhớ sắp được truy cập có trong RAM hay không:
  - Nếu bộ nhớ **đã được map vào RAM**, CPU sẽ truy cập dữ liệu trực tiếp.
  - Nếu bộ nhớ **không resident** (được chỉ định bởi flag trong translation table entry), CPU sẽ raise **page fault exception**. Memory manager's page fault handler sẽ fetch dữ liệu từ file thích hợp, copy vào RAM, cập nhật page table entries, và yêu cầu CPU thử lại.

### Page State

Mỗi page trong virtual address space có thể ở một trong ba trạng thái:

| Trạng thái | Mô tả |
|------------|-------|
| **Free** | Page chưa được cấp phát theo bất kỳ cách nào; không có gì ở đó. Mọi truy cập sẽ gây **access violation exception**. Hầu hết page trong process mới tạo là free. |
| **Committed** | Ngược lại với Free — page đã được cấp phát, có thể truy cập thành công (trừ protection attributes, ví dụ: ghi vào page read-only gây access violation). Committed pages thường được map vào RAM hoặc vào file (như page file). |
| **Reserved** | Page chưa được commit, nhưng dải địa chỉ được giữ cho possible future commitment. Từ góc nhìn CPU, nó giống hệt Free — mọi truy cập gây access violation. Tuy nhiên, các allocation attempt mới sử dụng `VirtualAlloc` (hoặc `NtAllocateVirtualMemory`) mà không chỉ định địa chỉ cụ thể sẽ **không cấp phát trong vùng reserved**. |
