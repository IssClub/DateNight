import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'C:\Alon\Claude\DateNight\Netlify'

with open(ROOT + r'\src.html', encoding='utf-8', newline='\n') as f:
    c = f.read()

ok = []

# ── 1. Arrow directions: ❮/❯ → ▲/▼ in HTML template ──────────────────
# prev (left, -1) → ▼ ; next (right, +1) → ▲
old = 'onclick=\\"DiceGameApp.navPose(-1)\\">\\u276e</button>\\n      <button class=\\"btn-nav-pose btn-nav-next\\" onclick=\\"DiceGameApp.navPose(1)\\">\\u276f'
new = 'onclick=\\"DiceGameApp.navPose(-1)\\">\\u25bc</button>\\n      <button class=\\"btn-nav-pose btn-nav-next\\" onclick=\\"DiceGameApp.navPose(1)\\">\\u25b2'
if old in c:
    c = c.replace(old, new, 1); ok.append('1. Arrows ✓')
else:
    ok.append('1. Arrows NOT FOUND')

# ── 2. GIF smart shuffle: replace rollEnding with shuffle logic ─────────
old2 = ('var GIF_FILES = null;\n'
        'async function loadGifFiles(){\n'
        '  if(GIF_FILES) return;\n'
        '  var r = await fetch(\'./gifs.json\');\n'
        '  GIF_FILES = await r.json();\n'
        '}')
new2 = ('var GIF_FILES = null;\n'
        'var GIF_SHUFFLE = null;\n'
        'var GIF_IDX = 0;\n'
        'async function loadGifFiles(){\n'
        '  if(GIF_FILES) return;\n'
        '  var r = await fetch(\'./gifs.json\');\n'
        '  GIF_FILES = await r.json();\n'
        '}\n'
        'function pickGif(){\n'
        '  if(!GIF_FILES||!GIF_FILES.length) return null;\n'
        '  if(!GIF_SHUFFLE||GIF_IDX>=GIF_SHUFFLE.length){\n'
        '    GIF_SHUFFLE=[...GIF_FILES].sort(()=>Math.random()-0.5);\n'
        '    GIF_IDX=0;\n'
        '  }\n'
        '  return GIF_SHUFFLE[GIF_IDX++];\n'
        '}')
if old2 in c:
    c = c.replace(old2, new2, 1); ok.append('2. GIF shuffle ✓')
else:
    ok.append('2. GIF shuffle NOT FOUND')

# ── 3. Use pickGif() in rollEnding ─────────────────────────────────────
old3 = ('  async function rollEnding(){\n'
        '    await loadGifFiles();\n'
        '    if(!GIF_FILES || !GIF_FILES.length) return;\n'
        '    var file = GIF_FILES[Math.floor(Math.random() * GIF_FILES.length)];')
new3 = ('  async function rollEnding(){\n'
        '    await loadGifFiles();\n'
        '    if(!GIF_FILES || !GIF_FILES.length) return;\n'
        '    var file = pickGif();')
if old3 in c:
    c = c.replace(old3, new3, 1); ok.append('3. rollEnding pickGif ✓')
else:
    ok.append('3. rollEnding NOT FOUND')

# ── 4. Face ID: only authenticate if already registered (no auto-register) ─
old4 = ('  const tryBiometricAuth = async () => {\n'
        '    try {\n'
        '      if (!(await biometricAvailable())) throw new Error("unavailable");\n'
        '      const stored = localStorage.getItem("dn_bio_id");\n'
        '      if (stored) {\n'
        '        await authenticateBiometric();\n'
        '      } else {\n'
        '        await registerBiometric();\n'
        '      }\n'
        '      setSkippedCat(true);\n'
        '      setSelectedSubcat("adults");\n'
        '      setView("subcat");\n'
        '    } catch {\n'
        '      setPasswordTarget("adults");\n'
        '      setShowPasswordModal(true);\n'
        '    }\n'
        '  };')
new4 = ('  const tryBiometricAuth = async () => {\n'
        '    if (localStorage.getItem("dn_bio_id")) {\n'
        '      try {\n'
        '        if (!(await biometricAvailable())) throw new Error();\n'
        '        await authenticateBiometric();\n'
        '        setSkippedCat(true);\n'
        '        setSelectedSubcat("adults");\n'
        '        setView("subcat");\n'
        '        return;\n'
        '      } catch {}\n'
        '    }\n'
        '    setPasswordTarget("adults");\n'
        '    setShowPasswordModal(true);\n'
        '  };')
if old4 in c:
    c = c.replace(old4, new4, 1); ok.append('4. tryBiometricAuth ✓')
else:
    ok.append('4. tryBiometricAuth NOT FOUND')

# ── 5. Add showBioOffer state ────────────────────────────────────────────
old5 = '  const [passwordError, setPasswordError] = useState(false);'
new5 = ('  const [passwordError, setPasswordError] = useState(false);\n'
        '  const [showBioOffer, setShowBioOffer] = useState(false);')
