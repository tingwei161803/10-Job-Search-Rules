"""Open both language editions with Playwright and verify they render correctly."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
SHOTS = ROOT / "screenshots"

EDITIONS = [
    {
        "lang": "en",
        "path": ROOT / "index.html",
        "title_contains": "Job-Search Rules",
        "switch_to": "./zh-Hant/",
    },
    {
        "lang": "zh-Hant",
        "path": ROOT / "zh-Hant" / "index.html",
        "title_contains": "求職守則",
        "switch_to": "../",
    },
]

VIEWPORTS = [
    ("desktop", {"width": 1440, "height": 900}),
    ("tablet", {"width": 834, "height": 1194}),
    ("mobile", {"width": 390, "height": 844}),
]


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    errors: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for edition in EDITIONS:
            lang = edition["lang"]
            url = edition["path"].resolve().as_uri()
            print(f"\n→ {lang} ({edition['path'].relative_to(ROOT)})")

            for label, viewport in VIEWPORTS:
                tag = f"{lang}-{label}"
                ctx = browser.new_context(viewport=viewport, device_scale_factor=2)
                page = ctx.new_page()
                page.on("pageerror", lambda e, t=tag: errors.append(f"[{t}] pageerror: {e}"))
                page.on(
                    "console",
                    lambda m, t=tag: errors.append(f"[{t}] console.{m.type}: {m.text}")
                    if m.type == "error"
                    else None,
                )
                page.goto(url, wait_until="networkidle")

                title = page.title()
                assert edition["title_contains"] in title, (
                    f"[{tag}] unexpected title: {title!r}"
                )

                rules = page.locator("article[id^='rule-']")
                count = rules.count()
                assert count == 10, f"[{tag}] expected 10 rules, got {count}"

                # Language switcher present and pointing to the other edition
                switcher = page.locator(f"a[href='{edition['switch_to']}']").first
                assert switcher.count() == 1, f"[{tag}] missing language switcher"

                # Trigger reveal animations and wait for fonts
                page.evaluate(
                    "document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'))"
                )
                page.evaluate("document.fonts && document.fonts.ready")
                page.wait_for_timeout(800)

                shot = SHOTS / f"{tag}.png"
                page.screenshot(path=str(shot), full_page=True)
                print(
                    f"  ✓ {label:<8} {viewport['width']}x{viewport['height']} → {shot.name}"
                )
                ctx.close()
        browser.close()

    if errors:
        print("\nConsole/page errors:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    print(f"\n✓ All checks passed for both editions. Screenshots in {SHOTS}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
