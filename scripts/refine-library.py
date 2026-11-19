"""Editorial pass and transparent grouping; counts, original text and IDs remain stable."""
from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parents[1];p=root/'dist/quotes.json';bank=json.loads(p.read_text())
added=[0,5,7,8,9,10,11,12,13,14,15,17,18,20,21,22,23,25,26,27,28,29,30,31,33]
uses={'說話的藝術':'提問、說明想法、確認理解與提出不同意見。','文化底蘊':'閱讀典故、交流生活經驗與理解陌生習俗。','知識見解':'辨認證據、核對資訊與討論不同觀點。','文字素養':'寫訊息、改寫段落與閱讀文字。','好好說話':'表達界線、安慰、請求與修補關係。'}
cautions={'說話的藝術':'先確認對方是否方便交談；清楚表達也要留意權力差異與場合。','文化底蘊':'個別經驗不代表所有人的文化；引用典故前仍要確認原始情境。','知識見解':'這是思考方法，不能取代查證，也不是對專業議題的具體結論。','文字素養':'文字方法應配合讀者與目的，不能只為修辭而犧牲事實與清楚。','好好說話':'句型不能保證對方的反應。尊重拒絕，也不必為了維持關係承擔不合理要求。'}
for q in bank:
 if q['id'] in added:q.update(curated=True,plainMeaning=q['insight'],useWhen=uses[q['category']],useCaution=cautions[q['category']])
 if 140<=q['id']<1015:
  q['contentGroup']='情境表達練習';q['familyKey']='method-'+str((q['id']-140)%25);q['editorialNote']='本則將表達方法放入生活情境，與同方法的其他短句合併理解即可，不必逐句背誦。';q['selectionWeight']=8
 elif q.get('curated'):
  q['contentGroup']='編輯精選';q['familyKey']='edited-'+str(q['id']);q['selectionWeight']=40
 elif q['kind']!='原創觀點':
  contextual=bool(re.search(r'曰|王|公|侯|臣|莊|伯|鄭|齊|晉',q['quote'])) and q['kind']!='古詩'
  q['contentGroup']='上下文閱讀' if contextual else '詩文閱讀';q['familyKey']='work-'+q.get('work',str(q['id']));q['selectionWeight']=10 if contextual else 22
  q['editorialNote']='本則涉及人物、對話或史事情境，請連讀下方同段原文；不要直接當成作者對所有情況的主張。' if contextual else '先辨認原句的畫面或論點，再閱讀同段原文。下方為閱讀提示，不是逐字翻譯。'
  if contextual:q['insight']='這一節先留意人物關係與發言者：誰在回應誰，事情發生在什麼條件下？讀完同段原文後，再判斷這句是敘事、引用他人發言，還是提出主張。'
  elif q['kind']=='古詩':q['insight']='從句中選出一個景物、動作或聲音，觀察它如何形成畫面與節奏。再對照同段詩句，區分詩中描寫與自己的聯想。'
  else:q['insight']='先用白話試述這句在段落中的作用，再找出支持你理解的字詞。遇到不熟的用語，保留疑問，避免單憑一句就推斷整篇立場。'
 else:q['contentGroup']='原創觀點';q['familyKey']='original-'+str(q['id']);q['selectionWeight']=25
p.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':'))+'\n')
rp=root/'dist/library-report.json';r=json.loads(rp.read_text());r.update(editorialSelection=50,editorialScope='35 則原創及 15 則古典詩文附白話解釋、情境與提醒。其餘內容依閱讀需求分組，情境方法標示相同方法群組，並非逐句校勘。',contentHash=hashlib.sha256(p.read_bytes()).hexdigest());rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('Refined 50 editorial selections and grouped 4000 entries without changing IDs/counts.')