if old5 in c:
    c = c.replace(old5, new5, 1); ok.append('5. showBioOffer state ✓')
else:
    ok.append('5. showBioOffer NOT FOUND')

# ── 6. handlePasswordSubmit: offer Face ID after success ────────────────
old6 = ('  const handlePasswordSubmit = pwd => {\n'
        '    if (pwd === "SexyNight") {\n'
        '      setShowPasswordModal(false);\n'
        '      setPasswordError(false);\n'
        '      if (passwordTarget === "adults") setSkippedCat(true);\n'
        '      setSelectedSubcat(passwordTarget);\n'
        '      setGenreFilter(null);\n'
        '      setView("subcat");\n'
        '    } else {\n'
        '      setPasswordError(true);\n'
        '    }\n'
        '  };')
new6 = ('  const handlePasswordSubmit = async pwd => {\n'
        '    if (pwd === "SexyNight") {\n'
        '      setShowPasswordModal(false);\n'
        '      setPasswordError(false);\n'
        '      if (passwordTarget === "adults") setSkippedCat(true);\n'
        '      setSelectedSubcat(passwordTarget);\n'
        '      setGenreFilter(null);\n'
        '      setView("subcat");\n'
        '      if (!localStorage.getItem("dn_bio_id") && await biometricAvailable()) {\n'
        '        setShowBioOffer(true);\n'
        '      }\n'
        '    } else {\n'
        '      setPasswordError(true);\n'
        '    }\n'
        '  };\n'
        '  const activateFaceId = async () => {\n'
        '    setShowBioOffer(false);\n'
        '    try { await registerBiometric(); } catch {}\n'
        '  };')
if old6 in c:
    c = c.replace(old6, new6, 1); ok.append('6. handlePasswordSubmit ✓')
else:
    ok.append('6. handlePasswordSubmit NOT FOUND')

# ── 7. Add Bio Offer UI near password modal render ──────────────────────
old7 = 'showPasswordModal && /*#__PURE__*/React.createElement(PasswordModal, {\n    onSubmit: handlePasswordSubmit,\n    onClose: () => {\n      setShowPasswordModal(false);'
new7 = ('showBioOffer && /*#__PURE__*/React.createElement("div", {\n'
        '    style: {position:"fixed",bottom:0,left:0,right:0,zIndex:9999,background:"#1a1520",borderTop:"1px solid rgba(201,168,76,0.3)",padding:"16px 20px calc(16px + env(safe-area-inset-bottom,0px))",direction:"rtl"}\n'
        '  }, /*#__PURE__*/React.createElement("div", {style:{color:"#e8d48f",fontSize:14,marginBottom:12,textAlign:"right"}}, "\U0001F44B \u05E8\u05D5\u05E6\u05D4 \u05DC\u05D4\u05E4\u05E2\u05D9\u05DC Face ID \u05DC\u05DB\u05E0\u05D9\u05E1\u05D4 \u05DE\u05D4\u05D9\u05E8\u05D4 \u05D1\u05E4\u05E2\u05DD \u05D4\u05D1\u05D0\u05D4?"),\n'
        '    /*#__PURE__*/React.createElement("div", {style:{display:"flex",gap:10}},\n'
        '      /*#__PURE__*/React.createElement("button", {onClick:activateFaceId,style:{flex:1,background:"rgba(201,168,76,0.15)",border:"1px solid rgba(201,168,76,0.4)",borderRadius:10,padding:"10px",color:"#e8d48f",cursor:"pointer",fontFamily:"DM Sans",fontSize:14}}, "\u2705 \u05DB\u05DF, \u05D4\u05E4\u05E2\u05DC"),\n'
        '      /*#__PURE__*/React.createElement("button", {onClick:()=>setShowBioOffer(false),style:{flex:1,background:"rgba(255,255,255,0.05)",border:"1px solid rgba(255,255,255,0.1)",borderRadius:10,padding:"10px",color:"rgba(255,255,255,0.45)",cursor:"pointer",fontFamily:"DM Sans",fontSize:14}}, "\u05DC\u05D0 \u05EA\u05D5\u05D3\u05D4")\n'
        '    )\n'
        '  ),\n'
        'showPasswordModal && /*#__PURE__*/React.createElement(PasswordModal, {\n    onSubmit: handlePasswordSubmit,\n    onClose: () => {\n      setShowPasswordModal(false);')
if old7 in c:
    c = c.replace(old7, new7, 1); ok.append('7. Bio offer UI ✓')
else:
    ok.append('7. Bio offer UI NOT FOUND')

with open(ROOT + r'\src.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

# ── 8. Update gifs.json with all files ──────────────────────────────────
files = sorted([f for f in os.listdir(ROOT + r'\GIF') if f.lower().endswith(('.gif','.webm'))])
with open(ROOT + r'\gifs.json', 'w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False)
ok.append(f'8. gifs.json updated ({len(files)} files) ✓')

for line in ok:
    print(line)
print('Done')
