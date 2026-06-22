"""
NER/RE Extractor — Pydantic-first extraction with graceful fallback.

Primary path  : Builds runtime Pydantic BaseModel subclasses from the live ontology,
                requests a json_schema response_format for protocol-level enforcement,
                then validates the response via Pydantic — no JSON retries needed.

Fallback path : Original prompt-based JSON extraction (unchanged) — activated
                automatically when the model / Ollama version does not support
                json_schema response_format, or when Pydantic validation fails.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, Field, create_model

from ..utils.llm_client import LLMClient

logger = logging.getLogger('mirofish.ner_extractor')


# ══════════════════════════════════════════════════════════════════════════════
# Pydantic model factory
# ══════════════════════════════════════════════════════════════════════════════

class _RelationItem(BaseModel):
    source: str = Field(..., description="Source entity name (must match an extracted entity)")
    target: str = Field(..., description="Target entity name (must match an extracted entity)")
    type: str   = Field(..., description="Relation type in UPPER_SNAKE_CASE from the ontology")
    fact: str   = Field("",  description="One sentence describing the relationship")


def _make_entity_model(entity_def: dict) -> Type[BaseModel]:
    """Build a Pydantic BaseModel from one ontology entity_type dict."""
    name = entity_def.get("name", "Entity")
    fields: dict = {
        "entity_name": (str, Field(..., description=f"Canonical name of this {name}"))
    }
    for attr in entity_def.get("attributes", []):
        a_name = attr.get("name", "").strip()
        a_desc = attr.get("description", a_name)
        if a_name:
            fields[a_name] = (Optional[str], Field(None, description=a_desc))
    return create_model(name, **fields)


def _make_extraction_model(ontology: dict) -> Type[BaseModel]:
    """
    Build the top-level ExtractionResult model.

    One Optional[List[<EntityModel>]] per entity type in the ontology,
    plus a 'relations' list. This lets Pydantic validate each extracted
    entity against its specific field schema.
    """
    top_fields: dict = {}
    for et in ontology.get("entity_types", []):
        name = et.get("name", "").strip()
        if not name:
            continue
        EntityModel = _make_entity_model(et)
        top_fields[name] = (
            Optional[List[EntityModel]],
            Field(default_factory=list, description=f"Extracted {name} entities"),
        )
    top_fields["relations"] = (
        Optional[List[_RelationItem]],
        Field(default_factory=list, description="Relations between extracted entities"),
    )
    return create_model("ExtractionResult", **top_fields)


# ══════════════════════════════════════════════════════════════════════════════
# Prompts
# ══════════════════════════════════════════════════════════════════════════════

_STRUCTURED_SYSTEM = """You are a Named Entity Recognition and Relation Extraction system.
Extract all entities and relations from the given text according to the schema.

Rules:
1. Only extract entity types and relation types listed in the ontology.
2. Normalize entity names: strip whitespace, use canonical form (e.g., "Jack Ma" not "ma jack").
3. Only extract what is explicitly stated or strongly implied in the text.
4. For relations: source and target must be entity names you have already extracted.
5. Return empty lists if nothing is found."""

_STRUCTURED_USER = """Ontology:
{ontology_summary}

Text to analyse:
{text}

Extract all entities and relations."""

# ── Fallback prompt (original behaviour, unchanged) ────────────────────────────

_FALLBACK_SYSTEM = """You are a Named Entity Recognition and Relation Extraction system.
Given a text and an ontology (entity types + relation types), extract all entities and relations.

ONTOLOGY:
{ontology_description}

RULES:
1. Only extract entity types and relation types defined in the ontology.
2. Normalize entity names: strip whitespace, use canonical form (e.g., "Jack Ma" not "ma jack").
3. Each entity must have: name, type (from ontology), and optional attributes.
4. Each relation must have: source entity name, target entity name, type (from ontology), and a fact sentence describing the relationship.
5. If no entities or relations are found, return empty lists.
6. Be precise — only extract what is explicitly stated or strongly implied in the text.

Return ONLY valid JSON in this exact format:
{{
  "entities": [
    {{"name": "...", "type": "...", "attributes": {{"key": "value"}}}}
  ],
  "relations": [
    {{"source": "...", "target": "...", "type": "...", "fact": "..."}}
  ]
}}"""

_FALLBACK_USER = """Extract entities and relations from the following text:

