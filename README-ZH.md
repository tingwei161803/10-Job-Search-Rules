# 剛剛失效的 10 條求職守則 · 讀者導讀版

Nikhyl Singhal 在 *The Skip* 發表的文章
[**10 Job-Search Rules That Just Broke**](https://theskip.substack.com/p/10-job-search-rules-that-just-broke)
(2026 年 5 月)的雙語單頁視覺導讀。

**🌐 線上版:** <https://tingwei161803.github.io/10-Job-Search-Rules/>

| | 網址 |
| --- | --- |
| 英文版 | <https://tingwei161803.github.io/10-Job-Search-Rules/> |
| 繁體中文版 | <https://tingwei161803.github.io/10-Job-Search-Rules/zh-Hant/> |

[← English README](./README.md)

---

## 預覽

![桌面版預覽 — 繁中](screenshots/zh-Hant-desktop.png)

| 英文 (手機) | 繁中 (手機) |
| :---: | :---: |
| ![EN mobile](screenshots/en-mobile.png) | ![ZH mobile](screenshots/zh-Hant-mobile.png) |

---

## 這是什麼

原文主張:AI 悄悄改寫了資深科技人的職涯腳本——關於到職磨合、頭銜、遠端、身份等
十條長年成立的假設,現在已經失效。這個專案把那篇文章變成一頁式編輯導讀,
每一條規則都用「**舊規則**(劃線淺色卡)」對上「**新規則**(黑底反白卡)」,
下方再附一行「為什麼」。

這是 **讀者導讀**,不是原文重現。完整論述與故事請讀
[原文](https://theskip.substack.com/p/10-job-search-rules-that-just-broke)。

## 設計筆記

- **編輯雜誌風格** — 英文版用 Instrument Serif + Inter,繁中版用 Noto Serif TC
  + Noto Sans TC。
- **米色紙質背景** 搭配 SVG 噪點,做出印刷品質感。
- **對照式排版** — 舊規則劃線,新規則放黑底反白卡片並列。
- **滾動進場動畫** 用原生 `IntersectionObserver`,沒有引入任何動畫框架;
  也保留 hook 讓 headless 截圖能顯示完整頁面。
- **每個語言一個檔案** — 沒有 build step、沒有 bundler,Tailwind 走 CDN。

## 專案結構

```
.
├── index.html              # 英文版
├── zh-Hant/
│   └── index.html          # 繁體中文版
├── verify.py               # 兩版本的 Playwright 結構與視覺檢查
├── screenshots/            # 三個尺寸 × 兩個語言的參考截圖
├── pyproject.toml          # uv 管理的 Python 專案(只裝 Playwright)
└── uv.lock
```

## 本機開發

頁面都是靜態 HTML,直接打開 `index.html` 就行,也可以起任何靜態伺服器:

```bash
python -m http.server 8000
# 或
uv run python -m http.server 8000
```

然後到 `http://localhost:8000/`(英文)或
`http://localhost:8000/zh-Hant/`(繁中)。

## 驗證

附了一個用 [Playwright](https://playwright.dev/) 寫的小腳本,跑兩個版本 × 三個
viewport(desktop / tablet / mobile),檢查標題、10 個 `article[id^="rule-"]`、
語言切換器都在,並把參考截圖寫到 `screenshots/`。

全程用 `uv`,不需要全域 Python:

```bash
# 第一次需要,把 Chromium 裝到 ~/Library/Caches/ms-playwright/
uv run playwright install chromium

# 跑檢查
uv run python verify.py
```

預期輸出:

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

## 部署

GitHub Pages,從 `main` 分支根目錄出。push 到 `main` 後一兩分鐘內就會更新,
不需要額外 CI。

## 出處與致謝

- 原文:**〈10 Job-Search Rules That Just Broke〉**,作者
  [Nikhyl Singhal](https://theskip.substack.com/),發表於 *The Skip*,
  2026 年 5 月 20 日。
- 本 repo 是非官方的讀者導讀,做為前端與排版練習,與原作者或 *The Skip* 無從屬關係。
- 所有導讀文字、中文翻譯、視覺設計皆為本專案原創。

## 授權

程式碼與設計:MIT。
所摘要的原文版權歸原作者,並依照 *The Skip* 的條款發布——請到原站閱讀。
