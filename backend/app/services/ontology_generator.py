"""
Ontology generation service
Analyzes document content and derives a domain-appropriate ontology
for knowledge graph construction — domain-agnostic, not locked to social simulation.
"""

import json
from typing import Dict, Any, List, Optional
from ..utils.llm_client import LLMClient


ONTOLOGY_SYSTEM_PROMPT = """You are a knowledge graph ontology expert. Your task is to read the provided text and derive entity types and relationship types that are NATIVE to that domain — do not impose a fixed schema, discover what the text is actually about.

**Output only valid JSON. No explanation, no markdown fences.**

## Step 1 — Identify the Domain

Read the text and determine what domain it belongs to. Examples:
- Business / Corporate: companies, products, executives, markets, deals
- Legal / Compliance: contracts, parties, clauses, obligations, jurisdictions
- Scientific / Research: papers, authors, institutions, concepts, experiments
- Medical / Clinical: patients, conditions, treatments, drugs, providers
- Technology / Engineering: systems, components, APIs, teams, dependencies
- Financial: instruments, transactions, issuers, portfolios, regulations
- Narrative / News: events, actors, locations, organisations, dates
- Any other domain — let the text guide you

## Step 2 — Design Entity Types

Rules:
- **6 to 10 entity types** — not more, not fewer than what the domain needs
- Types must be **concrete, nameable things** present in the text (not abstract concepts, not adjectives, not topics)
- Last 2 types MUST always be the universal fallbacks:
  - `Person` — any natural person not covered by a more specific type
  - `Organization` — any organisation not covered by a more specific type
- First 4–8 types are **domain-specific**, derived from what the text is actually about
- Each type needs 1–3 attributes (avoid reserved words: `name`, `uuid`, `group_id`, `created_at`, `summary`)

## Step 3 — Design Relationship Types

Rules:
- **5 to 10 relationship types**
- Names: UPPER_SNAKE_CASE verbs that describe how one entity acts on or relates to another
- Each must list valid source → target entity type pairs
- Relationships must be grounded in what the text describes, not generic fillers

## Output Format

```json
{
    "domain": "detected domain label (e.g. Business, Legal, Medical, Technology, Research, News)",
    "entity_types": [
        {
            "name": "PascalCase type name",
            "description": "One sentence, max 100 chars",
            "attributes": [
                {"name": "snake_case_attr", "type": "text", "description": "what it captures"}
            ],
            "examples": ["example 1", "example 2"]
        }
    ],
    "edge_types": [
        {
            "name": "UPPER_SNAKE_CASE",
            "description": "One sentence, max 100 chars",
            "source_targets": [
                {"source": "SourceType", "target": "TargetType"}
            ],
            "attributes": []
        }
    ],
    "analysis_summary": "2–3 sentences: what this document is about and why these types were chosen"
}
```

## Quality Checklist (verify before outputting)

- [ ] Entity types are concrete things, not abstract concepts
- [ ] Last 2 types are Person and Organization (in that order)
- [ ] No duplicate or overlapping types
- [ ] Every edge type has at least one valid source_target pair using defined entity types
- [ ] Attribute names avoid reserved words: name, uuid, group_id, created_at, summary
- [ ] Total entity types: 6–10
- [ ] Total edge types: 5–10
"""


