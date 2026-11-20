import json,re,collections,hashlib,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];load=lambda p:json.loads(p.read_text());bank=load(root/'dist/quotes.json');seed=load(root/'sources/seed-quotes.json')
assert len(bank)==6000
assert collections.Counter(q['kind'] for q in bank)==dict.fromkeys(['原創觀點','古典短句','文學節選','古詩'],1500)
assert all(bank[q['id']]['quote']==q['quote'] for q in seed)
baseline=load(root/'sources/library-4000.json')
assert all(all(q[k]==baseline[q['id']][k] for k in ['id','quote','kind','category','source']) for q in bank[:4000])
assert sum(bool(q.get('curated')) for q in bank)==100
assert sum(bool((q.get('workplaceDialogue') or q.get('dialogue',{})).get('tones')) for q in bank)==1000
assert sum(bool(q.get('workplace')) for q in bank)==500
assert sum(bool(q.get('parenting')) for q in bank)==500
assert all(q['dialogue'].get('ageRange') and q['dialogue'].get('child') and q['dialogue'].get('guidance') for q in bank if q.get('parenting'))
assert len({re.sub(r'[^\u3400-\u9fff]','',q['quote']).replace('衆','眾').replace('隣','鄰') for q in bank})==6000
paragraphs={}
def walk(o,out):
 if isinstance(o,dict):
  if 'paragraphs' in o:out.update(o['paragraphs'])
  for v in o.values():walk(v,out)
 elif isinstance(o,list):
  for v in o:walk(v,out)
for q in bank:
 if not q.get('corpusFile'):continue
 f=q['corpusFile']
 if f not in paragraphs:
  paragraphs[f]=set();walk(load(root/'sources'/f),paragraphs[f])
 assert q['sourceText'] in paragraphs[f]
 assert q['sourceText'][q['sourceStart']:q['sourceEnd']]==q['quote']
 assert all(q['quote'].count(a)==q['quote'].count(b) for a,b in [('「','」'),('『','』'),('“','”')])
 assert q['sourceCommit'] in q['url']
report=load(root/'dist/library-report.json');assert report['contentHash']==hashlib.sha256((root/'dist/quotes.json').read_bytes()).hexdigest()
with zipfile.ZipFile(root/'dist/shiju-offline.zip') as z:
 assert z.read('拾句離線版.html')==(root/'dist/shiju-offline.html').read_bytes()
 assert b'JackeyGao' in z.read('來源授權.txt')
 assert json.loads(z.read('句庫說明.json'))['total']==6000
print('PASS: 6000 unique entries, 1500/type; preserved IDs; each new excerpt matches retained corpus and source span; balanced quotations; report hash; offline ZIP and license.')
