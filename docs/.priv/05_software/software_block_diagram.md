# Layer diagram
```
┌─────────────────────────────┐
│            APP              │
│                             │
│ startup                     │
│ system_controller           │
│ motor_service               │
│ service_manager             │
│ command_manager             │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│         SERVICES            │
│                             │
│ calibration                 │
│ monitoring                  │
│ telemetry                   │
│ diagnostics                 │
│ logging                     │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│            CORE             │
│                             │
│ control                     │
│ estimation                  │
│ runtime                     │
│ safety                      │
│ state_machine               │
│ data_model                  │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│          DRIVERS            │
│                             │
│ encoder                     │
│ current_sense               │
│ gate_driver                 │
│ temp_sensor                 │
│ power_monitor               │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│         PLATFORM            │
│                             │
│ adc_stm32g4                 │
│ pwm_stm32g4                 │
│ spi_stm32g4                 │
│ dma_stm32g4                 │
│ irq_stm32g4                 │
└─────────────────────────────┘
```