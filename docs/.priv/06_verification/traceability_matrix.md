# Traceability Matrix (Ma trận truy vết yêu cầu)

Ma trận này thiết lập mối liên kết hai chiều (Bidirectional Traceability) theo mô hình chuẩn kỹ thuật V-Model:
**Business Requirement (BR) ➔ System Requirement (SR) ➔ Subsystem Allocation (HW/SW) ➔ Verification Method ➔ Test Case (TC) & Acceptance Criteria**.

---

## 1. Phương pháp xác thực (Verification Methods)
- **[T] Test**: Kiểm thử thực nghiệm thông qua đo đạc, đo kiểm bằng thiết bị (Oscilloscope, Logic Analyzer, Power Analyzer, Electronic Load, Motor Dyno).
- **[D] Demonstration**: Trình diễn chức năng hoạt động (thực thi lệnh điều khiển, quay động cơ, bắt tín hiệu CLI/CAN).
- **[I] Inspection**: Kiểm tra trực quan bằng mắt/kính hiển vi, kiểm tra kích thước vật lý, sơ đồ bố trí linh kiện hoặc rà soát mã nguồn (Code Review).
- **[A] Analysis**: Phân tích lý thuyết, tính toán mô phỏng mạch điện, phân tích nhiệt (Thermal Simulation), phân tích độ tin cậy MTBF.

---

## 2. Bảng Ma Trận Truy Vết (Traceability Matrix)

