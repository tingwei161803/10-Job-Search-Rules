# 10 Job-Search Rules That Just Broke — Reader's Edition

A bilingual, single-page visual summary of Nikhyl Singhal's essay
[**10 Job-Search Rules That Just Broke**](https://theskip.substack.com/p/10-job-search-rules-that-just-broke)
(*The Skip*, May 2026), built as an editorial reading exercise.

**🌐 Live site:** <https://10-job-search-rules.peteraim.com/>

| | URL |
| --- | --- |
| English edition | <https://10-job-search-rules.peteraim.com/> |
| 繁體中文 edition | <https://10-job-search-rules.peteraim.com/zh-Hant/> |

[繁體中文 README →](./README-ZH.md)

---

## Preview

![Desktop preview — English](screenshots/en-desktop.png)

| English (mobile) | 繁中 (mobile) |
| :---: | :---: |
| ![EN mobile](screenshots/en-mobile.png) | ![ZH mobile](screenshots/zh-Hant-mobile.png) |

---

## What this is

The original essay argues that AI quietly rewrote the senior-tech-career playbook
— ten long-standing assumptions about onboarding, titles, remote work, and
identity are now out of date. This site turns that thesis into a one-page
editorial: each rule is shown as a side-by-side **broken rule** vs.
**working rule** card, with a short "why" line underneath.

It is a **reader's summary**, not a reproduction. For the full argument and
the stories that didn't fit on a card, read the
[original on The Skip](https://theskip.substack.com/p/10-job-search-rules-that-just-broke).

## Design notes

- **Editorial / magazine feel** — Instrument Serif display + Inter body for
  English; Noto Serif TC + Noto Sans TC for Traditional Chinese.
- **Cream paper background** with an SVG noise grain for a printed texture.
- **Per-rule comparison** — the old rule is struck through on a light card;
  the new rule sits in a black inverted card next to it.
- **Scroll-revealed sections** via `IntersectionObserver` (no animation
  framework), with a graceful test hook so headless screenshots show the
  full page.
- **Single file per language** — no build step, no bundler. Tailwind ships
  via CDN and the only runtime dependency is the browser.

## Project structure

```
.
├── index.html              # English edition
├── zh-Hant/
│   └── index.html          # Traditional Chinese edition
├── verify.py               # Playwright structural + visual check (both editions)
├── screenshots/            # Reference renders, three viewports per language
├── pyproject.toml          # uv-managed Python project (Playwright only)
└── uv.lock
```

## Local development

The pages are static HTML — open `index.html` directly, or serve the folder
with any static file server.

```bash
# any of the following will work
python -m http.server 8000
uv run python -m http.server 8000
npx serve .
```

Then visit `http://localhost:8000/` (English) or
`http://localhost:8000/zh-Hant/` (繁中).

## Verifying the build

A small [Playwright](https://playwright.dev/) script renders both editions
across desktop / tablet / mobile viewports, asserts the structural pieces
are present (title, ten `article[id^="rule-"]` blocks, cross-language
switcher), and writes reference screenshots into `screenshots/`.

Everything is `uv`-managed — there is no global Python install.

```bash
# first time only — installs Chromium under ~/Library/Caches/ms-playwright/
uv run playwright install chromium

# run the checks
uv run python verify.py
```

Expected output:

```
→ en (index.html)
  ✓ desktop  1440x900 → en-desktop.png
  ✓ tablet   834x1194 → en-tablet.png
  ✓ mobile   390x844  → en-mobile.png

→ zh-Hant (zh-Hant/index.html)
  ✓ desktop  1440x900 → zh-Hant-desktop.png
  ✓ tablet   834x1194 → zh-Hant-tablet.png
  ✓ mobile   390x844  → zh-Hant-mobile.png

✓ All checks passed for both editions.
```

## Deployment

GitHub Pages, served from the `main` branch root. Pushing to `main` updates
the live site within a minute or so. No CI configuration is required.

## Attribution

- Original essay: **"10 Job-Search Rules That Just Broke"** by
  [Nikhyl Singhal](https://theskip.substack.com/), published in *The Skip*,
  May 20, 2026.
- This repository is an unofficial reader's edition built as a frontend /
  typography exercise. It is not affiliated with the author or *The Skip*.
- All editorial summary copy, translation, and visual design in this
  repository are original to this project.

## License

Code and design: MIT (see `LICENSE` if present, otherwise treat as MIT).
The original essay it summarizes is © its author and remains under whatever
terms *The Skip* publishes it under — please go read it there.
