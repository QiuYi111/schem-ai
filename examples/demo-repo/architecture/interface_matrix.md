# Interface Matrix

| Source | Destination | Type | Notes |
| --- | --- | --- | --- |
| 12V input | 3V3 regulator | power | Primary supply path |
| 3V3 regulator | MCU | power | Main digital rail |
| Sensor header | MCU ADC0 | analog | Single-ended 0-3.0V input |
| MCU GPIO | Status LED | control | Active-high through resistor |
| MCU UART | Maintenance header | digital | 3.3V TTL debug port |
