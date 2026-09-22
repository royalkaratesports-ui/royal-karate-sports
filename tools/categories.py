"""Reference-matched categories, expressed in Royal's own design."""
from html import escape
from akash_profile import build_profile
from kids_content import build_kids
from adults_content import build_adults
from media_content import build_media
from achievements_content import build_achievements
from events_content import build_events
from contact_content import build_contact
GROUPS=[('About Us',[('about-akash-shinde.html','About Akash Shinde'),('academy.html','About Royal Sports Academy'),('instructors.html','Instructors')]),('Programmes',[('kids-batches.html','Kids Batches'),('adult-batches.html','Adult Batches'),('seminars.html','Seminars')]),('Trending',[('media.html','Media'),('events.html','Events'),('achievements.html','Achievements')])]
def anchor(url,label,current):
 if current=='sensei.html':current='about-akash-shinde.html'
 return f'<a href="{url}"'+(' aria-current="page"' if current==url else '')+f'>{escape(label)}</a>'
def navigation(current,mobile=False):
 parts=[anchor('index.html','Home',current)]
 for label,items in GROUPS:
  active=any(u==current for u,_ in items)
  parts.append(f'<details class="nav-group'+(' current-group' if active else '')+f'" name="'+('mobile' if mobile else 'desktop')+f'-categories"><summary>{label}</summary><ul class="subnav">'+''.join(f'<li>{anchor(u,t,current)}</li>' for u,t in items)+'</ul></details>')
 parts.append(anchor('contact.html','Contact',current))
 return ''.join(parts)
def footer_navigation(current):
 items=[('index.html','Home')]+[item for _,group in GROUPS for item in group]+[('contact.html','Contact')]
 return ''.join(anchor(u,t,current) for u,t in items)

def build_category_pages(write,mast,image,button,link,cta,competition):
 sensei=build_profile(button,link)
 write('about-akash-shinde.html','About Akash Kishor Shinde',sensei,'profile-page')
 write('sensei.html','About Akash Kishor Shinde',sensei,'profile-page')
 write('kids-batches.html','Kids Batches',build_kids(button,link),'kids-page')
 write('adult-batches.html','Adult Batches',build_adults(button,link),'adults-page')
 seminars=mast('Programmes / Seminars','KNOWLEDGE SHARED.<br>CONFIDENCE BUILT.','Explore proposed karate and personal-safety workshops for schools, colleges, workplaces and community groups.')+'<section class="wrap section editorial-split"><figure>'+image(7045594,'Illustrative group martial arts training session')+'</figure><div><span class="eyebrow red">Seminars</span><h2>TAKE THE PRACTICE<br>BEYOND THE DOJO.</h2><p>A seminar can introduce purposeful movement, controlled technique and the principles of respectful training. Personal-safety sessions should emphasize awareness, avoidance and seeking help—not promises of guaranteed protection.</p><div class="coaching-lines"><div>School and college groups</div><div>Workplace and community groups</div><div>Karate fundamentals and personal-safety awareness</div></div>'+link('Discuss a seminar enquiry','contact.html')+'<div class="content-note"><strong>Proposed offering—not a confirmed event</strong>Topics, instructors, suitability, format, venue and availability need approval by Royal. There are no paid karate classes. No previous seminars or partnerships are claimed.</div></div></section>'+cta()
 write('seminars.html','Seminars',seminars)
 write('media.html','Media & Press',build_media(button,link),'media-page')
 write('events.html','Events & Camps',build_events(button,link),'events-page')
 write('achievements.html','Achievements',build_achievements(button,link),'achievements-page')
 write('contact.html','Contact',build_contact(button,link),'contact-refresh')
