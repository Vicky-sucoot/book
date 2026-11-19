"""Reproducible 4,000-entry offline library. Corpus excerpts retain exact spans and pinned provenance."""
import json,re,hashlib,collections
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'sources';DIST=ROOT/'dist'
load=lambda f:json.loads((SRC/f).read_text())
bank=load('seed-quotes.json');commit=load('provenance.json')['commit'];repo='https://github.com/chinese-poetry/chinese-poetry'
cats=['說話的藝術','文化底蘊','知識見解','文字素養','好好說話'];kinds=['原創觀點','古典短句','文學節選','古詩']
def norm(t):return re.sub(r'[^\u3400-\u9fff]','',t).replace('衆','眾').replace('隣','鄰')
seen={norm(q['quote']) for q in bank};counts=collections.Counter(q['kind'] for q in bank)
def add(q):
 n=norm(q['quote'])
 if n in seen:return False
 q['id']=len(bank);bank.append(q);seen.add(n);counts[q['kind']]+=1;return True
# Newly composed situational observations are labeled as such, never attributed to historical authors.
contexts='''面對會議裡的分歧|合作夥伴調整需求|家人提出不同期待|朋友詢問你的意見|團隊討論工作分配|初次認識新朋友|與長輩分享新想法|同事對進度有疑問|朋友談起生活選擇|向新人介紹工作方式|討論一項共同決定|和伴侶安排日常生活|與鄰居協調公共空間|向客戶說明處理進度|和同學合作報告|參與讀書會討論|談到不熟悉的地方文化|交換彼此的旅行經驗|討論一本書的觀點|分享自己的學習經驗|處理群組裡的訊息落差|為活動安排徵求意見|討論需要改進的流程|向家人說明自己的安排|與朋友規劃共同活動|談及彼此的生活習慣|討論一則尚待確認的消息|聽見與自己不同的看法|在忙碌時協調一項請託|為新的合作建立共識|在討論中提出修改建議|聽取別人對作品的回饋|向熟人解釋一個新概念|和團隊回顧一次經驗|討論下一步行動'''.split('|')
# technique: statement, rationale, exercise, example response, tag, theme
techniques=[
('先確認彼此正在回答哪一個問題。','相同的主題可能包含不同的關切，釐清問題能減少各說各話。','把正在討論的問題縮成一句話。','我們現在要先決定時間，還是先確認要做哪些事？','澄清',0),
('把觀察說在前面，把判斷留待核對。','可核對的事情和對它的解釋應分開表達。','先描述一項看見的事，再說自己的推測。','我看到安排有改動，想確認是不是出現新的限制？','澄清',2),
('讓提問留得下不同的答案。','問題若預設只有一個正確答案，就難以聽見真正的想法。','把一個誘導問句改成開放問句。','你最在意的是哪個部分？我想先聽你的考量。','提問',0),
('先說明用詞，再交換立場。','詞義沒有對齊時，意見可能在誤會上越走越遠。','找一個雙方可能理解不同的詞，先說明意思。','你說的彈性，是指時間可調整，還是工作範圍可調整？','澄清',3),
('用一個具體例子，替抽象的說法落地。','例子能讓對方辨認你說的是哪一種情況。','為自己的主張補上一個生活例子。','我舉個實際情況，看看我們是不是在談同一件事。','文字表達',3),
('先交代目的，再補上必要的背景。','聽者知道你想達成什麼，才容易安排後續訊息的輕重。','用一句目的開場，再說兩項背景。','我想先和你確認安排，因為接下來有兩件事需要配合。','文字表達',0),
('承認還不知道的部分，讓理解有繼續生長的位置。','把不確定標清楚，對方才不會把猜測當作承諾。','說出目前知道與尚待確認的各一項。','目前我只確認了這一部分，其餘我查清楚後再回覆。','求證',2),
('分清楚別人的經驗與自己的推測。','推測可以提出，但需要保留被對方修正的空間。','用一句核對，代替對他人動機的結論。','我猜你在意的是時間不夠，這樣理解對嗎？','傾聽',4),
('給不同背景的人一個解釋自己的機會。','文化與生活經驗不能只用外部印象概括。','把對一群人的概括改成對眼前經驗的提問。','我對這個做法不熟悉，你願意說說它的意義嗎？','文化交流',1),
('引用之前，先替那句話找回情境。','原話的對象與背景，會影響它在新場合中的意義。','分享引言時，補上作者、作品與原本情境。','這句話的原來背景是這樣，我想用它討論其中一個面向。','文化交流',1),
('把不同意落在做法上，別落在人格上。','具體指出方案的問題，比給人貼標籤更有討論空間。','指出一項可調整的行為，不評斷對方人格。','我對這個步驟有疑慮，我們能一起看一下限制嗎？','不同意',4),
('說明自己的範圍，也聽見別人的限制。','各自能做什麼攤開來，合作才不需要依靠猜測。','列出一項可承擔與一項無法承擔的事。','我能負責前半部分，後半部分需要另外安排。你這邊呢？','界線',4),
('讓請求包含可以協商的餘地。','對方有機會評估能力與時間，請求才較容易被誠實回應。','說明需要、時間，並詢問對方是否方便。','如果時間允許，可以請你幫忙確認這一項嗎？不便也請告訴我。','請託',4),
('把答應的事情說到能被確認的程度。','明確的行動與時間，比熱心卻模糊的承諾更可靠。','將一個籠統承諾改成具體交付內容。','我會在明天下午三點前，把整理好的重點傳給你。','請託',0),
('先重述對方的重點，再往下接話。','重述是核對理解，不是替對方決定他應該怎麼想。','用自己的話重述，再請對方確認。','我先確認一下，你最擔心的是後續沒有足夠時間，對嗎？','傾聽',0),
('把感受說清楚，也把需要說具體。','說出感受之後提出可執行的請求，對方才知道如何回應。','用感受加具體請求改寫一句抱怨。','我有些不安，想先知道目前有哪些選項，可以一起確認嗎？','澄清',4),
('讓證據有來源，讓結論有範圍。','可信的判斷需要能追查的資訊，也需要說明適用條件。','為一個主張補上來源與一項限制。','這是我找到的原始資料，但它只涵蓋這段期間。','求證',2),
('先辨認共識，再把分歧縮到可以討論的大小。','共同目標能提供方向，具體分歧才有處理的入口。','寫下雙方同意的一項與仍待討論的一項。','我們都希望安排可行，目前不同的是時間，我們先談這一點。','不同意',2),
('給思考一個停頓，也給回覆一個時間。','需要整理不等於拒絕溝通，清楚約定能減少等待中的猜測。','需要暫停時，說明何時會回覆。','我想整理一下細節，今晚八點前回覆你，可以嗎？','界線',4),
('把長句拆開，讓每一步意思都有位置。','一口氣塞入多個重點，容易讓聽者錯過最需要處理的事。','將一段說明分成三個重點。','我分成三點說，先談目前狀況，再談限制，最後確認下一步。','文字表達',3),
('替他人的付出說出具體的名字。','具體肯定能讓對方知道哪一項努力被看見。','指出對方的一個行動與帶來的影響。','謝謝你先整理了差異，讓我們比較容易看見要討論的地方。','感謝',4),
('把一次經驗放回它適用的情況。','個人的成功經驗可以參考，但不必直接套成每個人的答案。','分享經驗時，補上當時的條件。','我曾在這個條件下試過，你現在的情況可能需要調整。','鼓勵',2),
('先聽懂一種生活，再決定如何比較。','比較若太早開始，可能只是在用熟悉的標準替陌生事物評分。','為陌生的習慣問一個不帶評價的問題。','這跟我的經驗不太一樣，我想先了解你們通常怎麼安排。','文化交流',1),
('留下可以修正的句子，也留下可以再談的關係。','用暫定語氣標示尚未完成的想法，可以邀請補充而非迫使站隊。','用一句話表達立場與願意修正的條件。','這是我目前的理解，如果有新的資訊，我們可以再調整。','不同意',0),
('結束之前，替下一步找一個清楚的起點。','結論需要轉成可做的動作，才不會停在一場說完就散的談話。','確認誰會在何時先完成哪一步。','我們先各自確認資料，週五再用十分鐘對一下結果。','請託',0)
]
assert len(contexts)==35 and len(techniques)==25
for context in contexts:
 for statement,rationale,exercise,response,tag,ci in techniques:
  text=context+'時，'+statement
  assert add(dict(kind='原創觀點',category=cats[ci],quote=text,source='拾句編輯室 · 情境原創',insight=rationale,exercise=exercise,tags=[tag],dialogue=dict(scene=context,before='我先說我的結論，你照這個方向處理就好。',after=response),editorialMethod='情境化原創短句；非歷史人物引言'))