| Business Req ID | Nội dung Business Requirement | System Req ID | Đặc tả System Requirement | Phân hệ (Alloc) | P.Pháp | Test Case ID | Tiêu chí nghiệm thu (Acceptance Criteria) |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **BR-001** | Motor Control FOC (current, duty cycle, speed, position) | **SR-MOT-01** | Vòng lặp dòng FOC > 20 kHz (Clarke, Park, SVPWM), jitter < 1% | SW/HW | T | **TC-MOT-01** | Đo tần số ngắt FOC đạt $\ge$ 20kHz, thời gian tính toán FOC $\le$ 30µs, jitter vòng lặp < 1%. |
| | | **SR-MOT-02** | Vòng lặp tốc độ (Velocity Loop) 1 kHz | SW | T, D | **TC-MOT-02** | Động cơ duy trì dải tốc độ ổn định từ 1 RPM đến max RPM; đáp ứng tải không sụt > 5%. |
| | | **SR-MOT-03** | Vòng lặp vị trí (Position Loop) 1 kHz | SW | T, D | **TC-MOT-03** | Góc định vị bám vết chính xác, settling time < 100ms, sai số góc tĩnh < 0.2°. |
| | | **SR-MOT-04** | Tần số điện (Electrical Frequency) hỗ trợ tới 3000 Hz | SW/HW | T | **TC-MOT-04** | Động cơ nhiều cặp cực đạt tốc độ cao tương ứng $f_e = 3000\text{ Hz}$ mà không mất đồng bộ. |
| **BR-002** | Dòng chịu đựng cao cho khớp robot (30A liên tục, 60A đỉnh) | **SR-PWR-01** | Cấp dòng pha định mức liên tục 30A và dòng đỉnh 60A ($\ge 5\text{s}$) | HW | T | **TC-PWR-01** | Chạy tải liên tục với dòng 30A trong 30 phút, nhiệt độ MOSFET $\le$ 85°C; xung đỉnh 60A trong 5s không quá dòng. |
| | | **SR-PWR-02** | Current Limiting & Torque Limiting theo thời gian thực (Clamp ở 60A) | SW | T | **TC-PWR-02** | Khi tải ghì quá mức cài đặt, dòng $I_q$ được kẹp (clamp) chính xác ở ngưỡng giới hạn tối đa 60A. |
| **BR-003** | Encoder Feedback | **SR-SEN-01** | Hỗ trợ Encoder góc từ tính qua SPI (AS5047P/MT6835) độ phân giải $\ge$ 14-bit | HW/SW | T | **TC-SEN-01** | Đọc dữ liệu góc qua SPI tần số $\ge$ 10MHz, không có bit lỗi CRC, tốc độ lấy mẫu $\ge$ 20kHz. |
| | | **SR-SEN-02** | Căn chỉnh góc 0 điện (Electrical angle offset calibration) & lưu cấu hình | SW | D, T | **TC-SEN-02** | Chạy routine căn chỉnh tự động, tìm đúng offset góc và lưu chuẩn xác vào Flash. |
| **BR-004** | Đo dòng pha không bị nhiễu | **SR-HW-01** | Mạch shunt low-side/in-line kèm Op-Amp khuếch đại vi sai, lọc RC tối ưu | HW | T, I | **TC-HW-01** | Tín hiệu dòng pha trên oscilloscope sạch, SNR cao, biên độ gai ringing < 5% thang đo. |
| | | **SR-SW-01** | Kích hoạt ADC đồng bộ PWM ở tâm vector (Center-aligned trigger) | SW | T | **TC-SW-01** | Thời điểm trigger ADC rơi đúng giữa chu kỳ PWM (tránh vùng chuyển mạch switching noise). |
| **BR-005** | Thiết kế nhỏ gọn hình tròn, bán kính < 10cm gắn sau động cơ | **SR-HW-02** | Kích thước PCB dạng tròn bán kính $R < 10\text{cm}$ (tối ưu $R \le 25-45\text{mm}$) gắn vừa sau motor | HW/MECH| I | **TC-HW-02** | Kích thước bo mạch nằm trong biên dạng tròn bán kính $< 10\text{cm}$, tâm đồng trục và lỗ ốc bắt vừa khớp motor. |
| | | **SR-HW-03** | Đầu nối nguồn, pha và tín hiệu gọn gàng, chống rung lắc | HW | I, D | **TC-HW-03** | Dùng header khóa (JST-GH/Molex), pad công suất chịu dòng cao, cắm rút dễ dàng. |
| **BR-006** | Dễ điều khiển & tích hợp | **SR-COM-01** | CAN-FD (1Mbps Arbitration, 5Mbps Data), tối đa 64 node | HW/SW | T, D | **TC-COM-01** | Gửi/nhận 1000 frames/s ở tốc độ 5Mbps giữa các node trên bus, tỷ lệ lỗi gói = 0%. |
| | | **SR-COM-02** | Giao tiếp UART & USB CDC (115200 bps) với giao diện dòng lệnh (CLI Shell) | HW/SW | D | **TC-COM-02** | Kết nối qua cáp USB/UART, shell phản hồi các lệnh cấu hình, đọc log và debug mượt mà. |
| | | **SR-COM-03** | Giao tiếp RS485 Modbus RTU (115200 bps) | HW/SW | T, D | **TC-COM-03** | Đọc/ghi thông số qua bảng thanh ghi Modbus RTU chuẩn công nghiệp. |
| | | **SR-COM-04** | Cung cấp ROS2 Node driver chạy trên host | SW | D | **TC-COM-04** | Node ROS2 publish topic telemetry và subscribe command topic ổn định $\ge$ 100Hz. |
| **BR-007** | Phần mềm mở rộng và dễ bảo trì | **SR-SW-02** | Kiến trúc 3 tầng chuẩn hóa: Application - Services - Core & HAL | SW | I | **TC-SW-02** | Code base độc lập phần cứng (HAL tách biệt FOC core), tuân thủ coding convention. |
| | | **SR-SW-03** | Bảng từ điển đối tượng hợp nhất (Unified Object Dictionary) | SW | T | **TC-SW-03** | Tất cả các cổng CAN/UART/Modbus cùng truy xuất chung 1 schema dữ liệu Object Dictionary. |
| **BR-008** | Cân bằng mã nguồn mở và bảo vệ IP | **SR-SW-04** | Phân tách module giao tiếp mở (Open HAL/API) và thuật toán lõi | SW | I, A | **TC-SW-04** | Rà soát cấu trúc module, tài liệu hóa ranh giới mã nguồn mở và phần mã độc quyền. |
| **BR-009** | Bo mạch PCB chắc chắn, bền bỉ | **SR-HW-04** | PCB 4-6 lớp, đồng dày (2-3oz), via stitching thoát nhiệt, linh kiện chuẩn công nghiệp | HW | I, A | **TC-HW-05** | Thiết kế đạt chuẩn IPC-2221, clearance/creepage chuẩn cho dải áp 60V, via đủ chịu dòng. |
| | | **SR-ENV-01** | Hoạt động: -20°C ~ +85°C; Lưu trữ: -40°C ~ +105°C | HW | T, A | **TC-ENV-01** | Đặt bo mạch trong buồng nhiệt (-20°C và +85°C), bo mạch khởi động và vận hành bình thường. |
| **BR-010** | PCB có khả năng test từng khối chức năng | **SR-HW-05** | Bố trí đầy đủ Test Points (Nguồn, Gate, Shunt, VBUS, SWD, Bus) | HW | I, T | **TC-HW-04** | Đo kiểm tra độc lập từng khối: Nguồn 3.3V/5V/12V ➔ MCU ➔ Gate Driver ➔ Cầu H Inverter. |
| **BR-011** | Có phanh tái sinh (Regenerative braking) | **SR-PWR-03** | Mạch công tắc xả phanh (Brake Chopper) và cổng điện trở hãm (Brake Resistor) | HW | T | **TC-PWR-03** | Mạch kích hoạt MOSFET xả phanh khi điện áp VBUS vượt ngưỡng đặt. |
| | | **SR-PWR-04** | Thuật toán giám sát VBUS và điều khiển xả phanh | SW | T, D | **TC-PWR-04** | Cho motor hãm đột ngột từ tốc độ cao; VBUS được ghim an toàn dưới ngưỡng bảo vệ. |
| **BR-012** | Giám sát nguồn điện (Power Monitoring) | **SR-PWR-05** | Điện áp đầu vào 12V ~ 60V, dòng tiêu thụ không tải < 1W | HW | T | **TC-PWR-05** | Cấp nguồn dải 12V - 60V; đo công suất tiêu thụ tĩnh ở chế độ chờ < 1W. |
| | | **SR-PWR-06** | Đo lường điện áp VBUS Min/Max/Avg và dòng tiêu thụ tổng | SW/HW | T | **TC-PWR-06** | Sai số đo VBUS < 1%, sai số đo dòng tổng < 2% so với đồng hồ chuẩn. |
| **BR-013** | Giám sát nhiệt độ & Ramping down dòng | **SR-SAF-01** | Cảm biến nhiệt NTC đo nhiệt MOSFET và cảm biến nhiệt độ MCU | HW/SW | T | **TC-SAF-01** | Đo chính xác nhiệt độ các khối với sai số < $\pm 3^\circ\text{C}$. |
| | | **SR-SAF-02** | Thuật toán Smooth Thermal Derating (giảm dòng mềm mại khi quá nhiệt) | SW | T, D | **TC-SAF-02** | Khi $T_\text{MOS} > 75^\circ\text{C}$, dòng tối đa giảm tuyến tính; khi đạt $85^\circ\text{C}$ ngắt an toàn, không giật cục. |
| **BR-014** | Quản lý lỗi & An toàn (Fault Management) | **SR-SAF-03** | Bảo vệ phần cứng: Quá dòng, Quá áp, Thấp áp, Kẹt trục (Stall), Ngược cực, Inrush | HW/SW | T | **TC-SAF-03** | Cấp điện áp ngược/vượt áp/sụt áp; mạch bảo vệ ngắt an toàn, không cháy linh kiện. |
| | | **SR-SAF-04** | PWM Shutdown tức thì khi xảy ra lỗi nghiêm trọng (Critical Fault) | HW/SW | T | **TC-SAF-04** | Kích hoạt sự cố quá dòng; chân ngắt khẩn cấp (Break Input) tắt 6 PWM trong thời gian < 1µs. |
| | | **SR-SAF-05** | Bảo vệ phóng tĩnh điện (ESD Protection) trên các cổng ngoại vi | HW | T | **TC-SAF-05** | Đạt tiêu chuẩn IEC 61000-4-2 (tiếp xúc $\ge$ 4kV, không khí $\ge$ 8kV) trên cổng CAN, USB, UART. |
| | | **SR-REL-01** | Watchdog timer, Brown-out reset, Tự phục hồi lỗi CAN Bus-off | SW/HW | T | **TC-REL-01** | Tạo sự cố treo CPU và chập CAN bus; MCU tự reset qua Watchdog và bus CAN tự khôi phục. |
| **BR-015** | Cập nhật Firmware (FW Update) | **SR-FWU-01** | Hỗ trợ nạp qua ST-Link và Bootloader nạp qua bus CAN-FD | SW/HW | D, T | **TC-FWU-01** | Nạp file nhị phân firmware qua CAN bus thành công trong thời gian < 30 giây. |
| | | **SR-FWU-02** | Kiểm tra toàn vẹn (CRC integrity verification) và Rollback khi lỗi | SW | T | **TC-FWU-02** | Cắt nguồn đột ngột khi đang nạp FW; thiết bị tự nhận diện lỗi CRC và hoàn nguyên về bản FW cũ. |
| **BR-016** | Quản lý cấu hình (Configuration Mgmt) | **SR-CFG-01** | Lưu cấu hình vào Flash có thuật toán Wear Leveling và CRC validation | SW | T | **TC-CFG-01** | Lưu cấu hình, reset nguồn 100 lần; dữ liệu giữ nguyên toàn vẹn, không bị hỏng Flash. |
| | | **SR-CFG-02** | Hỗ trợ Versioned Schema, Migration v1 ➔ v2 và Factory Reset | SW | T, D | **TC-CFG-02** | Nạp file cấu hình cũ; hàm migrate tự chuyển đổi schema; lệnh Factory Reset khôi phục mặc định. |
| **BR-017** | Truyền dữ liệu trực tiếp (Telemetry) | **SR-TEL-01** | Stream Position, Velocity, Current, Voltage, Temp ở tần số 1Hz ~ 1000Hz | SW | T | **TC-TEL-01** | Cấu hình tần số telemetry 1000Hz qua CAN-FD; kiểm tra độ đều đặn gói tin, tỷ lệ rơi gói < 0.01%. |
| **BR-018** | Chẩn đoán trạng thái (Diagnostics) | **SR-DIA-01** | Runtime Health Monitoring: Peak/Avg current, Stall count, CAN error count... | SW | T, D | **TC-DIA-01** | Gây ra các sự cố giả lập; bộ đếm count và các chỉ số chẩn đoán cập nhật chính xác. |
| | | **SR-DIA-02** | Cung cấp dữ liệu chẩn đoán qua Object Dictionary | SW | D | **TC-DIA-02** | Lệnh truy vấn từ xa qua CAN/UART đọc được toàn bộ thống kê sức khỏe hệ thống. |
| **BR-019** | Ghi nhật ký lỗi (Logging) | **SR-LOG-01** | Lưu 8 bản ghi lịch sử lỗi gần nhất vào Flash (Overcurrent, Overvoltage, Stall...) | SW | T, D | **TC-LOG-01** | Kích hoạt lần lượt các lỗi; đọc lại từ Flash đúng thứ tự thời gian và mã lỗi tương ứng. |
| **BR-020** | Giá thành linh kiện mục tiêu (Target BOM < 1.000.000 VNĐ) | **SR-BOM-01** | Tổng giá thành linh kiện Bill of Materials $\le 1.000.000\text{ VNĐ}$ (~$38 - $40 USD) | HW | A | **TC-BOM-01** | Tính toán tổng giá thành danh sách linh kiện BOM từ các nhà phân phối (LCSC/DigiKey) đạt $\le 1.000.000\text{ VNĐ}$. |
| **BR-021** | Đảm bảo tính sẵn sàng chuỗi cung ứng linh kiện | **SR-SC-01** | Ưu tiên MCU, MOSFET, Gate Driver phổ biến, có linh kiện thay thế tương đương | HW | A, I | **TC-SC-01** | Đánh giá mức tồn kho nhà phân phối $\ge 10.000$ pcs, tối thiểu 1 mã linh kiện pin-compatible thay thế. |

