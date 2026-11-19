const categories=['說話的藝術','文化底蘊','知識見解','文字素養','好好說話'];
const raw=[
['話說得慢一點，理解才有走近的空間。','停頓不是空白，而是留給彼此思考的餘地。','今天回應一個問題前，先停三秒。'],
['好的表達，不是把話說滿，而是把意思說明白。','堆疊字句容易，辨認重點才需要用心。','用三句話說明你最近正在做的一件事。'],
['先聽見對方的在意，再說出自己的道理。','當感受被理解，意見才比較容易被聽見。','先說「你在意的是……，我理解得對嗎？」再回應。'],
['讓人願意聽的話，往往先讓人感到被尊重。','尊重不代表同意，而是容納另一種經驗。','把一次反駁改成「我有另一個觀察，想和你討論」。'],
['少一點急著證明，多一點好奇提問。','提問能打開對話，急著下結論容易關上它。','用「你是怎麼想到的？」延續一次對話。'],
['說話有分寸，是為真誠找到合適的形狀。','真誠需要照顧場合、時機和對方的承受度。','提出意見前，先問對方是否方便聽。'],
['一句具體的肯定，勝過十句空泛的讚美。','被看見的努力，比籠統的評價更能留下力量。','稱讚一個人時，說出他做了什麼與帶來的影響。'],
['把複雜說清楚，是一種替別人著想的能力。','清楚的表達會減少理解所需的負擔。','選一個專業概念，用生活中的例子解釋。'],
['文化不是記住多少典故，而是理解人如何生活。','器物、節慶與語言，都藏著人們回應世界的方法。','找一個熟悉的節日，查查其中一項習俗的來由。'],
['讀古人的文字，也是在辨認自己的心事。','時代不同，人對失落、相遇與理想的感受卻能相通。','選一句古詩，寫下它讓你想到的生活片段。'],
['一座城市的性格，藏在它願意留下的事物裡。','老屋、街名和市場，是理解地方記憶的入口。','留意住家附近一個老地名，查詢它的故事。'],
['理解一種文化，先放下替它打分數的習慣。','差異值得先被理解，再被評價。','遇見陌生習俗時，先提出一個不帶評判的問題。'],
['典故讓語言有根，觀察讓語言有生命。','引用不必炫學，貼近眼前的情境才有意義。','把一個成語換成今天發生的具體小故事。'],
['餐桌上的滋味，也是一部地方的歷史。','食物往往承載遷徙、氣候與家族的共同記憶。','詢問家人，一道家常菜是向誰學來的。'],
['向傳統提問，是讓它繼續活著的一種方式。','理解來由後，我們才能選擇如何延續。','寫下一個你想理解的傳統，查找兩種說法。'],
['看見不同的生活，自己的世界才會更寬。','文化素養來自與差異相處的經驗。','閱讀一篇與自己生活背景不同的人的自述。'],
['知道自己不知道，是見識開始生長的地方。','承認認知的邊界，才有重新學習的可能。','記下一個你常使用、卻無法清楚解釋的詞。'],
['看見一個答案，也要看見它回答的是什麼問題。','資訊離開原本的問題，容易被誤用。','讀一則研究報導時，先確認它研究了誰與什麼。'],
['觀點可以鮮明，證據仍要仔細。','立場的強烈程度，不能替代事實的可信程度。','轉傳資訊之前，找到原始來源與發布日期。'],
['把事實與推測分開，思考就多了一分清明。','清楚標記不確定，是負責任表達的一部分。','將一段判斷拆成「我看到的」與「我推測的」。'],
['理解一件事，也包括知道它何時不適用。','方法有條件，經驗有範圍。','為一個你相信的建議，找出一種不適用的情況。'],
['一個好問題，能讓熟悉的事物重新發光。','好奇使我們從習以為常走向深入理解。','選一件日用品，問自己它為什麼被設計成這樣。'],
['改變想法，是讓證據在心裡有位置。','修正觀點不必否定過去，而是回應新的認識。','回想一個你改變的看法，寫出關鍵原因。'],
['多讀一種觀點，不必少一分自己的判斷。','理解對方最好的理由，有助於形成更完整的判斷。','用對方會認同的方式，重述一個不同意的觀點。'],
['文字的力量，常在刪去之後才顯現。','留下必要的字，讓意思有清楚的輪廓。','把今天寫的一段文字刪短三分之一，保留原意。'],
['寫得具體，讀者才能在字裡看見風景。','抽象的感受，可以透過動作、聲音與細節被感知。','不用「很開心」，用一個動作寫出開心。'],
['一個準確的動詞，能讓整句話站穩。','動詞說明事情如何發生，是句子的支點。','檢查一段文字，將一個含糊的動詞換得更精確。'],
['先把意思寫清楚，再讓句子長出自己的聲音。','風格可以慢慢形成，清楚是最初的照顧。','寫完後朗讀一次，修改讓自己停頓困惑的地方。'],
['留白不是少說，而是讓重要的話被看見。','段落與節奏能幫助讀者辨認主次。','把一段過長的訊息，分成每段一個重點。'],
['好的比喻，讓陌生的事找到熟悉的門。','比喻是理解的橋，也有它無法涵蓋的範圍。','用一件日常物品比喻今天的心情，說明相似之處。'],
['詞語越貼切，心意越不容易走失。','近義詞也有語氣與程度的差異。','把「不錯」換成一個更準確的描述。'],
['讀懂一句話，也要聽見它沒有說出的語氣。','標點、情境與關係都會改變文字的意思。','替同一句邀請寫出正式與親切兩種版本。'],
['溫柔不是退讓，是把界線說得不傷人。','清楚的界線能保護關係，也保護自己。','練習說「這次我無法幫忙，但可以提供這個資訊」。'],
['把「你總是」換成「這一次」，對話就有了出口。','描述具體事件，才能一起尋找可以改變的行為。','把一個帶有「總是」的抱怨，改成具體情境。'],
['說出需要，比期待對方猜中更靠近理解。','沒有說出口的期待，容易變成彼此的誤會。','直接說明今天需要的一項協助與時間。'],
['道歉的重量，在於承擔，而不在於解釋。','具體承認影響，再提出可實行的修補方式。','用「我做了……，讓你……，接下來我會……」練習。'],
['不同意一個想法，也可以珍惜提出它的人。','把意見與人格分開，討論才能保留信任。','用「我對這個做法有疑慮」取代對人的評價。'],
['情緒需要被看見，決定可以晚一點再做。','辨認感受有助於選擇回應，而非立即反應。','生氣時先說「我需要十分鐘整理，稍後再談」。'],
['真正的傾聽，是暫時放下準備好的答案。','與其急著解決，不如先確認對方需要什麼。','問對方「你希望我聽你說，還是一起想辦法？」。'],
['讓謝謝有名字，讓心意有細節。','說明感謝的原因，能讓付出被確實看見。','向一個人說出一件具體讓你感激的事。']
];
const bank=raw.map((r,i)=>({id:i,category:categories[Math.floor(i/8)],quote:r[0],insight:r[1],exercise:r[2],source:'拾句編輯室 · 原創'}));
const day=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const offset=Math.floor(Date.parse(day)/86400000)%8;const daily=categories.flatMap((c,i)=>Array.from({length:4},(_,j)=>bank[i*8+(offset+j)%8]));
let saved=[],read=[],view='today',filter='全部';const key='shiju-v1';let state={};try{state=JSON.parse(localStorage.getItem(key)||'{}');saved=Array.isArray(state.saved)?state.saved:[];read=state.day===day&&Array.isArray(state.read)?state.read:[]}catch{};
const $=s=>document.querySelector(s);function persist(){try{localStorage.setItem(key,JSON.stringify({saved,read,day,practice:$('#practiceText').value}))}catch{toast('無法儲存，請確認瀏覽器允許本機儲存。')}}
$('#practiceText').value=state.practice||'';$('#date').textContent='◷  '+new Intl.DateTimeFormat('zh-TW',{timeZone:'Asia/Taipei',month:'long',day:'numeric',weekday:'long'}).format(new Date());
function toast(t){$('#toast').textContent=t;$('#toast').classList.add('visible');setTimeout(()=>$('#toast').classList.remove('visible'),2300)}
function toggle(id){saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];persist();render()}
function render(){
$('#savedCount').textContent=saved.length;$('#readLabel').textContent=`已讀 ${read.length} / 20 則`;$('#bar').style.width=`${read.length*5}%`;$('#encourage').textContent=read.length===20?'今天的 20 則已讀完。選一句話，帶進生活裡吧。':'不必急著讀完，讓一句話在心裡停留。';
$('#practicePanel').hidden=view!=='practice';$('#cards').hidden=view==='practice';$('#filters').hidden=view==='practice';$('.search').hidden=view==='practice';
$('#pageLabel').textContent={today:'今日拾句',saved:'我的書籤',practice:'表達練習'}[view];$('#sectionTitle').innerHTML={today:'今日精選 <span>DAILY PICKS</span>',saved:'我的書籤 <span>MY COLLECTION</span>',practice:'讓好句子成為你的話 <span>DAILY PRACTICE</span>'}[view];$('#sectionDesc').textContent=view==='saved'?'收藏讓你停下來的句子，隨時回來重讀。':view==='practice'?'從一句改寫開始，練習更有溫度的表達。':'讀一句好話，長一分見識。';
$('#filters').innerHTML=['全部',...categories].map(c=>`<button class="filter ${c===filter?'active':''}" data-category="${c}">${c}${c==='全部'?' '+(view==='today'?20:saved.length):''}</button>`).join('');
const term=$('#search').value.trim();let items=(view==='saved'?bank.filter(q=>saved.includes(q.id)):daily).filter(q=>(filter==='全部'||q.category===filter)&&[q.quote,q.category,q.insight].join('').includes(term));
$('#cards').innerHTML=items.length?items.map(q=>`<article class="card"><div class="card-top"><span class="tag">${q.category}</span><button class="bookmark ${saved.includes(q.id)?'saved':''}" data-save="${q.id}" aria-label="${saved.includes(q.id)?'取消收藏':'收藏金句'}" aria-pressed="${saved.includes(q.id)}">${saved.includes(q.id)?'▣':'♧'}</button></div><div class="quote-mark">“</div><h3 class="quote">${q.quote}</h3><div class="source">— ${q.source}</div><div class="card-bottom"><button class="read-detail" data-detail="${q.id}">讀解與練習 ＋</button><span class="read-state ${read.includes(q.id)?'done':''}">${read.includes(q.id)?'✓ 已閱讀':'約 1 分鐘'}</span></div></article>`).join(''):`<div class="empty">${term?'沒有找到符合的句子，試試其他關鍵字。':view==='saved'?'還沒有收藏。點選金句右上角的收藏圖示，留下喜歡的句子。':'此分類還沒有句子。'}</div>`;
}
$('#cards').addEventListener('click',e=>{let save=e.target.closest('[data-save]');if(save){toggle(+save.dataset.save);return}let b=e.target.closest('[data-detail]');if(!b)return;let q=bank[+b.dataset.detail];if(daily.some(x=>x.id===q.id)&&!read.includes(q.id)){read.push(q.id);persist();render()}$('#detailBody').innerHTML=`<span class="tag">${q.category}</span><h2>${q.quote}</h2><small class="source">${q.source}</small><h3>一句讀解</h3><p>${q.insight}</p><h3>今天，這樣練習</h3><p>${q.exercise}</p><button class="primary" id="detailSave">${saved.includes(q.id)?'取消收藏':'收藏這句話'}</button>`;$('#detailSave').onclick=()=>{toggle(q.id);$('#detailSave').textContent=saved.includes(q.id)?'取消收藏':'收藏這句話'};$('#detail').showModal()});
$('.close').onclick=()=>$('#detail').close();$('#detail').addEventListener('click',e=>{if(e.target===$('#detail')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close()}});
$('#filters').onclick=e=>{const b=e.target.closest('[data-category]');if(b){filter=b.dataset.category;render()}};$('#search').oninput=render;document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view;filter='全部';$('#search').value='';document.querySelectorAll('.nav').forEach(x=>x.classList.toggle('active',x===b));render()});$('#savePractice').onclick=()=>{if(!$('#practiceText').value.trim())return toast('先寫下一句你的練習吧。');persist();toast('練習已儲存，讓表達慢慢進步。')};$('#date').onclick=()=>toast('每日依台北時間更新，從句庫輪替精選 20 則。');render();setInterval(()=>{const now=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());if(now!==day)location.reload()},60000);
