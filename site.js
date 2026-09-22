'use strict';
const programs = {
  kids: {name:'Kids karate',tag:'Kids · Foundations',image:'kids-group-training',alt:'Young karate students practising stances together on training mats',copy:'A positive introduction to movement, listening and self-belief. Learn the basics, celebrate effort and grow one class at a time.'},
  teens: {name:'Teen karate',tag:'Teens · Focus & growth',image:'kids-line-practice',alt:'Young karate students practising punches in a line',copy:'Find focus and a stronger sense of self. A proposed pathway built around technique, perseverance and steady personal progress.'},
  adults: {name:'Adult karate',tag:'Adults · A lasting practice',image:'adults-class-practice',alt:'Adult practitioners and younger students lined up for karate practice',copy:'Start fresh or return to the mat. Build movement, technical foundations and a purposeful training routine at an appropriate pace.'},
  sport: {name:'Sport karate',tag:'Sport · Precision & performance',image:'adults-shotokan',alt:'Karate practitioners working on stances and punches indoors',copy:'Turn attention into performance. Explore kata and kumite with a proposed progression based on technique, control and readiness.'}
};
const tabs = [...document.querySelectorAll('[data-program]')];
function selectProgram(tab) {
  const key = tab.dataset.program, data = programs[key];
  tabs.forEach(t => {t.setAttribute('aria-selected',String(t===tab));t.tabIndex=t===tab?0:-1;});
  const img = document.querySelector('#program-image');
  img.src=`assets/${data.image}.webp`;img.alt=data.alt;
  document.querySelector('#program-tag').textContent=data.tag;
  document.querySelector('#program-description').textContent=data.copy;
  document.querySelector('#program-link').href=`programs.html#${key}`;
  document.querySelector('#program-panel').setAttribute('aria-labelledby',tab.id);
}
tabs.forEach((tab,index) => {
  tab.addEventListener('click',()=>selectProgram(tab));
  tab.addEventListener('keydown',event=>{
    let next;
    if(['ArrowRight','ArrowDown'].includes(event.key))next=(index+1)%tabs.length;
    if(['ArrowLeft','ArrowUp'].includes(event.key))next=(index-1+tabs.length)%tabs.length;
    if(event.key==='Home')next=0;
    if(event.key==='End')next=tabs.length-1;
    if(next!==undefined){event.preventDefault();selectProgram(tabs[next]);tabs[next].focus();}
  });
});
const tabOrientation = matchMedia('(max-width:760px)');
function updateTabOrientation(){document.querySelector('.program-tabs')?.setAttribute('aria-orientation',tabOrientation.matches?'horizontal':'vertical');}
updateTabOrientation();tabOrientation.addEventListener('change',updateTabOrientation);

const lightbox = document.querySelector('.lightbox');
let photoOpener;
document.querySelectorAll('[data-photo]').forEach(button => button.addEventListener('click',()=>{
  photoOpener=button;
  const image=lightbox.querySelector('img');
  image.src=button.dataset.photo;
  image.alt=button.querySelector('img').alt;
  document.querySelector('#lightbox-title').textContent=button.dataset.caption;
  lightbox.showModal();document.body.classList.add('locked');
}));
document.querySelector('[data-close-lightbox]')?.addEventListener('click',()=>lightbox.close());
lightbox?.addEventListener('close',()=>{document.body.classList.remove('locked');photoOpener?.focus({preventScroll:true});});
lightbox?.addEventListener('click',event=>{if(event.target===lightbox){const r=lightbox.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)lightbox.close();}});
const filters=[...document.querySelectorAll('[data-filter]')];
filters.forEach(button=>button.addEventListener('click',()=>{
  filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  let count=0;
  document.querySelectorAll('.gallery-grid figure').forEach(figure=>{figure.hidden=button.dataset.filter!=='all'&&figure.dataset.category!==button.dataset.filter;if(!figure.hidden)count++;});
  document.querySelector('#gallery-count').textContent=`${count} photograph${count===1?'':'s'}`;
}));

const desktopGroups = [...document.querySelectorAll('.desktop-nav .nav-group')];
document.addEventListener('click', event => {
  desktopGroups.forEach(group => { if (!group.contains(event.target)) group.open=false; });
});
document.addEventListener('keydown', event => {
  if(event.key!=='Escape') return;
  const open=desktopGroups.find(group=>group.open);
  if(open){open.open=false;open.querySelector('summary').focus();event.preventDefault();}
});

const menu = document.querySelector('#mobile-menu');
const menuToggle = document.querySelector('.menu-toggle');
menuToggle?.addEventListener('click', () => {
  menu.showModal();
  document.body.classList.add('locked');
});
document.querySelector('[data-close-menu]')?.addEventListener('click', () => menu.close());
menu?.addEventListener('close', () => {
  document.body.classList.remove('locked');
  menuToggle.focus({preventScroll:true});
});
menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.close()));