---

## 3. Danh mục Chi tiết các Test Case (Test Specification)

### 3.1. Nhóm Điều khiển Động cơ (Motor Control - TC-MOT)
- **TC-MOT-01**: **Current Loop Performance Test**
  - *Mục tiêu*: Xác minh tần số và độ ổn định của vòng lặp dòng FOC.
  - *Thiết bị*: Máy hiện sóng (Oscilloscope), Current Probe, DAC debug pin.
  - *Quy trình*: Xuất xung toggle tại ngắt ADC/FOC ra chân GPIO; đo thời gian thực thi (execution time) và chu kỳ lặp (jitter).
  - *Tiêu chuẩn*: Tần số $\ge 20\text{ kHz} \pm 0.5\%$, Execution time $\le 30\,\mu\text{s}$.
- **TC-MOT-02**: **Velocity Loop Step Response**
  - *Mục tiêu*: Đánh giá đáp ứng bước và khả năng giữ tốc độ dưới tải.
  - *Thiết bị*: Băng thử tải động cơ (Dynamometer / Brake).
  - *Quy trình*: Phát lệnh bậc thang tốc độ từ 0 lên 1000 RPM; sau đó áp tải 50% định mức.
  - *Tiêu chuẩn*: Độ vọt lố (Overshoot) $< 10\%$, thời gian ổn định $< 150\,\text{ms}$, sụt tốc khi có tải $< 5\%$.
