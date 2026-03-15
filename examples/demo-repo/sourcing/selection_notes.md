# Selection Notes

## Microcontroller Decision

- Winner: STM32G030F6P6
- Source: architecture/system_overview.md
- Rationale: Combines ADC sampling, GPIO, and UART debug in one small package.
- Confidence: 0.79
- Unresolved items: Confirm flash headroom after firmware sizing.

## Regulator Decision

- Winner: AP2112K-3.3
- Source: architecture/interface_matrix.md
- Rationale: Low-complexity 3.3V rail for the demo current budget.
- Confidence: 0.72
- Unresolved items: Validate thermal rise at 12V input.
