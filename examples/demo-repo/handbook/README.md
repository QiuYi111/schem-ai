# Handbook

## MCU Input Constraints

- Source: sourcing/datasheets/stm32g030.pdf
- Rationale: ADC input must stay within the MCU analog supply domain.
- Confidence: 0.75
- Unresolved items: Final source impedance budget still needs confirmation.

## Regulator Constraints

- Source: sourcing/datasheets/ap2112k.pdf
- Rationale: Input and output capacitors are required for regulator stability.
- Confidence: 0.74
- Unresolved items: Confirm capacitor derating at ambient temperature.
