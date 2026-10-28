import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Alon\Claude\DateNight\Netlify\src.html', encoding='utf-8', newline='\n') as f:
    content = f.read()

changes = 0

# 1. Fix button text: 🔮 💦 ... 💦 → 🔮 ... 💦
old1 = '\U0001f52e \U0001f4a6 \u05d0\u05d9\u05da \u05d6\u05d4 \u05d9\u05d9\u05d2\u05de\u05e8 \u05d4\u05dc\u05d9\u05dc\u05d4? \U0001f4a6'
new1 = '\U0001f52e \u05d0\u05d9\u05da \u05d6\u05d4 \u05d9\u05d9\u05d2\u05de\u05e8 \u05d4\u05dc\u05d9\u05dc\u05d4? \U0001f4a6'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('1. Button text OK')
    changes += 1
else:
    print('1. ERROR button text not found')

# 2. Fix confirm button: green neon → flame neon (yellow-red)
old2 = 'border:2px solid rgba(0,255,120,0.6);color:#00ff88;font-size:36px;width:64px;height:64px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(0,255,120,0.5),0 0 40px rgba(0,255,120,0.25);animation:confirm-pulse 2s ease-in-out infinite'
new2 = 'border:2px solid rgba(255,160,0,0.7);color:#ffcc00;font-size:36px;width:64px;height:64px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(255,100,0,0.6),0 0 40px rgba(255,50,0,0.3);animation:confirm-pulse 2s ease-in-out infinite'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('2. Confirm button color OK')
    changes += 1
else:
    print('2. ERROR confirm button not found')

old2b = '0%,100%{box-shadow:0 0 20px rgba(0,255,120,0.5),0 0 40px rgba(0,255,120,0.25)}50%{box-shadow:0 0 32px rgba(0,255,120,0.8),0 0 60px rgba(0,255,120,0.4)}'
new2b = '0%,100%{box-shadow:0 0 20px rgba(255,100,0,0.6),0 0 40px rgba(255,50,0,0.3)}50%{box-shadow:0 0 32px rgba(255,140,0,0.9),0 0 60px rgba(255,60,0,0.5)}'
if old2b in content:
    content = content.replace(old2b, new2b, 1)
    print('2b. Keyframe OK')
    changes += 1
else:
    print('2b. ERROR keyframe not found')

# 3. Move 💦 button from pose-name-row to next to dg-desc
# Remove from pose-name-row: unwrap to just pose-name, remove the button
old3 = ('<div class=\\"pose-name-row\\">\\n'
        '        <div class=\\"pose-name\\" id=\\"dg-pose-name\\"></div>\\n'
        '        <button class=\\"btn-gif-pose\\" onclick=\\"DiceGameApp.rollEnding()\\">\U0001f4a6</button>\\n'
        '      </div>')
new3 = '<div class=\\"pose-name\\" id=\\"dg-pose-name\\"></div>'
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('3a. Removed from name-row OK')
    changes += 1
else:
    print('3a. ERROR pose-name-row not found')

# Add 💦 button on the opposite side of dg-desc (right side, since desc is LTR/left)
old4 = '<div id=\\"dg-desc\\" class=\\"pose-desc\\"></div>'
new4 = ('<div class=\\"desc-row\\">\\n'
        '        <button class=\\"btn-gif-pose\\" onclick=\\"DiceGameApp.rollEnding()\\">\U0001f4a6</button>\\n'
        '        <div id=\\"dg-desc\\" class=\\"pose-desc\\"></div>\\n'
        '      </div>')
if old4 in content:
    content = content.replace(old4, new4, 1)
    print('3b. Added to desc-row OK')
    changes += 1
else:
    print('3b. ERROR dg-desc not found')

print(f'Total changes: {changes}')

with open(r'C:\Alon\Claude\DateNight\Netlify\src.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Saved')
