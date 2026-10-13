'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert');
function harness(name){
 const html=fs.readFileSync(process.argv[2]+'/'+name+'.html','utf8');
 const script=html.split('<script>')[1].split('</script>')[0];
 const ids={},keys=[],posts=[],timers=[];
 function el(a){return {value:'',type:a.type||'',dataset:{key:a['data-key']},classList:{add(){},remove(){}},listeners:{},focus(){},addEventListener(n,f){(this.listeners[n]??=[]).push(f)},fire(n,extra={}){for(const f of this.listeners[n]||[])f({preventDefault(){},clientX:0,clientY:0,...extra})}}}
 for(const tag of html.matchAll(/<(input|button|div|span|p)\b([^>]*)>/g)){
  const a={};for(const x of tag[2].matchAll(/([\w-]+)(?:=("[^"]*"|'[^']*'|[^\s>]+))?/g))a[x[1]]=(x[2]||'').replace(/^["']|["']$/g,'');
  const e=el(a);if(a.id)ids[a.id]=e;if(a['data-key'])keys.push(e);
 }
 const win=el({});
 const sandbox={document:{getElementById:id=>ids[id],querySelectorAll:()=>keys},window:win,
  setTimeout:(fn,ms)=>{timers.push({fn,ms});return timers.length},
  fetch:(url,opts)=>{
   if(!opts||opts.method!=='POST')return Promise.resolve({ok:true,status:200,text:()=>Promise.resolve('open qa')});
   return new Promise(resolve=>posts.push({body:opts.body,resolve,done:false}));
  },encodeURIComponent,Math,Array,Promise};
 vm.runInNewContext(script,sandbox);
 const settle=async()=>{for(let i=0;i<12;i++)await new Promise(setImmediate)};
 function resolve(p){p.done=true;p.resolve({ok:true,status:204})}
 return {ids,keys,posts,timers,win,settle,resolve,
  async drain(){for(let i=0;i<20;i++){for(const p of posts.filter(x=>!x.done))resolve(p);await settle();if(posts.every(x=>x.done))return}throw Error('queue failed to drain')},
  kinds(){return posts.map(p=>new URLSearchParams(p.body).keys().next().value)},
  totalMovement(){return posts.reduce((n,p)=>n+Number((new URLSearchParams(p.body).get('move')||'0,0').split(',')[0]),0)}
 };
}
async function run(name){
 const h=harness(name);await h.settle();h.ids.kb.value='qa-text';h.ids.kb.fire('input');await h.settle();
 assert.deepStrictEqual(h.kinds(),['type']);
 h.ids.pad.fire('mousedown');
 for(let x=1;x<=120;x++)h.win.fire('mousemove',{clientX:x});await h.settle();
 const held=h.kinds();await h.drain();
 assert.equal(h.totalMovement(),120);
 assert.deepStrictEqual(held,name==='before'?['type','move']:['type']);
 const b=harness(name);await b.settle();b.ids.pad.fire('mousedown');b.win.fire('mousemove',{clientX:1});await b.settle();
 for(let x=2;x<=120;x++)b.win.fire('mousemove',{clientX:x});await b.settle();
 const during=b.kinds().length;await b.drain();assert.equal(during,1);assert.equal(b.posts.length,2);assert.equal(b.totalMovement(),120);
 // A small drag followed by a tap: run only the old60ms click timer,
 // while holding the movement response. The new path needs no timer.
 const c=harness(name);await c.settle();c.ids.pad.fire('mousedown');c.win.fire('mousemove',{clientX:2});await c.settle();c.win.fire('mouseup');
 for(const t of c.timers.filter(t=>t.ms<100))t.fn();await c.settle();const tapHeld=c.kinds();
 assert.deepStrictEqual(tapHeld,name==='before'?['move','click']:['move']);await c.drain();assert.deepStrictEqual(c.kinds(),['move','click']);
 return {name,typing_response_held_posts:held,typing_response_released_posts:h.kinds(),movement_total:120,
  isolated_drag:{events:120,requests_before_ack:during,requests_after_drain:b.posts.length},
  tap_while_move_response_held:tapHeld,
  pass:true,limit:'Deferred mocked fetch responses, stub DOM and synthetic events; no elapsed device latency, WebKit, uinput or Wi-Fi measured.'};
}
(async()=>{const results=[];for(const name of ['before','accepted'])results.push(await run(name));console.log(JSON.stringify({results,pass:true},null,2))})().catch(e=>{console.error(e);process.exitCode=1});
