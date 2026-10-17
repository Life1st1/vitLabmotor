Thiết kế core điều khiển FOC cho STM32G474 + Zephyr theo hướng top-down:
1. bắt đầu từ hành vi hệ thống
2. phân rã thành các vòng điều khiển
3. kiến trúc thời gian thực
4. module phần mềm, rồi mới xuống ISR và API. 

Thiết kế ưu tiên deterministic, dễ kiểm thử, dễ thay encoder/current-sense, và không để Zephyr scheduler nằm trên đường critical của current loop.


# Mục tiêu cấp hệ thống
## Core điều khiển cần thực hiện
```
Đầu vào:
- Lệnh position / velocity / torque
- Dòng pha
- Điện áp DC bus
- Góc rotor
- Tốc độ rotor
- Trạng thái driver và fault

Đầu ra:
- Duty PWM pha U/V/W
- Trạng thái motor
- Fault code
- Telemetry
```

## Các yêu cầu chính
```
- Current loop chạy cố định 40 kHz, chu kỳ 25 µs.
- ADC sampling phải khóa pha với PWM.
- Mất deadline phải được phát hiện.
- Fault phần cứng phải tắt PWM độc lập với scheduler.
- Current loop không phụ thuộc k_thread, k_timer, semaphore.
- Velocity/position loop chạy chậm hơn và có thể ở thread.
- Thuật toán điều khiển không phụ thuộc trực tiếp thanh ghi STM32.
- Có thể unit test các phép biến đổi và PI trên host.
```

# Kiến trúc điều khiển phân tầng
```
Application / Communication
 CAN-FD | USB | RS485 | Shell
              |
              v
       Command Manager
 position / velocity / torque command
              |
              v
       Position Controller
           100-500 Hz
              |
              v
       Velocity Controller
             1 kHz
              |
              v
       Current Reference
          Id_ref, Iq_ref
              |
              v
       Current Controller
            40 kHz
              |
              v
     Voltage Reference Vd, Vq
              |
              v
         SVPWM / PWM
              |
              v
           Inverter
              |
              v
             Motor
```

## Tần số ban đầu đề xuất
```
#define FOC_CURRENT_LOOP_HZ   40000U
#define FOC_VELOCITY_LOOP_HZ   1000U
#define FOC_POSITION_LOOP_HZ    200U
#define FOC_SERVICE_LOOP_HZ      100U
```

# Kiến trúc thời gian thực
## Đường critical
```
TIM1 center-aligned PWM
        |
        +--> CH1/2/3: PWM U/V/W
        |
        +--> Compare event: trigger ADC injected conversion
                              |
                              v
                      ADC conversion complete
                              |
                              v
                           FOC ISR
                              |
                    +---------+---------+
                    |                   |
                 Read ADC          Read angle
                    |                   |
                    +---------+---------+
                              |
                     Current control
                              |
                        Calculate duty
                              |
                     Write TIM1 CCR shadow
                              |
                     Apply next PWM cycle
```
Dùng timer trigger ADC giúp thời điểm conversion cố định so với PWM, không phụ thuộc software latency. STM32 timer có khả năng tạo trigger cho ADC và các peripheral khác.

## ISR hay IRQ tách riêng?
Giai đoạn đầu, đơn giản và dễ debug, không mượn IRQ như ODrive ngay
- ADC timing đúng
- FOC hoàn thành trước deadline
- Không có overrun
- ISR latency chấp nhận được

