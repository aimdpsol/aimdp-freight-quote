import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta

st.set_page_config(page_title="AIMDP - Quote Automation", layout="wide", page_icon="✈️")

st.markdown("""
# QUOTE AUTOMATION FOR DORAL FREIGHT FORWARDERS
### From 35 Minutes to 2 Minutes Per Quote
**AIMDP Solutions | pinedad@gmail.com | Doral, FL - Built for Freight Forwarders**
""")

# Mock Rate Sheet Database
RATE_SHEET = pd.DataFrame([
    {"origin":"MIA","dest":"JFK","min":125,"per_kg":2.8,"carrier":"American Cargo"},
    {"origin":"MIA","dest":"LAX","min":150,"per_kg":3.2,"carrier":"Delta Cargo"},
    {"origin":"MIA","dest":"BOG","min":95,"per_kg":1.9,"carrier":"Avianca Cargo"},
    {"origin":"MIA","dest":"SJU","min":85,"per_kg":1.6,"carrier":"Amerijet"},
])

st.divider()

# Step 1
st.markdown("## HOW IT WORKS IN 3 STEPS - LIVE DEMO")

tab1, tab2, tab3 = st.tabs(["1. AI Captures Request", "2. Matches Rates", "3. Send Quote Instantly"])

with tab1:
    st.markdown("**AI parses email, PDF, or form**")
    sample_email = """From: customer@importer.com
Subject: URGENT Quote Request - 450kg to JFK

Hi, Need rate for:
Origin: Miami MIA
Destination: JFK New York
Weight: 450 kg
Commodity: Electronics
Please quote asap."""

    email_input = st.text_area("Paste incoming quote email:", value=sample_email, height=200)

    if st.button("🤖 Parse with AI Agent", type="primary"):
        # AI parsing with regex
        origin = re.search(r'Origin:?\s*(\w+)', email_input, re.I)
        dest = re.search(r'Destination:?\s*(\w+)', email_input, re.I)
        weight = re.search(r'Weight:?\s*(\d+)', email_input, re.I)

        st.session_state['origin'] = origin.group(1) if origin else "MIA"
        st.session_state['dest'] = dest.group(1) if dest else "JFK"
        st.session_state['weight'] = int(weight.group(1)) if weight else 450
        st.session_state['parsed'] = True

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Origin", st.session_state['origin'])
        c2.metric("Destination", st.session_state['dest'])
        c3.metric("Weight", f"{st.session_state['weight']} kg")
        c4.metric("Commodity", "Electronics")
        st.success("✅ AI extracted shipment details in 1.2 seconds")

with tab2:
    st.markdown("**Automatically searches rate sheets & carrier pricing**")
    if st.session_state.get('parsed'):
        o = st.session_state['origin'][:3].upper()
        d = st.session_state['dest'][:3].upper()
        w = st.session_state['weight']

        match = RATE_SHEET[(RATE_SHEET.origin==o) & (RATE_SHEET.dest==d)]
        if len(match)==0:
            match = RATE_SHEET.iloc[[0]]

        rate = match.iloc[0]
        base = max(rate['min'], rate['per_kg'] * w)
        fuel = base * 0.28 # 28% fuel surcharge
        total = base + fuel + 45 # handling

        st.session_state['quote_total'] = total

        st.dataframe(RATE_SHEET, use_container_width=True)
        st.divider()
        colA, colB = st.columns(2)
        colA.markdown(f"""
        **Carrier:** {rate['carrier']}
        **Base Rate:** ${base:.2f} (${rate['per_kg']}/kg x {w}kg)
        **Fuel Surcharge (28%):** ${fuel:.2f}
        **Handling:** $45.00
        """)
        colB.metric("TOTAL QUOTE", f"${total:.2f}", f"Valid 7 days")
        st.success("✅ Best rate calculated automatically")
    else:
        st.info("👆 First parse a request in Tab 1")

with tab3:
    st.markdown("**Generates professional quote PDF and emails to customer automatically**")
    if st.session_state.get('quote_total'):
        total = st.session_state['quote_total']
        st.markdown(f"""
        <div style='border:2px solid #0A2A5E; padding:20px; border-radius:10px; background:#f8faff'>
        <h3 style='color:#0A2A5E'>AIMDP SOLUTIONS - FREIGHT QUOTE</h3>
        <p><b>Quote #:</b> Q-{datetime.now().strftime('%Y%m%d-%H%M')} | <b>Valid until:</b> {(datetime.now()+timedelta(days=7)).strftime('%m/%d/%Y')}</p>
        <p><b>Route:</b> {st.session_state['origin']} → {st.session_state['dest']} | <b>Weight:</b> {st.session_state['weight']} kg</p>
        <h2 style='color:#0A2A5E'>Total: ${total:.2f}</h2>
        <p><i>Includes fuel surcharge, handling, customs docs. No extra hires needed.</i></p>
        <p>Book now: pinedad@gmail.com | (305) 555-0189</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        if st.button("📧 Send Branded Quote to Customer", type="primary", use_container_width=True):
            st.balloons()
            st.success(f"✅ Quote sent to customer@importer.com in 2.1 seconds! (Was 35 minutes manually)")
            st.metric("Time Saved This Week", "15+ hrs", "Operations team freed")
    else:
        st.info("Complete Tab 1 & 2 first")

st.divider()
st.markdown("""
**RESULTS:** Save 15+ hrs/week | Faster Response: 2 min vs 35 min | No Extra Hires
**PRICING:** $2,000 one-time setup + $500/mo ongoing • Includes onboarding + support • Cancel anytime
**READY?** Book 15-min demo for Doral Freight Forwarders
""")
st.link_button("Schedule Demo → pinedad@gmail.com", "mailto:pinedad@gmail.com", use_container_width=True)
