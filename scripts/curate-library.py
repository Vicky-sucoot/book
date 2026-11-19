"""Apply a bounded editorial selection without changing quote IDs or counts."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'dist/quotes.json';bank=json.loads(p.read_text())
originals=[1,2,3,4,6,16,19,24,32,38]
meanings=[
('言辭能把意思表達清楚就好。','說明想法、工作交接。','清楚不等於省略必要背景，也不代表文字不能有美感。'),
('教育不應按人的類別而加以區分。','討論學習機會、接納不同背景的人。','此語談教育態度，不宜直接推導成每個人都應採同一種教法。'),
('不只憑好聽的話推舉一個人，也不因不喜歡某人就否定他說的話。','評估建議、討論不同立場。','重視內容仍需要檢查證據，不能只因語氣中肯就相信。'),
('工匠要做好工作，必須先把工具準備妥當。','提醒自己為寫作、發言或工作做好準備。','原章接著談親近賢者與仁者；現代的工具比喻是延伸用法。'),
('自己不願承受的事，不要加在別人身上。','換位思考、尊重界線。','別人的需要未必與自己相同，仍應詢問，而非只按自己喜好猜測。'),
('人不是生來就懂所有道理的，誰會沒有疑惑呢？','鼓勵提問、坦白承認不懂。','承認疑惑之後，也需要查證或請教，不能停在放棄理解。'),
('這雖是簡陋的屋子，只因住在其中的人德行美好，就不覺得簡陋。','理解作者借居室表達的志趣。','這是作者的自我表述，不宜用來要求別人忍受不合理的生活條件。'),
('了解道理有先有後，學問與技藝各有專門研究。','跨領域合作、向不同年齡的人請教。','尊重專長不等於免除查證，也不表示專家在所有問題上都可靠。'),
('清風緩緩吹來，水面沒有泛起波浪。','學習用具體景物描寫安靜。','這是夜遊開場的景象，不宜單憑此句概括整篇賦的情緒。'),
('可以遠遠觀賞蓮花，卻不可以輕慢地玩弄它。','討論欣賞與尊重的分寸。','原文借蓮喻君子；將它用於人際界線是現代延伸，並非原文直接談溝通。'),
('天下只要有懂得自己的朋友，即使遠在天邊，也像在近鄰。','送別、問候遠方朋友。','可以用來表達情誼，不必用來否定對方對距離或離別的難過。'),
('山水迴環，好像已經沒有路，轉過柳蔭與花叢，又見一座村莊。','從景物轉折理解希望與探索。','比喻轉機不表示困難必然自行解決，仍需要尋找可行的行動。'),
('正面看是連綿的山嶺，側面看是高聳的山峰，遠近高低所見各不相同。','提醒討論者注意觀察位置。','不同視角可以補充理解，但不代表所有說法都同樣符合事實。'),
('想要看盡更遠的景色，就再登上一層樓。','鼓勵學習、拓展視野。','詩中由登樓寫遠望；用來鼓勵別人時，也應尊重對方的能力與休息需要。'),
('我終將登上最高的山頂，一眼望去，群山都顯得小了。','理解詩人的志向與想像。','這是登頂的願望，並非已登頂的紀錄；也不宜延伸成輕視他人的態度。')]
for q in bank:
 q.pop('curated',None);q.pop('plainMeaning',None);q.pop('useWhen',None);q.pop('useCaution',None)
 if q['id'] in originals:
  q.update(curated=True,plainMeaning=q['insight'],useWhen=q['dialogue']['scene'],useCaution='這是表達練習的方向，實際說法仍需依關係、場合與對方意願調整。')
 elif 40<=q['id']<=54:
  meaning,use,caution=meanings[q['id']-40];q.update(curated=True,plainMeaning=meaning,useWhen=use,useCaution=caution)
p.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n')
report_path=root/'dist/library-report.json';report=json.loads(report_path.read_text());report.update(editorialSelection=25,editorialScope='10 則原創及 15 則古典詩文，補白話解釋、適用情境與使用提醒；其餘內容仍為原有閱讀提示。',contentHash=hashlib.sha256(p.read_bytes()).hexdigest());report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Applied 25 editorial selections; IDs and type counts unchanged.')
