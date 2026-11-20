"""Curated reading candidates and purpose-specific dialogue tones. Quote text/IDs remain stable."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];p=root/'dist/quotes.json';bank=json.loads(p.read_text());baseline=json.loads((root/'sources/library-4000.json').read_text());base_edited={q['id'] for q in baseline if q.get('curated')};extra=[q['id'] for q in baseline if q['id']<140 and q['kind']=='原創觀點' and q['id'] not in base_edited][:50]
uses={'說話的藝術':'提出想法、確認理解或討論不同意見。','文化底蘊':'交流生活經驗、閱讀典故或理解不同習俗。','知識見解':'釐清資訊、辨認證據或重述不同觀點。','文字素養':'寫訊息、整理段落或用具體細節描述經驗。','好好說話':'說明界線、提出請求、安慰或修補關係。'}
for q in bank:
 if q['id'] in extra:q.update(curated=True,plainMeaning=q['insight'],useWhen=uses[q['category']],useCaution='先確認對方願意討論，再依角色、權力差異與當下需要調整。方法是參考，不保證對方會照期待回應。',selectionWeight=40,contentGroup='編輯精選')
# These are different purposes, not progressively stronger pressure.
work_boundaries={
'會議異議':'我對測試時間不足有疑慮；在風險與責任尚未確認前，我不能把方案視為已完成驗證。',
'需求協商':'新增範圍可以討論，但原定時間與費用需要重估，我不能直接承諾全部照原條件完成。',
'分工界線':'我可以負責已確認的部分；最後核對需要指定負責人，不能默認由我承擔所有未分配事項。',
'建立合作':'我願意協助你熟悉工作；若需要較完整的說明，我們先約一個雙方能專心的時間。',
'進度追蹤':'後續整合需要這份資料；若無法依約提供，請讓我們知道，好一起調整安排。',
'工作交接':'交接內容我會整理清楚；尚未確認理解的部分，請先提出，我們再決定是否能正式移交。',
'績效溝通':'我願意對合理的目標負責；若資源不變，需要一起調整優先順序或交付範圍。',
'延遲說明':'我會回報已確認的進度，但不能承諾尚未完成檢查的交付時間。',
'書面共識':'我會以共同確認的版本執行；尚未確認的訊息不先當成正式承諾。',
'徵求回饋':'希望大家提供可行時段；若沒有回覆，我會再確認，不把沉默直接當成同意。',
'向上提案':'我可以先做小規模試行；涉及跨部門或資源的調整，仍需確認授權與責任。',
'資訊求證':'目前我只能提供已核對的部分；其餘數字需要確認後再回報，不能先當成定案。',
'向上溝通':'我會依確認的方向執行，也需要把目前看見的風險說明清楚，避免誤認為已沒有疑慮。',
'工作界線':'新增任務可以討論，但目前無法同時維持所有原定期限，需要一起決定取捨。',
'跨部門協作':'我可以配合共同確認的節點；若時程衝突，需要明確協調，不能只由單一部門吸收延誤。',
'具體回饋':'我會針對內容提出具體建議，不對個人下評價；也請一起確認修改範圍與期限。',
'接受回饋':'我願意討論具體修改，但需要知道可核對的問題；對人格的評價無法直接轉成改善行動。',
'清楚簡報':'我可以換個例子說明；超出目前資料範圍的問題，需要另外確認，不能為了簡化而說成定論。',
'失誤修補':'這項核對是我的責任，我會說明影響與修補；不以未確認的原因轉移責任。',
'行動確認':'未確認負責人、交付內容與時間前，我不先把方向共識當成所有人都已承諾執行。'}
parent_boundaries=[
'你的日常安排由你負責。我能提供哪些支援會說清楚，也不以支援交換你照我的方式生活。',
'你可以選擇居住方式；家裡能負擔的金額與條件需要談清楚，不會替你直接作決定。',
'我願意一起看必要支出，也需要說明能支援的上限；不以金錢要求你交出全部隱私。',
'課業結果需要面對，但我不會用成績評斷你的價值，也不會未經同意聯絡學校。',
'轉系的資訊與後果需要了解，最後選擇仍需要你參與決定，我不替你承諾。',
'我可以分享工作資訊，但不替你答應實習或聯絡公司，除非你明確希望我協助。',
'我們可以談資源與期待；是否升學或就業，不用以別人的進度替你決定。',
'我能提供的協助會說清楚，不保證求職結果，也不把暫時沒有回音當成你不努力。',
'你可以保留感情細節。我想表達關心，但不會要求你提供不願分享的資訊。',
'我可以陪你整理要說的話，但不會未經同意聯絡室友或替你處理衝突。',
'我可以說明自己的擔心，但不把關心變成監控；聯繫方式需要雙方同意。',
'暫停學業的資源與期限需要談清楚，但我不以羞辱或關係威脅逼你立即決定。',
'我不替你辭職或安排工作。我們可以談實際負荷與能調整的資源。',
'我會停止拿你與別人比較；親友追問時，也尊重你不回答的選擇。',
'我們可以不同意觀點，但不辱罵或否定彼此的人格；需要時可以先暫停再談。',
'我可以表達想念，也尊重你的安排；不把返家頻率當成你是否在乎家人的證明。',
'沒有你的同意，我不替你聯絡學校或揭露私事；需要協助時，我們先談範圍。',
'我可以說出資源限制與擔心，但不以斷絕關係迫使你選擇我的職涯方向。',
'剛才傷人的話由我負責。我會調整自己的說法，不要求你立刻原諒或安慰我。',
'我可以先聽，不急著提供答案。你的選擇仍由你決定，我會說明能提供的支持。']
for q in bank:
 if not(q.get('parenting') or q.get('workplace')):continue
 d=q['workplaceDialogue'] if q.get('workplace') else q['dialogue'];direct=d['after']
 gentle=('我想先理解你的考量，再一起看怎麼處理。' if q.get('workplace') else '我想先聽你的想法，不急著替你決定。')+direct
 boundary=work_boundaries[q['workplaceTopic']] if q.get('workplace') else parent_boundaries[(q['id']-4000)//25]
 d['tones']={'gentle':{'label':'溫和版','text':gentle,'useWhen':'適合先建立理解、對方願意交流，而你也有時間傾聽時。'},'direct':{'label':'直接版','text':direct,'useWhen':'適合要清楚說明重點、確認條件或提出具體問題時；直接不等於責備。'},'boundary':{'label':'界線清楚版','text':boundary,'useWhen':'適合需要說明權責、隱私、資源或不能承諾的部分；保留對方回應與協商空間。'}}
assert sum(bool(q.get('curated')) for q in bank)==100
p.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n');rp=root/'dist/library-report.json';r=json.loads(rp.read_text());r.update(editorialSelection=100,editorialScope='85 則原創及 15 則古典詩文附讀解、情境與提醒；其餘保留閱讀提示，不宣稱逐句校勘。',toneEntries=1000,toneMethod='500 則職場及 500 則大學生親子示例各附三種語氣與適用時機，不把更強硬當成更有效。',contentHash=hashlib.sha256(p.read_bytes()).hexdigest());rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('100 editorial selections and 1000 three-tone dialogues; all quote texts/IDs preserved.')
