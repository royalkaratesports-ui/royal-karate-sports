'use strict';
(() => {
 const cards=[...document.querySelectorAll('.achievement-card')];
 const filters=[...document.querySelectorAll('[data-ach-filter]')];
 const viewer=document.querySelector('#achievement-viewer');
 const image=document.querySelector('#achievement-full');
 const stage=document.querySelector('.achievement-stage');
 const zoom=document.querySelector('[data-ach-zoom]');
 let collection=[],index=0,opener;
 filters.forEach(button=>button.addEventListener('click',()=>{
  filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  cards.forEach(card=>card.hidden=button.dataset.achFilter!=='all'&&card.dataset.achCategory!==button.dataset.achFilter);
  document.querySelector('#achievements-count').textContent=`${cards.filter(c=>!c.hidden).length} archive items`;
 }));
 function setZoom(active){
  stage.classList.toggle('is-zoomed',active);zoom.setAttribute('aria-pressed',String(active));zoom.textContent=active?'Fit image':'Zoom in';stage.scrollTop=0;stage.scrollLeft=0;
 }
 function show(next){
  index=(next+collection.length)%collection.length;
  const source=collection[index];
  image.src=source.dataset.view;image.alt=source.querySelector('img').alt;
  document.querySelector('#achievement-viewer-title').textContent=source.dataset.title;
  document.querySelector('#achievement-note').textContent=source.dataset.note;
  document.querySelector('#achievement-original').setAttribute('href',source.getAttribute('href'));
  document.querySelector('#achievement-position').textContent=`${index+1} / ${collection.length}`;
  setZoom(false);
 }
 document.querySelectorAll('[data-ach-open]').forEach(link=>link.addEventListener('click',event=>{
  event.preventDefault();opener=link;
  collection=cards.filter(c=>!c.hidden).map(c=>c.querySelector('[data-ach-open]'));
  let position=collection.findIndex(c=>c.dataset.view===link.dataset.view);
  if(position<0){collection=[link];position=0;}
  show(position);viewer.showModal();document.body.classList.add('locked');
 }));
 document.querySelector('[data-ach-close]').addEventListener('click',()=>viewer.close());
 document.querySelector('[data-ach-prev]').addEventListener('click',()=>show(index-1));
 document.querySelector('[data-ach-next]').addEventListener('click',()=>show(index+1));
 zoom.addEventListener('click',()=>setZoom(zoom.getAttribute('aria-pressed')!=='true'));
 viewer.addEventListener('keydown',event=>{
  if(event.key==='ArrowRight'&&!(event.target===stage&&zoom.getAttribute('aria-pressed')==='true')){event.preventDefault();show(index+1);}
  if(event.key==='ArrowLeft'&&!(event.target===stage&&zoom.getAttribute('aria-pressed')==='true')){event.preventDefault();show(index-1);}
 });
 viewer.addEventListener('close',()=>{document.body.classList.remove('locked');opener?.focus({preventScroll:true});});
 viewer.addEventListener('click',event=>{if(event.target!==viewer)return;const r=viewer.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)viewer.close();});
})();
