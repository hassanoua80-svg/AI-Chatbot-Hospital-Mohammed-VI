import json, re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="HUIM6 Learning Assistant", page_icon="🏥")
DATA = Path(__file__).parent / "Hospital-Mohammed-VI-knowledge.json"

@st.cache_data
def load_db():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

db = load_db()
facts = db.get("knowledge", [])
faqs = db.get("faq", [])
fact_map = {x.get("id"): x for x in facts}

st.title("🏥 Hôpital Universitaire International Mohammed VI")
st.subheader("Learning Assistant")
st.caption("Unofficial educational prototype • Static research snapshot: 18 October 2026")
st.info("Student prototype, not affiliated with the hospital. Administrative information only—not medical advice. Confirm important details through official channels.")

with st.sidebar:
    st.header("About")
    st.write("Python + Streamlit chatbot using a local JSON knowledge base.")
    st.write(f"Knowledge records: {len(facts)}")
    st.write(f"FAQ prompts: {len(faqs)}")
    st.markdown("Official website: https://hm6.ma/")
    st.caption("Do not enter passwords, identity documents, private medical records, or sensitive personal data.")

def norm(s):
    s = s.lower().replace("’", "'")
    s = re.sub(r"[^a-z0-9À-ÿ\s+]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def answer(q):
    nq = norm(q)
    medical = ["diagnose", "diagnosis", "prescribe", "dosage", "dose", "treatment",
               "symptom", "symptoms", "blood test", "test result", "scan",
               "medical advice", "interpret my", "what disease"]
    if any(x in nq for x in medical):
        return ("I can’t diagnose symptoms, interpret medical tests, recommend treatment, or suggest medication doses. "
                "Please contact a qualified healthcare professional. If this may be an emergency, seek emergency care immediately.")
    if any(x in nq for x in ["discount", "promotion", "promo code", "special offer"]):
        return "I don’t have a sourced record confirming a current promotion, so I can’t invent one. Please check https://hm6.ma/."

    stop = {"the","a","an","is","are","do","does","can","i","you","my","me","to","of","and","in","on","for","how","what","where","when","will","this","that","it","please","tell","about","at","be","with","from"}
    qt = {w for w in nq.split() if w not in stop and len(w) > 2}
    ranked = []
    for faq in faqs:
        ft = {w for w in norm(faq.get("question","")).split() if w not in stop and len(w)>2}
        score = len(qt & ft) / max(1, len(qt | ft))
        ranked.append((score, faq))
    ranked.sort(key=lambda x:x[0], reverse=True)
    if ranked and ranked[0][0] >= 0.18:
        faq = ranked[0][1]
        selected = [fact_map[x] for x in faq.get("fact_ids",[]) if x in fact_map]
        if selected:
            out=[]
            for item in selected:
                fact=item.get("fact","")
                if item.get("status")=="dated_snapshot":
                    fact += f" (listed in the research snapshot dated {item.get('research_date','18 October 2026')}; please confirm current details.)"
                elif item.get("status")=="indexed_reference":
                    fact += " (from an indexed official reference that was not freshly inspected.)"
                out.append("• "+fact)
            return "\n".join(out)+"\n\nOfficial website: https://hm6.ma/"
        if faq.get("answer_guidance"):
            return faq["answer_guidance"]+"\n\nPlease contact the hospital through https://hm6.ma/"

    ranked_facts=[]
    for item in facts:
        ft={w for w in norm(item.get("fact","")).split() if len(w)>2}
        score=len(qt & ft)
        if score: ranked_facts.append((score,item))
    ranked_facts.sort(key=lambda x:x[0], reverse=True)
    if ranked_facts:
        best=ranked_facts[0][0]
        out=[]
        for score,item in ranked_facts:
            if score != best: break
            fact=item.get("fact","")
            if item.get("status")=="dated_snapshot":
                fact += f" (research snapshot: {item.get('research_date','18 October 2026')}; confirm current details.)"
            out.append("• "+fact)
            if len(out)==3: break
        return "\n".join(out)+"\n\nOfficial website: https://hm6.ma/"
    return ("I couldn’t find a reliable answer in this project’s knowledge file. That does not mean the service is unavailable. "
            "Please contact the hospital or consult https://hm6.ma/.")

if "messages" not in st.session_state:
    st.session_state.messages=[{"role":"assistant","content":"Hello! I’m an unofficial student prototype. Ask about contact details, appointments, admission, listed specialties, or hospital services."}]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
prompt=st.chat_input("Ask an administrative question...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    response=answer(prompt)
    st.session_state.messages.append({"role":"assistant","content":response})
    with st.chat_message("assistant"): st.markdown(response)
st.divider()
st.caption("No live booking, real-time availability, billing decisions, or clinical decisions.")
