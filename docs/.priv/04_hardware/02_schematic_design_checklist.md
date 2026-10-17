# Schematic Design Review Checklist for an FOC Servo Driver

## 1. System Architecture

### Functional Blocks

Verify that all required functional blocks are present in the schematic.

- [ ] Power Input
- [ ] Reverse Polarity Protection
- [ ] Surge Protection
- [ ] Power Monitoring
- [ ] DC/DC Converter
- [ ] LDO Regulators
- [ ] MCU
- [ ] Gate Driver
- [ ] MOSFET Power Stage
- [ ] Current Sense
- [ ] Encoder Interface
- [ ] CAN / CAN-FD Interface
- [ ] RS485 Interface
- [ ] USB Interface
- [ ] Debug Interface
- [ ] Temperature Monitoring
- [ ] Protection and Fault Handling

### Requirement Traceability

- [ ] Every system requirement has corresponding hardware support.
- [ ] Every safety requirement is mapped to hardware.
- [ ] Every communication interface includes ESD protection.
- [ ] All sensor interfaces use compatible voltage levels.
- [ ] All external connectors have defined protection strategy.
- [ ] Failure modes are analyzed.

---

# 2. Power Input

## Input Supply Definition

- [ ] Operating voltage range defined.
- [ ] Maximum input voltage defined.
- [ ] Absolute maximum voltage defined.
- [ ] Startup voltage defined.
- [ ] Brown-out operating conditions defined.

## Protection

- [ ] Reverse polarity protection implemented.
- [ ] Fuse or PTC protection included.
- [ ] TVS diode selected.
- [ ] Inrush current protection considered.
- [ ] Hot-plug protection considered.
- [ ] Short-circuit protection strategy defined.

## Bulk Capacitance

- [ ] Bulk capacitor value verified.
- [ ] Ripple current rating verified.
- [ ] Voltage derating verified.
- [ ] Ceramic decoupling capacitors included.
- [ ] Capacitor ESR requirements reviewed.

---

# 3. Power Rails

## Power Budget

- [ ] Total board power consumption estimated.
- [ ] Peak power consumption estimated.
- [ ] Startup consumption estimated.
- [ ] Regenerative operation considered.

## DC/DC Converter

- [ ] Input voltage range compatible.
- [ ] Output current capability verified.
- [ ] Inductor value verified.
- [ ] Feedback network reviewed.
- [ ] Compensation network reviewed.
- [ ] Soft-start configured.

## 12V Rail

- [ ] Gate driver consumption calculated.
- [ ] Bootstrap charging demand considered.
- [ ] Protection included.

## 5V Rail

- [ ] Sensor current budget verified.
- [ ] Encoder current budget verified.
- [ ] USB consumption considered.

## 3.3V Rail

- [ ] MCU current budget verified.
- [ ] Peripheral current budget verified.
- [ ] Peak current margin included.

---

# 4. MCU

## Clock System

- [ ] Crystal frequency verified.
- [ ] Load capacitors calculated.
- [ ] Oscillator startup verified.
- [ ] Clock source selection reviewed.

## Reset Circuit

- [ ] Reset pull-up resistor present.
- [ ] Reset filtering reviewed.
- [ ] Reset button included.
- [ ] NRST accessible through debug connector.

## Boot Configuration

- [ ] Boot mode defined.
- [ ] Boot pins properly biased.
- [ ] Firmware update path considered.

## Debug Interface

- [ ] SWDIO exposed.
- [ ] SWCLK exposed.
- [ ] NRST exposed.
- [ ] Ground reference provided.
- [ ] Connector orientation documented.

## GPIO Review

For every MCU pin:

- [ ] Function assigned.
- [ ] Alternate function verified.
- [ ] Pull-up or pull-down verified.
- [ ] Voltage compatibility checked.
- [ ] Startup state known.
- [ ] Safe state during reset defined.

---

# 5. PWM and Gate Driver

## Gate Driver Selection

