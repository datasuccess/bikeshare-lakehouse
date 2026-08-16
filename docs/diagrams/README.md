# docs/diagrams/ — rendered visuals

> **Purpose:** hold the polished diagrams embedded across the README and docs. **Status:** planned.
> The README currently uses an inline **Mermaid** diagram; these SVG/PNG versions replace/augment it as
> the build progresses.

## The five planned diagrams
| File | Diagram | Tool | Status |
|---|---|---|---|
| `hero.svg` | **Local vs cloud** — "same code, swap the sink" (signature image) | Excalidraw | ⚪ |
| `medallion.svg` | Bronze → Silver (Data Vault) → Gold (Kimball) data flow | Excalidraw / Mermaid | ⚪ |
| `dag.svg` | Airflow cadence DAG graph | Mermaid / auto-gen | ⚪ |
| `star-schema.svg` | Kimball ERD (facts + dims) | dbterd / Mermaid | ⚪ |
| `lineage.svg` | dbt lineage graph | `dbt docs` (auto) | ⚪ |

## Guidance
- Hand-draw `hero` + `medallion` in **Excalidraw** for the polished look; auto-generate the rest.
- Export as **SVG** (crisp at any size); keep source files (`.excalidraw`) alongside.
- Every diagram is embedded where it's referenced — nobody should need to clone to see the architecture.
