import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r'C:\Alon\Claude\DateNight\Netlify\src.html'

with open(SRC, encoding='utf-8', newline='\n') as f:
    c = f.read()

# ── Updates: (old_link_or_dishes, new_content) per entry ──────────────────

# Helper: add/replace phone field after 'link:' line, and update link/dishes
def update_entry(content, entry_id, phone=None, link=None, dishes=None):
    changes = 0
    id_pat = rf'(  id: {entry_id},\n)'
    if entry_id not in [6, 9]:  # skip those with null phone
        pass

    # Update link
    if link:
        # Find the link line for this entry
        # Pattern: within the block starting with 'id: X,'
        # We'll do a targeted replacement
        pass

    return content, changes

# ── Direct targeted replacements ──────────────────────────────────────────
updates = 0

def rep(old, new, label):
    global c, updates
    if old in c:
        c = c.replace(old, new, 1)
        updates += 1
        print(f'  ✓ {label}')
    else:
        print(f'  ✗ NOT FOUND: {label}')

# ── RESTAURANTS ────────────────────────────────────────────────────────────

# 1. Nam
rep(
    '  dishes: ["פאד תאי", "מנגו קרי", "טוניאה"],\n  why: "שפים תאילנדיים אמיתיים + חומרי בלי שמגדלים בעצמם",\n  source: "Rest.co.il",\n  link: "https://namrestaurant.co.il"',
    '  phone: "03-6708050",\n  dishes: ["קארי מאסאמן", "פאד תאי בקר", "קארי ירוק"],\n  why: "שפים תאילנדיים אמיתיים + חומרי גלם שמגדלים בעצמם",\n  source: "Rest.co.il",\n  link: "https://namrestaurant.co.il"',
    'Nam phone+dishes'
)

# 2. Taizu
rep(
    '  dishes: ["דינסאה", "סשימי", "קארי ירוק"],\n  why: "אחת המסעדות הטובות בארץ! אסיה במיטבה",\n  source: "TimeOut",\n  link: "https://www.taizu.co.il"',
    '  phone: "03-5225005",\n  dishes: ["טרטר טאיזו בקונוסי אורז פריך", "הר גאו שרימפס", "פוט סטיקרס"],\n  why: "אחת המסעדות הטובות בארץ! אסיה במיטבה",\n  source: "TimeOut",\n  link: "https://www.taizu.co.il"',
    'Taizu phone+dishes'
)

# 3. Magazino
rep(
    '  dishes: ["פסטות טריות", "פיצה", "ריזוטו"],\n  why: "נוף לים + פסטה מעולה",\n  source: "Rest",\n  link: "https://www.magazino.co.il"',
    '  phone: "03-7570535",\n  dishes: ["קרבונרה", "פפרדלה אונטריב", "פיצת פטריות"],\n  why: "נוף לים + פסטה מעולה",\n  source: "Rest",\n  link: "https://www.magazzino.co.il"',
    'Magazino phone+dishes+link'
)

# 4. Amura Mio
rep(
    '  dishes: ["אנטיפסטי", "פסטות", "דגים"],\n  why: "אלגנטי ורומנטי במיוחד",\n  source: "Rest",\n  link: "https://www.instagram.com/amuramio"',
    '  phone: "03-5244040",\n  dishes: ["פסטה ארביאטה", "ניוקי פיורלה עם רוקפור", "פיצה 4 גבינות"],\n  why: "אלגנטי ורומנטי במיוחד",\n  source: "Rest",\n  link: "https://amoremio.co.il"',
    'Amura Mio phone+dishes+link'
)

# 5. Goshen
rep(
    '  dishes: ["מנות ישראליות", "בשרים", "דגים"],\n  why: "ביתי וחם! כמו לאכול אצל סבתא",\n  source: "Rest",\n  link: "https://www.instagram.com/goshen.tlv"',
    '  phone: "03-5600766",\n  dishes: ["קרפצ\'יו סינטה", "ספייר ריבס", "פילה בקר"],\n  why: "ביתי וחם! כמו לאכול אצל סבתא",\n  source: "Rest",\n  link: "https://goshentlv.co.il"',
    'Goshen phone+dishes+link'
)

