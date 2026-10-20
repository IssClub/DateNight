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
const rpDir = path.join(__dirname, 'img', 'roleplay');
if (fs.existsSync(rpDir)) {
  const roleplays = {};
  const entries = fs.readdirSync(rpDir);
  // Group direct files: stewardess.jpg + stewardess2.jpg → same session
  const directFiles = entries.filter(e => {
    try { return fs.statSync(path.join(rpDir, e)).isFile() && /\.(jpg|jpeg|png|webp)$/i.test(e); } catch { return false; }
  });
  const fileGroups = {};
  directFiles.forEach(file => {
    const base = file.replace(/\.[^.]+$/, '');
    const m = base.match(/^(.+?)(\d+)$/);
    const key = m ? m[1].toLowerCase() : base.toLowerCase();
    if (!fileGroups[key]) fileGroups[key] = [];
    fileGroups[key].push(file);
  });
  Object.entries(fileGroups).forEach(([key, files]) => {
    files.sort();
    roleplays[key] = [files.map(f => `img/roleplay/${f}`)];
  });
  entries.filter(e => {
    try { return fs.statSync(path.join(rpDir, e)).isDirectory(); } catch { return false; }
  }).forEach(dir => {
    const photos = fs.readdirSync(path.join(rpDir, dir))
      .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f))
      .sort()
      .map(f => `img/roleplay/${dir}/${f}`);
    if (!photos.length) return;
    const match = dir.match(/^(.+?)(\d+)$/);
    if (match) {
      const key = match[1].toLowerCase();
      const idx = parseInt(match[2]) - 1;
      if (!roleplays[key]) roleplays[key] = [];
      roleplays[key][idx] = photos;
    } else {
      roleplays[dir.toLowerCase()] = [photos];
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
