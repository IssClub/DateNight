import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Alon\Claude\DateNight\Netlify\src.html', encoding='utf-8', newline='\n') as f:
    content = f.read()

# 1. Add 💦 to button text
old1 = '\U0001F52E \u05d0\u05d9\u05da \u05d6\u05d4 \u05d9\u05d9\u05d2\u05de\u05e8 \u05d4\u05dc\u05d9\u05dc\u05d4?'
new1 = '\U0001F52E \U0001F4A6 \u05d0\u05d9\u05da \u05d6\u05d4 \u05d9\u05d9\u05d2\u05de\u05e8 \u05d4\u05dc\u05d9\u05dc\u05d4? \U0001F4A6'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('1. Button emoji OK')
else:
    print('1. ERROR: button text not found')

# 2. Replace X close button with bottom confirm button in ending overlay
# Remove top-left X button and add bottom confirm button
old2 = ('<div id=\\"dg-ending-overlay\\">\\n'
        '  <button class=\\"btn-close-ending\\" onclick=\\"DiceGameApp.closeEnding()\\">\u2715</button>\\n'
        '  <div id=\\"dg-ending-media\\"></div>\\n'
        '</div>')
new2 = ('<div id=\\"dg-ending-overlay\\">\\n'
        '  <div id=\\"dg-ending-media\\"></div>\\n'
        '  <button class=\\"btn-confirm-ending\\" onclick=\\"DiceGameApp.closeEnding()\\">\u2705</button>\\n'
        '</div>')
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('2. Overlay button OK')
else:
    print('2. ERROR: overlay not found')

# 3. Wrap pose-name with 💦 button on the right
old3 = '      <div class=\\"pose-name\\" id=\\"dg-pose-name\\"></div>'
new3 = ('      <div class=\\"pose-name-row\\">\\n'
        '        <div class=\\"pose-name\\" id=\\"dg-pose-name\\"></div>\\n'
        '        <button class=\\"btn-gif-pose\\" onclick=\\"DiceGameApp.rollEnding()\\">\U0001F4A6</button>\\n'
        '      </div>')
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('3. Pose name row OK')
else:
    print('3. ERROR: pose-name not found')

with open(r'C:\Alon\Claude\DateNight\Netlify\src.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Saved')
