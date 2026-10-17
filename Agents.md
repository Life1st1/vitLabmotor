# Project Map & Agents Overview

> **Dự án:** High-Performance FOC BLDC/PMSM Controller (Robotic Joint Actuator)  
> **Cấu hình phần cứng mục tiêu:** STM32G431 MCU + TI DRV8323RS Smart Gate Driver + 6x MOSFET (NCEP018N85LL / N-CH) + MT6816 14-bit Magnetic Encoder + CAN-FD SIT1042T  
> **Thời gian quét hệ thống:** 2026-10-10  

---

## 1. Bản Đồ Cấu Trúc Toàn Bộ Thư Mục (Workspace Tree)

```text
/home/cuong/Desktop/Foc_PCB/Brushless/
├── Agents.md                                # Bản đồ tổng thể dự án cho Agent và Kỹ sư
├── hw/                                      # Thư mục thiết kế phần cứng (KiCad)
│   └── DRV8323S/
│       ├── DRV8323S.kicad_pro              # KiCad 8.0 Project file
│       ├── DRV8323S.kicad_sch              # Nguyên lý mạch (Schematic)
│       ├── DRV8323S.kicad_pcb              # Bản vẽ mạch in (PCB Layout)
│       ├── DRV8323S.kicad_prl              # Thiết lập dự án cục bộ KiCad
│       ├── fp-lib-table                    # Bảng quản lý thư viện Footprint
│       ├── sym-lib-table                   # Bảng quản lý thư viện Ký hiệu Schematic
│       ├── fp-info-cache                   # Bộ đệm thông tin footprint KiCad
│       ├── element.txt                     # File ghi chú linh kiện tạm thời
│       └── DRV8323S-backups/               # Các bản sao lưu tự động của KiCad (.zip)
├── fw/                                      # Thư mục mã nguồn Firmware (Sẵn sàng khởi tạo STM32G4)
└── docs/                                    # Thư mục tài liệu kỹ thuật & kiến trúc hệ thống
    └── .priv/                               # Tài liệu thiết kế chi tiết & kiến thức dự án
        ├── main.md                          # Tổng quan trạng thái các hạng mục công việc
        ├── 00_httt/
        │   └── htt.md                       # Tổng quan hệ thống
        ├── 01_business/
        │   └── business_requirements.md     # Đặc tả 15 yêu cầu nghiệp vụ (BR-001 đến BR-015)
        ├── 02_system_req/
        │   └── sys_req.md                   # Yêu cầu hệ thống, truyền thông (CAN-FD, UART, USB, ROS2)
        ├── 03_system_arch/                  # Kiến trúc hệ thống tổng thể (đang phát triển)
        ├── 04_hardware/
        │   ├── 01_reference_design.md       # Phân tích các thiết kế tham khảo (Moteus, ODrive, Mini Cheetah)
        │   ├── 02_schematic_design_checklist.md  # Checklist nguyên lý mạch công suất & driver
        │   ├── 03_pcb_design_checklist.md        # Checklist layout PCB nhiều lớp, thoát nhiệt & EMI
        │   ├── 04_hw_testing.md             # Kế hoạch & quy trình đo kiểm phần cứng
        │   └── bom_and_tradeoff_analysis.md # Phân tích Trade-off kiến trúc & Bảng BOM chi tiết
        ├── 05_software/
        │   ├── FOC_core.md                  # Thiết kế lõi điều khiển FOC (Clarke, Park, SVPWM, PID)
        │   ├── FOC_algorithm.md             # Lý thuyết & thuật toán điều khiển động cơ
        │   ├── software_block_diagram.md    # Sơ đồ khối kiến trúc phần mềm
        │   ├── entry_struct.md              # Cấu trúc dữ liệu & biến trạng thái điều khiển
        │   ├── PG.md                        # Bộ sinh xung/quỹ đạo (Pulse Generation)
        │   └── web_configuration.md         # Yêu cầu công cụ cấu hình Web/GUI
        ├── 06_verification/
        │   └── traceability_matrix.md       # Ma trận truy vết yêu cầu (Traceability Matrix)
        └── 07_knowledge_gap/
            ├── Mosfet_deadtime.md           # Lý thuyết & tính toán Deadtime MOSFET
            ├── can_open.md                  # Giao thức CANopen / CAN-FD
            ├── ESD_Protection.md            # Giải pháp bảo vệ tĩnh điện ESD
            └── how_to_create_TraceabilityMatrix.md # Hướng dẫn xây dựng ma trận truy vết
```

