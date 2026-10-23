/**
 * build.js — DateNight build script
 *
 * קורא את src.html (קוד מקור עם JSX),
 * מקמפל את ה-JSX ל-JS רגיל,
 * ומייצר index.html מוכן ל-Netlify.
 *
 * שימוש: node build.js
 */

const fs   = require('fs');
const path = require('path');
const babel = require('@babel/core');

const SRC  = path.join(__dirname, 'src.html');
const DIST = path.join(__dirname, 'index.html');

console.log('Building DateNight...');

// 1. Read source
let content = fs.readFileSync(SRC, 'utf8');

// 2. Extract JSX from <script type="text/babel">...</script>
const BABEL_OPEN  = '<script type="text/babel">';
const SCRIPT_CLOSE = '</script>';
const startIdx = content.indexOf(BABEL_OPEN);
if (startIdx === -1) {
  console.error('ERROR: Could not find <script type="text/babel"> in src.html');
  process.exit(1);
}
const codeStart = startIdx + BABEL_OPEN.length;
const codeEnd   = content.indexOf(SCRIPT_CLOSE, codeStart);
const jsxCode   = content.slice(codeStart, codeEnd);

// 3. Compile JSX → JS
console.log('Compiling JSX...');
const result = babel.transform(jsxCode, {
  presets: [['@babel/preset-react', { runtime: 'classic' }]],
  filename: 'app.jsx',
});

// 3b. Inject build timestamp
const now = new Date();
const pad = n => String(n).padStart(2, '0');
const buildTs = `${pad(now.getDate())}.${pad(now.getMonth()+1)}.${String(now.getFullYear()).slice(2)} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
result.code = result.code.replace('"BUILD_TS"', `"${buildTs}"`);

// 4. Replace <script type="text/babel">...</script> with compiled output
content = content.slice(0, startIdx)
  + '<script>\n'
  + result.code
  + '\n</script>'
  + content.slice(codeEnd + SCRIPT_CLOSE.length);

// 5. Remove Babel CDN line
content = content.replace(
  /  <!-- Babel standalone for JSX \(dev only - removed in build\) -->\n  <script src="https:\/\/unpkg\.com\/@babel\/standalone\/babel\.min\.js"><\/script>\n/,
  ''
);

// 6. Write output
fs.writeFileSync(DIST, content);

// 7. Auto-regenerate gifs.json from GIF subfolders
const gifDir = path.join(__dirname, 'GIF');
if (fs.existsSync(gifDir)) {
  const gifData = {};
  const cats = fs.readdirSync(gifDir).filter(f =>
    fs.statSync(path.join(gifDir, f)).isDirectory()
  );
  cats.forEach(cat => {
    const files = fs.readdirSync(path.join(gifDir, cat))
      .filter(f => /\.(gif|mp4|webm|mov)$/i.test(f));
    if (files.length) {
      gifData[cat] = files.map(file => ({ file, path: `GIF/${cat}/${file}` }));
    }
  });
  fs.writeFileSync(path.join(__dirname, 'gifs.json'), JSON.stringify(gifData, null, 2));
  const total = Object.values(gifData).reduce((a, b) => a + b.length, 0);
  console.log(`  gifs.json  → ${cats.length} categories, ${total} files  ✓ auto-synced`);
}

// 8. Auto-regenerate roleplay.json from img/roleplay/ structure
// Structure: img/roleplay/<scenario>/          → single session (direct files)
//            img/roleplay/<scenario>/1/        → session 1
//            img/roleplay/<scenario>/2/        → session 2
const rpDir = path.join(__dirname, 'img', 'roleplay');
if (fs.existsSync(rpDir)) {
  const roleplays = {};
  const scenarioDirs = fs.readdirSync(rpDir).filter(e => {
    try { return fs.statSync(path.join(rpDir, e)).isDirectory(); } catch { return false; }
  });
  scenarioDirs.forEach(scenario => {
    const scenarioPath = path.join(rpDir, scenario);
    const children = fs.readdirSync(scenarioPath);
    const subDirs = children.filter(e => {
      try { return fs.statSync(path.join(scenarioPath, e)).isDirectory(); } catch { return false; }
    });
    const directPhotos = children
      .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f))
      .sort()
      .map(f => `img/roleplay/${scenario}/${f}`);
    if (subDirs.length > 0) {
      // Multiple sessions: numbered subfolders 1/, 2/, 3/...
      const sessions = subDirs
        .filter(d => /^\d+$/.test(d))
        .sort((a, b) => parseInt(a) - parseInt(b))
        .map(d => fs.readdirSync(path.join(scenarioPath, d))
          .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f))
          .sort()
          .map(f => `img/roleplay/${scenario}/${d}/${f}`)
        )
        .filter(s => s.length > 0);
      if (sessions.length > 0) roleplays[scenario] = sessions;
    } else if (directPhotos.length > 0) {
      // Single session: photos directly in scenario folder
      roleplays[scenario] = [directPhotos];
    }
  });
  Object.keys(roleplays).forEach(k => { roleplays[k] = roleplays[k].filter(Boolean); });
  fs.writeFileSync(path.join(__dirname, 'roleplay.json'), JSON.stringify(roleplays, null, 2));
  console.log(`  roleplay.json → ${Object.keys(roleplays).length} scenarios  ✓ auto-synced`);
}

const srcSize  = (fs.statSync(SRC).size  / 1024).toFixed(1);
const distSize = (fs.statSync(DIST).size / 1024).toFixed(1);
console.log(`Done!`);
console.log(`  src.html   → ${srcSize} KB`);
console.log(`  index.html → ${distSize} KB  ✓ ready for Netlify`);
