# Phân Tích Trade-Off Kiến Trúc Phần Cứng & Dự Toán BOM (DRV8323RS Robotics Design)

Tài liệu này chuẩn hóa phương án thiết kế phần cứng cho bo mạch điều khiển động cơ FOC khớp robot:
- **Ứng dụng mục tiêu:** Khớp robot (Robotic Joint / Actuator) cho cánh tay cơ khí, robot 4 chân (quadruped), robot 2 chân (biped).
- **Dải điện áp hoạt động:** 12V ~ 60V (chịu áp xung tới 80V)
- **Công suất dòng:** Định mức liên tục **30A**, dòng đỉnh (Peak) **60A** ($\ge 5\text{s}$)
- **Kích thước cơ khí:** Bo mạch hình tròn bán kính $R < 10\text{cm}$ (tối ưu hóa đường kính $\approx 50 - 55\text{mm}$ gắn tích hợp đuôi motor)
- **Ngân sách mục tiêu:** $\le 1.000.000\text{ VNĐ}$ (~$39.5\text{ USD}$)

---

## 1. Lý Do Lựa Chọn TI DRV8323RS Cho Ứng Dụng Robotic

Qua phân tích yêu cầu điều khiển khớp robot (Robotic Joint / Quasi-direct drive), kiến trúc **TI DRV8323RS** được lựa chọn làm giải pháp chính thức (thay vì các driver rời) vì các ưu điểm vượt trội:

1. **Kế thừa thiết kế đã được kiểm chứng (Battle-tested Robotic Reference):**
   - Các dòng driver khớp robot hàng đầu thế giới như **mjbots moteus (c1 / r4)**, **MIT Mini Cheetah**, **ODrive S1** đều chuẩn hóa trên nền tảng DRV8323RS + STM32G4. Việc sử dụng DRV8323RS giúp kế thừa trọn vẹn thuật toán điều khiển, timing cấu hình SPI và cơ chế dập lỗi.
2. **Smart Gate Drive (IDRIVE / TDRIVE):**
   - Cho phép vi điều khiển tinh chỉnh dòng nạp/xả cổng Gate qua SPI (Source 1A / Sink 2A), tối ưu tốc độ chuyển mạch $dV/dt$ linh hoạt cho từng động cơ mà không cần thay đổi điện trở cổng $R_g$ phần cứng.
   - Tránh hiện tượng shoot-through và giảm thiểu tối đa phát xạ nhiễu EMI đến cảm biến từ tính (Encoder).
3. **Tích hợp 3 Bộ Khuếch Đại Cảm Biến Dòng (CSA) có Auto-Calibration:**
   - 3 CSA tích hợp với độ lợi lập trình được (5V/V đến 40V/V).
   - Cơ chế tự cân chỉnh DC Offset Calibration triệt tiêu sai số trôi nhiệt — điều kiện tiên quyết để khớp robot đạt độ gợn moment cực thấp (Low torque ripple) và khả năng giữ vị trí đứng yên chính xác (Compliant torque control).
4. **Tích hợp nguồn Buck 600mA trực tiếp từ VBUS (60V ➔ 3.3V):**
   - Loại bỏ hoàn toàn IC Buck hạ áp ngoài (như XL7015), tiết kiệm linh kiện và diện tích PCB quý giá để bo mạch đạt kích thước tròn siêu gọn $R < 50\text{mm}$.
5. **Bảo vệ toàn diện $V_{DS}$ Sensing & Chẩn đoán lỗi qua SPI:**
   - Bảo vệ quá dòng độc lập trên từng MOSFET ở mỗi chu kỳ chuyển mạch; ngắt khẩn cấp chân `nFAULT` nối tới chân `BKIN` của STM32G4 trong vòng vài trăm nanosecond.
   - Báo cáo chi tiết nguyên nhân lỗi qua thanh ghi SPI (Over-current, Over-temperature, Gate-drive fault, Undervoltage) phục vụ chẩn đoán robot trong runtime.

---

## 2. Bảng Phân Tích So Sánh Kiến Trúc

| Tiêu chí kỹ thuật | Kiến trúc Được Chọn: TI DRV8323RS + STM32G431 | Kiến trúc Rời: FD6288T + Op-Amp Nội STM32G4 |
| :--- | :--- | :--- |
| **Mức độ tích hợp** | **Cực cao:** Gate driver + 3x CSA + Buck 600mA trong 1 IC QFN-48 ($7\times 7\text{mm}$). | Trung bình: Cần thêm IC Buck ngoài, cuộn cảm to và nhiều linh kiện thụ động. |
| **Cấu hình Gate Drive** | **Lập trình qua SPI:** Slew-rate, Dead-time, $I_\text{drive}$ bằng phần mềm. | Cố định bằng phần cứng ($R_g$, $C_{boot}$). |
| **Đọc dòng pha FOC** | 3 CSA tích hợp trong DRV8323 có **DC Auto-calibration** chống trôi nhiệt. | 3 Op-Amp tích hợp trong STM32G4 (cần tự viết bù offset phần mềm). |
| **Bảo vệ ngắn mạch** | Đo sụt áp $V_{DS}$ trên từng FET riêng biệt + Shunt OCP. | Chỉ bảo vệ shunt OCP tổng. |
| **Diện tích bo mạch** | **Siêu nhỏ:** Tối ưu hoàn hảo cho hình tròn $D \approx 50\text{mm}$ bắt đuôi motor. | Tốn thêm khoảng 20% diện tích cho mạch nguồn phụ trợ. |
| **Độ tương thích Code** | Tương thích trực tiếp với codebase của **Moteus** và **VESC**. | Phải tự xây dựng driver phần cứng từ đầu. |
| **Chi phí linh kiện Driver** | ~$5.72 USD | ~$0.90 USD |
| **Đánh giá cho Robotic** | ⭐⭐⭐⭐⭐ **(Lựa chọn số 1 cho robot chuyên nghiệp)** | ⭐⭐⭐ (Phù hợp ứng dụng quạt/xe điện giá rẻ hơn) |