- [ ] Voltage rating verified.
- [ ] Current drive capability verified.
- [ ] UVLO supported.
- [ ] Fault indication available.
- [ ] Propagation delay reviewed.

## Bootstrap Circuit

- [ ] Bootstrap capacitor calculated.
- [ ] Bootstrap diode selected.
- [ ] Voltage rating verified.
- [ ] Duty-cycle limitations understood.

## Gate Drive Network

- [ ] Turn-on resistor selected.
- [ ] Turn-off resistor selected.
- [ ] Optional diode network considered.
- [ ] Gate damping reviewed.
- [ ] Power dissipation verified.

## PWM Safety

- [ ] Hardware shutdown path available.
- [ ] Fault-to-PWM disable path defined.
- [ ] Brake input available.
- [ ] Dead-time configuration reviewed.

---

# 6. MOSFET Power Stage

## Voltage Margin

- [ ] MOSFET voltage rating exceeds bus voltage with margin.
- [ ] Avalanche capability reviewed.
- [ ] Transient conditions considered.

Example:

```text
24V Bus
→ Recommended MOSFET rating: 40V to 60V
```

## Current Capability

- [ ] Continuous current verified.
- [ ] Peak current verified.
- [ ] Stall current condition considered.

## Thermal Analysis

- [ ] Junction temperature estimated.
- [ ] Conduction loss estimated.
- [ ] Switching loss estimated.
- [ ] Thermal path reviewed.

## Body Diode

- [ ] Regenerative current path reviewed.
- [ ] Reverse recovery behavior reviewed.
- [ ] Dead-time behavior reviewed.

---

# 7. Current Sensing

## Shunt Resistors

- [ ] Resistance value calculated.
- [ ] Power dissipation calculated.
- [ ] Kelvin connection used.
- [ ] Tolerance selected.
- [ ] Temperature coefficient reviewed.

## Current-Sense Amplifier

- [ ] Gain calculated.
- [ ] Bandwidth sufficient.
- [ ] Common-mode voltage range verified.
- [ ] Offset voltage reviewed.

## ADC Interface

- [ ] ADC dynamic range utilized effectively.
- [ ] No clipping at maximum current.
- [ ] Filter network reviewed.
- [ ] Sampling timing strategy defined.

## Calibration

- [ ] Offset calibration method defined.
- [ ] Gain calibration method defined.
- [ ] Factory calibration strategy considered.

---

# 8. Protection Circuits

## Overcurrent Protection

- [ ] Hardware shutdown implemented.
- [ ] Comparator threshold defined.
- [ ] Response time verified.
- [ ] Fault output connected to MCU.

## Overvoltage Protection

- [ ] Detection implemented.
- [ ] ADC monitoring implemented.
- [ ] Fault action defined.

## Undervoltage Protection

- [ ] Detection implemented.
- [ ] Safe shutdown behavior defined.

## Overtemperature Protection

- [ ] MOSFET temperature monitored.
- [ ] PCB temperature monitored.
- [ ] Thermal limits defined.

---

# 9. Encoder Interface

## Electrical Interface

- [ ] Voltage levels compatible.
- [ ] Pull-ups/pull-downs defined.
- [ ] EMI protection included.
- [ ] Connector pinout verified.

## ABZ Encoder

- [ ] A channel connected.
- [ ] B channel connected.
- [ ] Z channel connected.
- [ ] Input filtering reviewed.

## SPI Encoder

- [ ] CS line verified.
- [ ] SCK line verified.
- [ ] MISO line verified.
- [ ] MOSI line verified.
- [ ] Signal integrity reviewed.

## RS422 Encoder

- [ ] Differential receiver selected.
- [ ] Termination resistor included.
- [ ] Fail-safe biasing reviewed.

---

# 10. Communication Interfaces

## CAN / CAN-FD

- [ ] Transceiver selected.
- [ ] Termination configurable.
- [ ] TVS protection included.
- [ ] Common-mode choke considered.
- [ ] Standby mode supported.

## RS485

- [ ] RE pin connected.
- [ ] DE pin connected.
- [ ] Fail-safe biasing implemented.
- [ ] Termination resistor reviewed.