class OntologyGenerator:
    """
    Ontology generator
    Analyze text content and generate entity and relationship type definitions
    """

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()

    def generate(
        self,
        document_texts: List[str],
        simulation_requirement: str = "",
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a domain-appropriate ontology from document content.

        Args:
            document_texts: List of document texts to analyse
            simulation_requirement: Optional user hint about the domain or use-case
            additional_context: Any additional context to guide generation

        Returns:
            Ontology dict with entity_types, edge_types, domain, analysis_summary
        """
        user_message = self._build_user_message(
            document_texts,
            simulation_requirement,
            additional_context,
        )

        messages = [
            {"role": "system", "content": ONTOLOGY_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        result = self.llm_client.chat_json(
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
        )

        return self._validate_and_process(result)

    MAX_TEXT_LENGTH_FOR_LLM = 50000

    def _build_user_message(
        self,
        document_texts: List[str],
        user_hint: str,
        additional_context: Optional[str],
    ) -> str:
        combined_text = "\n\n---\n\n".join(document_texts)
        original_length = len(combined_text)

        if len(combined_text) > self.MAX_TEXT_LENGTH_FOR_LLM:
            combined_text = combined_text[: self.MAX_TEXT_LENGTH_FOR_LLM]
            combined_text += (
                f"\n\n...(truncated — original {original_length} chars, "
                f"first {self.MAX_TEXT_LENGTH_FOR_LLM} shown for ontology analysis)..."
            )

        parts = ["## Document Content\n", combined_text]

        if user_hint and user_hint.strip():
            parts += ["\n## User Hint / Use-case\n", user_hint.strip()]

        if additional_context and additional_context.strip():
            parts += ["\n## Additional Context\n", additional_context.strip()]

        parts.append(
            "\n\nAnalyse the document above and output an ontology JSON "
            "that reflects the actual domain and entities present in this text."
        )

        return "\n".join(parts)
    
    def _validate_and_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Normalise LLM output and guarantee universal fallback types are present."""
        MAX_ENTITY_TYPES = 10
        MAX_EDGE_TYPES = 10

        result.setdefault("entity_types", [])
        result.setdefault("edge_types", [])
        result.setdefault("analysis_summary", "")
        result.setdefault("domain", "General")

        for entity in result["entity_types"]:
            entity.setdefault("attributes", [])
            entity.setdefault("examples", [])
            if len(entity.get("description", "")) > 100:
                entity["description"] = entity["description"][:97] + "..."

        for edge in result["edge_types"]:
            edge.setdefault("source_targets", [])
            edge.setdefault("attributes", [])
            if len(edge.get("description", "")) > 100:
                edge["description"] = edge["description"][:97] + "..."

        # Universal fallbacks — always present as last two entries
        _PERSON_FALLBACK = {
            "name": "Person",
            "description": "Any individual person not covered by a more specific type.",
            "attributes": [
                {"name": "full_name", "type": "text", "description": "Full name"},
                {"name": "role", "type": "text", "description": "Role or occupation"},
            ],
            "examples": ["individual", "unnamed person"],
        }
        _ORG_FALLBACK = {
            "name": "Organization",
            "description": "Any organisation not covered by a more specific type.",
            "attributes": [
                {"name": "org_name", "type": "text", "description": "Organisation name"},
                {"name": "org_type", "type": "text", "description": "Type of organisation"},
            ],
            "examples": ["small business", "community group"],
        }

        existing_names = {e["name"] for e in result["entity_types"]}
        fallbacks_needed = []
        if "Person" not in existing_names:
            fallbacks_needed.append(_PERSON_FALLBACK)
        if "Organization" not in existing_names:
            fallbacks_needed.append(_ORG_FALLBACK)

        if fallbacks_needed:
            slots_available = MAX_ENTITY_TYPES - len(result["entity_types"])
            if slots_available < len(fallbacks_needed):
                # Trim from the end of specific types to make room
                trim = len(fallbacks_needed) - slots_available
                result["entity_types"] = result["entity_types"][:-trim]
            result["entity_types"].extend(fallbacks_needed)

        # Hard caps
        result["entity_types"] = result["entity_types"][:MAX_ENTITY_TYPES]
        result["edge_types"] = result["edge_types"][:MAX_EDGE_TYPES]

        return result
    
    def generate_python_code(self, ontology: Dict[str, Any]) -> str:
        """
        [DEPRECATED] Convert ontology definition to Zep-format Pydantic code.
        Not used in MiroFish-Offline (ontology stored as JSON in Neo4j).
        Kept for reference only.
        """
        code_lines = [
            '"""',
            'Custom entity type definitions',
            'Auto-generated by MiroFish for social opinion simulation',
            '"""',
            '',
            'from pydantic import Field',
            'from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel',
            '',
            '',
            '# ============== Entity Type Definitions ==============',
            '',
        ]

        # Generate entity types
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            desc = entity.get("description", f"A {name} entity.")

            code_lines.append(f'class {name}(EntityModel):')
            code_lines.append(f'    """{desc}"""')

            attrs = entity.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')

            code_lines.append('')
            code_lines.append('')

        code_lines.append('# ============== Relationship Type Definitions ==============')
        code_lines.append('')

        # Generate relationship types
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            # Convert to PascalCase class name
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            desc = edge.get("description", f"A {name} relationship.")

            code_lines.append(f'class {class_name}(EdgeModel):')
            code_lines.append(f'    """{desc}"""')

            attrs = edge.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')

            code_lines.append('')
            code_lines.append('')

        # Generate type dictionaries
        code_lines.append('# ============== Type Configuration ==============')
        code_lines.append('')
        code_lines.append('ENTITY_TYPES = {')
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            code_lines.append(f'    "{name}": {name},')
        code_lines.append('}')
        code_lines.append('')
        code_lines.append('EDGE_TYPES = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            code_lines.append(f'    "{name}": {class_name},')
        code_lines.append('}')
        code_lines.append('')

        # Generate source_targets mapping for edges
        code_lines.append('EDGE_SOURCE_TARGETS = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            source_targets = edge.get("source_targets", [])
            if source_targets:
                st_list = ', '.join([
                    f'{{"source": "{st.get("source", "Entity")}", "target": "{st.get("target", "Entity")}"}}'
                    for st in source_targets
                ])
                code_lines.append(f'    "{name}": [{st_list}],')
        code_lines.append('}')

        return '\n'.join(code_lines)

