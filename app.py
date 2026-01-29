import os
import subprocess
import sys

# --- MAGICAL FIX FOR CLOUD DEPLOYMENT ---
# This forces the server to download the specific browser Ram needs
try:
    print("🔧 Installing Playwright Browsers...")
    subprocess.run(["playwright", "install", "chromium"], check=True)
    print("✅ Playwright Browsers Installed.")
except Exception as e:
    print(f"⚠️ Could not install browsers: {e}")

import asyncio
# CRITICAL FIX: Prevent Mac/Linux Crash
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

import streamlit as st
# Now we import the backend (after installing the browser)
from backend import get_knowledge_base, launch_analyst, sentiment_analyst, metrics_analyst, expand_competitor_report

st.set_page_config(page_title="Prajwal Labs | True North", layout="wide", page_icon="🚀")

if 'competitor_response' not in st.session_state: st.session_state.competitor_response = None
if 'sentiment_response' not in st.session_state: st.session_state.sentiment_response = None
if 'metrics_response' not in st.session_state: st.session_state.metrics_response = None

st.title("🚀 Prajwal Labs: True North Agent")
st.markdown("*AI-powered insights for GTM & Product Strategy*")
st.divider()

st.subheader("🏢 Company Analysis")
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        company_name = st.text_input("Target Company", placeholder="e.g., Salesforce", label_visibility="collapsed")
    with col2:
        if company_name: st.success(f"✓ Ready: **{company_name}**")

if company_name:
    with st.sidebar.container():
        st.markdown("### 📊 Analysis Status")
        st.markdown(f"**Target:** {company_name}")
        status_items = [
            ("🔍", "Competitor Analysis", st.session_state.competitor_response),
            ("💬", "Sentiment Analysis", st.session_state.sentiment_response),
            ("📈", "Metrics Analysis", st.session_state.metrics_response)
        ]
        for icon, name, status in status_items:
            if status: st.success(f"{icon} {name} ✓")
            else: st.info(f"{icon} {name} ⏳")
else:
    with st.sidebar.container():
        st.markdown("### 🤖 System Status")
        st.success("✅ Ram is Online")

tabs = st.tabs(["🔍 Competitor Strategy", "💬 Market Sentiment", "📈 Launch Metrics"])

with tabs[0]:
    if company_name:
        if st.session_state.competitor_response:
            st.markdown(st.session_state.competitor_response)
            if st.button("🔄 Regenerate"):
                st.session_state.competitor_response = None
                st.rerun()
        else:
            if st.button("🚀 Analyze Strategy", type="primary", use_container_width=True):
                with st.spinner("🔍 Gathering Intelligence..."):
                    try:
                        query = f'"{company_name}" product launch strategy features official blog'
                        raw_data, links = get_knowledge_base(query, role="general")
                        if raw_data:
                            bullet_prompt = (
                                f"Generate 16 evidence-based insight bullets about {company_name}.\n"
                                f"Tags: Positioning | Strength | Weakness | Learning.\n"
                                f"DATA:\n{raw_data}"
                            )
                            bullets = launch_analyst.run(bullet_prompt)
                            report = expand_competitor_report(bullets.content, company_name)
                            st.session_state.competitor_response = report
                            st.rerun()
                        else:
                            st.error("No data found.")
                    except Exception as e:
                        st.error(f"Error: {e}")

with tabs[1]:
    if company_name:
        if st.session_state.sentiment_response:
            st.markdown(st.session_state.sentiment_response)
        else:
            if st.button("🗣️ Analyze Sentiment", type="primary", use_container_width=True):
                with st.spinner("💬 Scanning Reddit & G2..."):
                    try:
                        query = f'"{company_name}"' 
                        raw_data, links = get_knowledge_base(query, role="sentiment")
                        if raw_data:
                            resp = sentiment_analyst.run(f"Analyze sentiment for {company_name} from:\n{raw_data}")
                            st.session_state.sentiment_response = resp.content
                            st.rerun()
                        else:
                            st.error("No discussion data found.")
                    except Exception as e:
                        st.error(f"Error: {e}")

with tabs[2]:
    if company_name:
        if st.session_state.metrics_response:
            st.markdown(st.session_state.metrics_response)
        else:
            if st.button("📈 Track Metrics", type="primary", use_container_width=True):
                with st.spinner("Hunting for KPIs..."):
                    try:
                        query = f'"{company_name}"'
                        raw_data, links = get_knowledge_base(query, role="metrics")
                        if raw_data:
                            resp = metrics_analyst.run(f"Extract KPIs for {company_name} from:\n{raw_data}")
                            st.session_state.metrics_response = resp.content
                            st.rerun()
                        else:
                            st.error("No metrics data found.")
                    except Exception as e:
                        st.error(f"Error: {e}")