- **TC-MOT-03**: **Position Loop Accuracy & Settling Test**
  - *Mục tiêu*: Đánh giá độ chính xác định vị bám góc.
  - *Thiết bị*: Cảm biến góc ngoài có độ chính xác cao (Calibrated Optical Encoder).
  - *Quy trình*: Điều khiển quay góc $90^\circ$, $180^\circ$, $360^\circ$ theo cấu hình chuyển động hình thang (Trapezoidal profile).
  - *Tiêu chuẩn*: Sai số tĩnh $\le 0.2^\circ$, thời gian định vị $\le 100\,\text{ms}$.
- **TC-MOT-04**: **Max Electrical Frequency Test**
  - *Mục tiêu*: Xác minh khả năng chạy ở tốc độ điện $3000\text{ Hz}$.
  - *Quy trình*: Cho động cơ tăng dần tốc độ tới khi $f_e = (RPM \times \text{Poles}) / 120 = 3000\text{ Hz}$.
  - *Tiêu chuẩn*: Động cơ không rung lắc bất thường, vòng lặp FOC không mất đồng bộ.

### 3.2. Nhóm Công suất & Nguồn (Power & Inverter - TC-PWR)
- **TC-PWR-01**: **Continuous Current & Thermal Test**
  - *Mục tiêu*: Xác nhận khả năng chịu tải dòng liên tục.
  - *Thiết bị*: Nguồn DC 48V, Tải giả điện tử, Camera nhiệt hồng ngoại (FLIR).
  - *Quy trình*: Cho driver phát dòng định mức liên tục trong 30 phút ở nhiệt độ phòng ($25^\circ\text{C}$).
  - *Tiêu chuẩn*: Nhiệt độ MOSFET $\le 85^\circ\text{C}$, không kích hoạt Over-temperature fault.
