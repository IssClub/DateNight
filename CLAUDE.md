# DateNight — CLAUDE.md

## פריסה
- **GitHub Pages**: `https://issclub.github.io/DateNight/`
- **אין Netlify** — לא לציין Netlify בשום הקשר
- כל URL פנימי חייב להיות relative: `new URL('rp-edit.html', location.href)` — לא `location.origin + '/...'`

## מבנה פרויקט
```
src.html          ← קוד מקור (JSX + Babel). לא לערוך index.html ישירות!
index.html        ← build output (נוצר אוטומטית)
build.js          ← מקמפל src.html → index.html + מסנכרן roleplay.json + gifs.json
rp-edit.html      ← עריכת תרחישי roleplay (שומר דרך GitHub API)
roleplay.json     ← auto-generated מ-img/roleplay/ בכל build
roleplay-meta.json← טקסטים מותאמים אישית לתרחישים + _token ל-PAT
gifs.json         ← auto-generated מ-GIF/ בכל build
sync-images.bat   ← סקריפט לסנכרון תמונות חדשות (דאבל-קליק)
```

## Build
```
node build.js
```
רץ אוטומטית כ-pre-commit hook ומייצר:
- `index.html` (Babel compiled)
- `roleplay.json` (מעץ img/roleplay/)
- `gifs.json` (מתיקיית GIF/)

**לעולם לא לערוך `index.html` ישירות** — השינויים ידרסו בbuild הבא.

## הוספת תמונות חדשות
דאבל-קליק על `sync-images.bat` — מוסיף, מבנה ודוחף הכל אוטומטית.

מבנה תיקיות:
```
img/roleplay/<scenario>/          → סשן בודד (תמונות ישירות בתיקייה)
img/roleplay/<scenario>/1/        → סשן 1
img/roleplay/<scenario>/2/        → סשן 2
GIF/<category>/                   → קטגוריית GIF
```

## אפליקציות המשנה
האפליקציה מכילה שלושה חלקים עיקריים באותו `src.html`:

### 1. DateNight — תכנון דייט (React)
קטגוריות: מסעדות, ברים, תיאטרון, סרטים, סטנד-אפ, בישול, סרטים בבית, משחקים, אינטימי, בוגרים, פיקניק, חוויות, הרפתקאות, קפה, ספא, סדנאות
- `RESTAURANTS`, `BARS`, `THEATER`, `MOVIES`, `STANDUP`, `COOKING`, `HOME_MOVIES`, `HOME_SERIES`, `HOME_GAMES`, `INTIMATE`, `ADULTS`, `PICNIC_SPOTS`, `EXPERIENCE`, `ADVENTURE`, `COFFEE_CARTS`, `SPA_ITEMS`, `WORKSHOP_ITEMS`
- Screens: `HomeScreen` → `CategoryScreen` → `SubcatScreen` → `ItemScreen`
- תוספות: `DrinksRouletteScreen`, `FavoritesScreen`, `HistoryScreen`, `SettingsScreen`

### 2. 365 Dice — ספר תנוחות (Vanilla JS)
- מרונדר ב-`#dice-game-root` בתוך `src.html` (לא React)
- 358+ תנוחות מ-`poses-data.json`
- פיצ'ר GIF: "איך זה ייגמר הלילה?" — קובץ אקראי מ-`GIF/` + `gifs.json`
- תמונות: `365/001.jpg`–`365/365.jpg`

### 3. Roleplay — משחקי תפקידים (React, בתוך ItemScreen)
- נפתח מקטגוריית "בוגרים"
- Picker modal: בחירת תרחיש וסשן
- Idea modal: slideshow תמונות + ZoomableImg (pinch/pan/tap-reset) + caption עם outfit + scene
- שני ה-modals ברונדרים ב-`ReactDOM.createPortal` → `#modal-root`
- עריכת טקסט: `rp-edit.html` (שומר ב-GitHub API עם PAT)
- נתונים: `roleplay.json` (תמונות) + `roleplay-meta.json` (טקסטים + PAT)

## Stack
- **React 18 UMD** — ללא build step לוגי (JSX נכתב ב-src.html עם `type="text/babel"`)
- `React.createElement(...)` — לא JSX syntax בקוד עצמו (כי build.js מטפל בהמרה)
- **ReactDOM.createPortal** — modals מרונדרים ל-`#modal-root` (מחוץ ל-`#root`)
- Google Fonts: **Rubik** (wght 300/400/500) — פונט הסצנות

## ארכיטקטורת modals
- `<div id="root">` — האפליקציה הראשית
- `<div id="modal-root">` — picker modal + idea modal (portal, מחוץ ל-root)
- חשוב: `#root { position: fixed; overflow: hidden }` — יוצר stacking context, לכן modals חייבים להיות ב-modal-root

## קבצי עריכה
- `rp-edit.html` — עריכת תרחישי roleplay. שומר ב-GitHub דרך PAT.
  - encoding: `btoa(unescape(encodeURIComponent(...)))` / `decodeURIComponent(escape(atob(...)))`
  - PAT מאוחסן ב-`roleplay-meta.json` תחת מפתח `_token`

## Hebrew encoding
תמיד להשתמש ב:
- encode: `btoa(unescape(encodeURIComponent(str)))`
- decode: `decodeURIComponent(escape(atob(b64)))`

לא `btoa(str)` ישירות — יגרום לגיבריש בעברית.

## Git
- Branch: `main`
- Commit attribution: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- לא לעשות push של קבצים לא רלוונטיים (`.netlify/`, `fix_*.py`, `out.txt`, `img/NEW/`)

## העדפות עבודה
- לערוך `src.html` → `node build.js` → commit `src.html + index.html`
- אחרי אישור ראשון לסוג פעולה (build, edit, push) — להמשיך בלי לשאול שוב באותו סשן
- לא לבנות עם הגיבוי/ניקוי קוד שלא נדרש — רק מה שנבקש
- commit messages: קצרים, ב-conventional commits (`feat:`, `fix:`, `sync:`)
