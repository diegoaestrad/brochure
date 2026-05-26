#!/usr/bin/env python3
"""Replace broken Unsplash photo IDs with verified URLs across the project."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Broken ID -> verified working replacement
REPLACEMENTS: dict[str, str] = {
    "photo-1501339847302-acfcbee2f5b0": "photo-1495474472287-4d71bcdd2085",
    "photo-1427504492413-84790444a9b0": "photo-1635070041078-e363dbe005cb",
    "photo-1434030216441-bb5eb4b0b0b0": "photo-1522202176988-66273c2fd55f",
    "photo-1447933601403-0c6688de56e3": "photo-1495474472287-4d71bcdd2085",
    "photo-1449965408869-eaa3f722e342": "photo-1486262715619-67b85e0b08d3",
    "photo-1464349095432-e22f213fe681": "photo-1414235077428-338989a2e8c0",
    "photo-1465495976277-aa0dcd068e2f": "photo-1519741497674-611481863552",
    "photo-1487754180591-762b83b383f2": "photo-1486262715619-67b85e0b08d3",
    "photo-1503676260728-1c1c1c1c1c1c": "photo-1522202176988-66273c2fd55f",
    "photo-1503951914875-452162b0a3ad": "photo-1595476108010-b4d1f102b1b1",
    "photo-1511285560929-80b4561120a2": "photo-1519741497674-611481863552",
    "photo-1511920170033-f8396924c10b": "photo-1495474472287-4d71bcdd2085",
    "photo-1516734212186-a967f81ad9d7": "photo-1518791841217-8f162f1e1131",
    "photo-1517701550927-4664d2a49335": "photo-1495474472287-4d71bcdd2085",
    "photo-1522337360788-8eee710a1a05": "photo-1560066984-138dadb4c035",
    "photo-1527515637468-c4f917a31494": "photo-1581578731548-c64695cc6952",
    "photo-1532094888888-8f8f8f8f8f8f": "photo-1635070041078-e363dbe005cb",
    "photo-1544025162-d766942659de": "photo-1555244162-803834f70033",
    "photo-1544161515-4ab6ce6db929": "photo-1540555700478-4be289fbecef",
    "photo-1544367567-0f2fcb009e03": "photo-1506126613408-eca07ce68773",
    "photo-1549931319-a545dcf3bc7b": "photo-1509440159596-0249088772ff",
    "photo-1551836022-d5d88e9c9639": "photo-1554224155-6726b3ff858f",
    "photo-1558171813-0c088a0a001f": "photo-1454165804606-c3d57bc86b40",
    "photo-1558907413-efae50ab9b36": "photo-1416879595882-3373a0480b5b",
    "photo-1560448204-e602f3c3e3e3": "photo-1560518883-ce09059eeffa",
    "photo-1562259949-e8e7689d782f": "photo-1589939705384-5185137a7f0f",
    "photo-1570172619644-dfd8eb2e8e8e": "photo-1540555700478-4be289fbecef",
    "photo-1571019613454-1cb457f9f9b2": "photo-1534438327276-14e5300c3a48",
    "photo-1571019614242-c5c5dee9f50c": "photo-1576091160550-2173dba999ef",
    "photo-1573496359142-b8d87734a775": "photo-1554224155-6726b3ff858f",
    "photo-1574680096145-d05b474e2a4c": "photo-1518611012118-696072aa579a",
    "photo-1575052814086-397a5d0c0c0c": "photo-1506126613408-eca07ce68773",
    "photo-1576201836106-db1758fd1c76": "photo-1518791841217-8f162f1e1131",
    "photo-1582735686739-4f8a9f2e1c3e": "photo-1454165804606-c3d57bc86b40",
    "photo-1583337130417-3346a1be1e1e": "photo-1518791841217-8f162f1e1131",
    "photo-1583511655857-d58738977f93": "photo-1518791841217-8f162f1e1131",
    "photo-1585704032915-c3400ca76e2f": "photo-1558618666-fcd25c85cd64",
    "photo-1585747860715-cd4628902d4a": "photo-1595476108010-b4d1f102b1b1",
    "photo-1585779034823-7e9ac237aee0": "photo-1581094794329-c8112a89af12",
    "photo-1587300003388-59208d0b0b0b": "photo-1609840114035-3c981b782dfe",
    "photo-1588776814546-1ff472f993b1": "photo-1609840114035-3c981b782dfe",
    "photo-1590644365607-1d9f8c4b0b0e": "photo-1486262715619-67b85e0b08d3",
    "photo-1593941707874-ef652b629750": "photo-1550355291-bbee04a92027",
    "photo-1598256980801-4581ff43e9b5": "photo-1609840114035-3c981b782dfe",
    "photo-1599351431202-1e0c0d11324a": "photo-1595476108010-b4d1f102b1b1",
    "photo-1600518464441-8d9d8e8e8e8e": "photo-1600585154340-be6161a56a0c",
    "photo-1601362871776-97b6e2e9b33d": "photo-1486262715619-67b85e0b08d3",
    "photo-1606811971618-4486d14f46ea": "photo-1609840114035-3c981b782dfe",
    "photo-1607860108855-edeefe6fe626": "photo-1486262715619-67b85e0b08d3",
    "photo-1611532736580-6b91ce1fee10": "photo-1554224155-6726b3ff858f",
    "photo-1619642751034-765f983a38af": "photo-1486262715619-67b85e0b08d3",
    "photo-1621605815977-fbc98d665ca0": "photo-1595476108010-b4d1f102b1b1",
    "photo-1621905252507-b35492daef8d": "photo-1621905251918-48416bd8575a",
    "photo-1622286342621-4bd786c244f8": "photo-1595476108010-b4d1f102b1b1",
    "photo-1625047509248-ec889cbff025": "photo-1486262715619-67b85e0b08d3",
    "photo-1629909613654-3796e08a7f82": "photo-1609840114035-3c981b782dfe",
    "photo-1631540591168-2164f4d8e2e4": "photo-1581094794329-c8112a89af12",
    "photo-1631813288648-9a5e248f04a6": "photo-1609840114035-3c981b782dfe",
    "photo-1632758146205-4a3e8e8e8e8e": "photo-1486406146926-c627a92fd1ab",
}


def replace_in_text(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS.items():
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def main() -> None:
    total = 0
    exts = {".html", ".css", ".js", ".json"}
    for path in ROOT.rglob("*"):
        if path.suffix not in exts:
            continue
        if path.name == "fix_images.py":
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = replace_in_text(text)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"  {path.relative_to(ROOT)}: {n} replacements")
            total += n

    # Regenerate portfolio embed
    catalog = json.loads((ROOT / "catalog.json").read_text())
    js = (
        "// Generated from catalog.json\n"
        "window.PORTFOLIO_DEMOS = "
        + json.dumps(catalog["demos"], indent=2)
        + ";\n"
    )
    (ROOT / "portfolio-data.js").write_text(js)
    print(f"\nTotal replacements: {total}")
    print("Updated portfolio-data.js")


if __name__ == "__main__":
    main()