- **TC-PWR-02**: **Torque & Current Limiting Clamping Test**
  - *Mục tiêu*: Kiểm tra tính năng kẹp dòng bảo vệ động cơ.
  - *Quy trình*: Cài đặt giới hạn $I_q = 10\text{ A}$; ghì trục động cơ về 0 RPM.
  - *Tiêu chuẩn*: Dòng pha thực tế đo bằng kẹp dòng không vượt quá $10\text{ A} \pm 2\%$.
- **TC-PWR-03**: **Brake Chopper Hardware Test**
  - *Mục tiêu*: Xác minh mạch kích hoạt xả điện trở phanh.
  - *Thiết bị*: Điện trở xả phanh công suất, nguồn tạo áp biến thiên.
  - *Quy trình*: Nâng áp bus giả lập vượt ngưỡng kích hoạt (ví dụ: $58\text{V}$ trên hệ 48V); quan sát xung kích MOSFET phanh.
  - *Tiêu chuẩn*: Gate mở dứt khoát, điện trở phanh nhận dòng xả, ngắt khi áp giảm dưới ngưỡng hysteresis.
- **TC-PWR-04**: **Regenerative Braking Bus Voltage Clamp Test**
  - *Mục tiêu*: Kiểm nghiệm bảo vệ xả phanh tái sinh khi động cơ hãm đột ngột.
  - *Quy trình*: Động cơ mang bánh đà quán tính quay ở 3000 RPM, phát lệnh dừng khẩn cấp (Emergency Stop / Fast Decel).
  - *Tiêu chuẩn*: VBUS không tăng vọt quá ngưỡng giới hạn bảo vệ quá áp ($V_\text{max} \le 62\text{V}$).
