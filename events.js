'use strict';
(() => {
 const links=[...document.querySelectorAll('[data-event-open]')];
 const dialog=document.querySelector('#event-viewer');
 const image=document.querySelector('#event-full');
 let current=0,opener;
 function show(index){
  current=(index+links.length)%links.length;
  const link=links[current];
  image.src=link.getAttribute('href');image.alt=link.querySelector('img').alt;
  document.querySelector('#event-viewer-title').textContent=link.dataset.title;
  document.querySelector('#event-original').setAttribute('href',link.getAttribute('href'));
  document.querySelector('#event-position').textContent=`${current+1} / ${links.length}`;
 }
 links.forEach((link,index)=>link.addEventListener('click',event=>{
  event.preventDefault();opener=link;show(index);dialog.showModal();document.body.classList.add('locked');
 }));
 document.querySelector('[data-event-prev]').addEventListener('click',()=>show(current-1));
 document.querySelector('[data-event-next]').addEventListener('click',()=>show(current+1));
 document.querySelector('[data-event-close]').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('keydown',event=>{
  if(event.key==='ArrowRight'){event.preventDefault();show(current+1);}
  if(event.key==='ArrowLeft'){event.preventDefault();show(current-1);}
 });
 dialog.addEventListener('close',()=>{document.body.classList.remove('locked');opener?.focus({preventScroll:true});});
 dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
})();
