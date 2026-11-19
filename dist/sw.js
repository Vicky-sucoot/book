'use strict';
const CACHE='shiju-offline-v7-parenting6000';
const ASSETS=['./','./index.html','./style.css','./app.js','./quotes.json','./manifest.webmanifest','./icon-192.png','./icon-512.png','./shiju-offline.html','./shiju-offline.zip','./source-license.txt','./library-report.json'];
const urlFor=path=>new URL(path,self.registration.scope).href;
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const cache=await caches.open(CACHE);
 for(const path of ASSETS){const response=await fetch(new Request(urlFor(path),{cache:'reload',credentials:'same-origin'}));if(!response.ok||response.redirected)throw Error('Offline resource unavailable');
 if(path==='./'||path==='./index.html'){if(!(await response.clone().text()).includes('id="featured"'))throw Error('App HTML unavailable')}
 if(path==='./quotes.json'){if(!Array.isArray(await response.clone().json()))throw Error('Quote data unavailable')}
 await cache.put(urlFor(path),response);
 }
 await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{await Promise.all((await caches.keys()).filter(k=>k.startsWith('shiju-offline-')&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);
 if(url.origin!==self.location.origin||!url.href.startsWith(self.registration.scope))return;
 const isAsset=ASSETS.some(path=>new URL(urlFor(path)).pathname===url.pathname);
 if(event.request.mode==='navigate'&&url.pathname===new URL(self.registration.scope).pathname){event.respondWith((async()=>{try{const response=await fetch(event.request);if(response.ok&&(await response.clone().text()).includes('id="featured"'))return response}catch{}return (await caches.match(urlFor('./')))||Response.error()})());return}
 if(isAsset)event.respondWith((async()=>{const cached=await caches.match(urlFor('./'+url.pathname.slice(new URL(self.registration.scope).pathname.length)));return cached||fetch(event.request)})());
});
