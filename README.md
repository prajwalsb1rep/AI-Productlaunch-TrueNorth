# 🚀 Prajwal Labs: True North Agent

**AI-Powered Market Intelligence & Product Strategy**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/YOUR_USERNAME/AI-Productlaunch-TrueNorth)

## 🌟 Overview
**True North** is an agentic AI system designed for Product Managers and GTM Strategists. It autonomously researches competitors, analyzes market sentiment, and tracks launch metrics using a multi-agent architecture.

Instead of generic searches, it uses specialized "Agent Personas" to hunt for specific signals:
* **Strategy Agent:** Deconstructs positioning and feature gaps.
* **Sentiment Agent:** Scans Reddit, G2, and Capterra for unfiltered user feedback.
* **Metrics Agent:** Hunts for hard revenue, user growth, and pricing data.

## 🛠️ Tech Stack
* **Framework:** [Agno (formerly Phidata)](https://github.com/agno-agi/agno)
* **UI:** Streamlit
* **Search Engine:** DuckDuckGo (Lite Backend for unblockable access)
* **Scraper:** Crawl4AI (Headless Chromium)
* **LLM:** Groq (Llama 3.3 70B)

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/AI-Productlaunch-TrueNorth.git](https://github.com/YOUR_USERNAME/AI-Productlaunch-TrueNorth.git)
    cd AI-Productlaunch-TrueNorth
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

3.  **Set up your API Key:**
    * Create a folder named `.streamlit`
    * Create a file `.streamlit/secrets.toml`
    * Add your key: `GROQ_API_KEY = "gsk_..."`

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## ☁️ Deployment (Streamlit Cloud)
This app is optimized for Streamlit Cloud.
1.  Fork this repo.
2.  Connect to Streamlit Cloud.
3.  **IMPORTANT:** Add your `GROQ_API_KEY` in the App Secrets settings.

---
*Built with ❤️ by Prajwal Labs*
