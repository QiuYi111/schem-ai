# Phase1: Solution Design

## Goal

Convert the clarified requirements into a reviewable system design.

## Required Outputs

- rchitecture/system_overview.md
- rchitecture/interface_matrix.md
- rchitecture/risk_register.md
"@ | Set-Content -Path phases/phase1.md -Encoding utf8
@"
# Phase2: Part Sourcing

## Goal

Compare candidate parts, choose approved parts, and collect relevant datasheets.

## Required Outputs

- sourcing/candidate_parts.csv
- sourcing/approved_parts.yaml
- sourcing/selection_notes.md
- sourcing/datasheets/
"@ | Set-Content -Path phases/phase2.md -Encoding utf8
@"
# Phase3: Datasheet Deep Read

## Goal

Turn approved datasheets into actionable handbook documents for implementation.

## Required Outputs

- handbook/
"@ | Set-Content -Path phases/phase3.md -Encoding utf8
@"
# Phase4: Interconnect Design

## Goal

Create the structured JSON design that a renderer can consume.

## Required Outputs

- design/interconnect.json
- design/design_notes.md
"@ | Set-Content -Path phases/phase4.md -Encoding utf8
@"
# Phase5: Rendering

## Goal

Produce a schematic artifact and capture the render history.

## Required Outputs

- ender/schematic_output/
- ender/render_log.md
"@ | Set-Content -Path phases/phase5.md -Encoding utf8
@"
# Clarifier Agent

Focus on requirement extraction, contradiction detection, and X-Y problem handling.

Outputs must be written into the spec/ documents, not left in chat only.