assert counts['原創觀點']==1000
# Sentence boundaries and original spans are preserved for offline verification, including surrounding context.
def sentences(text):
 for m in re.finditer(r'[^。！？]+[。！？][」』”’]*',text):
  start=m.start()+len(m.group())-len(m.group().lstrip());end=m.end()
  # Trim quotation framing at a sentence boundary without altering any retained source characters.
  for left,right in [('「','」'),('『','』'),('“','”')]:
   t=text[start:end]
   if t.count(left)>t.count(right):start+=t.rfind(left)+1
   t=text[start:end]
   while t.count(right)>t.count(left) and t.endswith(right):end-=1;t=text[start:end]
  t=text[start:end]
  balanced=all(t.count(l)==t.count(r) for l,r in [('「','」'),('『','』'),('“','”')])
  if 14<=len(t)<=75 and balanced and not re.search(r'[□�【】\[\]0-9a-zA-Z]',t):yield t,start,end
def themed(text):
 rules=[('言語辭說問聽',0),('學知思疑察辨',2),('文書字詩筆',3),('仁義禮古民國俗',1)]
 scores=[(sum(text.count(c) for c in chars),i) for chars,i in rules];score,ci=max(scores)
 return ci if score else 4
candidates=[]
for file,book,author in [('mengzi.json','孟子','孟子及其弟子（傳統歸屬）'),('daxue.json','大學','曾子及其門人（傳統歸屬）'),('zhongyong.json','中庸','子思（傳統歸屬）')]:
 data=load(file);data=data if isinstance(data,list) else [data]
 for ch in data:
  for pi,para in enumerate(ch['paragraphs']):
   for text,start,end in sentences(para):
    score=sum(text.count(c) for c in '言學知思善仁義心禮信道誠君子')
    candidates.append((score,dict(kind='古典短句',quote=text,work=book+'·'+ch['chapter'] if book!=ch['chapter'] else book,author=author,corpusFile=file,corpusPath={'mengzi.json':'四书五经/mengzi.json','daxue.json':'四书五经/daxue.json','zhongyong.json':'四书五经/zhongyong.json'}[file],chapter=ch['chapter'],paragraph=pi,sourceText=para,sourceStart=start,sourceEnd=end)))
