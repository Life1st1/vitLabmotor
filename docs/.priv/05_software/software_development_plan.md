# Kế Hoạch Thiết Kế & Phát Triển Phần Mềm FOC (Software Development Plan)

> **Mục tiêu:** Xây dựng phần mềm điều khiển FOC hiệu năng cao, đạt độ tin cậy chuẩn công nghiệp trên MCU **STM32G431CBU6**, đáp ứng các tiêu chuẩn trong [traceability_matrix.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/06_verification/traceability_matrix.md) và cấu trúc phân tầng tại [software_block_diagram.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/05_software/software_block_diagram.md).

---

## Giai Đoạn 1: Thiết Kế Chi Tiết Kiến Trúc & Lớp (Detailed Class Design)
*Mục tiêu: Hoàn thiện bản vẽ kỹ thuật chi tiết của tất cả các lớp trong [class_list.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/05_software/class_list.md) trước khi code.*

1. **Thiết kế thuộc tính và phương thức (Attributes & Methods Specification):**
   * Xác định dữ liệu private/public, cấu trúc dữ liệu chung (`structs`, `enums`).
   * Định nghĩa API (input parameters, return types, error codes) cho từng lớp.
   * Tạo tài liệu `docs/.priv/05_software/class_specifications.md`.
2. **Thiết kế mô hình thực thi thời gian thực (Timing & Execution Model):**
   * Phân bổ nhiệm vụ cho các vòng ngắt: Fast ISR (20–40kHz), Control Loop (1kHz), Slow Tasks (10Hz–100Hz).
   * Lập sơ đồ phân bổ tài nguyên phần cứng STM32G4 (TIM1, TIM2/3, ADC1/2, SPI1/2, FDCAN1, DMA).
3. **Thiết kế máy trạng thái hệ thống (System State Machine):**
   * Định nghĩa các trạng thái (`BOOT`, `CALIBRATING`, `IDLE`, `RUN_CLOSED_LOOP`, `ERROR_STOP`, `FAULT`).
   * Ma trận chuyển trạng thái (State Transition Table) và cơ chế khóa an toàn (Interlock).

---

## Giai Đoạn 2: Khởi Tạo Dự Án & Thiết Lập Nền Tảng (Platform Setup & HAL)
*Mục tiêu: Cấu hình phần cứng vi điều khiển, xung nhịp và ngoại vi mức thấp.*

1. **Khởi tạo project CubeMX / Makefile / CMake trong `fw/`:**
   * Cấu hình Clock Tree chạy tối đa 170MHz.
   * Cấu hình TIM1 xuất 6 kênh PWM bổ sung có Deadtime phần cứng.
   * Cấu hình ADC1/ADC2 chế độ Dual Simultaneous Sampling, trigger đồng bộ từ TIM1 TRGO (tâm PWM).
   * Cấu hình SPI tốc độ cao cho MT6816 và DRV8323RS.
   * Cấu hình FDCAN (1Mbps Arbitration, 5Mbps Data bit-rate).
2. **Tạo khung thư mục mã nguồn chuẩn hóa:**
   * `fw/app/`, `fw/services/`, `fw/core/`, `fw/safety/`, `fw/drivers/`, `fw/platform/`.

---

## Giai Đoạn 3: Phát Triển Tầng Drivers & Cảm Biến (Device Drivers Development)
*Mục tiêu: Đảm bảo giao tiếp phần cứng chính xác, tin cậy và không nhiễu.*

1. **Triển khai `GateDriver` (TI DRV8323RS):**
   * Đọc/ghi thanh ghi qua SPI, cấu hình dòng nạp/xả cổng Gate, bảo vệ VDS, deadtime.
2. **Triển khai `AngleSensor` (MT6816):**
   * Đọc góc 14-bit qua SPI/DMA, kiểm tra chẵn lẻ (Parity), tính toán vận tốc góc bằng lọc vi phân.
3. **Triển khai `CurrentSensor`:**
   * Lấy mẫu dòng điện 3 pha, trừ offset điểm 0, quy đổi sang Ampe ($I_a, I_b, I_c$).
