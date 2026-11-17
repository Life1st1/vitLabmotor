# Mô Hình Thực Thi Thời Gian Thực & Phân Bổ Ngoại Vi (Timing & Hardware Allocation Model)

> **Mục tiêu:** Đảm bảo độ chính xác điều khiển, jitter cực thấp (< 1%), thời gian trễ tối thiểu và không xảy ra xung đột tài nguyên giữa các tác vụ điều khiển động cơ trên vi điều khiển **STM32G431CBU6** (170 MHz).  
> **Tham chiếu tiêu chuẩn:** [SR-MOT-01](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/06_verification/traceability_matrix.md#L20) (FOC loop $\ge 20\text{ kHz}$, Execution time $\le 30\,\mu\text{s}$, Jitter $< 1\%$).

---

## 1. Phân Cấp Thời Gian Thực (Timing Hierarchy)

Hệ thống được chia thành 3 cấp độ thời gian độc lập:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ MỨC 1: FAST ISR (25 kHz / Chu kỳ 40 µs) - Ưu tiên cao nhất (Preempt)  │
│ Kích hoạt bởi: ADC1/ADC2 End-of-Conversion (Triggered by TIM1 TRGO)   │
│ Nhiệm vụ:                                                             │
│   1. Đọc dòng 3 pha (CurrentSensor::sample_isr)                       │
│   2. Đọc góc điện mới nhất từ AngleSensor qua SPI/DMA                 │
│   3. Biến đổi Clarke, Park (Sử dụng phần cứng CORDIC)                 │
│   4. Bộ điều khiển PI dòng điện Id, Iq (Clamp 60A)                    │
│   5. Biến đổi Inv-Park & SVPWM                                        │
│   6. Cập nhật thanh ghi TIM1 CCR1, CCR2, CCR3                         │
│ ➔ Thời gian thực thi mục tiêu: ≤ 12 - 18 µs (Dư > 50% CPU headroom)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ MỨC 2: CONTROL ISR (1 kHz / Chu kỳ 1 ms) - Ưu tiên trung bình         │
│ Kích hoạt bởi: TIM2 Update Interrupt                                  │
│ Nhiệm vụ:                                                             │
│   1. Đọc & ước lượng vận tốc góc (AngleSensor::update)                │
│   2. Vòng lặp điều khiển vận tốc (Velocity PID)                       │
│   3. Vòng lặp điều khiển vị trí (Position PID) + MotionProfile        │
│   4. Kiểm tra điện áp VBUS & điều khiển xả phanh (BrakeChopper)       │
│   5. Kiểm tra an toàn ngưỡng mềm (SafetyManager::check_thresholds)    │
│ ➔ Thời gian thực thi mục tiêu: ≤ 50 - 80 µs                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ MỨC 3: BACKGROUND TASKS (10 Hz - 100 Hz / Cooperative loop / RTOS)    │
│ Kích hoạt bởi: SysTick / Polling vòng lặp chính (Main loop)           │
│ Nhiệm vụ:                                                             │
│   1. Giám sát nhiệt độ MOSFET & MCU, Smooth Thermal Derating (10 Hz)  │
│   2. Truyền nhận gói tin CAN-FD (100 Hz - 1000 Hz)                    │
│   3. Đóng gói & gửi bản tin Telemetry                                 │
│   4. Giao diện dòng lệnh DebugShell (UART CDC)                        │
│   5. Ghi cấu hình tham số Flash (khi có yêu cầu)                      │
│ ➔ Chạy trong thời gian rảnh rỗi của CPU                               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Chi Tiết Chu Trình Đồng Bộ ADC & PWM (Center-Aligned Triggering)

Để triệt tiêu nhiễu chuyển mạch (switching noise) sinh ra khi MOSFET đóng/cắt, quá trình lấy mẫu dòng điện **phải diễn ra ở chính giữa vector 0 (Center-aligned)**:

```text
TIM1 Counter
   ▲
ARR│        /\                /\
   │       /  \              /  \
   │      /    \            /    \
  0└─────/──────\──────────/──────\────────► Thời gian
         ▲      ▲          ▲      ▲
        (A)    (B)        (A)    (B)

(A): Counter = 0 (Underflow) ➔ TIM1 sinh xung TRGO ➔ Trigger ADC1 & ADC2 cùng lấy mẫu.
     Lúc này tất cả các Low-side MOSFET đều ON (Vector V0 hoặc V7), dòng pha chạy êm qua Shunt.
(B): ADC chuyển đổi xong (EOC) ➔ Bắn ngắt ADC ISR ➔ Bắt đầu tính FOC.
     Tính toán xong, kết quả Duty Cycle nạp vào thanh ghi đệm CCRx (sẽ có hiệu lực ở đỉnh chu kỳ kế tiếp).
```

---

## 3. Phân Bổ Ngoại Vi Phần Cứng Trên STM32G431 (Hardware Resource Mapping)

| Ngoại vi STM32G4 | Cấu hình kỹ thuật | Chức năng trong hệ thống |
| :--- | :--- | :--- |
| **TIM1** | Advanced Timer, Center-Aligned Mode 1, Ch1/Ch2/Ch3 bổ sung (CHxN), Deadtime = 250ns | Phát 6 xung PWM điều khiển cầu H 3 pha. Kênh CH4 dùng trigger TRGO cho ADC. |
| **TIM1 BKIN** | Break Input 1 (Active High/Low) | Ngắt PWM phần cứng khẩn cấp trong $< 1\mu\text{s}$ khi IC Driver báo nFAULT hoặc phát hiện quá dòng phần cứng. |
| **TIM2** | 32-bit General Purpose Timer, tần số 1 kHz | Timer đồng hồ nhịp cho Control Loop (Vị trí, Vận tốc, Brake Chopper). |
| **TIM3/TIM4** | General Purpose Timer | Dùng phát xung PWM cho Brake Chopper hoặc đo thời gian vi giây microsecond timestamp. |
| **ADC1 & ADC2** | 12-bit Dual Simultaneous Mode, DMA / Injected | Đo đồng thời dòng pha U và pha V. Pha W được suy luận bằng thuật toán: $I_w = -(I_u + I_v)$ hoặc đo xen kẽ. |
| **ADC3** | Regular Mode, DMA Scan | Đo điện áp nguồn $V_{BUS}$, nhiệt độ MOSFET (NTC) và cảm biến nhiệt độ bên trong MCU. |
| **CORDIC** | Bộ tăng tốc toán học phần cứng (Hardware Accelerator) | Tính hàm $\sin(\theta), \cos(\theta)$ trong biến đổi Park/Inv-Park chỉ mất **4–8 chu kỳ xung nhịp CPU** (thay vì hàng trăm chu kỳ nếu tính bằng phần mềm). |
| **SPI1** | Master Mode, tốc độ $\ge 10\text{ MHz}$, CPOL=0, CPHA=1 | Giao tiếp tốc độ cao đọc góc Encoder MT6816 trong mỗi chu kỳ ngắt. |
| **SPI2** | Master Mode, tốc độ $2 - 5\text{ MHz}$ | Cấu hình thanh ghi và giám sát lỗi IC Gate Driver TI DRV8323RS. |
| **FDCAN1** | CAN 2.0B / CAN-FD (1Mbps Nominal, 5Mbps Data) | Giao tiếp điều khiển mạng robot tốc độ cao, nhận lệnh vận tốc/vị trí và trả Telemetry. |
| **USART1 / USB**| 115200 bps / USB CDC Virtual COM | Cổng giao tiếp DebugShell, gỡ lỗi và nạp tham số ban đầu. |
| **Flash** | Phân vùng sector cuối (Page 62-63) | Lưu trữ từ điển dữ liệu cấu hình động cơ và nhật ký lỗi. |

---

## 4. Bảng Phân Bổ Mức Ưu Tiên Ngắt (NVIC Priority Allocation)

> Quy tắc: Số Priority càng nhỏ thì mức độ ưu tiên càng cao (Priority 0 là cao nhất).

| Tên ngắt (Interrupt Handler) | Mức ưu tiên (Preemption Priority) | Nhận xét |
| :--- | :---: | :--- |
| **`TIM1_BRK_TIM15_IRQHandler`** | **0** | Ngắt khẩn cấp phần cứng, bảo vệ ngắt MOSFET lập tức. |
| **`ADC1_2_IRQHandler`** | **1** | Ngắt vòng lặp dòng FOC 25 kHz. Tuyệt đối không để bị block. |
| **`DMA1_Channel1_IRQHandler` (SPI1 RX)** | **2** | Đọc dữ liệu góc từ Encoder. |
| **`TIM2_IRQHandler`** | **3** | Vòng lặp điều khiển vận tốc & vị trí 1 kHz. |
| **`FDCAN1_IT0_IRQHandler`** | **4** | Nhận gói tin điều khiển từ bus CAN-FD. |
| **`USART1_IRQHandler`** | **5** | Nhận ký tự gõ phím từ Debug Shell. |
| **`SysTick_Handler`** | **6** | Định thì cơ bản cho hệ điều hành / task nền 10Hz. |
