"""Append to the 4,000-entry baseline; existing IDs, text and editorial fields stay stable."""
from pathlib import Path
import ast,json,re,collections,hashlib
from urllib.parse import quote as encode
root=Path(__file__).resolve().parents[1];src=root/'sources';dist=root/'dist';load=lambda f:json.loads((src/f).read_text())
helpers={"re":re,"collections":collections};tree=ast.parse((root/'scripts/expand-library.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['norm','sentences','themed','interleave']],type_ignores=[]),'<corpus helpers>','exec'),helpers)
norm,sentences,themed,interleave=[helpers[k] for k in ['norm','sentences','themed','interleave']]
bank=load('library-4000.json');assert len(bank)==4000;seen={norm(q['quote']) for q in bank};counts=collections.Counter(q['kind'] for q in bank);cats=['說話的藝術','文化底蘊','知識見解','文字素養','好好說話'];commit=load('provenance.json')['commit'];repo='https://github.com/chinese-poetry/chinese-poetry'
def add(q):
 if norm(q['quote']) in seen:return False
 q['id']=len(bank);bank.append(q);seen.add(norm(q['quote']));counts[q['kind']]+=1;return True
# Scene, ages, child's words, reflexive adult response, concern, next step, two choices, boundary.
scenes=[
('孩子不想開始寫功課','6–12 歲','我不想寫，太難了。','不要拖，快點寫。','不知道怎麼開始','一起看第一題','先讀題目','先找一題會做的','今天要安排一段練習時間'),
('孩子輸了遊戲很生氣','4–9 歲','我不要玩了，這不公平。','輸一次就這樣，真沒用。','很想贏卻沒有贏','先把遊戲放下來','喝一口水','坐一下再說','生氣時也不能打人'),
('孩子不願收玩具','3–7 歲','我還要玩，不要收。','不收我就全丟掉。','還沒準備好結束','先把積木放進盒子','先收積木','先收小車','走道需要留出可以通行的空間'),
('孩子被同學拒絕一起玩','6–12 歲','他們都不想跟我玩。','一定是你做了什麼。','被拒絕後很難過','先把事情經過說完','先讓我陪著','一起想下一次的邀請','別人可以拒絕邀請，你的感受也值得被聽見'),
('孩子擔心考試表現','9–15 歲','我一定考不好。','別想太多，考好就好了。','擔心努力沒有結果','一起看最需要準備的一小部分','先整理一個重點','先休息再訂計畫','成績不決定你值不值得被關心'),
('孩子抗拒關掉螢幕','6–12 歲','再五分鐘，我還沒結束。','你就是只會玩手機。','活動還沒有完成','確認目前活動可以停在哪裡','存檔後關掉','記下進度後關掉','今天約定的螢幕時間需要結束'),
('手足爭搶同一件物品','4–10 歲','是我先拿的，不給他。','你比較大，就讓給他。','擔心自己的使用機會被拿走','先讓雙方各說一次需要','訂一個輪流順序','先各選另一件物品','不能用搶奪或推人解決'),
('孩子打翻飲料','3–8 歲','不是故意的，你不要罵我。','怎麼又是你，笨手笨腳。','怕被責怪','先把杯子移到安全處','拿抹布擦桌面','幫忙把乾物品移開','需要一起把現場整理好'),
('孩子不想向親友打招呼','3–8 歲','我不想抱抱。','沒禮貌，人家都等你了。','對接觸感到不自在','確認你願意的問候方式','揮揮手','說一聲你好','不需要勉強身體接觸，也可以用其他方式問候'),
('孩子不願分享學校的事','9–15 歲','沒什麼，不想說。','問你什麼都不講。','想保留一點自己的空間','先說明我願意聽','晚點再聊','先一起做別的事','你可以保留隱私，遇到需要協助的事也能來找我'),
('孩子因作業出錯而自責','6–12 歲','我就是很笨。','這麼簡單還不會。','把一次錯誤當成對自己的評價','一起找到剛才卡住的步驟','先看一個例子','先指出哪裡不懂','錯誤可以修正，不需要用難聽的話定義自己'),
('孩子拖延準備出門','4–9 歲','我還沒好，不要催。','每次都是你害大家遲到。','還不清楚要先做什麼','先確認下一個出門步驟','先穿鞋','先拿水壺','出發時間到了，需要一起完成準備'),
('孩子提出不同的興趣選擇','9–15 歲','我想學這個，不想照你的安排。','我都是為你好，不准反對。','希望自己的想法被認真看待','一起了解這個選擇需要什麼','先查課程內容','先談時間與費用','需要一起考量時間、資源和你的意願'),
('孩子想獨自嘗試新任務','6–12 歲','讓我自己來。','你弄不好，我來就好。','希望有自己嘗試的機會','確認哪一部分想自己做','我在旁邊等你需要幫忙','你先試一個步驟','涉及安全的部分需要先一起確認'),
('孩子覺得大人沒有聽自己說話','6–15 歲','你都不聽我說。','大人說話你就聽。','希望自己的話被完整聽見','先放下手邊的事聽你說','現在先聽兩分鐘','約定一個我能專心的時間','我也會說明自己的時間，並照約定回來聽'),
('孩子被比較後感到受傷','6–15 歲','你只覺得別人比較好。','我是要你有上進心。','覺得自己的努力沒有被看見','先聽你說這句話帶來的感受','談一件你最近付出的努力','一起找自己的下一個小目標','我們討論你的需要，不拿別人當作你的標準'),
('孩子弄壞別人的東西','6–12 歲','我不敢跟他說。','你自己去道歉，不要丟我的臉。','害怕面對造成的影響','一起確認發生了什麼與可以修補的部分','先練習說明經過','一起討論合理的修補方式','需要承認影響並參與修補，不用羞辱自己'),
('孩子與家長意見僵持','9–15 歲','反正你都已經決定了。','不准頂嘴，沒有討論的餘地。','覺得自己沒有參與討論','先把可以討論與不能改變的部分分開','先聽你的方案','先一起列出限制','有些限制需要保留，但你的想法仍值得說明'),
('家長說重話後想修補關係','4–15 歲','你剛才的話讓我很難過。','誰叫你不聽話。','受到言語傷害後需要被承認','先為剛才說重話承擔責任','先聽你的感受','我先說明接下來會怎麼調整','大人也需要為自己的言語負責'),
('孩子遇到困難卻不願求助','9–15 歲','我自己可以，不要管。','早就說你辦不到。','想保有自主又還沒找到方法','先問你希望我怎麼陪伴','我先聽你說','需要時一起找可以幫忙的人','遇到超出自己能力的事，求助是可以討論的選擇')]
# Each method is contextualized with the child's words, the actual issue, concrete choices and age range.
methods=[
('先聽見孩子的困難，再討論下一步。','先承認感受不等於取消界線，而是讓孩子有機會把困難說清楚。','我聽到你說「{child}」。你是{concern}嗎？我們先{step}。','傾聽'),
('把指責改成具體的觀察。','描述眼前發生的事，較容易討論行為，而不把孩子整個人貼上標籤。','現在遇到的事是：{scene}。我們先{step}，再一起處理。','澄清'),
('用一個問題，取代替孩子猜好的答案。','孩子的想法可能與大人的推測不同，提問後需要真的等他回應。','你說「{child}」，最想讓我知道的是哪一部分？','提問'),
('把大人的限制說清楚，也把孩子的感受留下。','可以同時承認情緒與說明限制，不必要求孩子先高興才合作。','我知道你可能{concern}。{boundary}，我們一起想怎麼{step}。','界線'),
('給出能做到的選擇，不假裝所有事都能選。','選項需要是大人願意接受、孩子也能理解的真實選擇。','這部分我們可以選擇：{a}，或{b}。你想先哪一個？','請託'),
('先處理一小步，不把所有問題一起壓過去。','將眼前任務縮小，讓對話指向一個可開始的動作。','現在先不用一次解決全部，我們先{step}，做完再看下一步。','鼓勵'),
('孩子說不願意時，先分清楚不能與不想。','不願意可能包含不會、害怕或想法不同，需要了解而非直接判定動機。','你是不知道怎麼做，還是現在不想做？我們可以從{step}開始談。','提問'),
('先把話說短，再確認孩子聽懂什麼。','長篇說理不一定增加理解，短句與重述能幫忙確認。','我先說一件事：{boundary}。你聽到的意思是什麼？','文字表達'),
('不要讓一次衝突替孩子定義自己。','討論具體情況，不用「你總是」「你就是」把孩子說成固定不變的人。','今天我們遇到的是「{scene}」，不是你整個人不好。先一起{step}。','鼓勵'),
('大人不確定時，也可以坦白說還需要了解。','不必靠立即給答案維持權威，可以示範如何繼續理解。','我還沒完全了解你為什麼{concern}，你願意再說一點嗎？','澄清'),
('提問之後的停頓，也是傾聽的一部分。','問完不要立刻替孩子回答，留出思考與拒絕立即作答的空間。','我想聽你說「{child}」背後的想法。你可以慢慢說，我先等一下。','傾聽'),
('把自己的擔心說成感受，不當成孩子的罪名。','說明大人在意什麼，再一起尋找做法，避免用羞辱換取配合。','我有點擔心我們還沒有找到做法。可以先一起{step}嗎？','澄清'),
('允許孩子有情緒，也守住行為的界線。','感受可以被承認，會傷害人或物的行為仍需清楚處理。','你可以說出不高興。{boundary}。我們先{step}。','界線'),
('先確認理解，再提出自己的建議。','重述時用詢問語氣，讓孩子有機會修正大人的理解。','我理解你在意的是{concern}，對嗎？確認後我們再談怎麼{step}。','傾聽'),
('把幫忙說成邀請，保留孩子能做的部分。','提供陪伴不等於接手全部，也不要求孩子獨自承受超出能力的事。','你想自己先試，還是我陪你{step}？需要我時可以告訴我。','請託'),
('討論做法以前，先找回共同想照顧的事。','共同方向可以很小，例如彼此被聽見或把當下整理好。','我們都想把這件事處理得好一點。先{step}，你覺得哪裡需要調整？','不同意'),
('不拿別人的表現，代替對眼前孩子的了解。','比較容易掩蓋孩子具體的困難與努力，應回到當下情境。','我們先不談別人怎麼做。你說「{child}」，我想了解你的情況。','鼓勵'),
('先聽事情經過，不急著替任何一方判定動機。','大人需要了解資訊，不能只憑第一句話就下結論。','剛才發生了什麼？你可以從你記得的地方說，我先不急著下結論。','求證'),
('讓約定包含大人也會做到的部分。','承諾要具體且可實行，不以無法兌現的保證換取孩子配合。','我們先{step}。我會先把注意力放在這件事，聽清楚你說的內容。','請託'),
('用孩子能理解的話說明原因。','理由應貼近當下，避免抽象說教或只要求服從。','我在意的是：{boundary}。現在我們可以先{step}。','文字表達'),
('孩子的看法不同，不代表關係必須中斷。','不同意可以繼續討論，並說清楚哪些限制仍然存在。','你可以有不同想法。{boundary}，我們仍可以談怎麼做比較合適。','不同意'),
('把修正說成下一次可做的動作。','找出具體下一步，比反覆追問孩子為何又犯錯更容易實作。','這次先{step}。你覺得下次可以提早做哪個小動作？','鼓勵'),
('承認自己可能聽錯，是留給孩子的修正空間。','大人可以保持責任，也容許自己的理解被補充。','我可能沒有完全聽懂「{child}」。你願意換個方式說給我聽嗎？','澄清'),
('把對話結束在可行的一步，而不是一句責備。','一次談話不一定解決全部問題，先確認可開始的小動作。','我們先決定一件做得到的事：{step}。其他部分等做完再一起看。','請託'),
('陪伴不必急著變成教訓。','先回應孩子眼前的經驗，再決定是否需要建議或協助。','聽起來你是{concern}。你想先讓我聽，還是我們一起{step}？','安慰')]
assert len(scenes)==20 and len(methods)==25
for si,(scene,age,child,before,concern,step,a,b,boundary) in enumerate(scenes):
 step=step.removeprefix('先')
 if si==9:step='安靜待一下'
 if si==19:step='一起確認你需要的協助'
 values=dict(scene=scene,child=child,concern=concern,step=step,a=a,b=b,boundary=boundary)
 for mi,(principle,insight,response,tag) in enumerate(methods):
  text=scene+'時，'+principle
  if si==18:insight+=' 這個情境由成人先承擔自己的言語影響，孩子不必立即回應或原諒。'
  reply=response.format(**values) if si!=18 else '剛才我說了重話，讓你難過，這是我要負責的。我會先聽你的感受；你也可以晚一點再說。我不會要求你立刻原諒。'
  dialogue=dict(scene=scene,ageRange=age,child=child,before=before,after=reply,guidance='年齡為情境參考，可依孩子理解與當下狀態調整；先聽孩子回應，不要求照句型配合。')
  assert add(dict(kind='原創觀點',category='好好說話',quote=text,source='拾句編輯室 · 親子情境原創',insight=insight,exercise=('用一句孩子能理解的話，承認成人剛才說重話造成的影響，再寫出自己會調整的一個動作，不要求孩子立即原諒。' if si==18 else '以「'+scene+'」為情境，把原本可能說的話改寫成一個孩子能理解的請求，並留空間讓孩子回答。'),tags=['親子對話',tag],dialogue=dialogue,parenting=True,contentGroup='親子情境練習',familyKey='parent-method-'+str(mi),selectionWeight=24,editorialMethod='20 個親子情境 × 25 項表達方法；原創練習示例，非歷史人物引言。',editorialNote='本則為現代親子對話練習，年齡僅供參考。先理解孩子的需要，再依家庭情境調整說法。'))
# Reuse the pinned public-domain electronic source corpus; append only previously unselected exact excerpts.
classic=[]
for file,book,author,path in [('mengzi.json','孟子','孟子及其弟子（傳統歸屬）','四书五经/mengzi.json'),('daxue.json','大學','曾子及其門人（傳統歸屬）','四书五经/daxue.json'),('zhongyong.json','中庸','子思（傳統歸屬）','四书五经/zhongyong.json')]:
 data=load(file);data=data if isinstance(data,list) else [data]
 for ch in data:
  for pi,para in enumerate(ch['paragraphs']):
   for text,start,end in sentences(para):classic.append(dict(kind='古典短句',quote=text,work=book+('·'+ch['chapter'] if book!=ch['chapter'] else ''),author=author,corpusFile=file,corpusPath=path,chapter=ch['chapter'],paragraph=pi,sourceText=para,sourceStart=start,sourceEnd=end))
classic.sort(key=lambda q:-sum(q['quote'].count(c) for c in '言學知思善仁義心禮信道誠君子'));classic=interleave(classic,lambda q:q['chapter'])
prose=[]
for vol in load('guwen.json')['content']:
 for art in vol['content']:
  for pi,para in enumerate(art['paragraphs']):
   for text,start,end in sentences(para):prose.append(dict(kind='文學節選',quote=text,work=art['chapter'],author=art['author'].strip(),corpusFile='guwen.json',corpusPath='蒙学/guwenguanzhi.json',chapter=vol['title']+' / '+art['chapter'],paragraph=pi,sourceText=para,sourceStart=start,sourceEnd=end))
prose.sort(key=lambda q:-sum(q['quote'].count(c) for c in '故夫善學知思言心義理文誠信仁德'));prose=interleave(prose,lambda q:q['work'])
poems=[]
for sec in load('tang300.json')['content']:
 for art in sec['content']:
  for pi,para in enumerate(art['paragraphs']):
   if 9<=len(para)<=65 and not re.search(r'[□�【】\[\]0-9a-zA-Z]',para):poems.append(dict(kind='古詩',quote=para,work=art['chapter']+(('·'+art['subchapter']) if art.get('subchapter') else ''),author=art['author'],corpusFile='tang300.json',corpusPath='蒙学/tangshisanbaishou.json',chapter=sec['type']+' / '+art['chapter'],paragraph=pi,sourceText=para,sourceStart=0,sourceEnd=len(para)))
for file,corpusPath in [('tang1.json','全唐诗/poet.tang.1000.json'),('tang0.json','全唐诗/poet.tang.0.json')]:
 for art in load(file):
  for pi,para in enumerate(art['paragraphs'][:3]):
   if 9<=len(para)<=45 and not re.search(r'[□�【】\[\]0-9a-zA-Z]',para):poems.append(dict(kind='古詩',quote=para,work=art['title'],author=art['author'],corpusFile=file,corpusPath=corpusPath,chapter=art['title'],paragraph=pi,sourceText=para,sourceStart=0,sourceEnd=len(para)))
poems=interleave(poems,lambda q:q['work']);base={c:next(q for q in bank if q['category']==c) for c in cats}
for kind,items in [('古典短句',classic),('文學節選',prose),('古詩',poems)]:
 for q in items:
  if counts[kind]>=1500:break
  if norm(q['quote']) in seen:continue
  ci=themed(q['quote']);q.update(category=cats[ci],source=q['author']+'《'+q['work']+'》',url=repo+'/blob/'+commit+'/'+encode(q['corpusPath'],safe='/'),sourceLocator=q['chapter']+' · 第'+str(q['paragraph']+1)+'段',sourceCommit=commit,background='本句依固定版本電子底本節錄，附同段原文供離線對照；作者、異文與傳統歸屬依所採底本，並非逐句人工校勘。',readingGuide=True,insight='先辨認這句的發言者、景物或論點，再對照同段原文。把原文說了什麼與自己的現代延伸分開，不單憑一句推斷整篇立場。',exercise='對照同段原文，用白話試述這句的作用，再寫下一個需要查證或想討論的問題。',tags=base[cats[ci]]['tags'][:],dialogue=base[cats[ci]]['dialogue'].copy(),contentGroup='詩文閱讀' if kind=='古詩' else '上下文閱讀',familyKey='work-'+q['work'],selectionWeight=20 if kind=='古詩' else 10,editorialNote='請連讀同段原文；本則提供閱讀提示，並非逐字翻譯或已完成校勘的版本。')
  if all(q['quote'].count(a)==q['quote'].count(b) for a,b in [('「','」'),('『','』'),('“','”')]):add(q)
 assert counts[kind]==1500,(kind,counts[kind])
assert len(bank)==6000 and len(seen)==6000 and counts['原創觀點']==1500
assert bank[:4000]==load('library-4000.json'), 'Existing entries changed'
(dist/'quotes.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n')
r=json.loads((dist/'library-report.json').read_text());r.update(total=6000,byKind=dict(counts),cycleDays=300,dailyPerKind=5,parentingEntries=500,newOriginals='保留原有 125 則及 875 則情境短句，追加 500 則親子情境原創（20 個情境 × 25 種方法）。',parentingMethod='20 個親子情境 × 25 種表達方法，含孩子的話、成人前後說法及參考年齡；現代原創，非古典原文。',baseline='sources/library-4000.json；原有 4,000 則的 ID 與內容完整保留。',contentHash=hashlib.sha256((dist/'quotes.json').read_bytes()).hexdigest());(dist/'library-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'total':len(bank),'byKind':dict(counts),'parenting':500},ensure_ascii=False))
