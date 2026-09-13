import urllib.request
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_cast(show_id):
    req = urllib.request.Request(f'https://api.tvmaze.com/shows/{show_id}/cast', headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

tvd_cast = fetch_cast(63)
originals_cast = fetch_cast(62)

all_cast = tvd_cast + originals_cast

targets = {
    'klaus': ['Klaus', 'Joseph Morgan'],
    'elijah': ['Elijah', 'Daniel Gillies'],
    'rebekah': ['Rebekah', 'Claire Holt'],
    'alaric': ['Alaric', 'Matt Davis', 'Matthew Davis'],
    'tyler': ['Tyler', 'Michael Trevino'],
    'jeremy': ['Jeremy', 'Steven R. McQueen', 'Steven McQueen'],
    'damon': ['Damon', 'Ian Somerhalder'],
    'stefan': ['Stefan', 'Paul Wesley'],
    'elena': ['Elena', 'Nina Dobrev'],
    'katherine': ['Katherine', 'Katerina'],
    'caroline': ['Caroline', 'Candice King', 'Candice Accola'],
    'bonnie': ['Bonnie', 'Kat Graham', 'Katerina Graham'],
    'enzo': ['Enzo', 'Michael Malarkey']
}

found = {}

for member in all_cast:
    person = member.get('person', {})
    character = member.get('character', {})
    p_name = person.get('name', '')
    c_name = character.get('name', '')
    
    # Priority: character image > person image
    c_img = (character.get('image') or {}).get('original') or (character.get('image') or {}).get('medium')
    p_img = (person.get('image') or {}).get('original') or (person.get('image') or {}).get('medium')
    img_url = c_img or p_img
    
    for key, terms in targets.items():
        if key not in found or not found[key]['is_char_img']:
            if any(term.lower() in p_name.lower() or term.lower() in c_name.lower() for term in terms):
                if img_url:
                    found[key] = {
                        'person': p_name,
                        'char': c_name,
                        'url': img_url,
                        'is_char_img': bool(c_img)
                    }

print(f"Matched {len(found)} characters:")
for key, data in found.items():
    print(f"[{key}] {data['person']} as {data['char']}: {data['url']}")
    dest = os.path.join('static', 'img', f"{key}.jpg")
    try:
        req_img = urllib.request.Request(data['url'], headers=headers)
        with urllib.request.urlopen(req_img) as img_resp, open(dest, 'wb') as f:
            f.write(img_resp.read())
        print(f"  -> Saved {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"  -> Error {key}: {e}")
