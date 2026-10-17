# 2.Communication
- Local shell
- CAN-FD communication:
    + CAN Arbitration: 1Mbps
    + CAN-FD Data Rate: 5Mbps
    + Support software configurable node IDs
    + Support multi-node networks with up to 64 devices
- UART communication:
    + 115200 bps
- USB CDC(no HID) communication:
    + USB 2.0 Full Speed
    + 115200 bps
- RS485 communication:
    + Modbus RTU
    + 115200
- ROS2 support:
    + Have note run on host to support ROS2

# 3.Security Requirements
- Secure Boot # Maynot implement
- Integrity ensurance
- Firmware Authentication # Maynot implement
- Bootloader write protection # Maynot implement
- Debug port lock # Maynot implement

# 4.Diagnostic Requirements
- The driver shall record fault history
    + Wear leveling
    + 8 records of fault history:
        * OVERCURRENT
        * OVERVOLTAGE
        * UNDERVOLTAGE
        * OVERTEMPERATURE
        * ENCODER ERROR
        * CAN BUS OFF
        * DRV FAULT
        * WATCHDOG RESET

- The driver shall support health monitoring in runtime
    + Peak Current
    + Average Current
    + Motor Stall Count
    + CAN Bus Off Count
    + Encoder Error Count
    + CAN CRC Error Count
    + MOS Temperature
    + MCU Temperature
    + Highest Temperature Reached
    + VBUS Current
    + VBUS Average
    + VBUS Min
    + VBUS Max
    + OverCurrent Coun
- The driver shall expose diagnostic data through the object dictionary

# 5.FW Update Requirements
- Stlink
- CAN Firmware Update
- Firmware integrity verification
- Rollback support

# 6.Persistence Requirements
- Store configuration in Flash
    + Wear leveling
- Restore after reboot
- Factory reset support
- Versioned configuration schema
    ```cpp
    struct ConfigHeader
    {
        uint16_t version;
        uint16_t length;
        uint32_t crc;
    };


    if(config.version == 1)
    {
        migrate_v1_to_v2();
    }
    ```

# 7.Environmental Requirements
- Operating temperature: -20°C ~ +85°C
- Storage Temperature: -40°C ~ +105°C

# 8.Power Requirements
- Input Voltage: 12V ~ 60V
- Continuous Phase Current: 30A (với tản nhiệt cơ bản)
- Peak Phase Current: 60A (thời gian ngắn >= 5s)
- Consumption: < 1W without motor load
- Reverse Polarity Protection: Required
- Inrush Protection: Required
- Regenerative Braking Handling     #HW
- Inrush Current Limiting        
- Brake Resistor Support           #HW
- Input Voltage Monitoring
- Current Limiting (Configurable, kẹp dòng tối đa 60A)
- Torque Limiting

# 9.Motor Control
- Support FOC control.
- Current loop frequency > 20kHz
- Velocity loop frequency: 1kHz
- Position loop frequency: 1kHz
- Electrical frequency: 3000Hz.
- Control loop jitter < 1%

# 10.Data Model Requirements
- All configuration data shall be exposed through a unified object dictionary
- All communication interfaces shall access the same object dictionary
- Every object shall define:
    + Path
    + Type
    + Unit
    + Access Rights
    + Default Value

# 11.Telemetry
- Position
- Velocity
- Current
- Voltage
- Temperature

The driver shall publish telemetry at configurable frequencies.
Supported telemetry frequency:
1Hz ~ 1000Hz.


# 12.Reliability
- Automatic CAN bus-off recovery
- Watchdog support
- Brown-out recovery
- Power loss tolerant configuration storage
- MTBF > 10000 hours

# 13.Safety
- Overcurrent protection
- Overvoltage protection
- Undervoltage protection
- Overtemperature protection
- Motor Stall Detection
- Emergency Stop Support
- PWM Shutdown on Critical Fault
- ESD Protection

# 14.Mechanical & Commercial Requirements
- Form Factor: Circular PCB, Radius < 10cm (target R <= 25 ~ 45mm gắn tích hợp đuôi motor)
- Target BOM Cost: <= 1,000,000 VND (~$38 - $40 USD)
- Supply Chain: Ưu tiên linh kiện thông dụng (LCSC/DigiKey stock >= 10,000 pcs) có second-source thay thế.