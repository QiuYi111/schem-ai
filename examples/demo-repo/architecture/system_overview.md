# System Overview

## Objective

Provide a small controller board that reads a sensor input, drives a status LED, and exposes a UART maintenance interface.

## Modules

- Power input and regulation
- Microcontroller domain
- Sensor input conditioning
- Status and maintenance I/O

## Tradeoffs

- Use a simple MCU with integrated ADC to minimize BOM complexity.
- Keep the sensor path single-ended for the demo, while documenting noise risk explicitly.