# 7. Fifty and One
rep(
    '  dishes: ["טורטליני 76₪", "קאצ\'ו א פאפה 68₪"],\n  why: "כל המחוזות של איטליה בצלחת!",\n  source: "Time Out",\n  link: "https://www.instagram.com/fiftyandonetlv"',
    '  phone: "054-8975918",\n  dishes: ["טורטליני במילוי תירס", "פסטה קרועה עם קרם דלעת ופטה", "רביולי ניו זילנדי"],\n  why: "כל המחוזות של איטליה בצלחת!",\n  source: "Time Out",\n  link: "https://www.instagram.com/fifty.and.one"',
    'Fifty and One phone+dishes'
)

# 8. HaBasta
rep(
    '  dishes: ["בורקס סרטנים"],\n  why: "הגינה הכי יפה!",\n  source: "Time Out",\n  link: "https://www.habasta.co.il"',
    '  phone: "03-5169234",\n  dishes: ["קלמרי פלנצ\'ה", "שיפוד דג ים על פחמים", "שווארמה חזיר"],\n  why: "הגינה הכי יפה!",\n  source: "Time Out",\n  link: "https://www.habasta.co.il"',
    'HaBasta phone+dishes'
)

# 9. Jasmino - only update dishes (no phone/link found)
rep(
    '  dishes: ["פיתה לב חריף", "פיתה שקדי עגל"],\n  why: "הפיתות הכי טובות בארץ!",',
    '  dishes: ["קבב בפיתה", "נקניקייה פיקנטית תוצרת בית", "פיתה שקדי עגל"],\n  why: "הפיתות הכי טובות בארץ!",',
    'Jasmino dishes'
)

# 10. Mentanten
rep(
    '  dishes: ["ראמן טונקוצו"],\n  why: "מתכון מהור 3 מטוקיו!",\n  source: "Mako",\n  link: "https://www.instagram.com/mantantan.tlv"',
    '  phone: "03-6725318",\n  dishes: ["טונגארה ראמן - ציר חזיר", "קארה ראמן - ציר קארי יפני", "גיוזה תוצרת בית"],\n  why: "מתכון מהור 3 מטוקיו!",\n  source: "Mako",\n  link: "https://www.mentententlv.com"',
    'Mentanten phone+dishes+link'
)

# 11. Asif
rep(
    '  dishes: ["מנות יצירתיות"],\n  why: "ספרייה אינטימית!",\n  source: "Time Out",\n  link: "https://www.instagram.com/asif.tlv"',
    '  phone: "03-3752727",\n  dishes: ["כבד קצוץ על הגריל עם חזרת", "מרגז עם יוגורט חציל ואריסה", "סלט נחמה ריבלין"],\n  why: "ספרייה אינטימית!",\n  source: "Time Out",\n  link: "https://asif.org"',
    'Asif phone+dishes+link'
)

# 12. Dok
rep(
    '  dishes: ["יינתיכוני"],\n  why: "הגינה ביום חמאה = מושלם",\n  source: "Time Out",\n  link: "https://www.instagram.com/doc.tlv"',
    '  phone: "03-6098118",\n  dishes: ["קולורבי אפוי בפחם", "מטפונה טלה", "חמאה מותססת עם בייגל"],\n  why: "הגינה ביום חמאה = מושלם",\n  source: "Time Out",\n  link: "https://dok.haachim.co.il"',
    'Dok phone+dishes+link'
)

# ── BARS ───────────────────────────────────────────────────────────────────

# 102. Juno
rep(
    '  why: "120 סוגי יין + אוכל איטלקי פשוט ומצוין. תמיד מלא!",\n  source: "כלכליסט + השולחן",\n  link: "https://www.junowine.co.il"',
    '  phone: "03-5446620",\n  dishes: ["פרוסקו איטלקי", "יין אדום בכוס מהתפריט המתחלף", "אנטיפסטו"],\n  why: "120 סוגי יין + אוכל איטלקי פשוט ומצוין. תמיד מלא!",\n  source: "כלכליסט + השולחן",\n  link: "https://www.junowine.co.il"',
    'Juno phone+drinks'
)

# 103. Bosser
rep(
    '  why: "יבואנים קטניים ונהירים. אין הזמנת מקומות - בהצלחה!",\n  source: "Time Out + כלכליסט",\n  link: "https://www.instagram.com/bosser.wine"',
    '  phone: "054-7273443",\n  dishes: ["יינות טבעיים ממיקבים קטנים", "יינות בוטיק ישראליים", "יין מהמקרר הסודי"],\n  why: "יבואנים קטניים ונהירים. אין הזמנת מקומות - בהצלחה!",\n  source: "Time Out + כלכליסט",\n  link: "https://www.instagram.com/bosser.wine"',
    'Bosser phone+drinks'
)