## USB

- [ ] ESD protection included.
- [ ] CC resistors correct.
- [ ] VBUS sensing available.
- [ ] USB connector orientation verified.

## UART

- [ ] UART header available.
- [ ] Voltage levels documented.

---

# 11. ADC Inputs

For every ADC channel:

- [ ] Input range defined.
- [ ] Source impedance acceptable.
- [ ] RC filtering reviewed.
- [ ] ADC limits never exceeded.
- [ ] Calibration strategy defined.

---

# 12. Testability

## Power Test Points

- [ ] VBUS
- [ ] 12V
- [ ] 5V
- [ ] 3.3V
- [ ] VDDA

## PWM Test Points

- [ ] UH
- [ ] UL
- [ ] VH
- [ ] VL
- [ ] WH
- [ ] WL

## Current-Sense Test Points

- [ ] Current Sense A
- [ ] Current Sense B
- [ ] Current Sense C
- [ ] Bus Voltage

## Communication Test Points

- [ ] CAN_TX
- [ ] CAN_RX
- [ ] UART_TX
- [ ] UART_RX
- [ ] USB Signals (if practical)

---

# 13. Manufacturing Review

## Components

- [ ] All components available from preferred suppliers.
- [ ] Supply-chain risk reviewed.
- [ ] Second source available where possible.

## Package Selection

- [ ] Package manufacturable.
- [ ] Package assembly capability verified.
- [ ] Footprints verified.
- [ ] 3D models available.

## DFM Review

- [ ] Connector orientation verified.
- [ ] Polarized component orientation checked.
- [ ] Assembly notes prepared.

---

# 14. Bring-Up Support

## Indicators

- [ ] Power LED
- [ ] MCU Status LED
- [ ] Fault LED

## Debug Features

- [ ] SWD connector accessible.
- [ ] UART console available.
- [ ] Boot mode accessible.

## Measurements

- [ ] Current measurement accessible.
- [ ] Bus voltage accessible.
- [ ] Temperature measurement accessible.

---

# 15. Layout Readiness Review

Before PCB layout begins:

- [ ] Pin assignment optimized for routing.
- [ ] High-current paths identified.
- [ ] Sensitive analog signals identified.
- [ ] Gate-driver placement strategy defined.
- [ ] Current-sense placement strategy defined.
- [ ] Grounding strategy defined.
- [ ] Power-plane strategy defined.
- [ ] Thermal-via strategy planned.
- [ ] Connector placement strategy defined.

---

# 16. "Can I Debug This Board If Firmware Is Dead?"

## Hardware Recovery

- [ ] SWD always accessible.
- [ ] BOOT mode accessible.
- [ ] Power rails measurable.
- [ ] Reset signal measurable.
- [ ] External oscillator measurable.

## Gate Driver Safety

- [ ] Gate driver disabled by default.
- [ ] PWM outputs safe during reset.
- [ ] Hardware fault can disable inverter without firmware.

## Visibility

- [ ] LEDs provide bring-up status.
- [ ] UART available for logging.
- [ ] Critical analog signals accessible.

---

# Final Sign-Off Checklist

Before releasing the schematic:

- [ ] Power architecture reviewed.
- [ ] MCU reviewed.
- [ ] Gate driver reviewed.
- [ ] MOSFET stage reviewed.
- [ ] Current sensing reviewed.
- [ ] Protection circuits reviewed.
- [ ] Encoder interface reviewed.
- [ ] Communication interfaces reviewed.
- [ ] Test points reviewed.
- [ ] Bring-up strategy prepared.
- [ ] Manufacturing constraints reviewed.
- [ ] BOM availability checked.
- [ ] Peer review completed.

---

# Golden Design Rule

For every signal in the schematic, answer the following questions:

1. What is its purpose?
2. How will it be tested during bring-up?
3. What happens if it fails?
4. Can the failure be detected?
5. Can the system recover safely?

If you cannot answer all five questions, the schematic is not ready for layout.