# Phân rã module
```
servo_drive/
│
├── app/
│   │
│   ├── main.c
│   ├── startup.c
│   │
│   ├── motor_service.c
│   ├── command_manager.c
│   ├── service_manager.c
│   │
│   └── system_controller.c
│
├── core/
│   │
│   ├── control/
│   │   │
│   │   ├── foc_core.c
│   │   ├── current_controller.c
│   │   ├── velocity_controller.c
│   │   ├── position_controller.c
│   │   │
│   │   ├── transforms.c
│   │   ├── modulation.c
│   │   ├── field_weakening.c
│   │   │
│   │   ├── current_limiter.c
│   │   ├── torque_limiter.c
│   │   └── voltage_limiter.c
│   │
│   ├── estimation/
│   │   │
│   │   ├── velocity_estimator.c
│   │   ├── rotor_sensor.c
│   │   ├── observer.c
│   │   └── phase_reconstruction.c
│   │
│   ├── runtime/
│   │   │
│   │   ├── foc_scheduler.c
│   │   ├── timing_monitor.c
│   │   ├── cycle_profiler.c
│   │   └── event_dispatcher.c
│   │
│   ├── safety/
│   │   │
│   │   ├── fault_manager.c
│   │   ├── protection_manager.c
│   │   ├── overcurrent.c
│   │   ├── overvoltage.c
│   │   ├── undervoltage.c
│   │   └── thermal_protection.c
│   │
│   └── state_machine/
│       │
│       ├── motor_state_machine.c
│       ├── operational_modes.c
│       └── mode_manager.c
│
├── services/
│   │
│   ├── calibration/
│   │   │
│   │   ├── current_offset_cal.c
│   │   ├── encoder_calibration.c
│   │   ├── motor_parameter_id.c
│   │   └── phase_order_calibration.c
│   │
│   ├── monitoring/
│   │   │
│   │   ├── power_monitor.c
│   │   ├── current_monitor.c
│   │   ├── temperature_monitor.c
│   │   ├── bus_voltage_monitor.c
│   │   └── statistics_monitor.c
│   │
│   ├── telemetry/
│   │   │
│   │   ├── telemetry_stream.c
│   │   ├── telemetry_snapshot.c
│   │   └── telemetry_formatter.c
│   │
│   ├── diagnostics/
│   │   │
│   │   ├── self_test.c
│   │   ├── health_check.c
│   │   ├── runtime_diagnostics.c
│   │   └── diagnostics_service.c
│   │
│   └── logging/
│       │
│       ├── event_logger.c
│       ├── fault_logger.c
│       ├── trace_logger.c
│       └── log_manager.c
│
├── communication/
│   │
│   ├── canfd/
│   │   │
│   │   ├── can_transport.c
│   │   ├── can_dispatcher.c
│   │   └── can_protocol.c
│   │
│   ├── uart/
│   │   │
│   │   ├── uart_transport.c
│   │   └── uart_protocol.c
│   │
│   ├── usb/
│   │   │
│   │   ├── usb_transport.c
│   │   └── usb_protocol.c
│   │
│   ├── protocol/
│   │   │
│   │   ├── command_parser.c
│   │   ├── packet_encoder.c
│   │   ├── packet_decoder.c
│   │   └── crc.c
│   │
│   └── object_dictionary/
│       │
│       ├── object_dictionary.c
│       ├── parameter_access.c
│       └── endpoint_table.c
│
├── storage/
│   │
│   ├── configuration/
│   │   │
│   │   ├── motor_config.c
│   │   ├── parameter_store.c
│   │   ├── default_config.c
│   │   └── config_version.c
│   │
│   ├── flash/
│   │   │
│   │   ├── flash_driver.c
│   │   ├── flash_layout.c
│   │   └── nvm_manager.c
│   │
│   └── firmware_update/
│       │
│       ├── firmware_update.c
│       ├── image_manager.c
│       ├── image_verifier.c
│       └── rollback_manager.c
│
├── drivers/
│   │
│   ├── current_sense/
│   │   │
│   │   ├── current_sense.c
│   │   └── current_sense.h
│   │
│   ├── encoder/
│   │   │
│   │   ├── encoder.c
│   │   ├── incremental_encoder.c
│   │   ├── abi_encoder.c
│   │   ├── spi_encoder.c
│   │   └── hall_encoder.c
│   │
│   ├── gate_driver/
│   │   │
│   │   ├── gate_driver.c
│   │   ├── drv8323.c
│   │   └── drv8353.c
│   │
│   ├── temperature_sensor/
│   │   │
│   │   └── temperature_sensor.c
│   │
│   └── power_monitor/
│       │
│       └── power_monitor_hw.c
│
├── platform/
│   │
│   └── stm32g4/
│       │
│       ├── clock_stm32g4.c
│       │
│       ├── pwm_stm32g4.c
│       ├── adc_stm32g4.c
│       ├── dma_stm32g4.c
│       ├── cordic_stm32g4.c
│       │
│       ├── canfd_stm32g4.c
│       ├── spi_stm32g4.c
│       ├── uart_stm32g4.c
│       ├── usb_stm32g4.c
│       │
│       ├── flash_stm32g4.c
│       │
│       ├── irq_stm32g4.c
│       ├── control_irq_stm32g4.c
│       │
│       └── board_stm32g4.c
│
├── bootloader/
│   │
│   ├── bootloader_main.c
│   ├── image_loader.c
│   ├── image_verifier.c
│   └── backup_manager.c
│
├── tests/
│   │
│   ├── unit/
│   │   ├── test_clarke.c
│   │   ├── test_park.c
│   │   ├── test_pi.c
│   │   ├── test_svpwm.c
│   │   └── test_limits.c
│   │
│   ├── integration/
│   │   ├── test_current_loop.c
│   │   ├── test_velocity_loop.c
│   │   └── test_fault_handling.c
│   │
│   └── hardware/
│       ├── board_bringup.c
│       ├── adc_validation.c
│       └── pwm_validation.c
│
├── scripts/
│   │
│   ├── calibration_tools/
│   ├── telemetry_tools/
│   ├── log_decoder/
│   └── firmware_packager/
│
├── docs/
│   │
│   ├── requirements/
│   │   ├── business_requirements.md
│   │   ├── system_requirements.md
│   │   ├── software_requirements.md
│   │   └── traceability_matrix.md
│   │
│   ├── architecture/
│   │   ├── functional_architecture.md
│   │   ├── control_architecture.md
│   │   ├── timing_architecture.md
│   │   └── safety_architecture.md
│   │
│   └── bringup/
│       ├── schematic_review.md
│       ├── pcb_review.md
│       └── hw_bringup_plan.md
│
└── include/
    │
    ├── motor_types.h
    ├── motor_config.h
    ├── motor_status.h
    ├── motor_fault.h
    │
    ├── motor_control_api.h
    ├── motor_diagnostics_api.h
    ├── motor_telemetry_api.h
    └── motor_platform.h
```

Nguyên tắc:
```
- control/ không include stm32*.h
- control/ không gọi k_sem, k_mutex, LOG_*
- platform/ mới biết STM32 LL/HAL
- app/ mới biết Zephyr thread, shell, CAN
```