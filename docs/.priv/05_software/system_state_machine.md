# Thiết Kế Máy Trạng Thái Hệ Thống (System State Machine)

> **Tài liệu tham chiếu:** [class_specifications.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/05_software/class_specifications.md), [software_development_plan.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/05_software/software_development_plan.md), [traceability_matrix.md](file:///home/cuong/Desktop/Foc_PCB/Brushless/docs/.priv/06_verification/traceability_matrix.md).  
> **Module thực thi:** Class `Actuator` kết hợp với `SafetyManager`.

---

## 1. Sơ Đồ Chuyển Trạng Thái (State Transition Diagram)

Hệ thống hoạt động dựa trên máy trạng thái hữu hạn (FSM) với nguyên tắc **An toàn là trên hết (Safety-First)**: Mọi lỗi nghiêm trọng đều đưa hệ thống lập tức về trạng thái an toàn `FAULT` và ngắt phần cứng PWM.

```text
       ┌──────────────┐
       │     BOOT     │ ──(Khởi tạo HW thất bại)──────────────┐
       └──────┬───────┘                                       │
              │ (Khởi tạo HW thành công)                      │
              ▼                                               │
       ┌──────────────┐                                       │
┌────► │ CALIBRATING  │ ──(Lỗi đo dòng / lệch encoder)───────┤
│      └──────┬───────┘                                       │
│             │ (Cân chỉnh R, L, Offset thành công)           │
│             ▼                                               │
│      ┌──────────────┐                                       │
│      │     IDLE     │ ◄──(Lệnh Disable / Đạt đích dừng)────┐│
│      └──────┬───────┘                                      ││
│             │                                              ││
│   (Lệnh Arm & Enable)                                      ││
│             ▼                                              ││
│      ┌──────────────┐                                      ││
│      │ CLOSED_LOOP  │                                      ││
│      │  (Torque /   │ ──(Lỗi nhẹ: Quá nhiệt, lệch góc)──┐  ││
│      │ Speed / Pos) │                                   │  ││
│      └──────────────┘                                   │  ││
│                                                         │  ││
│                                                         ▼  ▼│
│                                                      ┌───────────┐
│ (Lệnh Re-calib)                                      │ ERROR_STOP│ (Giảm tốc an toàn)
│                                                      └─────┬─────┘
│                                                            │ (Dừng hẳn hoặc quá thời gian)
│                                                            ▼
│                                                      ┌───────────┐
│                                                      │   FAULT   │ ◄(Quá dòng/áp/Break-in)
│                                                      └─────┬─────┘
└───────────(Gửi lệnh Reset Fault & Kiểm tra an toàn)────────┘
```

---

## 2. Định Nghĩa Chi Tiết Các Trạng Thái (State Specifications)

| Mã Trạng Thái | Tên Trạng Thái | Trạng Thái Cầu H Inverter | Mô Tả & Điều Kiện Hoạt Động |
| :--- | :--- | :---: | :--- |
| **0x00** | **`STATE_BOOT`** | **DISABLED** (Hi-Z) | Trạng thái ngay sau Reset nguồn. Cấu hình Clocks (170MHz), GPIO, ngoại vi; đọc cấu hình Flash; kiểm tra nFAULT từ DRV8323RS. |
| **0x01** | **`STATE_CALIBRATING`** | **ENABLED** (Điện áp thấp) | Tự động đo điện trở pha $R$, tự cảm $L$, đo bù offset 0 của bộ đo dòng `CurrentSensor` và căn chỉnh góc 0 điện của `AngleSensor`. |
| **0x02** | **`STATE_IDLE`** | **DISABLED** (Hi-Z) | Sẵn sàng nhận lệnh. Cầu H thả nổi, motor quay tự do. Các sensor vẫn đọc liên tục để giám sát $V_{BUS}$ và nhiệt độ. |
| **0x03** | **`STATE_CLOSED_LOOP`** | **ENABLED** (FOC Active) | Động cơ được kích hoạt điều khiển kín (Closed-loop): Mô-men xoắn (Torque/Current), Tốc độ (Velocity), hoặc Vị trí (Position). |
| **0x04** | **`STATE_ERROR_STOP`** | **ENABLED / BRAKING** | Xảy ra khi có lỗi cấp 2 (Non-critical): Quá nhiệt nhẹ, lệch góc ngoài ngưỡng cho phép. Động cơ hãm tốc độ chủ động về 0 rồi mới ngắt cầu H. |
| **0x05** | **`STATE_FAULT`** | **DISABLED** (Latching) | Xảy ra khi có lỗi nghiêm trọng (Critical): Quá dòng, quá áp, nFAULT từ driver. PWM bị ngắt cứng tức thì ($< 1\mu\text{s}$). Chốt trạng thái này cho tới khi nhận lệnh `CLEAR_FAULT`. |

---

## 3. Ma Trận Chuyển Trạng Thái (State Transition Table)

| Trạng thái hiện tại | Sự kiện / Điều kiện kích hoạt (Event / Condition) | Hành động thực thi (Action) | Trạng thái tiếp theo |
| :--- | :--- | :--- | :--- |
| `BOOT` | Khởi tạo ngoại vi hoàn tất & Tham số hợp lệ | Nạp tham số Flash, chuyển sang cân chỉnh | `CALIBRATING` |
| `BOOT` | Lỗi phần cứng (SPI lỗi, DRV8323 không phản hồi) | Báo mã lỗi, khóa PWM | `FAULT` |
| `CALIBRATING` | Quy trình đo offset và góc 0 thành công | Lưu offset vào RAM, tắt cầu H | `IDLE` |
| `CALIBRATING` | Sai số cân chỉnh vượt ngưỡng (Đứt dây pha, kẹt trục) | Ghi log `CALIBRATION_FAILED` | `FAULT` |
| `IDLE` | Nhận lệnh `CMD_ENABLE` qua CAN-FD hoặc UART | Xóa tích phân PID, kích hoạt cầu H | `CLOSED_LOOP` |
| `IDLE` | Nhận lệnh `CMD_START_CALIBRATION` | Chuẩn bị đo đạc lại động cơ | `CALIBRATING` |
| `CLOSED_LOOP` | Nhận lệnh `CMD_DISABLE` | Tắt PWM cầu H, reset target | `IDLE` |
| `CLOSED_LOOP` | Cảnh báo quá nhiệt ($T > 85^\circ\text{C}$) hoặc mất bám góc | Kích hoạt giảm tốc có kiểm soát | `ERROR_STOP` |
| `CLOSED_LOOP` | Phát hiện lỗi khẩn cấp (Quá dòng, quá áp, nFAULT) | **Break-in PWM lập tức**, chốt cờ lỗi | `FAULT` |
| `ERROR_STOP` | Vận tốc motor về 0 hoặc hết thời gian timeout (500ms) | Tắt PWM hoàn toàn | `FAULT` |
| `FAULT` | Nhận lệnh `CMD_CLEAR_FAULT` VÀ không còn điều kiện lỗi | Đọc lại cảm biến, kiểm tra an toàn | `IDLE` |

---

## 4. Cơ Chế Khóa Liên Động An Toàn (Safety Interlocks)

Để tránh hư hỏng phần cứng MOSFET và động cơ, phần mềm bắt buộc phải tuân thủ 3 quy tắc liên động:

1. **Khóa góc điện (Angle Valid Interlock):**
   * Tuyệt đối không cho phép chuyển sang `CLOSED_LOOP` nếu cờ `measurement.is_valid` của `AngleSensor` bằng `false` hoặc chưa từng chạy qua cân chỉnh góc 0 điện.
2. **Khóa quá dòng phần cứng (Hardware PWM Break Interlock):**
   * Sử dụng chân `TIM1_BKIN` liên kết trực tiếp với ngõ ra nFAULT của DRV8323RS hoặc bộ so sánh nội Analog Comparator (COMP). Khi tín hiệu kích hoạt, các cổng ra PWM kênh U, V, W sẽ bị kéo về trạng thái ngắt độc lập với CPU.
3. **Khóa chống tái kích hoạt tự động (Latching Fault Interlock):**
   * Sau khi rơi vào `STATE_FAULT`, hệ thống **không bao giờ tự động quay lại chạy** nếu người vận hành hoặc Robot Controller chưa gửi bản tin xóa lỗi (`CMD_CLEAR_FAULT`) rõ ràng.