{text}"""


# ══════════════════════════════════════════════════════════════════════════════
# Extractor
# ══════════════════════════════════════════════════════════════════════════════

class NERExtractor:
    """
    Extract entities and relations from text using local LLM.

    Tries Pydantic structured output first; falls back to the original
    prompt-based JSON approach automatically.
    """

    def __init__(self, llm_client: Optional[LLMClient] = None, max_retries: int = 2):
        self.llm = llm_client or LLMClient()
        self.max_retries = max_retries

    def extract(self, text: str, ontology: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract entities and relations from text, guided by ontology.

        Returns:
            {"entities": [...], "relations": [...]}
        """
        if not text or not text.strip():
            return {"entities": [], "relations": []}

        try:
            result = self._extract_structured(text, ontology)
            logger.debug(
                f"[NER:pydantic] {len(result['entities'])} entities, "
                f"{len(result['relations'])} relations"
            )
            return result
        except Exception as e:
            logger.warning(f"[NER:pydantic] failed ({e!r}), falling back to prompt-based")
            return self._extract_prompt(text, ontology)

    # ── Primary: Pydantic structured output ────────────────────────────────────

    def _extract_structured(self, text: str, ontology: Dict[str, Any]) -> Dict[str, Any]:
        ExtractionModel = _make_extraction_model(ontology)
        schema = ExtractionModel.model_json_schema()

        messages = [
            {"role": "system", "content": _STRUCTURED_SYSTEM},
            {
                "role": "user",
                "content": _STRUCTURED_USER.format(
                    ontology_summary=self._format_ontology_summary(ontology),
                    text=text.strip(),
                ),
            },
        ]

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "ExtractionResult",
                "strict": False,
                "schema": schema,
            },
        }

        raw = self.llm.chat(
            messages=messages,
            temperature=0.1,
            max_tokens=4096,
            response_format=response_format,
        )

        # Validate via Pydantic — raises ValidationError if schema mismatch
        result_obj = ExtractionModel.model_validate(json.loads(raw))
        return self._pydantic_to_dict(result_obj, ontology)

    def _pydantic_to_dict(
        self, result_obj: BaseModel, ontology: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert a validated ExtractionResult Pydantic object to the standard dict format."""
        entity_type_names = {et["name"] for et in ontology.get("entity_types", [])}
        dumped = result_obj.model_dump()

        entities: List[Dict] = []
        seen: set = set()

        for field_name, items in dumped.items():
            if field_name == "relations" or field_name not in entity_type_names:
                continue
            for item in items or []:
                name = str(item.pop("entity_name", "")).strip()
                if not name or name.lower() in seen:
                    continue
                seen.add(name.lower())
                attrs = {k: v for k, v in item.items() if v is not None}
                entities.append({"name": name, "type": field_name, "attributes": attrs})

        relations: List[Dict] = []
        seen_lower = {e["name"].lower() for e in entities}

        for rel in dumped.get("relations") or []:
            source = str(rel.get("source", "")).strip()
            target = str(rel.get("target", "")).strip()
            rtype  = str(rel.get("type", "RELATED_TO")).strip()
            fact   = str(rel.get("fact", "")).strip()
            if not source or not target:
                continue
            for ep in (source, target):
                if ep.lower() not in seen_lower:
                    entities.append({"name": ep, "type": "Entity", "attributes": {}})
                    seen_lower.add(ep.lower())
            relations.append({
                "source": source,
                "target": target,
                "type": rtype,
                "fact": fact or f"{source} {rtype} {target}",
            })

        return {"entities": entities, "relations": relations}

    # ── Fallback: original prompt-based path ───────────────────────────────────

    def _extract_prompt(self, text: str, ontology: Dict[str, Any]) -> Dict[str, Any]:
        ontology_desc = self._format_ontology(ontology)
        system_msg = _FALLBACK_SYSTEM.format(ontology_description=ontology_desc)
        user_msg = _FALLBACK_USER.format(text=text.strip())

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                result = self.llm.chat_json(
                    messages=messages, temperature=0.1, max_tokens=4096
                )
                return self._validate_and_clean(result, ontology)
            except ValueError as e:
                last_error = e
                logger.warning(f"[NER:fallback] attempt {attempt+1}: invalid JSON — {e}")
            except Exception as e:
                last_error = e
                logger.error(f"[NER:fallback] error: {e}")
                if attempt >= self.max_retries:
                    break

        logger.error(f"[NER:fallback] exhausted all attempts: {last_error}")
        return {"entities": [], "relations": []}

    # ── Helpers ─────────────────────────────────────────────────────────────────

    def _format_ontology_summary(self, ontology: Dict[str, Any]) -> str:
        """Compact ontology listing for the structured extraction prompt."""
        parts = ["Entity types:"]
        for et in ontology.get("entity_types", []):
            name = et.get("name", "")
            attrs = [a.get("name") for a in et.get("attributes", []) if a.get("name")]
            line = f"  {name}"
            if attrs:
                line += f" (fields: {', '.join(attrs)})"
            parts.append(line)
        parts.append("\nRelation types:")
        for rt in ontology.get("edge_types", ontology.get("relation_types", [])):
            name = rt.get("name", "")
            sts = rt.get("source_targets", [])
            st_str = ", ".join(
                f"{s.get('source')}→{s.get('target')}" for s in sts
            )
            parts.append(f"  {name}" + (f" ({st_str})" if st_str else ""))
        return "\n".join(parts)

    def _format_ontology(self, ontology: Dict[str, Any]) -> str:
        """Format ontology dict into readable text for the fallback LLM prompt."""
        parts = []
        for et in ontology.get("entity_types", []):
            if not parts:
                parts.append("Entity Types:")
            if isinstance(et, dict):
                name = et.get("name", str(et))
                desc = et.get("description", "")
                attrs = et.get("attributes", [])
                line = f"  - {name}"
                if desc:
                    line += f": {desc}"
                if attrs:
                    attr_names = [
                        a.get("name", str(a)) if isinstance(a, dict) else str(a)
                        for a in attrs
                    ]
                    line += f" (attributes: {', '.join(attr_names)})"
                parts.append(line)
            else:
                parts.append(f"  - {et}")

        for rt in ontology.get("relation_types", ontology.get("edge_types", [])):
            if not any("Relation" in p for p in parts):
                parts.append("\nRelation Types:")
            if isinstance(rt, dict):
                name = rt.get("name", str(rt))
                desc = rt.get("description", "")
                source_targets = rt.get("source_targets", [])
                line = f"  - {name}"
                if desc:
                    line += f": {desc}"
                if source_targets:
                    st_strs = [
                        f"{st.get('source', '?')} → {st.get('target', '?')}"
                        for st in source_targets
                    ]
                    line += f" ({', '.join(st_strs)})"
                parts.append(line)
            else:
                parts.append(f"  - {rt}")

        if not parts:
            parts.append(
                "No specific ontology defined. Extract all entities and relations you find."
            )
        return "\n".join(parts)

    def _validate_and_clean(
        self, result: Dict[str, Any], ontology: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate and normalise LLM output from the fallback path."""
        entities = result.get("entities", [])
        relations = result.get("relations", [])

        valid_entity_types = set()
        for et in ontology.get("entity_types", []):
            if isinstance(et, dict):
                valid_entity_types.add(et.get("name", "").strip())
            else:
                valid_entity_types.add(str(et).strip())

        valid_relation_types = set()
        for rt in ontology.get("relation_types", ontology.get("edge_types", [])):
            if isinstance(rt, dict):
                valid_relation_types.add(rt.get("name", "").strip())
            else:
                valid_relation_types.add(str(rt).strip())

        cleaned_entities = []
        seen_names: set = set()
        for entity in entities:
            if not isinstance(entity, dict):
                continue
            name = str(entity.get("name", "")).strip()
            etype = str(entity.get("type", "Entity")).strip()
            if not name:
                continue
            name_lower = name.lower()
            if name_lower in seen_names:
                continue
            seen_names.add(name_lower)
            if valid_entity_types and etype not in valid_entity_types:
                logger.debug(f"Entity '{name}' type '{etype}' not in ontology, keeping")
            cleaned_entities.append({
                "name": name,
                "type": etype,
                "attributes": entity.get("attributes", {}),
            })

        cleaned_relations = []
        entity_names_lower = {e["name"].lower() for e in cleaned_entities}
        for relation in relations:
            if not isinstance(relation, dict):
                continue
            source = str(relation.get("source", "")).strip()
            target = str(relation.get("target", "")).strip()
            rtype  = str(relation.get("type", "RELATED_TO")).strip()
            fact   = str(relation.get("fact", "")).strip()
            if not source or not target:
                continue
            for ep in (source, target):
                if ep.lower() not in entity_names_lower:
                    cleaned_entities.append({"name": ep, "type": "Entity", "attributes": {}})
                    entity_names_lower.add(ep.lower())
            cleaned_relations.append({
                "source": source,
                "target": target,
                "type": rtype,
                "fact": fact or f"{source} {rtype} {target}",
            })

        return {"entities": cleaned_entities, "relations": cleaned_relations}