- **TC-PWR-05**: **Standby Power Consumption Test**
  - *Mục tiêu*: Đo công suất tiêu thụ tĩnh khi không quay động cơ.
  - *Thiết bị*: Đồng hồ đo dòng chính xác (uA/mA meter) tại nguồn cấp 12V, 24V, 48V, 60V.
  - *Tiêu chuẩn*: Công suất tiêu thụ không tải $< 1.0\text{ W}$.

### 3.3. Nhóm Phần cứng & Đo lường (Hardware & Sensing - TC-HW / TC-SEN)
- **TC-HW-01**: **Current Sense Analog Signal Quality**
  - *Mục tiêu*: Kiểm tra độ sạch tín hiệu dòng pha từ shunt và op-amp.
  - *Thiết bị*: Oscilloscope băng thông $\ge 200\text{MHz}$, đầu đo vi sai (Differential probe).
  - *Tiêu chuẩn*: Độ gợn nhiễu (noise peak-to-peak) khi không có tải $< 20\text{mV}$, không có hiện tượng bão hòa tín hiệu.
- **TC-HW-02 & 03**: **Mechanical Fit & Connector Robustness**
  - *Mục tiêu*: Kiểm tra kích thước hình học và đầu nối.
  - *Tiêu chuẩn*: Lắp vừa khung cơ khí actuator, giắc cắm chịu được thử nghiệm rung lắc theo chuẩn robot.
- **TC-HW-04**: **Subsystem Bring-up Test**
  - *Mục tiêu*: Xác nhận các điểm đo Test Points và phân tầng nguồn.
  - *Tiêu chuẩn*: Áp tại TP_3V3 $\in [3.25\text{V}, 3.35\text{V}]$, TP_5V $\in [4.9\text{V}, 5.1\text{V}]$, TP_12V $\in [11.5\text{V}, 12.5\text{V}]$; gợn ripple $< 30\text{mV}$.
- **TC-SEN-01**: **Encoder SPI Communication & Noise Test**
  - *Mục tiêu*: Đảm bảo giao tiếp đọc góc chính xác ở tốc độ cao.
  - *Quy trình*: Chạy động cơ ở tốc độ tối đa; đọc liên tục 1,000,000 mẫu góc qua SPI.
  - *Tiêu chuẩn*: Tỷ lệ lỗi bit (CRC error / Parity error) = 0.

### 3.4. Nhóm Giao tiếp & Hệ thống (Communication & System - TC-COM / TC-FWU / TC-CFG / TC-TEL)
- **TC-COM-01**: **CAN-FD 5Mbps Multi-node Stress Test**
  - *Mục tiêu*: Kiểm tra độ tin cậy bus CAN-FD tốc độ cao với nhiều node.
  - *Thiết bị*: CAN-FD Analyzer (PCAN / CANable), bus tải với 4 node.
  - *Tiêu chuẩn*: Chạy tải bus $80\%$ trong 1 giờ; không có frame lỗi, không rơi vào trạng thái Bus-off.
- **TC-COM-02**: **Command Shell CLI Functional Test**
  - *Mục tiêu*: Xác minh các lệnh cấu hình, hiệu chuẩn và điều khiển qua Shell.
  - *Tiêu chuẩn*: Lệnh phản hồi đúng cú pháp, thời gian đáp ứng $< 10\text{ms}$.
- **TC-FWU-01 & 02**: **CAN-FD Bootloader & CRC Rollback Test**
  - *Mục tiêu*: Kiểm tra cập nhật phần mềm từ xa an toàn.
  - *Quy trình*: Nạp FW qua CAN-FD; cố tình ngắt nguồn ở 50% tiến trình; khởi động lại mạch.
  - *Tiêu chuẩn*: Mạch tự phát hiện CRC corrupt, kích hoạt Bootloader an toàn chờ nạp lại hoặc rollback FW cũ.