# 104. Brix
rep(
    '  why: "השקט של כיכר בגעון + יין במחיר הגון + רושפלד!",\n  source: "Time Out רומנטי",\n  link: "https://www.instagram.com/brix.tlv"',
    '  phone: "050-8855796",\n  dishes: ["יינות מיקבים קטנים מכל העולם בכוסות", "יינות אורגניים ובאיו-דינמיים", "מנות אוכל עם יין"],\n  why: "השקט של כיכר בגעון + יין במחיר הגון + רושפלד!",\n  source: "Time Out רומנטי",\n  link: "https://brixwinebar.co.il"',
    'Brix phone+drinks+link'
)

# 105. Cote
rep(
    '  why: "230 יינות + השף אילייה גולדמן. סטייל אירופאי אמיתי",\n  source: "Ynet + Visit2Israel",\n  link: "https://www.instagram.com/cote_tlv"',
    '  phone: "050-8811218",\n  dishes: ["יינות נבחרים בכוס", "צלחת גבינות עם ריבת בצל", "סלט קיסר קריספי"],\n  why: "230 יינות + השף אילייה גולדמן. סטייל אירופאי אמיתי",\n  source: "Ynet + Visit2Israel",\n  link: "https://www.instagram.com/cote_tlv"',
    'Cote phone+drinks'
)

# 106. Gazzetta
rep(
    '  why: "קפיצה לאיטליה! יושבים על הרחוב עם טאפס",\n  source: "Secret TLV + Visit2Israel",\n  link: "https://www.instagram.com/gazzetta_tlv"',
    '  phone: "03-6202077",\n  dishes: ["יינות איטלקיים ועולמיים בכוסות", "ורמוטים", "טאפסים איטלקיים"],\n  why: "קפיצה לאיטליה! יושבים על הרחוב עם טאפס",\n  source: "Secret TLV + Visit2Israel",\n  link: "https://www.gazzetta.co.il"',
    'Gazzetta phone+drinks+link'
)

# 107. Bar 51
rep(
    '  why: "המקום הכי סקסי בתל אביב. אנייליוטי שמן זית אגדי!",\n  source: "Time Out רומנטי",\n  link: "https://www.bar51.co.il"',
    '  phone: "03-5406680",\n  dishes: ["קוקטיילים עונתיים של השף", "יינות בוטיק בכוסות", "מנות קטנות"],\n  why: "המקום הכי סקסי בתל אביב. אנייליוטי שמן זית אגדי!",\n  source: "Time Out רומנטי",\n  link: "https://www.bar51tlv.com"',
    'Bar 51 phone+drinks+link'
)

# 108. Bob - update instagram link + drinks
rep(
    '  why: "Happy Hour 18:00-20:00 עם 30% הנחה. אירופה בת״א!",\n  source: "Ynet + Time Out",\n  link: "https://www.instagram.com/bob.tlv"',
    '  dishes: ["יינות עד 170₪ לבקבוק", "צלחת גבינות ופרושוטו", "פטה כבד"],\n  why: "Happy Hour 18:00-20:00 עם 30% הנחה. אירופה בת״א!",\n  source: "Ynet + Time Out",\n  link: "https://www.instagram.com/bobtlv"',
    'Bob drinks+link'
)

# 110. Fleur - update instagram link + drinks
rep(
    '  why: "יינות טבעיים מרתקים + אווירה משוחררת",\n  source: "Secret TLV + Ynet",\n  link: "https://www.instagram.com/fleur.tlv"',
    '  dishes: ["יינות טבעיים מהארץ ומהעולם", "מנות קלות עונתיות", "אפרטיבו עם 30% הנחה עד 19:00"],\n  why: "יינות טבעיים מרתקים + אווירה משוחררת",\n  source: "Secret TLV + Ynet",\n  link: "https://www.instagram.com/flor.telaviv"',
    'Fleur drinks+link'
)

