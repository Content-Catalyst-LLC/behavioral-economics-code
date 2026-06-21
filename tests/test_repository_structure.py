#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
required = ["README.md", "repository_manifest.json", "article-map.md", "_shared", "articles", "scripts", "docs"]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required repository paths:", missing)
    sys.exit(1)
manifest = json.loads((root / "repository_manifest.json").read_text(encoding="utf-8"))
errors = []
for article in manifest.get("articles", []):
    article_dir = root / article["path"]
    if not article_dir.exists():
        errors.append(f"missing article directory: {article['path']}")
    if not (article_dir / "calculators" / "calculator_manifest.json").exists():
        errors.append(f"missing calculator manifest: {article['path']}")
if errors:
    print("Repository structure errors:")
    for error in errors:
        print("-", error)
    sys.exit(1)
print(f"Repository structure OK: {manifest.get('repository')} ({len(manifest.get('articles', []))} articles)")