---

## 2. Chi Tiết Các Phân Vùng Chức Năng

### 2.1. Phân Vùng Phần Cứng (`hw/DRV8323S`)
* **Công cụ thiết kế:** KiCad v8.0.
* **Tệp nguyên lý:** `DRV8323S.kicad_sch`
  * Đã có IC Gate Driver `U1` (DRV8323S).
  * Khối cầu H 3 pha gồm 6 MOSFET (`Q1` đến `Q6`).
  * Khối tụ lọc DC-Link, tụ Bootstrap, shunt sensing và các linh kiện thụ động.
* **Tệp mạch in:** `DRV8323S.kicad_pcb`
  * Bo mạch tròn mục tiêu gắn đuôi motor ($R < 50\text{mm}$).
  * Thiết kế 4-6 lớp chịu dòng liên tục 30A, đỉnh 60A.

### 2.2. Phân Vùng Mã Nguồn Firmware (`fw/`)
* Chuẩn bị phát triển phần mềm nhúng điều khiển FOC trên vi điều khiển **STM32G431CBU6** (170MHz Cortex-M4, CORDIC, FMAC).
* Sẽ triển khai các lớp: HAL, FOC Core, Communication (CAN-FD, UART Shell, ROS2 interface).

### 2.3. Phân Vùng Tài Liệu Kỹ Thuật (`docs/.priv/`)
* **Nghiệp vụ & Yêu cầu:**
  * `01_business/business_requirements.md`: 15 yêu cầu cốt lõi (BR-001: FOC torque ripple thấp, BR-002: 30A/60A, BR-005: Form factor tròn gắn đuôi động cơ, BR-011: Xả phanh tái sinh,...).
  * `02_system_req/sys_req.md`: Hỗ trợ CAN-FD 5Mbps, USB CDC, UART, RS485 Modbus, ROS2 node.
* **Thiết kế phần cứng & BOM:**
  * `bom_and_tradeoff_analysis.md`: Khẳng định lựa chọn TI DRV8323RS vượt trội so với giải pháp rời (Smart Gate Drive SPI, tích hợp 3 CSA có Auto-calibration, Buck 600mA).
  * `02_schematic_design_checklist.md` & `03_pcb_design_checklist.md`: Toàn bộ quy chuẩn về vòng lặp dòng Gate, bảo vệ Miller dV/dt, vias nhiệt dưới MOSFET và PAD tản nhiệt.
* **Lõi điều khiển & Kiểm thử:**
  * `05_software/FOC_core.md`: Thiết kế FOC với ngắt chu kỳ 20kHz - 40kHz, chuyển đổi góc rotor và điều khiển vector không gian SVPWM.
  * `06_verification/traceability_matrix.md`: Khung kiểm thử toàn diện từ yêu cầu nghiệp vụ đến phần cứng và phần mềm.

---

## 3. Bản Đồ Linh Kiện Chính (Bill of Materials - BOM Core)

| Linh Kiện | Mã Hiệu (MPN) | Đóng Gói | Vai Trò Trong Mạch |
| :--- | :--- | :---: | :--- |
| **MCU** | STM32G431CBU6 | QFN-48 | Vi điều khiển trung tâm, tính toán FOC, bộ tăng tốc toán học |
| **Gate Driver** | DRV8323RSRGZR | QFN-48 | Driver 3 pha thông minh, 3 Op-Amp dòng (CSA), Buck 600mA |
| **Power MOSFETs** | NCEP018N85LL | DFN5x6 | 6x Cầu H 3 pha ($85\text{V}, 1.8\text{m}\Omega$) + 1x MOSFET phanh xả |
| **Shunt Resistor**| HoJLR2512-3W-1mR | 2512 | 3x Điện trở shunt $1\text{m}\Omega$ đo dòng từng pha |
| **Encoder** | MT6816CT-STD | SOP-8 | Cảm biến góc từ tính 14-bit qua bus SPI |
| **CAN Transceiver**| SIT1042T/3 | SOP-8 | Thu phát CAN-FD tốc độ cao 5Mbps |
