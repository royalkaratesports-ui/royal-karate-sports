"""Reading-first heading copy; factual body content and identifiers stay unchanged."""
import re
from html import escape

TITLES = {
    'index.html': 'Train with<br><span>Akash Shinde.</span>',
    'contact.html': 'Contact Royal Karate Sports',
    'about-akash-shinde.html': 'Akash Kishor Shinde',
    'sensei.html': 'Akash Kishor Shinde',
    'academy.html': 'About Royal Sports Academy',
    'kids-batches.html': 'Karate for kids',
    'adult-batches.html': 'Karate for adults',
    'competition.html': 'Sport karate',
    'enroll-now.html': 'Plan your first class',
    'trial.html': 'Plan your first class',
    'programs.html': 'Karate programmes',
    'instructors.html': 'Our instructors',
    'locations.html': 'Training centres',
    'seminars.html': 'Karate &amp; self-defense seminars',
    'achievements.html': 'Achievements &amp; recognition',
    'media.html': 'Media &amp; press',
    'events.html': 'Events &amp; karate camps',
    'gallery.html': 'Photo gallery',
    'information.html': 'About this website preview',
}
HEADINGS = {
 'TRAINING IS FREE. THE OPPORTUNITY IS YOURS.':'Training centres',
 'MORE TIME TO TRAIN. MORE ROOM TO GROW.':'Summer & winter camps',
 'A PRACTICE FOR EVERY NEXT STEP.':'Choose your karate programme',
 'GUIDANCE ON THE MAT. OPPORTUNITY BEYOND IT.':'Meet Akash Kishor Shinde',
 'A LITTLE CLARITY. A CONFIDENT START.':'Before your first class',
 'Two centres. Training for everyone.':'Our training centres',
 'A little clarity goes a long way.':'Common questions',
 'A FEW THINGS WORTH KNOWING.':'Common questions',
 'STEP ON THE MAT. CHANGE YOUR EVERYDAY.':'Enquire about your first class',
 'FREE KARATE TRAINING IN MUMBAI.':'Free karate training in Mumbai',
 'LESSONS THAT GO BEYOND THE MAT.':'Discipline, respect and confidence',
 'PRACTITIONER. COMPETITOR. TRAINER. ORGANIZER.':'Karate practice and experience',
 'A JOURNEY RECOGNIZED.':'Recognition',
 'THE MOST IMPORTANT PART IS THE STUDENTS.':'Working with students',
 'OPPORTUNITY FOR EVERY CHILD.':'Making karate accessible',
 'MORE COMMUNITIES. MORE POSSIBILITIES.':'Community work',
 'NO MONTHLY FEES. NO PAID CLASSES.':'Training is completely free',
 'STRENGTH WITH CONTROL.':'What you will practise',
 'MAKE PROGRESS PART OF YOUR LIFE.':'Develop technique at your pace',
 'A SHARED COMMITMENT.':'Training together',
 'START WHERE YOU ARE.':'Enquire about adult training',
 'KATA. KUMITE. ONE COMMITMENT.':'Kata and kumite',
 'RESULTS. NOT JUST NUMBERS.':'Competition records',
 'WHAT A FIRST CLASS CAN LOOK LIKE':'What to expect',
 'FIND YOUR STARTING POINT.':'Choose a programme',
 'A LITTLE ABOUT YOU.':'Your details',
 'YOUR NEXT STEP, READY TO REVIEW.':'Review your enquiry',
 'MORE THAN INSTRUCTIONS.':'Our coaching approach',
 'KNOW YOUR COACH. ASK THE RIGHT QUESTIONS.':'Questions for your instructor',
 'A CLEAR PATH. AT EVERY STEP.':'Learning step by step',
 'MORE THAN THE MOVEMENT.':'Skills beyond karate',
 'THEIR PRACTICE. THEIR PEOPLE.':'Our young learners',
 'LET’S FIND THEIR STARTING POINT.':'Enquire for your child',
 'THE RIGHT SPACE TO BEGIN.':'Where we train',
 'SPORT. OPPORTUNITY. COMMUNITY.':'Karate in the community',
 'THE STORY BEHIND THE RECOGNITION.':'Meet the founder',
 'TAKE THE PRACTICE BEYOND THE DOJO.':'Seminars for schools and groups',
 'A record of the journey.':'Browse the archive',
 'The purpose stays the same.':'Supporting the next generation',
 'What happens at camp.':'Camp activities',
}

def simplify_content(name, body):
    title = TITLES[name]
    body = re.sub(r'(<h1\b[^>]*>).*?(</h1>)', lambda m:m[1]+title+m[2], body, count=1, flags=re.S)
    def heading(match):
        plain = re.sub(r'<[^>]+>', ' ', match[2])
        plain = ' '.join(plain.split())
        return match[1]+escape(HEADINGS[plain])+match[3] if plain in HEADINGS else match[0]
    return re.sub(r'(<h[23]\b[^>]*>)(.*?)(</h[23]>)', heading, body, flags=re.S)
