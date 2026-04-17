# Data_validation

## Project overview

The diagram below provides an overview of the project workflow, which is organized into four main steps and one optional component. This repository corresponds to the data validation steps, highlighted in red in the figure.

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 40, 'rankSpacing': 50}}}%%
flowchart LR

    A[Database Structure]:::data -->  B[Validation<br/>Rules]:::validation
    B --> D[Defect Distribution<br/>Analysis]:::analysis
    D --> E[Defect-Factor<br/>Correlation]:::analysisP2

    %% Optional branch BELOW
    subgraph optional_branch[ ]
        direction TB
        C[Optional: Validation<br/>Report]:::optional
    end
    style optional_branch fill:none,stroke:none

    subgraph stage1[ ]
        B[Validation<br/>Rules]
    end
 
    style stage1 stroke:#FF0000,stroke-width:3px,fill:none
    B -.-> C

    %% Click links
    click A "https://github.com/SewerDefectAnalysis/Database_Structure"
    click B "https://github.com/SewerDefectAnalysis/Data_validation"
    click C "https://github.com/SewerDefectAnalysis/Data_validation"

    %% Styles
    classDef data fill:#E8F0FE,stroke:#1A73E8,stroke-width:1.8px
    classDef validation fill:#E6F4EA,stroke:#188038,stroke-width:1.8px
    classDef analysis fill:#F3E8FD,stroke:#9334E6,stroke-width:1.8px
    classDef analysisP2 fill:#FDEBD0,stroke:#E67E22,stroke-width:1.8px
    classDef prediction fill:#FEF7E0,stroke:#F9AB00,stroke-width:1.8px
    classDef optional fill:#F5F5F5,stroke:#666666,stroke-width:1.8px,stroke-dasharray: 5 5

```

This repository performs validation of the data used in the sewer defect analysis. It consists of two main processes. On one hand, a validation report is generated to identify potential errors and inconsistencies. On the other hand, pipe properties are validated using a set of validation rules.
