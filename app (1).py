"""
╔══════════════════════════════════════════════════════════════════╗
║           LIBRARY AI PRO  ·  Complete Management System          ║
║         AI · QR · E-Book · Book Shop · Gamification · Reports        ║
╚══════════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random, string, base64, time, warnings
from datetime import date, timedelta, datetime
from collections import defaultdict
from data import (BOOKS_DATA, BOOK_SUMMARIES, LEARNING_PATHS, DEMO_REVIEWS,
                  GENRES, AVATARS, LANGS, LANG_LABELS)
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════
st.set_page_config(page_title="📚 LibraryAI Pro",page_icon="📚",layout="wide",initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#030712 0%,#060c1a 40%,#030b17 100%);}
.main .block-container{padding:1.2rem 2rem;max-width:1440px;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#070e24 0%,#0a1228 60%,#060e20 100%) !important;
  border-right:1px solid rgba(99,102,241,0.15) !important;
}
section[data-testid="stSidebar"] *{color:#b4bfd6 !important;}
section[data-testid="stSidebar"] .stButton>button{
  background:rgba(255,255,255,0.02) !important;
  border:1px solid rgba(99,102,241,0.12) !important;
  color:#7c8db5 !important; border-radius:10px;
  font-size:0.82rem; padding:8px 14px;
  text-align:left !important; width:100%;
  transition:all 0.2s;
}
section[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(99,102,241,0.12) !important;
  border-color:rgba(99,102,241,0.4) !important;
  color:#a5b4fc !important; transform:translateX(3px);
}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
  color:white !important; border:none !important;
  border-radius:10px; font-weight:500; font-size:0.84rem;
  box-shadow:0 4px 15px rgba(79,70,229,0.25);
  transition:all 0.25s;
}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(79,70,229,0.45) !important;}
.stButton>button[kind="secondary"]{
  background:rgba(99,102,241,0.08) !important;
  border:1px solid rgba(99,102,241,0.3) !important;
  color:#a5b4fc !important; box-shadow:none;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(10,18,40,0.8); border-radius:12px;
  padding:5px; gap:3px; border:1px solid rgba(99,102,241,0.12);
}
.stTabs [data-baseweb="tab"]{
  background:transparent; border-radius:9px;
  color:#4b5568; font-weight:500; font-size:0.82rem; padding:8px 16px;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(79,70,229,0.3),rgba(124,58,237,0.25)) !important;
  color:#c4b5fd !important; box-shadow:0 2px 12px rgba(79,70,229,0.18);
}

/* ── Metrics ── */
div[data-testid="stMetric"]{
  background:linear-gradient(135deg,rgba(10,18,40,0.9),rgba(14,24,50,0.8));
  border:1px solid rgba(99,102,241,0.18); border-radius:14px;
  padding:18px 20px; transition:transform 0.2s,box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(79,70,229,0.2);}
div[data-testid="stMetric"] label{color:#4b5568 !important;font-size:0.72rem !important;text-transform:uppercase;letter-spacing:0.06em;}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{color:#a5b4fc !important;font-size:1.75rem !important;font-weight:800 !important;}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"]{color:#34d399 !important;}

/* ── Inputs ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input{
  background:rgba(10,18,40,0.8) !important; border:1px solid rgba(99,102,241,0.18) !important;
  color:#e2e8f0 !important; border-radius:10px !important;
}
.stTextInput>div>div>input:focus{border-color:rgba(99,102,241,0.55) !important;box-shadow:0 0 0 3px rgba(99,102,241,0.1) !important;}
.stSelectbox>div>div,.stMultiSelect>div>div{
  background:rgba(10,18,40,0.8) !important; border:1px solid rgba(99,102,241,0.18) !important;
  border-radius:10px !important; color:#e2e8f0 !important;
}
.stSlider>div>div>div{background:rgba(99,102,241,0.25) !important;}
.stDataFrame{border:1px solid rgba(99,102,241,0.12);border-radius:12px;overflow:hidden;}
hr{border-color:rgba(99,102,241,0.08) !important;}
.stProgress .st-bo{background:linear-gradient(90deg,#4f46e5,#a855f7) !important;}

/* ── Typography ── */
.hero{
  font-family:'Playfair Display',serif; font-size:2.8rem; font-weight:900;
  background:linear-gradient(135deg,#818cf8,#c084fc,#38bdf8,#818cf8);
  background-size:200% auto; -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; background-clip:text;
  animation:shimmer 4s linear infinite; line-height:1.1;
}
@keyframes shimmer{0%{background-position:0% center}100%{background-position:200% center}}
.page-h{
  font-family:'Playfair Display',serif; font-size:1.7rem; font-weight:700;
  background:linear-gradient(135deg,#818cf8,#c084fc);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.sub{color:#374151;font-size:0.88rem;margin-top:4px;}

/* ── Cards ── */
.card{
  background:linear-gradient(135deg,rgba(10,18,40,0.95),rgba(14,24,52,0.75));
  border:1px solid rgba(99,102,241,0.13); border-radius:16px;
  padding:20px; backdrop-filter:blur(10px);
  transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;
}
.card:hover{border-color:rgba(99,102,241,0.38);transform:translateY(-3px);box-shadow:0 14px 40px rgba(79,70,229,0.14);}
.book-card{
  background:linear-gradient(135deg,rgba(8,15,35,0.97),rgba(12,22,46,0.82));
  border:1px solid rgba(99,102,241,0.1); border-radius:14px;
  padding:0 0 14px; overflow:hidden; transition:all 0.25s; height:100%;
}
.book-card:hover{border-color:rgba(99,102,241,0.42);transform:translateY(-4px);box-shadow:0 16px 45px rgba(79,70,229,0.16);}
.book-spine{width:100%;height:7px;}
.book-inner{padding:12px 14px 0;}
.bk-title{font-weight:700;color:#e2e8f0;font-size:0.88rem;line-height:1.35;margin:6px 0 3px;}
.bk-author{color:#4b5568;font-size:0.76rem;}
.bk-desc{color:#374151;font-size:0.73rem;line-height:1.5;margin-top:6px;}

/* ── Badges ── */
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:500;margin:1px;}
.bp{background:rgba(139,92,246,.15);color:#a78bfa;border:1px solid rgba(139,92,246,.25);}
.bb{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.25);}
.bg{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.25);}
.br{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.25);}
.ba{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.25);}
.bc{background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.25);}
.bpk{background:rgba(236,72,153,.15);color:#f472b6;border:1px solid rgba(236,72,153,.25);}
.award-tag{font-size:0.67rem;color:#fbbf24;padding:2px 8px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:10px;}

/* ── Chat ── */
.chat-u{background:linear-gradient(135deg,#3730a3,#4f46e5);border-radius:16px 16px 4px 16px;padding:11px 16px;margin:7px 0 7px auto;max-width:78%;color:white;font-size:0.86rem;box-shadow:0 4px 18px rgba(79,70,229,.3);}
.chat-b{background:rgba(10,18,40,.9);border:1px solid rgba(99,102,241,.18);border-radius:16px 16px 16px 4px;padding:11px 16px;margin:7px 0;max-width:84%;color:#e2e8f0;font-size:0.86rem;}

/* ── Loan / Train cards ── */
.loan-card{background:rgba(10,18,40,.9);border:1px solid rgba(99,102,241,.12);border-left:3px solid var(--lc,#4f46e5);border-radius:14px;padding:16px;margin:8px 0;transition:transform .2s;}
.loan-card:hover{transform:translateY(-2px);}
/* train-card removed */

/* ── Misc ── */
.xp-bg{background:rgba(99,102,241,.12);border-radius:4px;height:6px;width:100%;}
.xp-fill{background:linear-gradient(90deg,#4f46e5,#a855f7);border-radius:4px;height:6px;}
.ebook{background:rgba(8,15,33,.97);border:1px solid rgba(99,102,241,.18);border-radius:14px;padding:28px 34px;font-size:0.92rem;line-height:1.95;color:#cbd5e1;min-height:280px;}
.qr-wrap{background:white;border-radius:10px;padding:8px;display:inline-block;text-align:center;}
.notif{background:rgba(10,18,40,.95);border:1px solid rgba(99,102,241,.15);border-radius:9px;padding:7px 12px;font-size:0.77rem;color:#64748b;margin:3px 0;}
.divider{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.25),transparent);margin:1.4rem 0;}
.ai-pill{display:inline-flex;align-items:center;gap:5px;background:linear-gradient(135deg,rgba(79,70,229,.18),rgba(124,58,237,.18));border:1px solid rgba(99,102,241,.28);border-radius:20px;padding:4px 12px;font-size:0.73rem;color:#a5b4fc;}
.stat-card{background:rgba(10,18,40,.8);border:1px solid rgba(99,102,241,.12);border-radius:12px;padding:12px 16px;text-align:center;}
.stat-n{font-size:1.6rem;font-weight:800;color:#a5b4fc;}
.stat-l{font-size:0.71rem;color:#374151;text-transform:uppercase;letter-spacing:.05em;margin-top:2px;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  STATE BOOTSTRAP
# ══════════════════════════════════════════════════════
def _books():
    out = []
    avail_pool = [True,True,True,False]
    for i,b in enumerate(BOOKS_DATA):
        e = {**b}
        e["id"]       = i+1
        e["available"]= random.choice(avail_pool)
        e["copies"]   = random.randint(2,5)
        e["tags"]     = [b["genre"].lower(), b["author"].split()[-1].lower()]
        e["reviews"]  = DEMO_REVIEWS.get(b["title"],[])
        e["demand"]   = round(b["borrows"]/200*5,1)
        out.append(e)
    return out

def _users():
    return [
        {"id":1,"name":"Dr. Admin","email":"admin@library.com","pass":"admin123","role":"admin",
         "age":38,"fav":"Technology","borrowed":0,"xp":800,"level":8,
         "badges":["🏆 Library Champion","⭐ Super Admin"],"history":[],"avatar":"👨‍💼",
         "joined":"2022-01-01","fines":0.0,"lang":"en","bio":"Library Administrator"},
        {"id":2,"name":"Ahmed Mohammed","email":"ahmed@email.com","pass":"pass123","role":"member",
         "age":24,"fav":"Fiction","borrowed":12,"xp":240,"level":3,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl"],"history":[1,2,7,13,15],
         "avatar":"👨‍🎓","joined":"2023-03-15","fines":2.50,"lang":"en","bio":"Computer Science student"},
        {"id":3,"name":"Sara Hassan","email":"sara@email.com","pass":"pass123","role":"member",
         "age":29,"fav":"Science","borrowed":18,"xp":420,"level":5,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl","⭐ Elite Reader"],"history":[16,21,38,3,11],
         "avatar":"👩‍🔬","joined":"2022-09-10","fines":0.0,"lang":"en","bio":"Biology researcher"},
        {"id":4,"name":"James Wilson","email":"james@email.com","pass":"pass123","role":"member",
         "age":35,"fav":"History","borrowed":25,"xp":580,"level":6,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl","🏆 Library Champion"],"history":[23,24,22,36,40],
         "avatar":"👨‍🏫","joined":"2022-05-20","fines":1.00,"lang":"en","bio":"History teacher"},
        {"id":5,"name":"Mia Chen","email":"mia@email.com","pass":"pass123","role":"member",
         "age":21,"fav":"Fantasy","borrowed":8,"xp":160,"level":2,
         "badges":["🌱 Seedling Reader","📖 Bookworm"],"history":[11,13,15],"avatar":"👩‍🎓",
         "joined":"2024-01-05","fines":0.5,"lang":"en","bio":"Literature student"},
    ]

def _loans():
    loans=[]
    templates=[
        (2,2,-45,-31,True,0.0,"Sara Hassan"),(2,7,-30,-17,True,0.0,"Sara Hassan"),
        (2,15,-20,-8,True,3.0,"James Wilson"),(3,16,-60,-47,True,0.0,"Ahmed Mohammed"),
        (3,21,-35,-21,True,0.0,"Ahmed Mohammed"),(4,23,-50,-34,True,2.0,"Dr. Admin"),
        (4,36,-25,-12,True,0.0,"Dr. Admin"),(5,11,-18,-5,True,0.5,"Mia Chen"),
        # Active
        (2,3,-5,None,False,0.0,""),(3,38,-10,None,False,0.0,""),
        (4,1,-8,None,False,0.0,""),(5,13,-2,None,False,0.0,""),
    ]
    for lid,(uid,bid,bd_off,rd_off,ret,fine,_) in enumerate(templates,1):
        bk=next((b for b in st.session_state.books if b["id"]==bid),{})
        bdate=date.today()+timedelta(days=bd_off)
        ddate=bdate+timedelta(days=14)
        rdate=(bdate+timedelta(days=abs(rd_off))) if rd_off else None
        loans.append({"id":lid,"uid":uid,"bid":bid,"title":bk.get("title","?"),
                      "author":bk.get("author",""),"genre":bk.get("genre",""),
                      "bdate":bdate.isoformat(),"ddate":ddate.isoformat(),
                      "rdate":rdate.isoformat() if rdate else None,
                      "returned":ret,"fine":fine,"late":fine>0,"risk":round(random.uniform(.1,.45),2),"days":14})
    return loans

# _trains() removed

def _monthly():
    months=[]
    for i in range(12):
        d=(date.today().replace(day=1)-timedelta(days=30*i))
        months.append({"month":d.strftime("%b %Y"),"borrows":random.randint(95,260),
                       "returns":random.randint(85,250),"new_users":random.randint(4,22),
                       "fines":round(random.uniform(15,95),2)})
    return list(reversed(months))

def boot():
    if "booted" not in st.session_state:
        st.session_state.booted  = True
        st.session_state.user    = None
        st.session_state.books   = _books()
        st.session_state.users   = _users()
        st.session_state.loans   = []
        st.session_state.reservations = []
        st.session_state.cart    = []
        st.session_state.orders  = []
        st.session_state.chat    = []
        st.session_state.page    = "🏠 Home"
        st.session_state.monthly = _monthly()
        st.session_state.lid     = 20
        st.session_state.notifs  = []
        st.session_state.vq      = ""
        st.session_state.loans   = _make_seed_loans()

def _make_seed_loans():
    if "books" not in st.session_state: return []
    loans=[]
    templates=[
        (2,2,-45,-31,True,0.0),(2,7,-30,-17,True,0.0),(2,15,-20,-8,True,3.0),
        (3,16,-60,-47,True,0.0),(3,21,-35,-21,True,0.0),(4,23,-50,-34,True,2.0),
        (4,36,-25,-12,True,0.0),(5,11,-18,-5,True,0.5),
        (2,3,-5,None,False,0.0),(3,38,-10,None,False,0.0),
        (4,1,-8,None,False,0.0),(5,13,-2,None,False,0.0),
    ]
    for lid,(uid,bid,bd_off,rd_off,ret,fine) in enumerate(templates,1):
        bk=next((b for b in st.session_state.books if b["id"]==bid),{})
        bdate=date.today()+timedelta(days=bd_off)
        ddate=bdate+timedelta(days=14)
        rdate=(bdate+timedelta(days=abs(rd_off))) if rd_off else None
        loans.append({"id":lid,"uid":uid,"bid":bid,"title":bk.get("title","?"),
                      "author":bk.get("author",""),"genre":bk.get("genre",""),
                      "bdate":bdate.isoformat(),"ddate":ddate.isoformat(),
                      "rdate":rdate.isoformat() if rdate else None,
                      "returned":ret,"fine":fine,"late":fine>0,"risk":round(random.uniform(.1,.45),2),"days":14})
    return loans

boot()

# ══════════════════════════════════════════════════════
#  UTILS
# ══════════════════════════════════════════════════════
def U():       return st.session_state.user
def admin():   return U() and U()["role"]=="admin"
def logged():  return U() is not None
def bk(i):     return next((b for b in st.session_state.books if b["id"]==i),None)
def usr(i):    return next((u for u in st.session_state.users if u["id"]==i),None)
def by_em(e):  return next((u for u in st.session_state.users if u["email"]==e),None)
def nav(p):    st.session_state.page=p; st.rerun()
def notify(m,k="success"):
    st.session_state.notifs.append({"m":m,"k":k,"t":datetime.now().strftime("%H:%M")})
def xp_up(uid,pts,badge=None):
    for u in st.session_state.users:
        if u["id"]==uid:
            u["xp"]+=pts; u["level"]=max(1,u["xp"]//100)
            if badge and badge not in u["badges"]: u["badges"].append(badge)
    if U() and U()["id"]==uid:
        st.session_state.user["xp"]+=pts
        st.session_state.user["level"]=max(1,st.session_state.user["xp"]//100)
        if badge and badge not in st.session_state.user.get("badges",[]):
            st.session_state.user.setdefault("badges",[]).append(badge)

def qr(text):
    n=18; cell=6
    random.seed(abs(hash(text))%99999)
    cells=[[random.random()>0.48 for _ in range(n)] for _ in range(n)]
    for r in range(7):
        for c in range(7):   cells[r][c]=(r in[0,6] or c in[0,6] or (2<=r<=4 and 2<=c<=4))
        for c in range(n-7,n):cells[r][c]=(r in[0,6] or c in[n-7,n-1] or (2<=r<=4 and n-5<=c<=n-3))
    for c in range(7):
        for r in range(n-7,n):cells[r][c]=(r in[n-7,n-1] or c in[0,6] or (n-5<=r<=n-3 and 2<=c<=4))
    rects="".join(f'<rect x="{c*cell+4}" y="{r*cell+4}" width="{cell}" height="{cell}" fill="#1a0a3a"/>'
                  for r in range(n) for c in range(n) if cells[r][c])
    W=n*cell+8
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}"><rect width="100%" height="100%" fill="white" rx="4"/>{rects}</svg>'
    return base64.b64encode(svg.encode()).decode()

def late_risk(u,b,days):
    s=0.07
    if u.get("age",25)<22: s+=0.20
    elif u.get("age",25)<28: s+=0.09
    if days<=7: s+=0.19
    if u.get("borrowed",0)>20: s+=0.07
    if u.get("fav")!=b.get("genre"): s+=0.05
    s+=sum(1 for l in st.session_state.loans if l["uid"]==u["id"] and l.get("late"))*0.06
    return min(round(s+random.uniform(-.03,.04),2),.95)

def smart_recs(u,n=6):
    hist_g=[]; hist_a=[]
    for bid in u.get("history",[]):
        b=bk(bid)
        if b: hist_g.append(b["genre"]); hist_a.append(b["author"])
    fav=u.get("fav","Fiction"); done=set(u.get("history",[]))
    scored=[]
    for b in st.session_state.books:
        if b["id"] in done: continue
        s=0
        if b["genre"]==fav:            s+=5
        if b["genre"] in hist_g:       s+=3
        if b["author"] in hist_a:      s+=4
        s+=b["rating"]*.6+b["borrows"]/60
        scored.append((s,b))
    scored.sort(key=lambda x:-x[0])
    return [b for _,b in scored[:n]]

def nlp_search(q):
    ql=q.lower()
    kw={"space":"Science","universe":"Science","history":"History","magic":"Fantasy",
        "mystery":"Mystery","tech":"Technology","code":"Technology","program":"Technology",
        "children":"Children","habit":"Self-Help","money":"Self-Help","bio":"Biography",
        "philosophy":"Philosophy","war":"History","love":"Romance","health":"Health",
        "dystopia":"Fiction","classic":"Fiction","award":"","popular":"","recent":""}
    results=[]
    for b in st.session_state.books:
        s=0
        if ql in b["title"].lower():   s+=6
        if ql in b["author"].lower():  s+=5
        if ql in b["genre"].lower():   s+=4
        if ql in b["desc"].lower():    s+=2
        if any(ql in t for t in b.get("tags",[])):  s+=3
        for word,genre in kw.items():
            if word in ql:
                if genre and b["genre"]==genre: s+=4
                if word=="award" and b.get("award"): s+=3
                if word=="popular": s+=b["borrows"]/40
                if word=="recent" and b["year"]>2010: s+=3
        if b.get("award") and ql in b["award"].lower(): s+=4
        if s>0: results.append((s,b))
    results.sort(key=lambda x:-x[0])
    return [b for _,b in results[:12]]

def bot(msg):
    m=msg.lower().strip(); u=U()
    if any(w in m for w in ["hello","hi","hey","greetings","good morning","good afternoon"]):
        name=u["name"].split()[0] if u else "there"
        return (f"👋 Hello, **{name}**! I'm **LibBot**, your AI Librarian.\n\n"
                "I can help you:\n• 🔍 `find books about [topic]`\n• 🧠 `recommend books for me`\n"
                "• 📖 `summary of [title]`\n• 🚂 `train schedules`\n• 📊 `library stats`")
    for title,summary in BOOK_SUMMARIES.items():
        if title.lower() in m and ("summary" in m or "about" in m or "tell" in m or title.lower() in m):
            return f"📖 **{title}**\n\n{summary}"
    if u and any(w in m for w in ["recommend","suggest","what should i read","good book"]):
        recs=smart_recs(u,4)
        r=f"🧠 **Personalised for {u['name']}** ({u['fav']} lover, Level {u['level']}):\n"
        for b in recs:
            av="✅" if b["available"] else "❌"
            aw=" 🏆" if b.get("award") else ""
            r+=f"\n{av} **{b['title']}** by {b['author']} — ★{b['rating']}{aw}"
        return r
    if any(w in m for w in ["find","search","look for","books about","books on","show me"]):
        query=m
        for w in ["find","search","look for","books about","books on","show me","books","a book"]:
            query=query.replace(w,"")
        query=query.strip()
        results=nlp_search(query) if len(query)>1 else []
        if results:
            r=f"🔍 Found **{len(results)} books** matching *'{query}'*:\n"
            for b in results[:5]:
                av="✅" if b["available"] else "❌"
                r+=f"\n{av} **{b['title']}** ★{b['rating']} — {b['genre']}{'🏆' if b.get('award') else ''}"
            return r
        return f"🤔 No books found for *'{query}'*. Try: *fiction, science, mystery, technology*..."
    if any(w in m for w in ["available","free book","borrow"]):
        av=sum(1 for b in st.session_state.books if b["available"])
        return f"📖 **{av}** books are currently available out of **{len(st.session_state.books)}** total."
    if any(w in m for w in ["stat","how many","total","count"]):
        ov=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<date.today())
        return (f"📊 **Library Statistics:**\n• 📚 Books: **{len(st.session_state.books)}** "
                f"({sum(1 for b in st.session_state.books if b['available'])} available)\n"
                f"• 👥 Members: **{len(st.session_state.users)}**\n"
                f"• 📋 Loans: **{len(st.session_state.loans)}**\n"
                f"• 🚨 Overdue: **{ov}**\n"
                f"• 🏆 Award Books: **{sum(1 for b in st.session_state.books if b.get('award'))}**")
    if any(w in m for w in ["buy","shop","purchase","price","cost","order"]):
        shop_books=[b for b in st.session_state.books if b.get("price",0)>0]
        return (f"🛒 **Book Shop:**\n• **{len(shop_books)}** books available to buy\n"
                f"• Prices from £{min(b['price'] for b in shop_books):.2f}\n"
                f"• AI recommendations available\n• Instant purchase with QR receipt\n\n👉 Go to **🛒 Book Shop** to browse!")
    if any(w in m for w in ["overdue","late","fine","penalty","fee"]):
        return ("⏰ **Overdue & Fines:**\n• Rate: **£0.50 per day** after due date\n"
                "• Check: **📋 My Loans** section\n• Return on time → earn ⚡ Speed Reader badge!")
    if any(w in m for w in ["learn","career","path","study","goal","reading list"]):
        r="🎯 **Learning Paths:**\n"
        for p in LEARNING_PATHS: r+=f"\n• {p}"
        return r+"\n\n👉 **🤖 AI Features → Learning Path**"
    if any(w in m for w in ["bye","goodbye","thanks","thank you","cheers"]):
        return "👋 **Happy reading!** I'm here 24/7 — come back anytime! 📚✨"
    return ("🤖 I can help with:\n• `find books about [topic]`\n• `recommend books for me`\n"
            "• `summary of [book title]`\n• `library statistics`\n• `train info`\n"
            "• `learning path`\n• `overdue policy`")

# delay_p() removed

def plt_config(ax,fig=None):
    ax.set_facecolor("#06091a")
    if fig: fig.patch.set_alpha(0)
    ax.tick_params(colors="#374151",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#1e2d4a")

# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:8px 0 4px"><span style="font-size:1.4rem;font-weight:700;background:linear-gradient(135deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent">📚 LibraryAI Pro</span></div>',unsafe_allow_html=True)
    if logged():
        u=U(); lp=u["xp"]%100
        bdg=" ".join(b[:2] for b in u.get("badges",[])[:4])
        st.markdown(
            f'<div class="card" style="padding:13px;margin:8px 0">'
            f'<div style="display:flex;align-items:center;gap:10px">'
            f'<span style="font-size:2rem">{u["avatar"]}</span>'
            f'<div><div style="font-weight:700;color:#e2e8f0;font-size:0.9rem">{u["name"]}</div>'
            f'<div style="color:#374151;font-size:0.7rem">{u["role"].upper()} · Lv.{u["level"]} · ⚡{u["xp"]}XP</div>'
            f'<div style="margin-top:2px;font-size:0.9rem">{bdg}</div></div></div>'
            f'<div style="margin-top:8px"><div class="xp-bg"><div class="xp-fill" style="width:{lp}%"></div></div>'
            f'<div style="color:#1e293b;font-size:0.67rem;margin-top:2px">{100-lp} XP to Level {u["level"]+1}</div></div>'
            f'</div>',unsafe_allow_html=True)
    st.markdown('<div class="divider" style="margin:8px 0"></div>',unsafe_allow_html=True)

    adm_pages=["🏠 Home","📖 Books","🛒 Book Shop","🔍 Smart Search","🤖 AI Features","📋 My Loans",
               "🎯 Reservations","⚙️ Admin Panel","📊 Reports","👤 Profile"]
    mem_pages=["🏠 Home","📖 Books","🛒 Book Shop","🔍 Smart Search","🤖 AI Features","📋 My Loans",
               "🎯 Reservations","👤 Profile"]
    gst_pages=["🏠 Home","📖 Books","🛒 Book Shop","🔍 Smart Search","🔐 Login"]
    pages=adm_pages if admin() else (mem_pages if logged() else gst_pages)

    for p in pages:
        if st.session_state.page==p:
            st.markdown(f'<div style="background:linear-gradient(135deg,rgba(79,70,229,.22),rgba(124,58,237,.12));border:1px solid rgba(99,102,241,.32);border-radius:10px;padding:8px 14px;color:#c4b5fd;font-size:0.82rem;font-weight:600;margin:2px 0">{p}</div>',unsafe_allow_html=True)
        else:
            if st.button(p,key=f"n_{p}",use_container_width=True): nav(p)

    st.markdown('<div class="divider" style="margin:8px 0"></div>',unsafe_allow_html=True)
    for n in reversed(st.session_state.notifs[-2:]):
        emoji={"success":"✅","info":"ℹ️","warning":"⚠️","error":"❌"}.get(n["k"],"ℹ️")
        st.markdown(f'<div class="notif">{emoji} {n["m"][:38]}... <span style="color:#1e293b">{n["t"]}</span></div>',unsafe_allow_html=True)
    if logged():
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("🚪 Sign Out",use_container_width=True):
            st.session_state.user=None; st.session_state.page="🏠 Home"; st.rerun()
    st.markdown('<div style="text-align:center;color:#1e293b;font-size:0.66rem;margin-top:10px">LibraryAI Pro v3.0 · © 2025</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════
if st.session_state.page=="🏠 Home":
    lang=U()["lang"] if logged() else "en"
    greet=LANG_LABELS.get(lang,"Welcome")
    name=U()["name"].split()[0] if logged() else "Guest"
    st.markdown(f'<div style="text-align:center;padding:2rem 0 1.5rem"><div class="hero">📚 LibraryAI Pro</div><div style="color:#374151;font-size:1rem;margin-top:8px">{greet}, {name}! · AI-Powered Library · Book Shop · Smart Analytics</div></div>',unsafe_allow_html=True)

    total=len(st.session_state.books); avail=sum(1 for b in st.session_state.books if b["available"])
    active_l=sum(1 for l in st.session_state.loans if not l.get("returned"))
    overdue=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<date.today())
    award_b=sum(1 for b in st.session_state.books if b.get("award"))

    c=st.columns(5)
    c[0].metric("📚 Books",total,f"+{sum(1 for b in st.session_state.books if b['year']>2015)} recent")
    c[1].metric("✅ Available",avail,f"{avail/total*100:.0f}% of catalog")
    c[2].metric("📋 Active Loans",active_l,f"-{overdue} overdue" if overdue else "All on time ✨")
    c[3].metric("🛒 Books in Shop",len([b for b in st.session_state.books if b.get("price",0)>0]))
    c[4].metric("🏆 Award Books",award_b)

    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    col1,col2,col3=st.columns([5,5,4])

    with col1:
        st.markdown('<div class="page-h" style="font-size:1.05rem">📈 Monthly Activity</div>',unsafe_allow_html=True)
        mdf=pd.DataFrame(st.session_state.monthly[-6:])
        fig,ax=plt.subplots(figsize=(6,3.2),facecolor="none"); plt_config(ax,fig)
        x=np.arange(len(mdf))
        ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
        ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
        ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=28)
        ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
        plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with col2:
        st.markdown('<div class="page-h" style="font-size:1.05rem">📊 Genre Distribution</div>',unsafe_allow_html=True)
        gc=pd.Series([b["genre"] for b in st.session_state.books]).value_counts().head(9)
        fig,ax=plt.subplots(figsize=(5,3.2),facecolor="none"); plt_config(ax,fig)
        pal=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706","#dc2626","#84cc16","#0f766e"]
        ax.pie(gc.values,labels=gc.index,autopct="%1.0f%%",startangle=90,colors=pal[:len(gc)],
               wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
        for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(7.5)
        plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with col3:
        st.markdown('<div class="page-h" style="font-size:1.05rem">🔥 Most Borrowed</div>',unsafe_allow_html=True)
        for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])[:5]:
            av="✅" if b["available"] else "❌"
            aw=f'<span class="award-tag">🏆</span> ' if b.get("award") else ""
            st.markdown(
                f'<div class="card" style="padding:10px 14px;margin:4px 0">'
                f'<div style="width:100%;height:2px;background:{b["color"]};border-radius:1px;margin-bottom:6px"></div>'
                f'<div class="bk-title" style="font-size:0.78rem">{b["title"][:30]}</div>'
                f'<div class="bk-author">{b["author"][:22]} {aw}</div>'
                f'<div style="font-size:0.73rem;color:#374151;margin-top:3px">{av} {b["borrows"]}× · ★{b["rating"]}</div>'
                f'</div>',unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    st.markdown('<div class="page-h" style="font-size:1.15rem;text-align:center">🤖 Complete AI Feature Suite</div>',unsafe_allow_html=True)
    feats=[
        ("🧠","Smart Recommendations","Genre, Author, History, Similar"),
        ("🔍","NLP Search Engine","Natural language understanding"),
        ("💬","AI Chatbot Librarian","24/7 intelligent assistant"),
        ("⏰","Overdue Prediction","ML late-return risk scoring"),
        ("📈","Demand Forecasting","Predict book popularity trends"),
        ("🎯","Learning Paths","10 curated reading journeys"),
        ("💭","Sentiment Analysis","Review mood detection NLP"),
        ("📖","Book Summaries","AI-generated full summaries"),
        ("🎙️","Voice Search","Speak to search catalog"),
        ("📊","Reading Analytics","Personal reading pattern AI"),
        ("💰","Fine Predictor","Smart fine risk assessment"),
        ("🛒","AI Book Shop","Buy books with AI recommendations"),
        ("🏅","Gamification","XP · Levels · Badges · Achievements"),
    ]
    fc=st.columns(6)
    for i,(icon,title,desc) in enumerate(feats):
        with fc[i%6]:
            st.markdown(
                f'<div class="card" style="padding:14px;text-align:center;margin:4px 0">'
                f'<div style="font-size:1.7rem;margin-bottom:6px">{icon}</div>'
                f'<div style="font-weight:700;font-size:0.78rem;color:#a5b4fc;margin-bottom:3px">{title}</div>'
                f'<div style="font-size:0.7rem;color:#1e293b;line-height:1.4">{desc}</div>'
                f'</div>',unsafe_allow_html=True)

    if not logged():
        st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        _,cc,_=st.columns([1,2,1])
        with cc:
            st.markdown('<div style="text-align:center;padding:20px"><div style="font-size:2.2rem">🔐</div><div style="color:#374151;margin:8px 0">Sign in to access all 40+ features</div></div>',unsafe_allow_html=True)
            if st.button("🔐 Login / Register",use_container_width=True): nav("🔐 Login")
            st.markdown('<div style="text-align:center;color:#1e293b;font-size:0.77rem;margin-top:8px">Demo: admin@library.com / admin123</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: BOOKS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📖 Books":
    st.markdown('<div class="page-h">📖 Book Catalog</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="sub">{len(st.session_state.books)} world-famous books · Borrow · Reserve · Read E-Book · Get AI Summary</div>',unsafe_allow_html=True)
    fc1,fc2,fc3,fc4=st.columns([4,2,2,2])
    with fc1: srch=st.text_input("",placeholder="🔍 Search title, author, award, ISBN...",label_visibility="collapsed")
    with fc2: gf=st.selectbox("",["All Genres"]+GENRES,label_visibility="collapsed")
    with fc3: af=st.selectbox("",["All","✅ Available","❌ Borrowed","🏆 Award Winners","📱 E-Book","🎧 Audiobook"],label_visibility="collapsed")
    with fc4: sf=st.selectbox("",["⭐ Rating","🔥 Most Borrowed","🆕 Newest","🔤 A-Z"],label_visibility="collapsed")
    books=list(st.session_state.books)
    if srch:
        q=srch.lower()
        books=[b for b in books if q in b["title"].lower() or q in b["author"].lower() or q in b.get("isbn","") or q in b.get("award","").lower() or q in b["genre"].lower()]
    if gf!="All Genres": books=[b for b in books if b["genre"]==gf]
    if af=="✅ Available":       books=[b for b in books if b["available"]]
    elif af=="❌ Borrowed":      books=[b for b in books if not b["available"]]
    elif af=="🏆 Award Winners": books=[b for b in books if b.get("award")]
    elif af=="📱 E-Book":        books=[b for b in books if b.get("ebook")]
    elif af=="🎧 Audiobook":     books=[b for b in books if b.get("audio")]
    sk={"⭐ Rating":lambda b:-b["rating"],"🔥 Most Borrowed":lambda b:-b["borrows"],"🆕 Newest":lambda b:-b["year"],"🔤 A-Z":lambda b:b["title"]}
    books.sort(key=sk.get(sf,lambda b:-b["rating"]))
    st.caption(f"Showing **{len(books)}** books")
    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)

    for i in range(0,len(books),4):
        row=books[i:i+4]; cols=st.columns(4)
        for j,b in enumerate(row):
            with cols[j]:
                ei="📱" if b.get("ebook") else ""
                ai="🎧" if b.get("audio") else ""
                gmap={"Fiction":"bp","Fantasy":"bg","Science":"bb","History":"bc","Biography":"bpk","Technology":"bb","Self-Help":"ba","Philosophy":"bc","Mystery":"bp","Children":"bg","Romance":"bpk","Health":"bg","Art":"ba","Sports":"bc"}
                gc2=gmap.get(b["genre"],"bb")
                av='<span class="badge bg">✅ Available</span>' if b["available"] else '<span class="badge br">❌ Borrowed</span>'
                aw=f'<div style="margin:4px 0"><span class="award-tag">🏆 {b["award"][:24]}</span></div>' if b.get("award") else ""
                st.markdown(
                    f'<div class="book-card">'
                    f'<div class="book-spine" style="background:{b["color"]}"></div>'
                    f'<div class="book-inner">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span class="badge {gc2}">{b["genre"]}</span>'
                    f'<span style="font-size:0.82rem">{ei}{ai}</span></div>'
                    f'<div class="bk-title">{b["title"]}</div>'
                    f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                    f'{aw}'
                    f'<div class="bk-desc">{b["desc"][:88]}...</div>'
                    f'<div style="margin-top:8px;display:flex;justify-content:space-between">'
                    f'<span style="color:#fbbf24;font-size:0.8rem">★ {b["rating"]}</span>'
                    f'<span style="color:#1e293b;font-size:0.71rem">{b["borrows"]}× borrowed</span></div>'
                    f'<div style="margin-top:7px">{av}</div>'
                    f'</div></div>',unsafe_allow_html=True)

                bc1,bc2,bc3=st.columns(3)
                if logged() and b["available"]:
                    with bc1:
                        if st.button("📥",key=f"bw{b['id']}",help="Borrow",use_container_width=True):
                            u=U(); r=late_risk(u,b,14)
                            lid=st.session_state.lid+1; st.session_state.lid=lid
                            st.session_state.loans.append({"id":lid,"uid":u["id"],"bid":b["id"],
                                "title":b["title"],"author":b["author"],"genre":b["genre"],
                                "bdate":date.today().isoformat(),
                                "ddate":(date.today()+timedelta(days=14)).isoformat(),
                                "rdate":None,"returned":False,"fine":0.0,"late":False,"risk":r,"days":14})
                            for b2 in st.session_state.books:
                                if b2["id"]==b["id"]: b2["available"]=False; b2["borrows"]+=1
                            for u2 in st.session_state.users:
                                if u2["id"]==u["id"]:
                                    u2["borrowed"]+=1
                                    if b["id"] not in u2["history"]: u2["history"].append(b["id"])
                            tb=U()["borrowed"]+1
                            bdg=None
                            if tb==1: bdg="🌱 Seedling Reader"
                            elif tb==5: bdg="📖 Bookworm"
                            elif tb==10: bdg="🦉 Wise Owl"
                            elif tb==20: bdg="🏆 Library Champion"
                            xp_up(u["id"],15,bdg)
                            rk="🔴 HIGH" if r>.5 else "🟡 MED" if r>.3 else "🟢 LOW"
                            notify(f"Borrowed '{b['title'][:22]}'","success")
                            st.toast(f"✅ Borrowed! Risk: {rk}"); st.rerun()
                elif logged() and not b["available"]:
                    already=any(rv["bid"]==b["id"] and rv["uid"]==U()["id"] for rv in st.session_state.reservations)
                    with bc1:
                        if not already:
                            if st.button("🎯",key=f"rv{b['id']}",help="Reserve",use_container_width=True):
                                st.session_state.reservations.append({"id":len(st.session_state.reservations)+1,
                                    "uid":U()["id"],"bid":b["id"],"title":b["title"],"date":date.today().isoformat()})
                                notify(f"Reserved '{b['title'][:22]}'","info"); st.toast("🎯 Reserved!"); st.rerun()
                        else:
                            st.markdown('<div style="font-size:0.72rem;color:#fbbf24;padding-top:6px">🎯 Reserved</div>',unsafe_allow_html=True)
                with bc2:
                    if b.get("ebook"):
                        if st.button("📱",key=f"eb{b['id']}",help="E-Book",use_container_width=True):
                            st.session_state.ebid=b["id"]; st.session_state.ebpg=0; st.rerun()
                with bc3:
                    if st.button("🔎",key=f"si{b['id']}",help="AI Summary",use_container_width=True):
                        s=BOOK_SUMMARIES.get(b["title"],b["desc"])
                        rvs=b.get("reviews",[])
                        rv_str="\n".join(f'⭐{"★"*r["rating"]} *{r["user"]}:* {r["text"][:60]}...' for r in rvs[:2]) if rvs else ""
                        st.info(f"📖 **{b['title']}**\n\n{s}\n\n{'🏆 '+b['award'] if b.get('award') else ''}\n\n{rv_str}")

    if "ebid" in st.session_state:
        b=bk(st.session_state.ebid)
        if b:
            st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
            st.markdown(f'<div class="page-h" style="font-size:1.1rem">📱 E-Book Reader — <em>{b["title"]}</em></div>',unsafe_allow_html=True)
            summary=BOOK_SUMMARIES.get(b["title"],b["desc"])
            pages=[
                f"**📖 About This Book**\n\n{summary}\n\n*{b['author']} · {b['year']} · {b.get('pages','?')} pages · ★{b['rating']}*\n\n{'🏆 Award: '+b['award'] if b.get('award') else ''}",
                f"**Chapter 1 — The Beginning**\n\nThe story opens with a world both familiar and strange. Every detail carefully placed, every sentence deliberate. The author wastes no words, drawing you in from the very first line.\n\nThemes of identity, purpose, and human connection emerge with remarkable clarity as the narrative unfolds.",
                f"**Chapter 2 — Rising Action**\n\nConflict deepens. The protagonist faces choices that will define the entire arc of the story. Loyalties are tested, and the world begins revealing its hidden complexities.\n\nThe prose is especially remarkable here — each paragraph a careful balance of tension and release.",
                f"**Chapter 3 — The Heart of It**\n\nThis is the core of the author's vision. Questions that seemed peripheral suddenly become central. The reader is drawn into reflection about their own life and values.\n\n*'{b['title']}' stands as one of the defining works of its genre, precisely because it refuses easy answers.*",
            ]
            pg=st.session_state.get("ebpg",0)
            st.markdown(f'<div class="ebook">{pages[pg%len(pages)]}</div>',unsafe_allow_html=True)
            pc1,pc2,pc3,pc4=st.columns([1,1,3,1])
            with pc1:
                if st.button("◀ Prev") and pg>0: st.session_state.ebpg=pg-1; st.rerun()
            with pc2:
                if st.button("Next ▶") and pg<len(pages)-1: st.session_state.ebpg=pg+1; st.rerun()
            with pc3:
                st.markdown(f'<div style="text-align:center;color:#374151;font-size:0.8rem;padding-top:8px">Page {pg+1} of {len(pages)}</div>',unsafe_allow_html=True)
            with pc4:
                if st.button("✖ Close"): del st.session_state["ebid"]; st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: SMART SEARCH
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🔍 Smart Search":
    st.markdown('<div class="page-h">🔍 Smart Search Engine</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">NLP-powered · Voice search · Trend analysis · Demand forecasting</div>',unsafe_allow_html=True)
    tabs=st.tabs(["⌨️ Text Search","🎙️ Voice Search","📈 Trends & Demand"])

    with tabs[0]:
        sc1,sc2=st.columns([5,1])
        with sc1: query=st.text_input("",placeholder="e.g. award-winning dystopian fiction · machine learning beginners · biographies of entrepreneurs",label_visibility="collapsed")
        with sc2: st.markdown("<br>",unsafe_allow_html=True); sbtn=st.button("🔍 Search",use_container_width=True)
        st.markdown('<div style="color:#1e293b;font-size:0.78rem;margin:6px 0">💡 Try: <code>Pulitzer Prize novels</code> · <code>classic science fiction</code> · <code>popular self help</code> · <code>award winning mystery</code> · <code>recent technology</code></div>',unsafe_allow_html=True)
        if query:
            with st.spinner("🔍 Analysing with NLP..."):
                results=nlp_search(query)
            st.markdown(f'<div style="color:#374151;margin:10px 0">Found <b style="color:#a5b4fc">{len(results)}</b> results for <em>"{query}"</em></div>',unsafe_allow_html=True)
            if results:
                for i in range(0,min(len(results),9),3):
                    row=results[i:i+3]; cols=st.columns(3)
                    for j,b in enumerate(row):
                        with cols[j]:
                            av="✅ Available" if b["available"] else "❌ Borrowed"
                            st.markdown(
                                f'<div class="book-card">'
                                f'<div class="book-spine" style="background:{b["color"]}"></div>'
                                f'<div class="book-inner">'
                                f'<span class="badge bp">{b["genre"]}</span> {"<span class=award-tag>🏆</span>" if b.get("award") else ""}'
                                f'<div class="bk-title">{b["title"]}</div>'
                                f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                                f'<div class="bk-desc">{b["desc"][:90]}...</div>'
                                f'<div style="margin-top:8px;font-size:0.8rem"><span style="color:#fbbf24">★ {b["rating"]}</span> · <span style="color:#374151">{av}</span></div>'
                                f'</div></div>',unsafe_allow_html=True)
            else:
                st.warning("No results found. Try different keywords.")

    with tabs[1]:
        st.markdown("### 🎙️ Voice Search Simulator")
        st.markdown('<div class="card" style="text-align:center;padding:28px"><div style="font-size:3.5rem;margin-bottom:10px">🎙️</div><div style="color:#a5b4fc;font-weight:700;margin-bottom:6px">Speak to Search</div><div style="color:#374151;font-size:0.85rem">Click a sample query to simulate voice recognition</div></div>',unsafe_allow_html=True)
        vsamples=["Award-winning science fiction","Books about artificial intelligence","Classic mystery novels","Best self help books","Biographies of entrepreneurs","Children fantasy adventures"]
        vc=st.columns(3)
        for i,vs in enumerate(vsamples):
            with vc[i%3]:
                if st.button(f"🎙 {vs}",key=f"vc{i}",use_container_width=True):
                    st.session_state.vq=vs
        if st.session_state.vq:
            st.success(f"🎙️ Recognised: **\"{st.session_state.vq}\"**")
            vres=nlp_search(st.session_state.vq)
            if vres:
                vc2=st.columns(min(len(vres),4))
                for i,b in enumerate(vres[:4]):
                    with vc2[i]:
                        st.markdown(f'<div class="card" style="padding:12px;text-align:center"><div style="width:100%;height:3px;background:{b["color"]};border-radius:2px;margin-bottom:7px"></div><div class="bk-title">{b["title"][:26]}</div><div class="bk-author">{b["genre"]} · ★{b["rating"]}</div></div>',unsafe_allow_html=True)
            if st.button("🗑 Clear"): st.session_state.vq=""; st.rerun()

    with tabs[2]:
        st.markdown("### 📈 Trend Analysis & Demand Forecasting")
        tc1,tc2=st.columns(2)
        with tc1:
            st.markdown("**Book Demand Scores**")
            dd=sorted([(b["title"][:28],round(b["borrows"]/200*5+random.uniform(-.3,.3),1)) for b in st.session_state.books],key=lambda x:-x[1])[:12]
            fig,ax=plt.subplots(figsize=(5,5),facecolor="none"); plt_config(ax,fig)
            n,v=zip(*dd)
            cx=["#ef4444" if x>=4 else "#f59e0b" if x>=3 else "#4f46e5" for x in v]
            ax.barh(n,v,color=cx,height=.65); ax.set_xlabel("Demand Score (0–5)",color="#374151"); ax.axvline(3,color="#1e2d4a",linestyle="--",alpha=.6)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with tc2:
            st.markdown("**Genre Borrow Trends**")
            gbc=defaultdict(int)
            for b in st.session_state.books: gbc[b["genre"]]+=b["borrows"]
            gbs=sorted(gbc.items(),key=lambda x:-x[1])
            fig,ax=plt.subplots(figsize=(5,5),facecolor="none"); plt_config(ax,fig)
            pal2=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706","#dc2626","#84cc16","#0f766e","#b45309","#9333ea","#0369a1","#065f46","#92400e"]
            ax.pie([v for _,v in gbs[:10]],labels=[g for g,_ in gbs[:10]],autopct="%1.0f%%",startangle=90,colors=pal2[:10],wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
            for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(8)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

# ══════════════════════════════════════════════════════
#  PAGE: AI FEATURES
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🤖 AI Features":
    st.markdown('<div class="page-h">🤖 AI Features Centre</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">10 intelligent features powered by NLP, ML, and data analytics</div>',unsafe_allow_html=True)
    aitabs=st.tabs(["💬 Chatbot","🧠 Recommendations","⏰ Overdue","📈 Demand","🎯 Learning Path","💭 Sentiment","📊 Analytics","💰 Fine Pred.","📖 Summaries","🏅 Gamification"])

    # ── CHATBOT ──
    with aitabs[0]:
        st.markdown("### 💬 LibBot — AI Librarian Chatbot")
        st.markdown('<div style="color:#374151;font-size:0.84rem;margin-bottom:14px">Available 24/7 · NLP-powered · Knows every book in the catalog</div>',unsafe_allow_html=True)
        if not st.session_state.chat:
            st.markdown('<div class="chat-b">👋 Hello! I\'m <b>LibBot</b>, your AI Librarian. I can find books, give recommendations, summarise any title, check availability, explain our policies, and much more! Just ask!</div>',unsafe_allow_html=True)
        for msg in st.session_state.chat:
            if msg["r"]=="u":
                st.markdown(f'<div style="display:flex;justify-content:flex-end"><div class="chat-u">👤 {msg["t"]}</div></div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-b">🤖 <b>LibBot:</b><br>{msg["t"]}</div>',unsafe_allow_html=True)
        cc1,cc2=st.columns([5,1])
        with cc1: uin=st.text_input("",placeholder="Ask me anything about books, the shop, reading policies...",key="cin",label_visibility="collapsed")
        with cc2: st.markdown("<br>",unsafe_allow_html=True); send_btn=st.button("Send ➤",use_container_width=True)
        st.markdown("**Quick prompts:**")
        qcols=st.columns(4)
        qps=["recommend books for me","summary of Atomic Habits","find award-winning fiction","buy books info"]
        for i,qp in enumerate(qps):
            with qcols[i]:
                if st.button(qp,key=f"qp{i}",use_container_width=True):
                    st.session_state.chat.append({"r":"u","t":qp}); st.session_state.chat.append({"r":"b","t":bot(qp)}); st.rerun()
        if send_btn and uin:
            st.session_state.chat.append({"r":"u","t":uin}); st.session_state.chat.append({"r":"b","t":bot(uin)}); st.rerun()
        if st.button("🗑 Clear Chat"): st.session_state.chat=[]; st.rerun()

    # ── RECOMMENDATIONS ──
    with aitabs[1]:
        st.markdown("### 🧠 Smart Book Recommendations")
        if not logged(): st.info("Login to get personalized recommendations."); st.stop()
        u=U()
        st.markdown(f'<div class="card" style="padding:12px 16px;margin-bottom:14px">Recommendations for <b>{u["name"]}</b> · Favourite: <b>{u["fav"]}</b> · Read <b>{u["borrowed"]}</b> books · Level <b>{u["level"]}</b></div>',unsafe_allow_html=True)
        filter_by=st.radio("",["🧠 Personalised","📚 By Genre","✍️ By Author","🆕 New Arrivals","🏆 Award Winners","📖 Reading History Based"],horizontal=True,label_visibility="collapsed")
        if filter_by=="📚 By Genre":
            sg=st.selectbox("Genre",GENRES); recs=[b for b in st.session_state.books if b["genre"]==sg and b["id"] not in u.get("history",[])][:6]
        elif filter_by=="✍️ By Author":
            auths=sorted(set(b["author"] for b in st.session_state.books)); sa=st.selectbox("Author",auths); recs=[b for b in st.session_state.books if b["author"]==sa][:6]
        elif filter_by=="🆕 New Arrivals":
            recs=sorted(st.session_state.books,key=lambda b:-b["year"])[:6]
        elif filter_by=="🏆 Award Winners":
            recs=[b for b in sorted(st.session_state.books,key=lambda b:-b["rating"]) if b.get("award")][:6]
        elif filter_by=="📖 Reading History Based":
            hist=[bk(i) for i in u.get("history",[]) if bk(i)]
            if hist:
                hist_genres=set(b["genre"] for b in hist)
                recs=[b for b in st.session_state.books if b["genre"] in hist_genres and b["id"] not in u.get("history",[])][:6]
            else: recs=smart_recs(u,6)
        else:
            recs=smart_recs(u,6)
        if recs:
            rc=st.columns(3)
            for i,b in enumerate(recs[:6]):
                with rc[i%3]:
                    match=round(random.uniform(72,98),1)
                    st.markdown(
                        f'<div class="book-card">'
                        f'<div class="book-spine" style="background:{b["color"]}"></div>'
                        f'<div class="book-inner">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center">'
                        f'<span class="badge bp">{b["genre"]}</span>'
                        f'<span class="ai-pill">🧠 {match}% match</span></div>'
                        f'<div class="bk-title">{b["title"]}</div>'
                        f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                        f'<div style="color:#fbbf24;font-size:0.8rem;margin-top:5px">★ {b["rating"]}</div>'
                        f'{"<div class=award-tag>🏆 "+b.get("award","")[:28]+"</div>" if b.get("award") else ""}'
                        f'</div></div>',unsafe_allow_html=True)

    # ── OVERDUE PREDICTION ──
    with aitabs[2]:
        st.markdown("### ⏰ AI Overdue Return Prediction")
        st.markdown("ML model predicts late return probability before a book is issued.")
        oc1,oc2=st.columns(2)
        with oc1:
            if st.button("🔮 Analyse All Active Loans",use_container_width=True):
                active=[l for l in st.session_state.loans if not l.get("returned")]
                if not active: st.info("No active loans."); st.stop()
                rows=[]
                for l in active:
                    u2=usr(l["uid"]); b=bk(l["bid"])
                    if u2 and b:
                        r=l.get("risk",late_risk(u2,b,14))
                        due=date.fromisoformat(l["ddate"]); days=(due-date.today()).days
                        rows.append({"User":u2["name"],"Book":b["title"][:24],"Due":l["ddate"],
                                     "Days Left":days,"Late Risk":f"{r:.0%}",
                                     "Risk Level":"🔴 HIGH" if r>.5 else "🟡 MEDIUM" if r>.3 else "🟢 LOW"})
                if rows:
                    df=pd.DataFrame(rows); st.dataframe(df,use_container_width=True,hide_index=True)
                    hi=sum(1 for r in rows if "HIGH" in r["Risk Level"])
                    if hi: st.warning(f"⚠️ {hi} loan(s) are HIGH risk for late return!")
                    else: st.success("✅ All loans are low-medium risk.")
        with oc2:
            st.markdown("**Predict a Specific Borrow**")
            pa=st.slider("User Age",12,70,24); pd2=st.selectbox("Loan Period",["7 days","14 days","21 days"])
            ph=st.slider("Past Late Returns",0,10,1); pb=st.slider("Total Borrows",0,50,8)
            if st.button("🔮 Predict",use_container_width=True):
                s=0.08
                if pa<22: s+=.20
                if "7" in pd2: s+=.19
                s+=ph*.07
                if pb<3: s+=.09
                s=min(s+random.uniform(-.03,.04),.95)
                lv="🔴 HIGH RISK" if s>.5 else "🟡 MEDIUM RISK" if s>.3 else "🟢 LOW RISK"
                fe=round(int(s*10)*.5,2)
                st.markdown(f"**Prediction: {lv}**"); st.progress(s)
                c1,c2=st.columns(2)
                c1.metric("Late Probability",f"{s:.0%}"); c2.metric("Expected Fine",f"£{fe:.2f}")

    # ── DEMAND FORECASTING ──
    with aitabs[3]:
        st.markdown("### 📈 Book Demand Forecasting")
        dc1,dc2=st.columns(2)
        with dc1:
            st.markdown("**Demand by Genre**")
            gd=defaultdict(list)
            for b in st.session_state.books: gd[b["genre"]].append(b["demand"])
            gd_avg={g:round(np.mean(v),2) for g,v in gd.items()}
            gds=sorted(gd_avg.items(),key=lambda x:-x[1])
            fig,ax=plt.subplots(figsize=(5,4),facecolor="none"); plt_config(ax,fig)
            ax.bar([g for g,_ in gds],[v for _,v in gds],color="#4f46e5",alpha=.9)
            ax.set_ylabel("Avg Demand",color="#374151"); ax.tick_params(labelsize=8)
            plt.xticks(rotation=35,fontsize=7); plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with dc2:
            st.markdown("**Top 15 High-Demand Books**")
            ddf=pd.DataFrame([{"Title":b["title"][:28],"Genre":b["genre"],"Demand":round(b["demand"],1),"Rating":b["rating"],"Borrows":b["borrows"]} for b in sorted(st.session_state.books,key=lambda b:-b["demand"])[:15]])
            st.dataframe(ddf,use_container_width=True,hide_index=True)

    # ── LEARNING PATH ──
    with aitabs[4]:
        st.markdown("### 🎯 Learning Path Recommendation")
        lp2=st.selectbox("Choose your goal / career path",list(LEARNING_PATHS.keys()))
        path=LEARNING_PATHS[lp2]
        st.markdown(f'<div class="card" style="margin-bottom:14px;padding:12px 16px">Reading path for <b>{lp2}</b> — {len(path)} carefully curated books</div>',unsafe_allow_html=True)
        for i,title in enumerate(path):
            b=next((bk2 for bk2 in st.session_state.books if title.lower() in bk2["title"].lower()),None)
            if b:
                av="✅" if b["available"] else "❌"
                aw=f"🏆 {b['award'][:22]}" if b.get("award") else ""
                st.markdown(
                    f'<div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 16px;margin:5px 0">'
                    f'<div style="width:32px;height:32px;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:.9rem;flex-shrink:0">{i+1}</div>'
                    f'<div style="flex:1"><div class="bk-title">{b["title"]}</div>'
                    f'<div class="bk-author">{b["author"]} · ★{b["rating"]} · {av} {aw}</div></div>'
                    f'<span class="badge bp">{b["genre"]}</span>'
                    f'</div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card" style="padding:11px 16px"><b>{i+1}. {title}</b> <span style="color:#1e293b">(not in catalog)</span></div>',unsafe_allow_html=True)

    # ── SENTIMENT ──
    with aitabs[5]:
        st.markdown("### 💭 Sentiment Analysis")
        sc1,sc2=st.columns(2)
        with sc1:
            st.markdown("**Analyse a Review**")
            rtxt=st.text_area("Enter text",placeholder="e.g. This book was absolutely brilliant and life-changing!",height=100)
            if st.button("🔍 Analyse",use_container_width=True) and rtxt:
                pos=["great","amazing","love","excellent","wonderful","best","fantastic","awesome","brilliant","perfect","life-changing","inspiring","profound","masterpiece","beautiful","powerful"]
                neg=["bad","terrible","boring","awful","worst","hate","disappointing","poor","waste","dull","confusing","overrated","slow","unreadable"]
                pl=sum(1 for w in pos if w in rtxt.lower())
                nl=sum(1 for w in neg if w in rtxt.lower())
                if pl>nl: label,conf,cls="😊 Positive",round(pl/(pl+nl+.01),2),"bg"
                elif nl>pl: label,conf,cls="😞 Negative",round(nl/(pl+nl+.01),2),"br"
                else: label,conf,cls="😐 Neutral",.5,"ba"
                st.markdown(f'<span class="badge {cls}" style="font-size:1rem;padding:6px 16px">{label}</span>',unsafe_allow_html=True)
                st.progress(conf); st.caption(f"Confidence: {conf:.0%}")
        with sc2:
            st.markdown("**Real Book Reviews Sentiment**")
            all_reviews=[]
            for b2 in st.session_state.books:
                for rv in b2.get("reviews",[]): all_reviews.append((b2["title"],rv["text"],rv["rating"]))
            if all_reviews:
                rows=[]
                for title,text,rating in all_reviews[:10]:
                    pos_w=["amazing","love","excellent","best","life-changing","brilliant","profound","masterpiece","powerful","inspiring"]
                    ps=sum(1 for w in pos_w if w in text.lower())
                    sent="😊 Positive" if ps>0 else "😐 Neutral"
                    rows.append({"Book":title[:20],"Rating":f"★{rating}","Sentiment":sent,"Review":text[:50]+"..."})
                st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    # ── READING ANALYTICS ──
    with aitabs[6]:
        st.markdown("### 📊 Reading Pattern Analytics")
        if not logged(): st.info("Login to see your analytics."); st.stop()
        u=U(); my_loans=[l for l in st.session_state.loans if l["uid"]==u["id"]]
        if not my_loans:
            st.info("Borrow some books to unlock your reading analytics!")
        else:
            ra1,ra2=st.columns(2)
            genres_read=[l.get("genre","") for l in my_loans if l.get("genre")]
            with ra1:
                if genres_read:
                    st.markdown("**Your Genre Distribution**")
                    gc3=pd.Series(genres_read).value_counts()
                    fig,ax=plt.subplots(figsize=(4,4),facecolor="none"); plt_config(ax,fig)
                    pal3=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706"]
                    ax.pie(gc3.values,labels=gc3.index,autopct="%1.0f%%",startangle=90,colors=pal3[:len(gc3)],wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
                    for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(9)
                    plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
            with ra2:
                st.markdown("**Your Reading Stats**")
                ret_time=sum(1 for l in my_loans if l.get("returned") and not l.get("late"))
                fines=sum(l.get("fine",0) for l in my_loans)
                read_books=[bk(l["bid"]) for l in my_loans if bk(l["bid"])]
                avg_r=np.mean([b["rating"] for b in read_books]) if read_books else 0
                st.metric("📚 Books Borrowed",u["borrowed"])
                st.metric("✅ Returned on Time",ret_time)
                st.metric("⭐ Avg Book Rating",f"{avg_r:.1f}")
                st.metric("💰 Total Fines Paid",f"£{fines:.2f}")

    # ── FINE PREDICTOR ──
    with aitabs[7]:
        st.markdown("### 💰 Smart Fine Predictor")
        if not logged(): st.info("Login to use fine predictor."); st.stop()
        u=U()
        fp1,fp2=st.columns(2)
        with fp1:
            fp_bk=st.selectbox("Select Book",st.session_state.books,format_func=lambda b:b["title"])
            fp_d=st.selectbox("Loan Period",[7,14,21])
            if st.button("💰 Predict Fine",use_container_width=True):
                r=late_risk(u,fp_bk,fp_d); fine=round(int(r*10)*.5,2)
                lv="🔴 HIGH" if r>.5 else "🟡 MEDIUM" if r>.3 else "🟢 LOW"
                st.markdown(f"**Late Risk: {lv}**"); st.progress(r)
                st.metric("Late Probability",f"{r:.0%}")
                st.metric("Predicted Fine (if late)",f"£{fine:.2f}")
                if fine>0: st.warning(f"⚠️ Return on time to avoid a £{fine:.2f} fine!")
                else: st.success("✅ Low risk — you are likely to return on time!")
        with fp2:
            if admin():
                st.markdown("**Highest Fine Risk Users**")
                rows=[]
                for u2 in st.session_state.users:
                    active=[l for l in st.session_state.loans if l["uid"]==u2["id"] and not l.get("returned")]
                    if active:
                        ar=np.mean([l.get("risk",.2) for l in active])
                        rows.append({"User":u2["name"],"Active":len(active),"Avg Risk":f"{ar:.0%}","Level":"🔴" if ar>.5 else "🟡" if ar>.3 else "🟢"})
                if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    # ── SUMMARIES ──
    with aitabs[8]:
        st.markdown("### 📖 AI Book Summary Generator")
        sum_bk=st.selectbox("Choose a book",st.session_state.books,format_func=lambda b:f"★{b['rating']} {b['title']}")
        if st.button("📖 Generate AI Summary",use_container_width=True):
            with st.spinner("✨ Generating AI summary..."):
                time.sleep(.8)
            s=BOOK_SUMMARIES.get(sum_bk["title"],sum_bk["desc"])
            rvs=sum_bk.get("reviews",[])
            st.markdown(
                f'<div class="card" style="padding:24px">'
                f'<div style="width:100%;height:4px;background:{sum_bk["color"]};border-radius:3px;margin-bottom:16px"></div>'
                f'<div class="page-h" style="font-size:1.2rem">{sum_bk["title"]}</div>'
                f'<div style="color:#374151;margin:4px 0 14px">by {sum_bk["author"]} · {sum_bk["genre"]} · {sum_bk["year"]} · {sum_bk.get("pages","?")} pages</div>'
                f'{"<div class=award-tag style=margin-bottom:12px>🏆 "+sum_bk.get("award","")+"</div>" if sum_bk.get("award") else ""}'
                f'<div style="color:#cbd5e1;line-height:1.85;font-size:0.92rem">{s}</div>'
                f'<div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap">'
                f'<span class="ai-pill">★ {sum_bk["rating"]}</span>'
                f'<span class="ai-pill">📱 E-Book: {"Yes" if sum_bk.get("ebook") else "No"}</span>'
                f'<span class="ai-pill">🎧 Audio: {"Yes" if sum_bk.get("audio") else "No"}</span>'
                f'<span class="ai-pill">📦 ISBN: {sum_bk.get("isbn","N/A")}</span>'
                f'</div></div>',unsafe_allow_html=True)
            if rvs:
                st.markdown("**📝 Reader Reviews:**")
                for rv in rvs:
                    st.markdown(f'<div class="card" style="padding:10px 14px;margin:4px 0"><b style="color:#fbbf24">{"★"*rv["rating"]}</b> <b style="color:#e2e8f0">{rv["user"]}</b> <span style="color:#374151;font-size:0.73rem">{rv.get("date","")}</span><br><span style="color:#94a3b8;font-size:0.82rem">{rv["text"]}</span></div>',unsafe_allow_html=True)

    # ── GAMIFICATION ──
    with aitabs[9]:
        st.markdown("### 🏅 Gamification & Achievements")
        if not logged(): st.info("Login to see your achievements."); st.stop()
        u=U()
        g1,g2,g3,g4=st.columns(4)
        g1.metric("🎮 Level",u["level"]); g2.metric("⚡ XP",u["xp"])
        g3.metric("🏅 Badges",len(u.get("badges",[]))); g4.metric("📚 Books Read",u["borrowed"])
        lp3=u["xp"]%100
        st.markdown(f"**Level {u['level']} → Level {u['level']+1}** · {lp3}/100 XP")
        st.progress(lp3/100)
        if u.get("badges"):
            st.markdown("**🏅 Your Badges:**")
            bc2=st.columns(min(len(u["badges"]),5))
            for i,bdg in enumerate(u["badges"]):
                with bc2[i%5]:
                    st.markdown(f'<div class="card" style="text-align:center;padding:13px"><div style="font-size:1.7rem">{bdg[:2]}</div><div style="color:#a5b4fc;font-size:0.74rem;margin-top:3px">{bdg[2:].strip()}</div></div>',unsafe_allow_html=True)
        st.markdown("**🎯 Achievement Progress:**")
        tb=u["borrowed"]
        achiev=[("🌱","Seedling Reader","Borrow 1 book",1),("📖","Bookworm","Borrow 5 books",5),
                ("🦉","Wise Owl","Borrow 10 books",10),("🏆","Library Champion","Borrow 20 books",20),("👑","Master Reader","Borrow 50 books",50)]
        acols=st.columns(5)
        for i,(icon,name,desc,need) in enumerate(achiev):
            with acols[i]:
                pct=min(tb/need,1.); done=tb>=need
                st.markdown(
                    f'<div class="card" style="text-align:center;padding:12px;{"border-color:rgba(79,70,229,.5)" if done else ""}">'
                    f'<div style="font-size:1.6rem">{icon}</div>'
                    f'<div style="color:{"#4ade80" if done else "#a5b4fc"};font-size:0.77rem;font-weight:700;margin:4px 0">{name}</div>'
                    f'<div style="color:#1e293b;font-size:0.69rem;margin-bottom:7px">{desc}</div>'
                    f'<div class="xp-bg"><div class="xp-fill" style="width:{pct*100:.0f}%;{"background:#22c55e" if done else ""}"></div></div>'
                    f'<div style="color:#374151;font-size:0.69rem;margin-top:3px">{min(tb,need)}/{need}</div>'
                    f'</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: MY LOANS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📋 My Loans":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">📋 My Loans & Borrowing History</div>',unsafe_allow_html=True)
    u=U(); my_loans=[l for l in st.session_state.loans if l["uid"]==u["id"]]
    active=[l for l in my_loans if not l.get("returned")]
    returned=[l for l in my_loans if l.get("returned")]
    today=date.today()
    overdue=[l for l in active if date.fromisoformat(l["ddate"])<today]
    total_fines=sum(l.get("fine",0) for l in my_loans)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("📚 Active",len(active)); c2.metric("✅ Returned",len(returned))
    c3.metric("🚨 Overdue",len(overdue)); c4.metric("💰 Fines",f"£{total_fines:.2f}")
    if not my_loans:
        st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:2rem">📚</div><div style="color:#374151;margin-top:8px">No loans yet — go to 📖 Books to borrow your first!</div></div>',unsafe_allow_html=True)
    else:
        lt1,lt2=st.tabs([f"📌 Active ({len(active)})",f"📜 History ({len(returned)})"])
        with lt1:
            if not active: st.success("🎉 No active loans — all returned!")
            for l in active:
                due=date.fromisoformat(l["ddate"]); dl=(due-today).days
                ov=dl<0; r=l.get("risk",.2)
                lc="#ef4444" if ov else ("#f59e0b" if r>.3 else "#4f46e5")
                b=bk(l["bid"]); qrb64=qr(f"LOAN-{l['id']}-{l['title']}")
                lc1,lc2=st.columns([5,1])
                with lc1:
                    st.markdown(
                        f'<div class="loan-card" style="--lc:{lc}">'
                        f'<div style="display:flex;justify-content:space-between;align-items:start">'
                        f'<div><div style="font-weight:700;color:#e2e8f0;font-size:0.95rem">{l["title"]}</div>'
                        f'<div style="color:#374151;font-size:0.78rem">{l["author"]} · {l.get("genre","")}</div>'
                        f'<div style="margin-top:9px;font-size:0.81rem;color:#64748b">📅 Borrowed: <b>{l["bdate"]}</b> &nbsp; ⏰ Due: <b style="color:{"#f87171" if ov else "#4ade80"}">{l["ddate"]}</b></div>'
                        f'<div style="margin-top:5px;font-size:0.81rem">{"🚨 OVERDUE <b>"+str(abs(dl))+" days</b> — Fine: £"+str(round(abs(dl)*.5,2)) if ov else "⏳ <b>"+str(dl)+" days</b> remaining"}'
                        f' &nbsp;·&nbsp; {"🔴" if r>.5 else "🟡" if r>.3 else "🟢"} Late risk: {r:.0%}</div></div>'
                        f'<span class="badge {"br" if ov else "bb"}">{"OVERDUE" if ov else "ACTIVE"}</span>'
                        f'</div></div>',unsafe_allow_html=True)
                    if st.button(f"↩ Return '{l['title'][:26]}'",key=f"ret{l['id']}",use_container_width=True):
                        dl2=max(0,(today-due).days); fine=round(dl2*.5,2)
                        l["rdate"]=today.isoformat(); l["returned"]=True; l["fine"]=fine; l["late"]=dl2>0
                        for b2 in st.session_state.books:
                            if b2["id"]==l["bid"]: b2["available"]=True
                        if not l["late"]: xp_up(u["id"],8,"⚡ Speed Reader")
                        notify(f"Returned '{l['title'][:22]}'","success")
                        st.toast(f"✅ {'Fine: £'+str(fine) if fine>0 else 'On time — no fine!'}"); st.rerun()
                with lc2:
                    st.markdown(f'<div class="qr-wrap"><img src="data:image/svg+xml;base64,{qrb64}" width="72"/><div style="color:#333;font-size:0.6rem;margin-top:3px">Scan Ticket</div></div>',unsafe_allow_html=True)
        with lt2:
            if not returned: st.info("No returned books yet.")
            else:
                df=pd.DataFrame([{"Book":l["title"][:28],"Genre":l.get("genre",""),
                                   "Borrowed":l["bdate"],"Due":l["ddate"],
                                   "Returned":l.get("rdate","—"),"Fine £":l.get("fine",0),
                                   "Status":"⚠️ Late" if l.get("late") else "✅ On Time"}
                                  for l in returned])
                st.dataframe(df,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
#  PAGE: RESERVATIONS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🎯 Reservations":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">🎯 Book Reservations</div>',unsafe_allow_html=True)
    u=U(); my_res=[r for r in st.session_state.reservations if r["uid"]==u["id"]]
    if not my_res:
        st.markdown('<div class="card" style="text-align:center;padding:28px"><div style="font-size:2rem">🎯</div><div style="color:#374151;margin-top:8px">No reservations yet.<br>When a book is unavailable, click <b>🎯 Reserve</b> on the book card!</div></div>',unsafe_allow_html=True)
    else:
        for rv in my_res:
            b=bk(rv["bid"]); ready=b and b["available"]
            rc1,rc2=st.columns([4,1])
            with rc1:
                st.markdown(
                    f'<div class="card" style="padding:14px;border-left:3px solid {"#4ade80" if ready else "#f59e0b"}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<div><div style="font-weight:700;color:#e2e8f0">{rv["title"]}</div>'
                    f'<div style="color:#374151;font-size:0.78rem">Reserved on {rv["date"]}</div></div>'
                    f'<span class="badge {"bg" if ready else "ba"}">{"📗 Ready!" if ready else "⏳ Waiting"}</span>'
                    f'</div></div>',unsafe_allow_html=True)
                ca,cb=st.columns(2)
                with ca:
                    if st.button("❌ Cancel",key=f"cr{rv['id']}",use_container_width=True):
                        st.session_state.reservations=[x for x in st.session_state.reservations if x["id"]!=rv["id"]]
                        st.toast("Cancelled."); st.rerun()
                with cb:
                    if ready and st.button("📥 Borrow Now!",key=f"brv{rv['id']}",use_container_width=True):
                        r=late_risk(u,b,14); lid=st.session_state.lid+1; st.session_state.lid=lid
                        st.session_state.loans.append({"id":lid,"uid":u["id"],"bid":b["id"],
                            "title":b["title"],"author":b["author"],"genre":b["genre"],
                            "bdate":date.today().isoformat(),"ddate":(date.today()+timedelta(days=14)).isoformat(),
                            "rdate":None,"returned":False,"fine":0.,"late":False,"risk":r,"days":14})
                        for b2 in st.session_state.books:
                            if b2["id"]==b["id"]: b2["available"]=False; b2["borrows"]+=1
                        st.session_state.reservations=[x for x in st.session_state.reservations if x["id"]!=rv["id"]]
                        notify(f"Borrowed reserved '{b['title'][:22]}'","success"); st.toast("✅ Borrowed!"); st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: BOOK SHOP
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🛒 Book Shop":
    st.markdown('<div class="page-h">🛒 AI Book Shop</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">AI-powered recommendations · Browse & buy · Instant QR receipt · Order history</div>',unsafe_allow_html=True)
    st1,st2,st3,st4=st.tabs(["🛍️ Browse & Buy","🧠 AI Picks For Me","📦 My Orders","💳 Cart"])

    with st1:
        sc1,sc2,sc3=st.columns([4,2,2])
        with sc1: srch2=st.text_input("",placeholder="🔍 Search books to buy...",label_visibility="collapsed",key="shop_srch")
        with sc2: sg2=st.selectbox("",["All Genres"]+GENRES,label_visibility="collapsed",key="shop_g")
        with sc3: ss2=st.selectbox("",["⭐ Top Rated","💰 Price: Low→High","💰 Price: High→Low","🔥 Most Popular","🏆 Award Winners"],label_visibility="collapsed",key="shop_s")
        shop_books=list(st.session_state.books)
        if srch2:
            q=srch2.lower()
            shop_books=[b for b in shop_books if q in b["title"].lower() or q in b["author"].lower() or q in b["genre"].lower()]
        if sg2!="All Genres": shop_books=[b for b in shop_books if b["genre"]==sg2]
        if ss2=="💰 Price: Low→High": shop_books.sort(key=lambda b:b.get("price",0))
        elif ss2=="💰 Price: High→Low": shop_books.sort(key=lambda b:-b.get("price",0))
        elif ss2=="🔥 Most Popular": shop_books.sort(key=lambda b:-b["borrows"])
        elif ss2=="🏆 Award Winners": shop_books=[b for b in shop_books if b.get("award")]; shop_books.sort(key=lambda b:-b["rating"])
        else: shop_books.sort(key=lambda b:-b["rating"])
        st.caption(f"Showing **{len(shop_books)}** books")
        st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        cart_ids=[c["bid"] for c in st.session_state.cart]
        for i in range(0,len(shop_books),4):
            row=shop_books[i:i+4]; cols=st.columns(4)
            for j,b in enumerate(row):
                with cols[j]:
                    in_cart=b["id"] in cart_ids
                    gmap={"Fiction":"bp","Fantasy":"bg","Science":"bb","History":"bc","Biography":"bpk","Technology":"bb","Self-Help":"ba","Philosophy":"bc","Mystery":"bp","Children":"bg","Romance":"bpk","Health":"bg","Art":"ba","Sports":"bc"}
                    gc2=gmap.get(b["genre"],"bb")
                    aw=f'<div style="margin:3px 0"><span class="award-tag">🏆 {b["award"][:22]}</span></div>' if b.get("award") else ""
                    ei="📱" if b.get("ebook") else ""; ai2="🎧" if b.get("audio") else ""
                    st.markdown(
                        f'<div class="book-card">'
                        f'<div class="book-spine" style="background:{b["color"]}"></div>'
                        f'<div class="book-inner">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center">'
                        f'<span class="badge {gc2}">{b["genre"]}</span>'
                        f'<span style="font-size:0.82rem">{ei}{ai2}</span></div>'
                        f'<div class="bk-title">{b["title"]}</div>'
                        f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                        f'{aw}'
                        f'<div class="bk-desc">{b["desc"][:80]}...</div>'
                        f'<div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center">'
                        f'<span style="color:#4ade80;font-size:1rem;font-weight:700">£{b.get("price",0):.2f}</span>'
                        f'<span style="color:#fbbf24;font-size:0.8rem">★ {b["rating"]}</span></div>'
                        f'</div></div>',unsafe_allow_html=True)
                    sc_a,sc_b=st.columns(2)
                    with sc_a:
                        if logged():
                            if in_cart:
                                st.markdown('<div style="color:#4ade80;font-size:0.77rem;padding:6px 0;text-align:center">✅ In Cart</div>',unsafe_allow_html=True)
                            else:
                                if st.button("🛒 Add",key=f"ac{b['id']}",use_container_width=True):
                                    st.session_state.cart.append({"bid":b["id"],"title":b["title"],"price":b.get("price",0),"author":b["author"],"color":b["color"]})
                                    notify(f"Added '{b['title'][:20]}' to cart","success")
                                    st.toast("🛒 Added to cart!"); st.rerun()
                        else:
                            if st.button("🔐 Login",key=f"sl{b['id']}",use_container_width=True): nav("🔐 Login")
                    with sc_b:
                        if st.button("📖",key=f"si2{b['id']}",help="AI Summary",use_container_width=True):
                            s=BOOK_SUMMARIES.get(b["title"],b["desc"])
                            st.info(f"📖 **{b['title']}**\n\n{s}\n\n{'🏆 '+b['award'] if b.get('award') else ''}")

    with st2:
        st.markdown("### 🧠 AI-Powered Book Recommendations")
        if not logged():
            st.info("Login to get personalised AI book recommendations."); 
            if st.button("🔐 Login to Get Recommendations",use_container_width=True): nav("🔐 Login")
        else:
            u=U()
            st.markdown(f'<div class="card" style="padding:12px 16px;margin-bottom:14px">AI picks for <b>{u["name"]}</b> · Favourite genre: <b>{u["fav"]}</b> · Level <b>{u["level"]}</b> reader</div>',unsafe_allow_html=True)
            recs=smart_recs(u,6)
            if recs:
                rc=st.columns(3)
                cart_ids2=[c["bid"] for c in st.session_state.cart]
                for i,b in enumerate(recs[:6]):
                    with rc[i%3]:
                        match=round(random.uniform(75,98),1)
                        in_cart2=b["id"] in cart_ids2
                        st.markdown(
                            f'<div class="book-card">'
                            f'<div class="book-spine" style="background:{b["color"]}"></div>'
                            f'<div class="book-inner">'
                            f'<span class="badge bp">{b["genre"]}</span>'
                            f'<span class="ai-pill" style="float:right;margin-top:-2px">🧠 {match}% match</span>'
                            f'<div class="bk-title" style="margin-top:6px">{b["title"]}</div>'
                            f'<div class="bk-author">{b["author"]}</div>'
                            f'<div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center">'
                            f'<span style="color:#4ade80;font-size:1rem;font-weight:700">£{b.get("price",0):.2f}</span>'
                            f'<span style="color:#fbbf24;font-size:0.8rem">★ {b["rating"]}</span></div>'
                            f'</div></div>',unsafe_allow_html=True)
                        if in_cart2:
                            st.markdown('<div style="color:#4ade80;font-size:0.77rem;padding:6px 0;text-align:center">✅ In Cart</div>',unsafe_allow_html=True)
                        else:
                            if st.button(f"🛒 Add to Cart",key=f"arc{b['id']}",use_container_width=True):
                                st.session_state.cart.append({"bid":b["id"],"title":b["title"],"price":b.get("price",0),"author":b["author"],"color":b["color"]})
                                notify(f"Added '{b['title'][:20]}' to cart","success")
                                st.toast("🛒 Added!"); st.rerun()

    with st3:
        st.markdown("### 📦 My Order History")
        if not logged():
            st.info("Login to see your orders.")
        else:
            my_orders=[o for o in st.session_state.orders if o["uid"]==U()["id"]]
            if not my_orders:
                st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:2rem">📦</div><div style="color:#374151;margin-top:8px">No orders yet — browse the shop and buy your first book!</div></div>',unsafe_allow_html=True)
            else:
                total_spent=sum(o["total"] for o in my_orders)
                oc1,oc2=st.columns(2)
                oc1.metric("📦 Total Orders",len(my_orders))
                oc2.metric("💰 Total Spent",f"£{total_spent:.2f}")
                st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
                for o in reversed(my_orders):
                    qrb64=qr(f"ORDER-{o['ref']}")
                    lc1,lc2=st.columns([5,1])
                    with lc1:
                        items_str=", ".join(i["title"][:22] for i in o["items"][:3])
                        if len(o["items"])>3: items_str+=f" +{len(o['items'])-3} more"
                        st.markdown(
                            f'<div class="loan-card">'
                            f'<div style="display:flex;justify-content:space-between;align-items:start">'
                            f'<div><div style="font-weight:700;color:#60a5fa;font-size:1rem">🧾 {o["ref"]}</div>'
                            f'<div style="color:#374151;font-size:0.78rem;margin-top:3px">{o["date"]}</div>'
                            f'<div style="color:#e2e8f0;font-size:0.83rem;margin-top:7px">{items_str}</div>'
                            f'<div style="color:#4ade80;font-weight:700;margin-top:6px">£{o["total"]:.2f} · {len(o["items"])} book(s)</div></div>'
                            f'<span class="badge bg">✅ Completed</span>'
                            f'</div></div>',unsafe_allow_html=True)
                    with lc2:
                        st.markdown(f'<div class="qr-wrap"><img src="data:image/svg+xml;base64,{qrb64}" width="72"/><div style="color:#333;font-size:0.6rem;margin-top:3px">Receipt</div></div>',unsafe_allow_html=True)

    with st4:
        st.markdown("### 💳 Shopping Cart")
        if not logged():
            st.info("Login to use the cart.")
        else:
            cart=st.session_state.cart
            if not cart:
                st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:2rem">🛒</div><div style="color:#374151;margin-top:8px">Your cart is empty — browse the shop to add books!</div></div>',unsafe_allow_html=True)
            else:
                total=sum(c["price"] for c in cart)
                ct1,ct2=st.columns([2,1])
                with ct1:
                    for idx,item in enumerate(cart):
                        ic1,ic2=st.columns([5,1])
                        with ic1:
                            st.markdown(
                                f'<div class="card" style="padding:12px 16px;border-left:3px solid {item["color"]}">'
                                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                                f'<div><div style="font-weight:700;color:#e2e8f0">{item["title"]}</div>'
                                f'<div style="color:#374151;font-size:0.78rem">{item["author"]}</div></div>'
                                f'<div style="color:#4ade80;font-weight:700;font-size:1rem">£{item["price"]:.2f}</div>'
                                f'</div></div>',unsafe_allow_html=True)
                        with ic2:
                            if st.button("🗑",key=f"rm{idx}",use_container_width=True):
                                st.session_state.cart.pop(idx); st.rerun()
                with ct2:
                    st.markdown(
                        f'<div class="card" style="padding:20px;text-align:center">'
                        f'<div style="font-size:0.8rem;color:#374151;text-transform:uppercase;letter-spacing:.05em">Order Summary</div>'
                        f'<div style="font-size:2rem;font-weight:800;color:#4ade80;margin:10px 0">£{total:.2f}</div>'
                        f'<div style="color:#374151;font-size:0.78rem">{len(cart)} book(s)</div>'
                        f'</div>',unsafe_allow_html=True)
                    if st.button("💳 Complete Purchase",use_container_width=True,key="buy_btn"):
                        import string as _str
                        ref="ORD"+"".join(random.choices(_str.digits,k=6))
                        order={"uid":U()["id"],"ref":ref,"date":date.today().isoformat(),"items":list(cart),"total":total}
                        st.session_state.orders.append(order)
                        xp_up(U()["id"],len(cart)*10)
                        st.session_state.cart=[]
                        notify(f"Order {ref} placed — £{total:.2f}","success")
                        qrb64=qr(f"ORDER-{ref}")
                        st.success(f"✅ **Order Placed!** Ref: `{ref}` · £{total:.2f}")
                        st.markdown(f'<div class="qr-wrap" style="margin-top:8px"><img src="data:image/svg+xml;base64,{qrb64}" width="100"/><div style="color:#333;font-size:0.63rem;margin-top:3px">Your Receipt QR</div></div>',unsafe_allow_html=True)
                        st.balloons(); st.rerun()
                    if st.button("🗑 Clear Cart",use_container_width=True,key="clear_cart"):
                        st.session_state.cart=[]; st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════-wrap"><img src="data:image/svg+xml;base64,{qrb64}" width="72"/><div style="color:#333;font-size:0.6rem;margin-top:3px">Receipt</div></div>',unsafe_allow_html=True)

    with st4:
        st.markdown("### 💳 Shopping Cart")
        if not logged():
            st.info("Login to use the cart.")
        else:
            cart=st.session_state.cart
            if not cart:
                st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:2rem">🛒</div><div style="color:#374151;margin-top:8px">Your cart is empty — browse the shop to add books!</div></div>',unsafe_allow_html=True)
            else:
                total=sum(c["price"] for c in cart)
                ct1,ct2=st.columns([2,1])
                with ct1:
                    for idx,item in enumerate(cart):
                        ic1,ic2=st.columns([5,1])
                        with ic1:
                            st.markdown(
                                f'<div class="card" style="padding:12px 16px;border-left:3px solid {item["color"]}">'
                                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                                f'<div><div style="font-weight:700;color:#e2e8f0">{item["title"]}</div>'
                                f'<div style="color:#374151;font-size:0.78rem">{item["author"]}</div></div>'
                                f'<div style="color:#4ade80;font-weight:700;font-size:1rem">£{item["price"]:.2f}</div>'
                                f'</div></div>',unsafe_allow_html=True)
                        with ic2:
                            if st.button("🗑",key=f"rm{idx}",use_container_width=True):
                                st.session_state.cart.pop(idx); st.rerun()
                with ct2:
                    st.markdown(
                        f'<div class="card" style="padding:20px;text-align:center">'
                        f'<div style="font-size:0.8rem;color:#374151;text-transform:uppercase;letter-spacing:.05em">Order Summary</div>'
                        f'<div style="font-size:2rem;font-weight:800;color:#4ade80;margin:10px 0">£{total:.2f}</div>'
                        f'<div style="color:#374151;font-size:0.78rem">{len(cart)} book(s)</div>'
                        f'</div>',unsafe_allow_html=True)
                    if st.button("💳 Complete Purchase",use_container_width=True,key="buy_btn"):
                        import string as _str
                        ref="ORD"+"".join(random.choices(_str.digits,k=6))
                        order={"uid":U()["id"],"ref":ref,"date":date.today().isoformat(),"items":list(cart),"total":total}
                        st.session_state.orders.append(order)
                        xp_up(U()["id"],len(cart)*10)
                        st.session_state.cart=[]
                        notify(f"Order {ref} placed — £{total:.2f}","success")
                        qrb64=qr(f"ORDER-{ref}")
                        st.success(f"✅ **Order Placed!** Ref: `{ref}` · £{total:.2f}")
                        st.markdown(f'<div class="qr-wrap" style="margin-top:8px"><img src="data:image/svg+xml;base64,{qrb64}" width="100"/><div style="color:#333;font-size:0.63rem;margin-top:3px">Your Receipt QR</div></div>',unsafe_allow_html=True)
                        st.balloons(); st.rerun()
                    if st.button("🗑 Clear Cart",use_container_width=True,key="clear_cart"):
                        st.session_state.cart=[]; st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════
elif st.session_state.page=="⚙️ Admin Panel":
    if not admin(): st.error("❌ Admin access only."); st.stop()
    st.markdown('<div class="page-h">⚙️ Admin Panel</div>',unsafe_allow_html=True)
    at=st.tabs(["📊 Overview","➕ Add Book","✏️ Edit/Delete","👁 View Books","👥 Users","📜 Loan History","🛒 Shop Orders"])

    with at[0]:
        total=len(st.session_state.books); avail=sum(1 for b in st.session_state.books if b["available"])
        loans=len(st.session_state.loans); today=date.today()
        overdue=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<today)
        fines=sum(l.get("fine",0) for l in st.session_state.loans)
        shop_orders=len(st.session_state.orders); shop_rev=sum(o["total"] for o in st.session_state.orders)
        c1,c2,c3,c4,c5,c6,c7=st.columns(7)
        c1.metric("📚 Books",total); c2.metric("✅ Available",avail)
        c3.metric("📋 Loans",loans); c4.metric("🚨 Overdue",overdue)
        c5.metric("💰 Fines £",f"{fines:.2f}"); c6.metric("🛒 Shop Orders",shop_orders); c7.metric("💳 Revenue",f"£{shop_rev:.2f}")
        st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        oc1,oc2=st.columns(2)
        with oc1:
            st.markdown("**Monthly Borrows vs Returns**")
            mdf=pd.DataFrame(st.session_state.monthly[-6:])
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            x=np.arange(len(mdf))
            ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
            ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
            ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=25)
            ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with oc2:
            st.markdown("**Top Genres by Borrows**")
            gbc2=defaultdict(int)
            for b in st.session_state.books: gbc2[b["genre"]]+=b["borrows"]
            gbs2=sorted(gbc2.items(),key=lambda x:-x[1])[:8]
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            ax.barh([g for g,_ in gbs2],[v for _,v in gbs2],color="#7c3aed",alpha=.9)
            ax.tick_params(labelsize=8); ax.set_xlabel("Borrows",color="#374151")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with at[1]:
        st.markdown("### ➕ Add New Book")
        with st.form("add_bk"):
            ac1,ac2=st.columns(2)
            with ac1:
                a_t=st.text_input("Title *"); a_a=st.text_input("Author *")
                a_g=st.selectbox("Genre",GENRES); a_y=st.number_input("Year",1000,2025,2020)
                a_isbn=st.text_input("ISBN","978-")
            with ac2:
                a_r=st.slider("Rating",1.0,5.0,4.0,.1); a_c=st.number_input("Copies",1,20,2)
                a_col=st.color_picker("Cover Colour","#4f46e5")
                a_eb=st.checkbox("Has E-Book",True); a_au=st.checkbox("Has Audiobook")
                a_aw=st.text_input("Award (optional)","")
            a_d=st.text_area("Description *")
            if st.form_submit_button("➕ Add Book",use_container_width=True):
                if a_t and a_a and a_d:
                    nid=max(b["id"] for b in st.session_state.books)+1
                    st.session_state.books.append({"id":nid,"title":a_t,"author":a_a,"genre":a_g,"year":int(a_y),
                        "desc":a_d,"available":True,"copies":int(a_c),"rating":a_r,"borrows":0,"color":a_col,
                        "ebook":a_eb,"audio":a_au,"isbn":a_isbn,"award":a_aw,"pages":200,
                        "tags":[a_g.lower()],"reviews":[],"demand":0.})
                    notify(f"Added '{a_t}'","success"); st.toast(f"✅ '{a_t}' added!"); st.rerun()
                else: st.error("Fill all required fields (*)")

    with at[2]:
        st.markdown("### ✏️ Edit / ❌ Delete Books")
        eb=st.selectbox("Select book",st.session_state.books,format_func=lambda b:f"★{b['rating']} {b['title']}")
        if eb:
            with st.form("edit_bk"):
                ec1,ec2=st.columns(2)
                with ec1:
                    et=st.text_input("Title",eb["title"]); ea=st.text_input("Author",eb["author"])
                    eg=st.selectbox("Genre",GENRES,index=GENRES.index(eb["genre"]) if eb["genre"] in GENRES else 0)
                    ey=st.number_input("Year",1000,2025,eb["year"])
                with ec2:
                    er=st.slider("Rating",1.0,5.0,float(eb["rating"]),.1)
                    ec_=st.number_input("Copies",1,20,int(eb["copies"]))
                    eav=st.checkbox("Available",eb["available"])
                    eaw=st.text_input("Award",eb.get("award",""))
                ed=st.text_area("Description",eb["desc"])
                sv,dl=st.columns(2)
                with sv:
                    if st.form_submit_button("💾 Save Changes",use_container_width=True):
                        for b2 in st.session_state.books:
                            if b2["id"]==eb["id"]:
                                b2.update({"title":et,"author":ea,"genre":eg,"year":int(ey),"rating":er,"copies":int(ec_),"available":eav,"desc":ed,"award":eaw})
                        notify(f"Updated '{et}'","success"); st.toast("✅ Updated!"); st.rerun()
                with dl:
                    if st.form_submit_button("🗑 Delete This Book",use_container_width=True):
                        st.session_state.books=[b2 for b2 in st.session_state.books if b2["id"]!=eb["id"]]
                        notify(f"Deleted '{eb['title']}'","warning"); st.toast("🗑 Deleted."); st.rerun()

    with at[3]:
        st.markdown("### 👁 All Books")
        bdf=pd.DataFrame([{"ID":b["id"],"Title":b["title"][:30],"Author":b["author"][:22],"Genre":b["genre"],
                            "Year":b["year"],"Rating":b["rating"],"Borrows":b["borrows"],"Copies":b["copies"],
                            "Available":"✅" if b["available"] else "❌","Award":"🏆" if b.get("award") else "","E-Book":"📱" if b.get("ebook") else ""}
                           for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])])
        st.dataframe(bdf,use_container_width=True,hide_index=True)
        st.caption(f"Total: {len(st.session_state.books)} · Available: {sum(1 for b in st.session_state.books if b['available'])} · Award winners: {sum(1 for b in st.session_state.books if b.get('award'))}")

    with at[4]:
        st.markdown("### 👥 Manage Users")
        udf=pd.DataFrame([{"ID":u["id"],"Avatar":u["avatar"],"Name":u["name"],"Email":u["email"],
                            "Role":u["role"].upper(),"Age":u["age"],"Borrowed":u["borrowed"],
                            "Level":u["level"],"XP":u["xp"],"Badges":len(u.get("badges",[]))}
                           for u in st.session_state.users])
        st.dataframe(udf,use_container_width=True,hide_index=True)
        st.markdown("---"); st.markdown("**Change User Role**")
        eu=st.selectbox("User",st.session_state.users,format_func=lambda u:f"{u['name']} ({u['role']})")
        nr=st.selectbox("New Role",["member","admin"])
        if st.button("💾 Update Role",use_container_width=True):
            for u2 in st.session_state.users:
                if u2["id"]==eu["id"]: u2["role"]=nr
            st.toast(f"✅ {eu['name']} is now {nr}."); st.rerun()

    with at[5]:
        st.markdown("### 📜 Complete Borrowing History")
        if not st.session_state.loans: st.info("No loans yet.")
        else:
            today=date.today()
            ov=[l for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<today]
            if ov:
                st.warning(f"🚨 {len(ov)} overdue loans!")
                for l in ov:
                    u2=usr(l["uid"]); days_ov=(today-date.fromisoformat(l["ddate"])).days
                    st.markdown(f'<div class="card" style="border-color:#ef4444;padding:12px">🚨 <b>{l["title"]}</b> · {u2["name"] if u2 else "?"} · {days_ov} days overdue · Fine: £{days_ov*.5:.2f}</div>',unsafe_allow_html=True)
            ldf=pd.DataFrame([{"Loan#":l["id"],"User":usr(l["uid"])["name"] if usr(l["uid"]) else "?",
                                "Book":l["title"][:26],"Genre":l.get("genre",""),
                                "Borrowed":l["bdate"],"Due":l["ddate"],"Returned":l.get("rdate","—"),
                                "Fine £":l.get("fine",0),"Risk":f'{l.get("risk",0):.0%}',
                                "Status":"✅ Returned" if l.get("returned") else ("🚨 Overdue" if date.fromisoformat(l["ddate"])<today else "📖 Active")}
                               for l in st.session_state.loans])
            st.dataframe(ldf,use_container_width=True,hide_index=True)

    with at[6]:
        st.markdown("### 🛒 Shop Order Administration")
        sa1,sa2,sa3,sa4=st.columns(4)
        sa1.metric("Total Orders",len(st.session_state.orders))
        sa2.metric("Total Revenue",f"£{sum(o['total'] for o in st.session_state.orders):.2f}")
        sa3.metric("Books Sold",sum(len(o['items']) for o in st.session_state.orders))
        sa4.metric("Avg Order",f"£{(sum(o['total'] for o in st.session_state.orders)/max(len(st.session_state.orders),1)):.2f}")
        st.markdown("---")
        if st.session_state.orders:
            odf=pd.DataFrame([{"Ref":o["ref"],"User":usr(o["uid"])["name"] if usr(o["uid"]) else "?",
                                "Date":o["date"],"Books":len(o["items"]),"Total":f"£{o['total']:.2f}",
                                "Items":", ".join(i["title"][:20] for i in o["items"][:2])+("..." if len(o["items"])>2 else "")}
                               for o in reversed(st.session_state.orders)])
            st.dataframe(odf,use_container_width=True,hide_index=True)
        else:
            st.info("No orders yet.")

# ══════════════════════════════════════════════════════
#  PAGE: REPORTS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📊 Reports":
    if not admin(): st.error("Admin only."); st.stop()
    st.markdown('<div class="page-h">📊 Reports & Analytics</div>',unsafe_allow_html=True)
    rt=st.tabs(["📈 Monthly","📚 Book Analytics","👥 User Analytics","🛒 Shop Reports"])

    with rt[0]:
        mdf=pd.DataFrame(st.session_state.monthly)
        r1,r2=st.columns(2)
        with r1:
            fig,ax=plt.subplots(figsize=(6,4),facecolor="none"); plt_config(ax,fig)
            x=np.arange(len(mdf))
            ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
            ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
            ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=30)
            ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
            ax.set_title("Monthly Borrows vs Returns",color="#a5b4fc",fontsize=10)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with r2:
            fig,ax=plt.subplots(figsize=(6,4),facecolor="none"); plt_config(ax,fig)
            ax.plot(range(len(mdf)),mdf["new_users"],color="#f59e0b",linewidth=2.5,marker="o",markersize=5)
            ax.fill_between(range(len(mdf)),mdf["new_users"],alpha=.12,color="#f59e0b")
            ax.set_xticks(range(len(mdf))); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=30)
            ax.set_title("New Users per Month",color="#a5b4fc",fontsize=10)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        col_r1,col_r2,col_r3=st.columns(3)
        col_r1.metric("Total Borrows",sum(mdf["borrows"]))
        col_r2.metric("New Users",sum(mdf["new_users"]))
        col_r3.metric("Fines Collected",f"£{sum(mdf['fines']):.2f}")
        st.dataframe(mdf,use_container_width=True,hide_index=True)

    with rt[1]:
        bdf2=pd.DataFrame([{"Title":b["title"][:30],"Author":b["author"][:20],"Genre":b["genre"],
                             "Year":b["year"],"Rating":b["rating"],"Borrows":b["borrows"],
                             "Available":"✅" if b["available"] else "❌","Award":"🏆 "+b["award"][:18] if b.get("award") else ""}
                            for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])])
        st.dataframe(bdf2,use_container_width=True,hide_index=True)

    with rt[2]:
        udf2=pd.DataFrame([{"Name":u["name"],"Borrowed":u["borrowed"],"Level":u["level"],
                             "XP":u["xp"],"Badges":len(u.get("badges",[])),"Role":u["role"].upper()}
                            for u in sorted(st.session_state.users,key=lambda u:-u["borrowed"])])
        st.dataframe(udf2,use_container_width=True,hide_index=True)

    with rt[3]:
        rc1,rc2,rc3=st.columns(3)
        rc1.metric("Total Orders",len(st.session_state.orders))
        rc2.metric("Total Revenue",f"£{sum(o['total'] for o in st.session_state.orders):.2f}")
        rc3.metric("Books Sold",sum(len(o['items']) for o in st.session_state.orders))
        if st.session_state.orders:
            sdf2=pd.DataFrame([{"Order":o["ref"],"User":usr(o["uid"])["name"] if usr(o["uid"]) else "?",
                                 "Date":o["date"],"Items":len(o["items"]),"Total":f"£{o['total']:.2f}"}
                                for o in reversed(st.session_state.orders)])
            st.dataframe(sdf2,use_container_width=True,hide_index=True)
        else:
            st.info("No orders yet. Once members buy books they appear here.")

# ══════════════════════════════════════════════════════
#  PAGE: PROFILE
# ══════════════════════════════════════════════════════
elif st.session_state.page=="👤 Profile":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">👤 My Profile</div>',unsafe_allow_html=True)
    u=U()
    pc1,pc2=st.columns([1,2])
    with pc1:
        st.markdown(f'<div style="font-size:4.5rem;text-align:center;margin:12px 0">{u["avatar"]}</div>',unsafe_allow_html=True)
        lp4=u["xp"]%100
        st.markdown(
            f'<div class="card" style="text-align:center;padding:16px">'
            f'<div style="font-size:1.15rem;font-weight:700;color:#e2e8f0">{u["name"]}</div>'
            f'<div style="color:#374151;font-size:0.78rem">{u["role"].upper()} · Age {u["age"]}</div>'
            f'<div style="margin:10px 0"><div class="xp-bg"><div class="xp-fill" style="width:{lp4}%"></div></div>'
            f'<div style="color:#1e293b;font-size:0.7rem;margin-top:3px">Level {u["level"]} · {u["xp"]} XP</div></div>'
            f'<div style="font-size:0.76rem;color:#374151">📅 Member since {u.get("joined","2023")}</div>'
            f'</div>',unsafe_allow_html=True)
        nav_av=st.selectbox("Change Avatar",AVATARS,index=AVATARS.index(u["avatar"]) if u["avatar"] in AVATARS else 0)
        if nav_av!=u["avatar"]:
            for u2 in st.session_state.users:
                if u2["id"]==u["id"]: u2["avatar"]=nav_av
            st.session_state.user["avatar"]=nav_av; st.rerun()

        # Language selector
        st.markdown("**🌐 Language**")
        cur_lang=u.get("lang","en")
        for flag,code in LANGS.items():
            active=code==cur_lang
            if st.button(flag,key=f"lang{code}",use_container_width=True):
                for u2 in st.session_state.users:
                    if u2["id"]==u["id"]: u2["lang"]=code
                st.session_state.user["lang"]=code; st.rerun()

    with pc2:
        st.markdown(f"**Email:** {u['email']} · **Favourite Genre:** {u['fav']}")
        st.markdown(f"**Books Borrowed:** {u['borrowed']} · **Fines Paid:** £{u.get('fines',0):.2f}")
        if u.get("bio"): st.markdown(f"*{u['bio']}*")
        if u.get("badges"): st.markdown("**Badges:** "+" ".join(u["badges"]))
        st.markdown("---")
        with st.form("edit_prof"):
            ep1,ep2=st.columns(2)
            with ep1:
                en=st.text_input("Name",u["name"]); ea=st.number_input("Age",10,100,u["age"]); ebio=st.text_area("Bio",u.get("bio",""),height=70)
            with ep2:
                eg=st.selectbox("Fav Genre",GENRES,index=GENRES.index(u["fav"]) if u["fav"] in GENRES else 0)
                ep=st.text_input("New Password (leave blank to keep)",type="password")
            if st.form_submit_button("💾 Save Profile",use_container_width=True):
                for u2 in st.session_state.users:
                    if u2["id"]==u["id"]:
                        u2["name"]=en; u2["age"]=int(ea); u2["fav"]=eg; u2["bio"]=ebio
                        if ep: u2["pass"]=ep
                st.session_state.user["name"]=en; st.session_state.user["fav"]=eg
                st.toast("✅ Profile saved!"); st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: LOGIN
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🔐 Login":
    st.markdown('<div style="text-align:center;margin-bottom:20px"><div class="hero" style="font-size:2rem">📚 LibraryAI Pro</div><div style="color:#374151;margin-top:6px">Sign in to access all 40+ features</div></div>',unsafe_allow_html=True)
    _,lc,_=st.columns([1,2,1])
    with lc:
        lt1,lt2=st.tabs(["🔐 Sign In","📝 Create Account"])
        with lt1:
            with st.form("login_f"):
                le=st.text_input("Email",placeholder="your@email.com")
                lp5=st.text_input("Password",type="password")
                if st.form_submit_button("🔐 Sign In",use_container_width=True):
                    u=by_em(le)
                    if u and u["pass"]==lp5:
                        st.session_state.user=u; nav("🏠 Home")
                    else: st.error("❌ Invalid email or password.")
            st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
            st.markdown("**🎮 Demo Accounts:**")
            st.code("Admin:   admin@library.com  /  admin123\nMember:  ahmed@email.com    /  pass123\nMember:  sara@email.com     /  pass123\nMember:  james@email.com    /  pass123\nMember:  mia@email.com      /  pass123")
        with lt2:
            with st.form("reg_f"):
                rn=st.text_input("Full Name *"); re=st.text_input("Email *")
                rp=st.text_input("Password *",type="password")
                rc1_,rc2_=st.columns(2)
                with rc1_: ra=st.number_input("Age",10,100,20)
                with rc2_: rg=st.selectbox("Favourite Genre",GENRES)
                rav=st.selectbox("Avatar",AVATARS,format_func=lambda x:x)
                if st.form_submit_button("✅ Create Account",use_container_width=True):
                    if by_em(re): st.error("Email already registered.")
                    elif rn and re and rp:
                        nid=max(u["id"] for u in st.session_state.users)+1
                        nu={"id":nid,"name":rn,"email":re,"pass":rp,"role":"member",
                            "age":int(ra),"fav":rg,"borrowed":0,"xp":0,"level":1,"badges":[],
                            "history":[],"avatar":rav,"joined":date.today().isoformat(),"fines":0.0,"lang":"en","bio":""}
                        st.session_state.users.append(nu); st.session_state.user=nu
                        notify(f"Welcome, {rn}!","success"); nav("🏠 Home")
                    else: st.error("Please fill all required fields.")
