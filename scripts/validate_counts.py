#!/usr/bin/env python3
import csv
import pathlib
import re
import sys


root = pathlib.Path(__file__).resolve().parents[1]
with (root / "decision-matrix" / "criteria.csv").open(newline="", encoding="utf-8") as handle:
    criteria = list(csv.DictReader(handle))
questions = (root / "workshops" / "question-bank.md").read_text(encoding="utf-8")
question_ids = re.findall(r"^Q-(\d{3})\.", questions, flags=re.MULTILINE)

errors = []
if len(criteria) != 120:
    errors.append(f"expected 120 criteria; found {len(criteria)}")
if len({row["criterion_id"] for row in criteria}) != 120:
    errors.append("criterion IDs are not unique")
if len(question_ids) != 180:
    errors.append(f"expected 180 questions; found {len(question_ids)}")
if len(set(question_ids)) != 180:
    errors.append("question IDs are not unique")

if errors:
    print("ERROR: " + "; ".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("OK: 120 unique criteria and 180 unique workshop questions")