- **TC-CFG-01 & 02**: **Flash Wear-Leveling & Power-Cut Resilience**
  - *Mục tiêu*: Đảm bảo không hỏng dữ liệu Flash khi mất nguồn đột ngột.
  - *Quy trình*: Tạo vòng lặp ghi cấu hình và ngắt nguồn ngẫu nhiên 500 chu kỳ.
  - *Tiêu chuẩn*: Sau khi cấp lại nguồn, dữ liệu cấu hình luôn đọc lại hợp lệ (hoặc phục hồi bản backup gần nhất).
- **TC-TEL-01**: **High-speed Telemetry Streaming Test**
  - *Mục tiêu*: Đảm bảo tần số stream 1000Hz không gây nghẽn CPU.
  - *Tiêu chuẩn*: CPU load $< 70\%$, khoảng cách giữa 2 gói tin liên tiếp $= 1.0\text{ ms} \pm 5\%$.

### 3.5. Nhóm An toàn & Chẩn đoán (Safety & Diagnostics - TC-SAF / TC-DIA / TC-LOG)
- **TC-SAF-01 & 02**: **Thermal Derating & Over-temperature Protection**
  - *Mục tiêu*: Đánh giá thuật toán giảm dòng mượt mà khi nóng.
  - *Quy trình*: Dùng máy sấy nhiệt gia nhiệt cưỡng bức lên cụm MOSFET từ $60^\circ\text{C}$ lên $90^\circ\text{C}$.
  - *Tiêu chuẩn*: Từ $75^\circ\text{C}$ dòng giảm tuyến tính mượt; tới $85^\circ\text{C}$ kích hoạt shutdown an toàn, không giật động cơ.
- **TC-SAF-03**: **Hardware Fault Protection (Short-circuit, Overvoltage, Undervoltage)**
  - *Mục tiêu*: Kiểm tra bảo vệ chập pha, quá áp, sụt áp.
  - *Tiêu chuẩn*: Ngắt bảo vệ kịp thời, linh kiện nguyên vẹn.
- **TC-SAF-04**: **Ultra-fast PWM Hardware Shutdown Test**
  - *Mục tiêu*: Đo thời gian ngắt 6 xung PWM khi xảy ra lỗi ngắn mạch qua chân Break (BKIN).
  - *Thiết bị*: Máy hiện sóng đo đồng thời tín hiệu phát hiện lỗi và 6 chân Gate.
  - *Tiêu chuẩn*: Thời gian từ lúc tín hiệu lỗi kích hoạt đến khi cả 6 xung PWM tắt hoàn toàn $< 1.0\,\mu\text{s}$.
- **TC-LOG-01**: **Persistent Fault Logging Verification**
  - *Mục tiêu*: Kiểm tra lưu 8 lỗi lịch sử vào Flash.
  - *Tiêu chuẩn*: Ghi lại chính xác loại lỗi, giá trị điện áp/dòng/nhiệt độ tại thời điểm xảy ra lỗi.

### 3.6. Nhóm Thương mại & Chuỗi cung ứng (Commercial & Supply Chain - TC-BOM / TC-SC)
- **TC-BOM-01**: **Bill of Materials Cost Audit**
  - *Mục tiêu*: Xác minh tổng chi phí danh mục linh kiện không vượt ngân sách.
  - *Phương pháp*: Phân tích bảng báo giá BOM chi tiết (BOM quotation) tại số lượng 100 chiếc trên LCSC/DigiKey.
  - *Tiêu chuẩn*: Tổng giá trị linh kiện điện tử trên 1 bo mạch $\le 1.000.000\text{ VNĐ}$ (~$38 - $40 USD).
- **TC-SC-01**: **Component Supply Chain & Second-source Audit**
  - *Mục tiêu*: Đảm bảo khả năng mua linh kiện và không bị phụ thuộc vào linh kiện độc quyền hiếm hàng.
  - *Phương pháp*: Rà soát số lượng tồn kho và xác định tối thiểu 1 mã linh kiện thay thế tương thích (pin-compatible) cho MCU, Gate Driver, Shunt Amplifier và MOSFET.
  - *Tiêu chuẩn*: 100% linh kiện chính có hàng sẵn $\ge 10.000$ pcs tại thời điểm thiết kế.
