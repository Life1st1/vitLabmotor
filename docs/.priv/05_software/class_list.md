# Software Class List & Architecture Allocation

Tài liệu này định nghĩa danh sách các Lớp/Module phần mềm được chuẩn hóa theo kiến trúc phân tầng (Layered Architecture) trong [software_block_diagram.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/05_software/software_block_diagram.md) và đáp ứng đầy đủ yêu cầu truy vết từ [traceability_matrix.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/06_verification/traceability_matrix.md).

---

## 1. Tầng Ứng Dụng (Application Layer)
* **`Actuator`**: Lớp điều phối cấp cao nhất; tích hợp máy trạng thái hệ thống (`StateMachine`: IDLE, CALIBRATION, CLOSED_LOOP, FAULT), quản lý chu trình khởi động và an toàn.

---

## 2. Tầng Dịch Vụ (Services Layer)
* **`ControlService`**: Điều phối các vòng lặp điều khiển thời gian thực (Position Loop 1kHz, Velocity Loop 1kHz, Torque/Current Loop 20–40kHz).
* **`CalibrationService`**: Tự động đo thông số động cơ ($R, L$), offset cảm biến dòng và căn chỉnh góc 0 điện (*SR-SEN-02*).
* **`ConfigurationService`**: Quản lý phiên bản schema cấu hình, kiểm tra tính toàn vẹn CRC, migration tham số và factory reset (*SR-CFG-01/02*).
* **`TelemetryService`**: Đóng gói và truyền dữ liệu thời gian thực (Angle, Speed, Current, VBUS, Temp) ở tần số từ 1Hz đến 1000Hz (*SR-TEL-01*).
* **`DiagnosticsService` & `FaultLogger`**: Theo dõi sức khỏe hệ thống (Runtime Health), đếm lỗi CAN/Stall, lưu trữ 8 bản ghi sự cố gần nhất vào bộ nhớ Flash (*SR-DIA-01*, *SR-LOG-01*).
* **`DebugShell`**: Giao diện dòng lệnh (CLI Shell) tương tác qua UART / USB CDC phục vụ gỡ lỗi (*SR-COM-02*).
* **`FwUpdateDaemon`**: Dịch vụ kiểm tra và cập nhật nạp firmware an toàn qua bus CAN-FD / Bootloader, hỗ trợ CRC check và rollback (*SR-FWU-01/02*).

---

## 3. Tầng Lõi Điều Khiển & Giao Tiếp (Core & Communication Layer)
* **`FocCore`**: Triển khai toán học lõi điều khiển vector không gian (Clarke, Park, Inverse Park, SVPWM, kẹp dòng $I_q$ giới hạn mô-men) kết hợp bộ tăng tốc CORDIC/FMAC trên STM32G4 (*SR-MOT-01*, *SR-PWR-02*).
* **`MotionProfile`**: Bộ sinh quỹ đạo chuyển động mượt mà (Trapezoidal / S-Curve) cho vòng lặp vị trí và vận tốc.
* **`BrakeChopper`**: Thuật toán giám sát điện áp bus $V_{BUS}$ và điều chế xả phanh tái sinh qua MOSFET điện trở hãm (*SR-PWR-03/04*).
* **`ObjectDictionary`**: Bảng từ điển đối tượng hợp nhất chuẩn CANopen / CiA 402, cho phép các giao thức CAN, UART, Modbus cùng truy cập một schema dữ liệu duy nhất (*SR-SW-03*).
* **`CanComm`**: Driver giao thức và xử lý khung truyền CAN-FD (1Mbps Arbitration, 5Mbps Data), hỗ trợ tối đa 64 node (*SR-COM-01*).

---

## 4. Tầng An Toàn & Bảo Vệ (Safety Layer)
* **`SafetyManager` (`ErrorProtect`)**: Giám sát lỗi khẩn cấp phần cứng/phần mềm (quá dòng OCP, quá áp OVP, thấp áp UVP, kẹt trục Stall, mất tín hiệu phản hồi) và ngắt PWM ngay lập tức qua Break Input (< 1µs) (*SR-SAF-03/04*).
* **`ThermalManager`**: Giám sát nhiệt độ MOSFET và lõi MCU, thực hiện thuật toán **Smooth Thermal Derating** (giảm dần công suất khi vượt $75^\circ\text{C}$, ngắt an toàn tại $85^\circ\text{C}$) (*SR-SAF-01/02*).

---

## 5. Tầng Driver Thiết Bị Ngoại Vi (Device Drivers Layer)
* **`CurrentSensor`**: Giao tiếp bộ đo dòng 3 pha (3 Shunt + Op-Amp DRV8323 CSA), kích hoạt ADC đồng bộ tâm chu kỳ PWM (*SR-HW-01*, *SR-SW-01*).
* **`AngleSensor`**: Driver cảm biến góc từ tính MT6816 qua bus SPI tốc độ cao $\ge 10\text{MHz}$, kiểm tra tính toàn vẹn CRC (*SR-SEN-01*).
* **`GateDriver`**: Giao tiếp SPI cấu hình tham số, đọc thanh ghi lỗi và quản lý chế độ hoạt động của TI DRV8323RS.
* **`PowerMonitor`**: Đọc và tính toán điện áp đầu vào $V_{BUS}$, phát hiện sụt áp/mất nguồn sớm (*SR-PWR-05/06*).
* **`FlashStorage`**: Driver giao tiếp bộ nhớ Flash nội/ngoại, hỗ trợ cơ chế Wear-Leveling và ghi dữ liệu an toàn.