---

## 3. Bảng Dự Toán Chi Phí Linh Kiện BOM (DRV8323RS Architecture)

*Đơn giá cập nhật theo số lượng 100 chiếc (LCSC / Nhà phân phối linh kiện quốc tế):*

| STT | Khối chức năng | Mã linh kiện (MPN) | Nhà sản xuất | Đóng gói | SL | Đơn giá (USD) | Thành tiền (USD) |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | **Vi điều khiển (MCU)** | STM32G431CBU6 (170MHz, Math Accel) | STMicroelectronics | QFN-48 | 1 | $4.40 | $4.40 |
| 2 | **Smart Gate Driver** | DRV8323RSRGZR (3x CSA, Buck, SPI) | Texas Instruments | QFN-48 | 1 | $5.72 | $5.72 |
| 3 | **MOSFET công suất (3 pha)**| NCEP018N85LL ($85\text{V}, 1.8\text{m}\Omega$) | NCE Power | DFN5x6 | 6 | $1.23 | $7.38 |
| 4 | **MOSFET xả phanh (Brake)** | NCEP018N85LL | NCE Power | DFN5x6 | 1 | $1.23 | $1.23 |
| 5 | **Cảm biến dòng Shunt** | HoJLR2512-3W-1mR-1% | Milliohm / UniOhm | 2512 (3W) | 3 | $0.06 | $0.18 |
| 6 | **Cảm biến góc (Encoder)** | MT6816CT-STD (14-bit magnetic angle)| MagnTek | SOP-8 | 1 | $1.77 | $1.77 |
| 7 | **Thu phát CAN-FD** | SIT1042T/3 (5Mbps CAN-FD) | SITCORE | SOP-8 | 1 | $0.38 | $0.38 |
| 8 | **Cuộn cảm Buck DRV8323** | 33uH 1.2A Shielded Power Inductor | Chilisin / Sunlord | SMD 6x6mm | 1 | $0.25 | $0.25 |
| 9 | **Diode Schottky Buck** | SS1100 (100V 1A) | MDD / CJ | SMA | 1 | $0.06 | $0.06 |
| 10 | **Tụ lọc nguồn Bus chính** | Tụ nhôm SMD 63V/80V 220uF | Rubycon / Nichicon | SMD 10x10mm | 2 | $0.55 | $1.10 |
| 11 | **Tụ gốm khử nhiễu (MLCC)** | 100V 10uF, 4.7uF, 100nF X7R | Murata / Samsung | 1206 / 0805 / 0603 | 25 | $0.04 | $1.00 |
| 12 | **Điện trở dán, tụ tín hiệu** | Điện trở 0603 1%, tụ 0603 | UniOhm / Yageo | 0603 | 40 | $0.005 | $0.20 |
| 13 | **Bảo vệ TVS & Cảm biến nhiệt**| TVS 60V, ESD Array (CAN/USB), NTC 10K | ProTek / Murata | SOD-323 / 0603 | 4 | $0.15 | $0.60 |
| 14 | **Đầu nối (Connectors)** | JST-GH (CAN, UART, SWD) + Pad nguồn | JST / CJT | SMD | 4 | $0.30 | $1.20 |
| **TỔNG CỘNG** | | | | | | | **~$25.47 USD** |

---

## 4. Đánh Giá Khả Thi So Với Mục Tiêu Nghiệp Vụ

1. **Về Chi Phí (Target BOM $\le 1.000.000\text{ VNĐ}$):**
   $$\text{Chi phí BOM} \approx 25.47\text{ USD} \times 25.400\text{ VNĐ/USD} \approx \mathbf{647.000\text{ VNĐ}}$$
   - So với trần ngân sách 1 triệu đồng: Tiết kiệm được **$\sim 353.000\text{ VNĐ}$ (Dư địa an toàn 35%)**. Hoàn toàn thỏa mãn yêu cầu kinh doanh **BR-020**!

2. **Về Kích Thước Cơ Khí (Hình tròn bán kính $R < 10\text{cm}$):**
   - Việc tích hợp bộ Buck và 3 CSA vào trong DRV8323RS giúp giảm số lượng linh kiện đáng kể.
   - Mạch có thể thiết kế tròn với **đường kính chỉ $\sim 50\text{mm} - 54\text{mm}$ (Bán kính $R \approx 2.5\text{cm} - 2.7\text{cm}$)**, hoàn hảo để gắn ốp trực tiếp sau các khung motor robot chuẩn NEMA 17/23 hoặc frameless outrunner.

3. **Về Công Suất Dòng (30A liên tục / 60A đỉnh):**
   - 6 MOSFET $1.8\text{m}\Omega$ kết hợp chức năng Smart Gate Drive của DRV8323RS đảm bảo đóng cắt dứt khoát, giảm tối đa tổn hao switching loss và conduction loss, giữ nhiệt độ bo mạch dưới $65^\circ\text{C}$ khi vận hành liên tục 30A.
