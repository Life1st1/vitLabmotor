# Reference Design: Kiến Trúc FOC Driver Dựa Trên TI DRV8323RS Cho Robotic Joint

Tài liệu này tổng hợp thiết kế tham chiếu phần cứng tiêu chuẩn công nghiệp dựa trên chip **TI DRV8323RS**, học hỏi từ các thiết kế robotic controller thành công nhất thế giới: **mjbots moteus (r4.x / c1)** và **TI BOOSTXL-DRV8323RS**.

---

## 1. Nguồn Tham Chiếu Chính (Reference Sources)
1. **mjbots moteus (hw/c1 & r4.x):**
   - Repository: [https://github.com/mjbots/moteus/tree/main/hw/c1](https://github.com/mjbots/moteus/tree/main/hw/c1)
   - Đặc điểm: Thiết kế hình tròn nhỏ gọn chuyên dụng cho cánh tay robot, quadruped (chó robot) và biped. Dùng STM32G4 + DRV8323R + Cảm biến từ tính AS5047P / MT6835.
2. **Texas Instruments BOOSTXL-DRV8323RS Reference Design:**
   - Link: [https://www.ti.com/tool/BOOSTXL-DRV8323RS](https://www.ti.com/tool/BOOSTXL-DRV8323RS)
   - Đặc điểm: Mạch mẫu chuẩn từ Texas Instruments, tối ưu layout công suất và lọc nhiễu vi sai cho Current Sense Amplifier (CSA).

---

## 2. Vì Sao DRV8323RS Là Tiêu Chuẩn Vàng Cho Robotic Actuator?

Đối với các ứng dụng robot (khớp chân, khớp khuỷu, cơ cấu chấp hành quasidirect-drive):
1. **Smart Gate Drive (IDRIVE / TDRIVE):**
   - Điều khiển dòng nạp/xả cổng Gate (Source 1A / Sink 2A) hoàn toàn bằng phần mềm qua SPI.
   - Loại bỏ điện trở Gate ($R_g$) và diode xả ngoài, tiết kiệm diện tích PCB đáng kể.
   - Điều chỉnh tốc độ chuyển mạch ($dV/dt$) theo thời gian thực để dập tắt dao động ký sinh (ringing) và nhiễu EMI mà không bị quá nhiệt MOSFET.
2. **3 Bộ Khuếch Đại Cảm Biến Dòng (Current Sense Amplifiers - CSA) Tích Hợp:**
   - Hệ số khuếch đại lập trình được qua SPI: 5V/V, 10V/V, 20V/V, 40V/V.
   - Tính năng tự động hiệu chuẩn độ lệch DC (DC offset calibration) giúp triệt tiêu trôi điểm 0 theo nhiệt độ — yếu tố sống còn để robot giữ vị trí đứng yên hoặc điều khiển lực tĩnh (zero torque ripple / compliant control).
3. **Bộ Nguồn Buck Hạ Áp 600mA Tích Hợp (Integrated Buck Regulator):**
   - Hạ trực tiếp từ điện áp nguồn chính $V_\text{bus}$ (12V ~ 60V) xuống $3.3\text{V}$ (hoặc $5\text{V}$) nuôi thẳng vi điều khiển STM32G4 và cảm biến góc.
   - **Loại bỏ hoàn toàn IC Buck rời** (như XL7015), giải phóng diện tích quý giá trên bo mạch tròn $R < 10\text{cm}$.
4. **Bảo Vệ Ngắn Mạch Độc Lập Cho Từng MOSFET ($V_{DS}$ Sensing per FET):**
   - Đo sụt áp $V_{DS}$ trên cả 6 MOSFET độc lập ở từng chu kỳ đóng cắt.
   - Ngắt phần cứng tức thời trong vòng vài trăm nanosecond khi có chạm chập hoặc kẹt cơ cấu, kích hoạt chân `nFAULT` kéo ngắt khẩn cấp chân `BKIN` của STM32G4.
5. **Chẩn Đoán Trực Tiếp Qua Thanh Ghi SPI (SPI Diagnostics):**
   - Báo cáo chính xác lỗi: Quá nhiệt cảnh báo (OTW), Quá nhiệt ngắt (OTSD), Sụt áp nguồn (UVLO), Lỗi Gate Driver (GDF), Quá dòng VDS trên từng FET cụ thể.
   - Đáp ứng trực tiếp yêu cầu nghiệp vụ BR-014, BR-018 và BR-019.

---

## 3. Sơ Đồ Khối Hệ Thống (System Block Diagram)

```
       +-----------------------------------------------------------+
       |                  VBUS (12V - 60V Power)                   |
       +--------------+-----------------------------+--------------+
                      |                             |
                      v                             v
           +--------------------+         +--------------------+
           |  DRV8323RS Buck    |         |  3-Phase Inverter  |
           |  (600mA Regulator) |         |  6x NCEP018N85LL   |
           +----------+---------+         +----+----------+----+
                      | 3.3V Power             |          |
                      v                        | Phase    | Low-side
+------------------------------------+         | Output   | Current
|            STM32G431               |         | (U,V,W)  | (Shunts)
|       (MCU Cortex-M4 170MHz)       |         |          |
|                                    |         v          v
| - 6x Advanced PWM (TIM1) ----------> DRV8323RS Driver -> Phase Sense
| - Fast ADC (Phase Currents) <------- 3x CSA Outputs <---+
| - SPI1 (DRV8323 Config/Fault) <----> SPI Control
| - SPI2 (MT6816 Angle Encoder) <----> MT6816 Magnetic Sensor (Motor shaft)
| - FDCAN (1M/5M Robot Bus) <--------> SIT1042T Transceiver <--> CAN-FD Bus
| - TIM_CH (Brake Chopper) ----------> Brake Gate Drive ---> Brake Resistor
+------------------------------------+
```

---

## 4. Bố Trí Phân Chân Đề Xuất (Pin Mapping Strategy: STM32G431CBU6)

| Ngoại vi STM32G4 | Chân MCU | Chức năng kết nối |
| :--- | :--- | :--- |
| **TIM1_CH1 / CH1N** | PA8 / PB13 | PWM Pha A: High-side / Low-side (INHA, INLA vào DRV8323) |
| **TIM1_CH2 / CH2N** | PA9 / PB14 | PWM Pha B: High-side / Low-side (INHB, INLB vào DRV8323) |
| **TIM1_CH3 / CH3N** | PA10 / PB15 | PWM Pha C: High-side / Low-side (INHC, INLC vào DRV8323) |
| **TIM1_BKIN** | PB12 | Ngắt khẩn cấp PWM nhận từ chân `nFAULT` của DRV8323 |
| **ADC1_IN1** | PA0 | Đọc điện áp dòng pha A (`SO1` từ DRV8323 CSA) |
| **ADC1_IN2** | PA1 | Đọc điện áp dòng pha B (`SO2` từ DRV8323 CSA) |
| **ADC2_IN1** | PA4 | Đọc điện áp dòng pha C (`SO3` từ DRV8323 CSA) |
| **ADC1_IN3** | PA2 | Giám sát điện áp nguồn chính $V_\text{bus}$ (Cầu phân áp trở) |
| **ADC1_IN4** | PA3 | Giám sát cảm biến nhiệt độ NTC (gần cụm MOSFET) |
| **SPI1_SCK/MISO/MOSI**| PB3/PB4/PB5| Cấu hình và chẩn đoán DRV8323RS qua SPI |
| **GPIO Output** | PB0 | `nSCS` (Chip Select DRV8323) |
| **GPIO Output** | PB1 | `ENABLE` (Bật/tắt DRV8323) |
| **SPI2_SCK/MISO/MOSI**| PB10/PC2/PC3| Đọc cảm biến góc từ tính MT6816 / AS5047P |
| **GPIO Output** | PC4 | `CS_ENC` (Chip Select Encoder) |
| **FDCAN1_TX / RX** | PB9 / PB8 | Giao tiếp CAN-FD với bộ điều khiển robot chính |
| **TIM2_CH1 (PWM)** | PA5 | Điều khiển MOSFET xả phanh tái sinh (Brake Chopper) |
| **USART1_TX / RX** | PA15 / PB7 | Debug CLI / Shell (115200 bps) |
| **SWDIO / SWCLK** | PA13 / PA14 | Nạp chương trình và Debug qua ST-Link |