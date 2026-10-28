import pandas as pd
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXCEL_PATH = 'C:/Alon/Claude/DateNight/Netlify/365/Description.xlsx'
JSON_PATH  = 'C:/Alon/Claude/DateNight/Netlify/poses-data.json'

df = pd.read_excel(EXCEL_PATH, header=None, dtype=str)
df.columns = ['pose_num', 'name', 'description', 'male_benefits',
              'female_benefits', 'hot_tip', 'difficulty']
data_rows = df.iloc[1:]  # skip header

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    poses = json.load(f)

# Match by pose NUMBER (column A) — most reliable
num_to_idx = {p['num']: i for i, p in enumerate(poses)}

updated, skipped, no_match = 0, 0, []

def val(cell):
    s = str(cell).strip()
    return None if s.lower() in ('nan', 'none', '') else s

for _, row in data_rows.iterrows():
    num_str = val(row['pose_num'])
    if num_str is None:
        skipped += 1
        continue
    try:
        num = int(float(num_str.replace('#', '').strip()))
    except:
        skipped += 1
        continue

    if num not in num_to_idx:
        no_match.append(num_str)
        continue

    pose = poses[num_to_idx[num]]

    name            = val(row['name'])
    description     = val(row['description'])
    male_benefits   = val(row['male_benefits'])
    female_benefits = val(row['female_benefits'])
    hot_tip         = val(row['hot_tip'])
    difficulty_raw  = val(row['difficulty'])

    if name            is not None: pose['name']            = name
    if description     is not None: pose['description']     = description
    if male_benefits   is not None: pose['male_benefits']   = male_benefits
    if female_benefits is not None: pose['female_benefits'] = female_benefits
    if hot_tip         is not None: pose['hot_tip']         = hot_tip
    if difficulty_raw  is not None:
        try:    pose['difficulty'] = int(float(difficulty_raw))
        except: pass

    updated += 1

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(poses, f, ensure_ascii=False, indent=2)

print(f'Poses updated : {updated}')
print(f'Rows skipped  : {skipped}')
print(f'No match      : {len(no_match)}')
if no_match:
    for n in no_match: print(f'  - {n}')
print('Done.')
