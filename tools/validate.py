#!/usr/bin/env python3
"""Validează schemele și exemplele din TechTable Standard.

Rulare, din rădăcina repo-ului:

    pip install -r tools/requirements.txt
    python tools/validate.py

Ce verifică:
  1. toate fișierele .json și .jsonld sunt JSON valid;
  2. fiecare schemă este JSON Schema Draft 2020-12 validă;
  3. fiecare exemplu canonical trece schema entității lui, cu verificarea
     formatelor activă (dată, URI, email);
  4. fiecare exemplu canonical are o pereche lite;
  5. `@context` începe cu schema.org și include contextul standardului;
  6. verificarea formatelor chiar funcționează (un eveniment cu dată
     invalidă este respins).

Iese cu cod 0 dacă totul e în regulă, altfel cu 1.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
TIERS = {
    "v0.1": "https://standard.techtable.ro/v0.1/context.jsonld",
    "v0.1-strategic": "https://standard.techtable.ro/v0.1-strategic/context.jsonld",
}
SCHEMA_ORG = "https://schema.org"

errors: list[str] = []
checked = 0


def fail(where: Path | str, message: str) -> None:
    errors.append(f"{where}: {message}")


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(path.relative_to(ROOT), f"JSON invalid ({exc})")
        return None


def schema_errors(schema: dict, document: dict) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    found = []
    for err in sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(part) for part in err.absolute_path) or "<rădăcină>"
        found.append(f"{location}: {err.message}")
    return found


def check_context(path: Path, document: dict, context_url: str) -> None:
    context = document.get("@context")
    if not isinstance(context, list):
        fail(path, "`@context` trebuie să fie o listă: schema.org, apoi contextul standardului")
        return
    if not context or context[0] != SCHEMA_ORG:
        fail(path, f"primul element din `@context` trebuie să fie {SCHEMA_ORG}")
    if context_url not in context:
        fail(path, f"`@context` nu include {context_url}")


def main() -> int:
    global checked

    # 1. orice fișier JSON din repo se poate citi
    for path in sorted(ROOT.rglob("*.json")) + sorted(ROOT.rglob("*.jsonld")):
        if ".git" in path.parts or "node_modules" in path.parts or ".venv" in path.parts:
            continue
        load(path)

    for tier, context_url in TIERS.items():
        base = ROOT / tier
        for schema_path in sorted((base / "schemas").glob("*.schema.json")):
            entity = schema_path.name.removesuffix(".schema.json")
            rel_schema = schema_path.relative_to(ROOT)
            schema = load(schema_path)
            if schema is None:
                continue

            # 2. schema însăși e validă
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:  # noqa: BLE001
                fail(rel_schema, f"schemă invalidă ({exc})")
                continue

            canonical_path = base / "examples" / f"{entity}.canonical.json"
            lite_path = base / "examples" / f"{entity}.lite.json"
            rel_example = canonical_path.relative_to(ROOT)

            # 4. perechea canonical + lite există
            if not canonical_path.exists():
                fail(rel_schema, f"lipsește exemplul {rel_example}")
                continue
            if not lite_path.exists():
                fail(rel_example, f"lipsește perechea {lite_path.name}")

            document = load(canonical_path)
            if document is None:
                continue

            # 3. exemplul trece schema, cu formatele verificate
            for message in schema_errors(schema, document):
                fail(rel_example, message)

            # 5. ordinea și conținutul din @context
            check_context(rel_example, document, context_url)
            checked += 1

            # 6. verificarea formatelor e activă
            if entity == "event":
                broken = copy.deepcopy(document)
                broken["startDate"] = "mâine seară"
                if not schema_errors(schema, broken):
                    fail(rel_schema, "o dată invalidă în `startDate` a trecut validarea: formatele nu sunt verificate")

    if errors:
        print(f"EȘUAT: {len(errors)} probleme\n")
        for line in errors:
            print(f"  - {line}")
        return 1

    print(f"OK: {checked} exemple validate pe schemele lor, formate verificate.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    sys.exit(main())
