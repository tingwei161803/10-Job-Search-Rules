"""Open index.html with Playwright and verify it renders correctly."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
PAGE = ROOT / "index.html"
SHOTS = ROOT / "screenshots"


def main() -> int:
    SHOTS.mkdir(exist_ok=True)
    url = PAGE.resolve().as_uri()

    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for label, viewport in [
            ("desktop", {"width": 1440, "height": 900}),
            ("tablet", {"width": 834, "height": 1194}),
            ("mobile", {"width": 390, "height": 844}),
        ]:
            ctx = browser.new_context(viewport=viewport, device_scale_factor=2)
            page = ctx.new_page()
            page.on("pageerror", lambda e: errors.append(f"[{label}] pageerror: {e}"))
            page.on(
                "console",
                lambda m: errors.append(f"[{label}] console.{m.type}: {m.text}")
                if m.type == "error"
                else None,
            )
            page.goto(url, wait_until="networkidle")

            # Structural assertions
            title = page.title()
            assert "Job-Search Rules" in title, f"unexpected title: {title!r}"

            rules = page.locator("article[id^='rule-']")
            count = rules.count()
            assert count == 10, f"expected 10 rules, got {count}"

            # Trigger any scroll-revealed sections, then settle
            page.evaluate(
                "document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'))"
            )
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_timeout(800)

            shot = SHOTS / f"{label}.png"
            page.screenshot(path=str(shot), full_page=True)
            print(f"  ✓ {label:<8} {viewport['width']}x{viewport['height']} → {shot.name}")
            ctx.close()
        browser.close()

    if errors:
        print("\nConsole/page errors:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    print(f"\n✓ All checks passed. Screenshots in {SHOTS}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