# Balanced round-robin chapters prevents the first book from consuming the entire library.
def interleave(items,key):
 groups=collections.defaultdict(list)
 for q in items:groups[key(q)].append(q)
 ordered=[]
 while groups:
  for k in list(groups):
   if groups[k]:ordered.append(groups[k].pop(0))
   if not groups[k]:del groups[k]
 return ordered
classic=interleave([q for score,q in sorted(candidates,key=lambda x:-x[0])],lambda q:q['chapter'])
guwen=[]
for vol in load('guwen.json')['content']:
 for art in vol['content']:
  for pi,para in enumerate(art['paragraphs']):
   for text,start,end in sentences(para):
    guwen.append(dict(kind='文學節選',quote=text,work=art['chapter'],author=art['author'].strip(),corpusFile='guwen.json',corpusPath='蒙学/guwenguanzhi.json',chapter=vol['title']+' / '+art['chapter'],paragraph=pi,sourceText=para,sourceStart=start,sourceEnd=end))
guwen.sort(key=lambda q:-sum(q['quote'].count(c) for c in '故夫善學知思言心義理文誠信仁德'))
prose=interleave(guwen,lambda q:q['work'])
poems=[]
for section in load('tang300.json')['content']:
 for art in section['content']:
  for pi,para in enumerate(art['paragraphs'][:4]):
   if 9<=len(para)<=65 and not re.search(r'[□�【】\[\]0-9a-zA-Z]',para):
    poems.append(dict(kind='古詩',quote=para,work=art['chapter']+(('·'+art['subchapter']) if art.get('subchapter') else ''),author=art['author'],corpusFile='tang300.json',corpusPath='蒙学/tangshisanbaishou.json',chapter=section['type']+' / '+art['chapter'],paragraph=pi,sourceText=para,sourceStart=0,sourceEnd=len(para)))