# 111. Romia
rep(
    '  why: "חצר יפהפייה בשוק! רק בישראל זה נראה טבעי",\n  source: "Ynet",\n  link: "https://www.instagram.com/romia.tlv"',
    '  phone: "054-3929299",\n  dishes: ["יינות ישראליים של יקב טוליפ", "יינות עולם קלאסיים", "מנות ים-תיכוניות קטנות"],\n  why: "חצר יפהפייה בשוק! רק בישראל זה נראה טבעי",\n  source: "Ynet",\n  link: "https://rumiyah.co.il"',
    'Romia phone+drinks+link'
)

# 113. HaBosser HaHadash - add drinks
rep(
    '  why: "יינות מספרה וצרפת שלא תמצאו בשום מקום אחר",\n  source: "השולחן",\n  link: "https://www.instagram.com/bosser.wine"',
    '  phone: "054-7273443",\n  dishes: ["יינות טבעיים ממיקבים קטנים", "קפה ספיישלטי", "גבינות ונשנושים"],\n  why: "יינות מספרה וצרפת שלא תמצאו בשום מקום אחר",\n  source: "השולחן",\n  link: "https://www.instagram.com/bosser.wine"',
    'HaBosser HaHadash phone+drinks'
)

# 115. Terza
rep(
    '  why: "נרות לבנים, שולחנות עץ והראמן של 2025!",\n  source: "Time Out רומנטי",\n  link: "https://www.instagram.com/terza.tlv"',
    '  phone: "050-2091887",\n  dishes: ["מעל 40 יינות בכוס המתחלפים יומית", "יינות ישראליים ועולמיים נדירים", "מנות מהמטבח הישראלי"],\n  why: "נרות לבנים, שולחנות עץ והראמן של 2025!",\n  source: "Time Out רומנטי",\n  link: "https://www.ocdtlv.com/tirza"',
    'Terza phone+drinks+link'
)

# 116. El Vecino
rep(
    '  why: "ישיבה בחוץ על הירקון + סטייק סינטה מעולה!",\n  source: "Time Out רומנטי",\n  link: "https://www.instagram.com/elvecino.tlv"',
    '  phone: "03-5460679",\n  dishes: ["יינות בוטיק ישראליים", "יינות מיובאים", "גבינות מעדניית בוטיק"],\n  why: "ישיבה בחוץ על הירקון + סטייק סינטה מעולה!",\n  source: "Time Out רומנטי",\n  link: "https://elvecino.co.il"',
    'El Vecino phone+drinks+link'
)

# 117. Cassata - update instagram + add drinks
rep(
    '  why: "יין + גלידה = גאוני! אווירה ומוסיקה מנצחות",\n  source: "Secret TLV",\n  link: "https://www.instagram.com/cassata.tlv"',
    '  dishes: ["גלידה שוקולד שחור עם רוזמרין", "יינות מתחלפים", "קסטה תוצרת בית"],\n  why: "יין + גלידה = גאוני! אווירה ומוסיקה מנצחות",\n  source: "Secret TLV",\n  link: "https://www.instagram.com/cassata.telaviv"',
    'Cassata drinks+link'
)

# 118. HaGefen - add phone + drinks
rep(
    '  why: "חצר עם צמחים! מבחר יינות מתעדכן כל הזמן",\n  source: "Secret TLV",\n  link: "https://www.instagram.com/thegefen.tlv"',
    '  phone: "058-6609025",\n  dishes: ["124 יינות ישראליים בלבד", "צלחת גבינות מקומיות", "מנות שוק פשפשים עונתיות"],\n  why: "חצר עם צמחים! מבחר יינות מתעדכן כל הזמן",\n  source: "Secret TLV",\n  link: "https://www.instagram.com/thegefen.tlv"',
    'HaGefen phone+drinks'
)

# 120. Croute - add phone + update instagram + drinks
rep(
    '  why: "תור מ-17:45! הופך למלאן-18:00. הכי שווה בעיר",\n  source: "TheMarker 2024",\n  link: "https://www.instagram.com/croute.tlv"',
    '  phone: "052-6410150",\n  dishes: ["מוסקדה לבן מעמק הלואר", "קברנה פרנק צרפתי", "יין טבעי יווני"],\n  why: "תור מ-17:45! הופך למלאן-18:00. הכי שווה בעיר",\n  source: "TheMarker 2024",\n  link: "https://www.instagram.com/croute_telaviv"',
    'Croute phone+drinks+link'
)

with open(SRC, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print(f'\nTotal updates: {updates}')
print('Done.')
