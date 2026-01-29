import asyncio
import os
from duckduckgo_search import DDGS
from textwrap import dedent
import nest_asyncio
from crawl4ai import AsyncWebCrawler
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import streamlit as st

# CRITICAL FIX: Prevent Mac Crash
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

try:
    nest_asyncio.apply()
except ValueError:
    pass

# --- CONFIGURATION (SECURE) ---
# We load the key securely from Streamlit Cloud.
# If running locally, you must set this in your .streamlit/secrets.toml file or just ignore if pushing to cloud.
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = "" # Leave EMPTY for GitHub safety!

# --- 1. SEARCH ENGINE ---
def search_web(query, role="general", max_results=4):
    print(f"🔎 Ram is hunting for: {query} (Role: {role})")
    valid_links = []
    
    bad_domains = [
        "zhihu.com", "taobao.com", "tmall.com", "jd.com", 
        "aliexpress", "temu", "pinduoduo", "1688.com",
        "trailblazer.me", "linkedin.com", "facebook.com", "instagram.com",
        "tiktok.com", "pinterest.com"
    ]

    clean_name = query.replace('"', '').split(' ')[0]

    # MVP HARDCODED TARGETS
    if role == "sentiment":
        target_query = f'{clean_name} site:reddit.com OR site:g2.com OR site:trustradius.com OR site:capterra.com "review"'
    elif role == "metrics":
        target_query = f'{clean_name} pricing revenue funding users site:techcrunch.com OR site:saasworthy.com OR site:getlatka.com OR site:crunchbase.com'
    else:
        target_query = f'{clean_name} product launch strategy features official blog -jobs -profile'

    # SEARCH
    try:
        results = DDGS().text(keywords=target_query, region='wt-wt', backend='lite', max_results=max_results)
        if results:
            for r in results:
                link = r.get('href', '')
                if any(bad in link for bad in bad_domains): continue
                if link not in valid_links: valid_links.append(link)
    except Exception as e:
        print(f"   ⚠️ Search Error: {e}")

    # FALLBACK
    if len(valid_links) == 0:
        try:
            news_results = DDGS().news(keywords=clean_name, region='wt-wt', max_results=3)
            if news_results:
                for r in news_results:
                    link = r.get('url', '')
                    if link not in valid_links: valid_links.append(link)
        except:
            pass

    return valid_links[:3]

async def scrape_concurrent(urls):
    print(f"🕸️ Scraping {len(urls)} sites...")
    results = []
    async with AsyncWebCrawler(verbose=True) as crawler:
        for url in urls:
            try:
                await asyncio.sleep(0.5)
                res = await crawler.arun(url=url)
                if res.markdown:
                    text = res.markdown[:4000] 
                    results.append(f"### SOURCE: {url}\n{text}\n{'='*30}")
            except Exception as e:
                print(f"Failed: {url}")
    return "\n\n".join(results)

def get_knowledge_base(query, role="general"):
    links = search_web(query, role=role)
    if not links: return None, []
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    content = loop.run_until_complete(scrape_concurrent(links))
    return content, links

# --- 2. AGENTS ---
def get_groq_model():
    # Helper to prevent crashes if Key is missing locally
    if not GROQ_API_KEY:
        return None 
        
    return OpenAIChat(
        id="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

launch_analyst = Agent(
    name="Product Launch Analyst",
    description=dedent("""
    You are a senior Go-To-Market strategist.
    Evaluate competitor launches. Uncover Positioning, Tactics, Strengths, Weaknesses.
    Always cite observable signals.
    """),
    model=get_groq_model(),
    markdown=True
)

sentiment_analyst = Agent(
    name="Market Sentiment Specialist",
    description=dedent("""
    You are a market research expert.
    Analyze social media sentiment (Reddit, G2) and identify positive/negative drivers.
    """),
    model=get_groq_model(),
    markdown=True
)

metrics_analyst = Agent(
    name="Launch Metrics Specialist", 
    description=dedent("""
    You are a product launch performance analyst.
    Track KPIs: User adoption, Revenue, Market penetration, Growth rates.
    """),
    model=get_groq_model(),
    markdown=True
)

def expand_competitor_report(bullet_text: str, competitor: str) -> str:
    prompt = (
        f"Transform these bullets into a professional launch review for {competitor}.\n"
        f"Format: Markdown with Tables.\n"
        f"=== FORMAT ===\n"
        f"# {competitor} -- Launch Review\n\n"
        f"## 1. Positioning\n• Summary (max 6 bullets).\n\n"
        f"## 2. Strengths\n| Strength | Evidence |\n|---|---|\n| ... | ... |\n\n"
        f"## 3. Weaknesses\n| Weakness | Evidence |\n|---|---|\n| ... | ... |\n\n"
        f"## 4. Takeaways\n1. ...\n\n"
        f"=== INPUT ===\n{bullet_text}\n"
    )
    resp = launch_analyst.run(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)