for file in ['tang1.json','tang0.json']:
 for art in load(file):
  para=art['paragraphs'][0] if art['paragraphs'] else ''
  if 9<=len(para)<=45 and not re.search(r'[□�【】\[\]0-9a-zA-Z]',para):poems.append(dict(kind='古詩',quote=para,work=art['title'],author=art['author'],corpusFile=file,corpusPath='全唐诗/poet.tang.'+('1000' if file=='tang1.json' else '0')+'.json',chapter=art['title'],paragraph=0,sourceText=para,sourceStart=0,sourceEnd=len(para)))
poems=interleave(poems,lambda q:q['work'])
base={c:next(q for q in bank if q['category']==c and q.get('dialogue')) for c in cats}
for kind,items in [('古典短句',classic),('文學節選',prose),('古詩',poems)]:
 for q in items:
  if counts[kind]>=1000:break
  ci=themed(q['quote']);q['category']=cats[ci];q['source']=q['author']+'《'+q['work']+'》';q['url']=repo+'/blob/'+commit+'/'+quote(q['corpusPath'],safe='/');q['sourceLocator']=q['chapter']+' · 第'+str(q['paragraph']+1)+'段';q['sourceCommit']=commit
  q['background']='本句節錄自《'+q['work']+'》。離線附有同段原文，可對照上下文閱讀；作者署名依所採電子底本，異文及歸屬仍以作品版本為準。'
  # These are reading prompts rather than invented literal translations or philological claims.
  if kind=='古詩':
   q['insight']='先讀出「'+q['quote']+'」的節奏，再辨認其中的景物、動作或情感。留意詩中所寫的畫面，與自己聯想到的意思有何不同。';q['exercise']='選出這句裡一個有畫面感的詞，不直接沿用詩句，寫一個今天的生活片段。'
  elif kind=='文學節選':
   q['insight']='把「'+q['quote']+'」放回同段原文，辨認它是在敘事、描景、對話，還是提出主張。節選的一句不能代替整篇文章的立場。';q['exercise']='用白話試述這句在段落中做了什麼，再寫下你還需要查證的一個字詞。'
  else:
   q['insight']='閱讀「'+q['quote']+'」時，先確認誰在說話、回應什麼問題，再區分原文的主張與今天的延伸。古典中的情境不必直接當成現代生活的規則。';q['exercise']='對照同段原文，寫下一個你認同的觀點或想追問的問題，並說明理由。'
  q['readingGuide']=True;q['tags']=base[cats[ci]]['tags'];q['dialogue']=base[cats[ci]]['dialogue'].copy();q['dialogue']['scene']='延伸練習：'+q['dialogue']['scene'];add(q)
 assert counts[kind]==1000,(kind,counts[kind])
assert len(bank)==4000 and len(seen)==4000
for q in bank:
 if q.get('corpusFile'):assert q['sourceText'][q['sourceStart']:q['sourceEnd']]==q['quote']
(DIST/'quotes.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n')
report={'total':len(bank),'byKind':dict(counts),'cycleDays':200,'dailyPerKind':5,'sourceRepository':repo,'sourceCommit':commit,'newOriginals':'875 則情境化原創短句（35 個情境 × 25 項表達方法），加上原有 125 則。','newExcerpts':'依電子底本句界擷取、去重；提供閱讀提示與同段原文，並非逐句人工校勘或白話翻譯。','contentHash':hashlib.sha256((DIST/'quotes.json').read_bytes()).hexdigest()}
(DIST/'library-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
