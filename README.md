# 🤖 RINDAX AI Automation Workflows

**Built by [Prasanna Kumar Das](https://rindax.com) | RINDAX — AI Automation Agency, Assam, India**

This repository showcases production-ready AI automation workflows built with **n8n**, **Claude AI**, **Airtable**, and **Gmail**. These are real workflows running live for RINDAX's content and client operations.

> ⚠️ Credentials have been replaced with placeholders for security. Replace `YOUR_*` values with your own before use.

---

## 📄 Documents

| Document | Description |
|---|---|
| [📋 AI Automation Capability Statement (Download PDF)](https://github.com/prasannadas03-gif/rindax-ai-workflows/raw/main/Prasanna_Kumar_Das_AI_Automation_Capability_Statement.pdf) | Full service overview, tech stack, and case studies |
| [📊 Data Analytics Portfolio](https://github.com/prasannadas03-gif/Data-analytics-portfolio) | Power BI & Excel dashboard projects |

---

## 📂 Workflows

### 1. 📱 Social Media Post Automation
**File:** `workflows/01-social-media-post.json`

Scheduled workflow that reads blog posts from Google Sheets and auto-publishes to **LinkedIn**, **Facebook**, and **Instagram** with Claude AI-generated captions.

**Stack:** n8n · Google Sheets · Claude AI · LinkedIn API · Facebook Graph API · Instagram Graph API

**Flow:**
```
Schedule Trigger → Google Sheets (fetch pending post) → Claude AI (generate captions)
→ LinkedIn Post → Facebook Post → Instagram Publish → Google Sheets (mark published)
```

---

### 2. 📡 RSS Feed → Social Media Pipeline
**File:** `workflows/02-rss-social-media-post.json`

Fully automated pipeline that monitors the RINDAX blog RSS feed and instantly publishes new articles to all 3 social platforms — zero manual input required.

**Stack:** n8n · RSS Feed Trigger · HTML Parser · Claude AI · LinkedIn · Facebook · Instagram

**Flow:**
```
RSS Feed Trigger → HTML Parser (extract image) → Claude AI (generate captions)
→ Facebook Post → LinkedIn Post → Instagram Publish
```

---

### 3. 🧠 Autonomous CRM Outreach Agent
**File:** `workflows/03-crm-outreach-agent.json`

Fully autonomous CRM agent powered by **Claude Sonnet** that handles the entire outreach lifecycle — fetches leads from Airtable, writes personalized emails, sends via Gmail, tracks replies, and updates lead status automatically.

**Stack:** n8n · Claude Sonnet 4.6 · Airtable · Gmail · AI Agent Nodes

**Two agents running in parallel:**
- **Outreach Agent** — runs at 9 AM daily
- **Response Tracker** — runs every 4 hours

**Flow:**
```
[Outreach Agent]
Schedule (9 AM) → Airtable (fetch leads) → Extract Email → Filter → Deduplicate
→ Loop: Claude Agent → Send Gmail → Update Airtable

[Response Tracker]
Schedule (every 4h) → Claude Agent:
  Check Gmail → Match replies → Classify intent → Update Airtable
```

---

## 🛠️ How to Use

1. Import the `.json` file into your n8n instance
2. Replace all `YOUR_*` placeholder values with your real credentials
3. Set up required connections in n8n (Google Sheets, Gmail, Airtable, LinkedIn, etc.)
4. Activate the workflow

---

## 📬 Contact

Want a custom AI automation workflow for your business?

**Prasanna Kumar Das**
AI Solutions Consultant | RINDAX
🌐 [rindax.com](https://rindax.com)
📧 prasannadas03@gmail.com
📍 Guwahati, Assam, India