4. **Triển khai `PowerMonitor` & `TempSensor`:**
   * Đo $V_{BUS}$, dòng tổng, tính toán nhiệt độ cầu H từ điện trở NTC.

---

## Giai Đoạn 4: Phát Triển Lõi FOC & Điều Khiển (FOC Core & Control Loops)
*Mục tiêu: Thuật toán điều khiển chuyển động đạt độ chính xác cao.*

1. **Triển khai `FocCore`:**
   * Biến đổi Clarke ($I_a, I_b \rightarrow I_\alpha, I_\beta$).
   * Biến đổi Park ($I_\alpha, I_\beta, \theta_e \rightarrow I_d, I_q$) sử dụng bộ tăng tốc toán học CORDIC.
   * Bộ điều khiển dòng điện PID ($I_d = 0$, $I_q = I_{target}$) kèm giới hạn điện áp (Anti-windup).
   * Biến đổi Inverse Park & Bộ điều chế vector không gian (SVPWM) 7-segment.
2. **Triển khai `ControlService`:**
   * Vòng lặp vị trí (Position loop) và vòng lặp vận tốc (Velocity loop) tần số 1kHz.
   * Tích hợp `MotionProfile` (Trapezoidal / S-curve trajectory).
3. **Triển khai `CalibrationService`:**
   * Routine tự động đo điện trở pha ($R$), độ tự cảm ($L$).
   * Tự động căn chỉnh góc 0 điện (Electrical angle zero offset alignment).
4. **Triển khai `BrakeChopper`:**
   * Thuật toán băm xung xả năng lượng tái sinh khi $V_{BUS}$ tăng cao.

---

## Giai Đoạn 5: An Toàn, Giám Sát & Lưu Trữ (Safety, Diagnostics & Storage)
*Mục tiêu: Bảo vệ phần cứng khỏi cháy nổ và lưu trữ cấu hình bền bỉ.*

1. **Triển khai `SafetyManager` (`ErrorProtect`):**
   * Ngắt phần cứng Break-in (tắt PWM $< 1\mu\text{s}$) khi quá dòng phần cứng.
   * Ngắt phần mềm khi quá áp, sụt áp, kẹt trục (Stall), mất tín hiệu encoder.
2. **Triển khai `ThermalManager`:**
   * Thuật toán Smooth Thermal Derating giảm dòng khi quá nhiệt.
3. **Triển khai `ConfigurationService` & `FlashStorage`:**
   * Lưu cấu hình (PID gains, motor poles, encoder offset) kèm kiểm tra CRC32.
4. **Triển khai `FaultLogger`:**
   * Lưu 8 lỗi gần nhất kèm timestamp vào sector Flash riêng.

---

## Giai Đoạn 6: Giao Tiếp & Điều Khiển Từ Xa (Communications & Telemetry)
*Mục tiêu: Tích hợp với Robot Host, ROS2 và công cụ GUI/CLI.*

1. **Triển khai `ObjectDictionary`:**
   * Bảng ánh xạ tham số chuẩn theo chỉ số Index/Sub-index (CANopen / CiA 402).
2. **Triển khai `CanComm` (CAN-FD):**
   * Truyền/nhận lệnh điều khiển vị trí, tốc độ, mô-men và trả lời telemetry định kỳ.
3. **Triển khai `DebugShell` (UART/USB CDC):**
   * CLI tương tác dòng lệnh gõ trực tiếp từ terminal máy tính.
4. **Triển khai `FwUpdateDaemon`:**
   * Hỗ trợ cập nhật nạp firmware từ xa qua CAN bus.

---

## Giai Đoạn 7: Kiểm Thử, Đo Đạc & Tối Ưu Hóa (Verification & Benchmarking)
*Mục tiêu: Hoàn tất 100% các Test Case theo `traceability_matrix.md`.*

1. Đo thời gian thực thi ngắt FOC ($\le 30\mu\text{s}$).
2. Test khả năng đáp ứng bước dòng điện (Current step response).
3. Test kẹp dòng 60A và xả phanh tái sinh.
4. Chạy kiểm thử nhiệt độ và khả năng chịu tải liên tục 30A.
