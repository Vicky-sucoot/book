const path=require('path');
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const quotes=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/quotes.json'),'utf8'));
const nodes={};function el(){return {value:'',style:{},dataset:{},open:false,innerHTML:'',hidden:false,attributes:{},classList:{add(){},remove(){},toggle(){}},listeners:{},setAttribute(k,v){this.attributes[k]=v},addEventListener(k,f){this.listeners[k]=f},showModal(){this.open=true},close(){this.open=false;this.listeners.close?.()},focus(){}}}
let selectedTags=[];const local={'shiju-v1':JSON.stringify({saved:[0,39,50],practice:'原有練習',notes:{50:'原有心得'},labels:{50:['感謝']},day:'old',edition:2,read:[0]})};
const ctx={console,Intl,Date,setTimeout(){},clearTimeout(){},setInterval(){},location:{reload(){}},fetch:async()=>({ok:true,json:async()=>quotes}),localStorage:{getItem:k=>local[k],setItem:(k,v)=>local[k]=v},document:{querySelector:s=>nodes[s]??=el(),querySelectorAll:s=>s.includes(':checked')?selectedTags.map(value=>({value})):[]}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(__dirname,'../dist/app.js'),'utf8'),ctx);
function check(expr){assert(vm.runInContext(expr,ctx),expr)}
(async()=>{await new Promise(r=>setImmediate(r));check('bank.length===140');check('new Set(bank.map(q=>q.id)).size===140');check('new Set(bank.map(q=>q.quote)).size===140');check('categories.every(c=>bank.filter(q=>q.category===c).length===28)');check('bank.every(q=>q.dialogue.scene&&q.dialogue.before&&q.dialogue.after&&q.exercise&&q.tags.length)');check('bank.filter(q=>q.kind!=="原創觀點").every(q=>q.url&&q.author&&q.work&&q.background&&q.glossary)');
for(let start=-14;start<366;start++){check(`(()=>{let week=Array.from({length:7},(_,i)=>selectDaily(${start}+i));return week.every(day=>day.length===20&&new Set(day.map(q=>q.id)).size===20&&categories.every(c=>day.filter(q=>q.category===c).length===4))&&new Set(week.flat().map(q=>q.id)).size===140})()`)}
check('saved.join(",")==="0,39,50"');assert.equal(nodes['#practiceText'].value,'原有練習');check('read.length===0');assert.equal((nodes['#cards'].innerHTML.match(/class="chapter"/g)||[]).length,5);assert.equal((nodes['#cards'].innerHTML.match(/<article/g)||[]).length,20);
vm.runInContext('setView("library");kindFilter="古詩";render()',ctx);assert.equal((nodes['#cards'].innerHTML.match(/<article/g)||[]).length,5);nodes['#search'].value='王勃';vm.runInContext('render()',ctx);assert.equal((nodes['#cards'].innerHTML.match(/<article/g)||[]).length,1);
vm.runInContext('openDetail(50)',ctx);assert(nodes['#detailBody'].innerHTML.includes('作品背景'));assert(nodes['#detailBody'].innerHTML.includes('生活裡，這樣說'));assert(nodes['#detailBody'].innerHTML.includes('原有心得'));
ctx.document.querySelector('#quoteNote').value='<img src=x onerror=alert(1)> 想用在道謝';selectedTags=['感謝','安慰'];nodes['#saveNote'].onclick();let stored=JSON.parse(local['shiju-v1']);assert(stored.notes[50].includes('<img'));assert.deepEqual(stored.labels[50],['感謝','安慰']);
vm.runInContext('openDetail(50)',ctx);assert(nodes['#detailBody'].innerHTML.includes('&lt;img'));assert(!nodes['#detailBody'].innerHTML.includes('<img src=x'));
vm.runInContext('setView("saved");tagFilter="感謝";render()',ctx);assert(nodes['#cards'].innerHTML.includes('海內存知己'));
nodes['#useExercise'].onclick();check('view==="practice"');assert(nodes['#practiceText'].value.includes('海內存知己'));assert(nodes['#practiceText'].value.includes('我的改寫'));
vm.runInContext('setView("today")',ctx);const firstReview=nodes['#review'].innerHTML.match(/data-review="(\d+)"/)[1];nodes['#review'].listeners.click({target:{closest:s=>s==='[data-review]'?{dataset:{review:firstReview}}:null}});assert.equal(JSON.parse(local['shiju-v1']).reviewed,+firstReview);assert(nodes['#review'].innerHTML.includes('今天已複習'));
vm.runInContext('openDetail(daily[0].id)',ctx);check('read.length===1');vm.runInContext('openDetail(daily[0].id)',ctx);check('read.length===1');assert.equal(nodes['#progressTrack'].attributes['aria-valuenow'],1);
// Exercise storage failure is surfaced, without a false success message.
ctx.localStorage.setItem=()=>{throw Error('quota')};nodes['#practiceText'].value='新練習';nodes['#savePractice'].onclick();assert(nodes['#toast'].textContent.includes('無法儲存'));
console.log('PASS: 380 rolling weeks; balanced 20/day, no seven-day repeats; 140 unique entries; legacy data; citations; author search; tags; note XSS escaping; exercise transfer; review; reading progress; storage errors.');
})().catch(e=>{console.error(e);process.exitCode=1});
