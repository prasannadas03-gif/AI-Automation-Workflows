# 🤖 AI Automation Workflows

**Built by [Prasanna Kumar Das](https://rindax.com) | AI Automation & Data Analytics Professional | Assam, India**

This repository showcases production-ready AI automation workflows built with **n8n**, **Claude AI**, **Google Gemini**, **Airtable**, **Gmail**, and **Telegram**. These are real workflows running live for content, lead generation, job search, and inbox automation.

> ⚠️ Credentials have been replaced with placeholders for security. Replace `YOUR_*` values with your own before use.

---

## 📄 Documents

| Document | Description |
|---|---|
| [📋 Resume (Download PDF)](https://github.com/prasannadas03-gif/AI-Automation-Workflows/raw/main/Resume_Prasanna_Kumar_Das.pdf) | AI Automation & Workflow Engineer — experience, key projects, and skills |
| [📊 Data Analytics Portfolio](https://github.com/prasannadas03-gif/Data-analytics-portfolio) | Power BI & Excel dashboard projects |

---

## 📂 Workflows

### 🆕 Enterprise Knowledge Base RAG — Ingestion & Q&A
**File:** `workflows/enterprise-kb-rag.json`

Two independent webhook-triggered branches on one canvas: a document ingestion pipeline that dedupes against Postgres before chunking and embedding into a Supabase pgvector store, and a Q&A pipeline that retrieves top-K chunks, checks retrieval sufficiency, and answers strictly from retrieved context via a Gemini-powered grounded agent — with a Telegram escalation fallback when no answer is found.

**Stack:** n8n · Supabase (pgvector) · Postgres · Google Gemini · Telegram

**Flow:**
```
[Ingestion]
Webhook → Clean & Normalize Text → Check If Already Ingested (Postgres dedupe)
→ Insert into Knowledge Base (Supabase vector store) → Notify Ingestion Success

[Q&A]
Webhook → Normalize Question → Retrieve Top-K Chunks → Assess Retrieval Sufficiency
→ [Sufficient: Grounded Answer Agent → Respond] / [Insufficient: Fallback → Telegram Escalation → Respond]
```

![Enterprise KB RAG Workflow](./assets/Enterprise%20KB%20RAG.PNG)

---

### 🆕 Personal Email Workflow → Telegram
**File:** `workflows/personal-email-telegram.json`

Gmail inbox triage with a Gemini classifier that sorts every unread email into promotional / important / needs-reply, drafts a ready-to-send reply for anything needing one, and routes it to Telegram with inline Send/Reject buttons — a tap sends the Gmail reply (with signature) and marks the thread read, or rejects it with no email sent.

**Stack:** n8n · Gmail · Google Gemini · Telegram · n8n Data Tables

**Flow:**
```
Gmail Trigger (unread) → Classify Email (Gemini) → Route by Category
→ [Promotional: Mark as Read] / [Important: Telegram Notify → Mark as Read]
→ [Needs Reply: Store Draft → Telegram Approval (Send/Reject buttons)
   → Send: Gmail Reply + Mark Sent / Reject: Mark Rejected]
```

![Personal Email Workflow → Telegram](./assets/Personal%20Email%20Workflow.webp)

---

### 🆕 AI Lead Generation Automation
**File:** `workflows/ai-lead-generation-automation.json`

Zero-cost B2B lead qualification engine: pulls from free job-board APIs (Arbeitnow, Jobicy, RemoteOK) and Hacker News signal search, keyword-scores for automation pain, dedupes against the CRM, then runs candidates through a two-stage Gemini pipeline — a primary qualifier followed by a deliberately skeptical auditor with veto power — before saving to Airtable.

**Stack:** n8n · Google Gemini (dual-stage) · Airtable

**Flow:**
```
Trigger (manual / 8 AM & 4 PM) → 5 parallel feed fetches → Normalize & Signal Scoring
→ Dedup vs CRM → Primary Gemini Qualification → Qualification Gate
→ Skeptical Gemini Audit → Validation Gate → Format & Enrich → Save to Airtable CRM
```

![AI Lead Generation Automation Workflow](./assets/AI%20Lead%20Generation%20Automation.webp)

---

### 🆕 Multi-Tenant WhatsApp AI Agent
**File:** `workflows/multi-tenant-whatsapp-agent.json`

One reusable WhatsApp support agent deployable per client: resolves which business owns the inbound number, loads that client's own knowledge text and system prompt from Supabase, answers strictly from it via Claude Haiku with per-conversation memory, and replies on WhatsApp — never inventing details outside the client's knowledge doc.

**Stack:** n8n · WhatsApp Cloud API · Supabase · Claude Haiku 4.5

**Flow:**
```
WhatsApp Trigger → Normalize Input → Lookup Client by Phone Number (Supabase)
→ Build Session Context → WhatsApp Support Agent (Claude Haiku, per-client memory)
→ Send WhatsApp Reply
```

![Multi-Tenant WhatsApp AI Agent Workflow](./assets/Multi-Tenant%20WhatsApp%20AI%20Agent.PNG)

---

### 1. 📱 Social Media Post Automation
**File:** `workflows/01-social-media-post.json`

Scheduled workflow that reads blog posts from Google Sheets and auto-publishes to **LinkedIn**, **Facebook**, and **Instagram** with Claude AI-generated captions.

**Stack:** n8n · Google Sheets · Claude AI · LinkedIn API · Facebook Graph API · Instagram Graph API

**Flow:**
```
Schedule Trigger → Google Sheets (fetch pending post) → Claude AI (generate captions)
→ LinkedIn Post → Facebook Post → Instagram Publish → Google Sheets (mark published)
```

![Social Media Post Automation Workflow](./assets/Social%20Media%20Post%20Automation.PNG)

---

### 2. 📡 RSS Feed → Social Media Pipeline
**File:** `workflows/02-rss-social-media-post.json`

Fully automated pipeline that monitors a blog RSS feed and instantly publishes new articles to all 3 social platforms — zero manual input required.

**Stack:** n8n · RSS Feed Trigger · HTML Parser · Claude AI · LinkedIn · Facebook · Instagram

**Flow:**
```
RSS Feed Trigger → HTML Parser (extract image) → Claude AI (generate captions)
→ Facebook Post → LinkedIn Post → Instagram Publish
```

![RSS Feed Social Media Pipeline Workflow](./assets/RSS%20Feed_Social%20Media%20Pipeline.PNG)

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

![CRM Agent Workflow](./assets/CRM%20Agent.PNG)

---

### 4. 📋 Google Sheet → Airtable Leads Sync
**File:** `workflows/04-leads-crm-sync.json`

Daily sync that reads new leads from a Google Sheet, checks for duplicates in Airtable by company name, and adds only genuinely new leads with an auto-assigned Temperature based on city.

**Stack:** n8n · Google Sheets · Airtable

**Flow:**
```
Schedule (9 AM) → Google Sheets (read leads) → Check for data
→ Airtable (dedup search by company) → Map fields + set Temperature → Create Airtable record
```

Paired with a Telegram approval bridge (native inline buttons) that approves or rejects the AI-drafted outreach email for each new lead with a single tap.

---

### 5. 🔍 RSS Job Finder
**File:** `workflows/05-rss-job-finder.json`

Daily search across 11 freelance/remote job sources (Upwork, LinkedIn, Contra, PeoplePerHour, Freelancer, Truelancer, Hubstaff Talent, Naukri, Reddit r/forhire, and general web search) for n8n, Power BI, Excel, and AI-automation roles. Scores and filters results, splits into "Direct Mail" (named contact email) vs "ATS" (apply-on-portal), logs new ones to Airtable, and sends a Telegram digest.

**Stack:** n8n · Search API · Airtable · Telegram

**Flow:**
```
Schedule → 17 parallel job searches → Score & filter → Split (Direct Mail / ATS)
→ Airtable dedup + log → Build digest → Telegram alert
```

Paired with a Telegram approval bridge that drafts and sends the application email on tap.

---

### 6. 🌐 Multi-Platform ATS Job Finder
**File:** `workflows/06-multi-platform-ats-job-finder.json`

Twice-daily scan of 11 job feeds across 6 ATS platforms (Himalayas, Arbeitnow, RemoteOK, WeWorkRemotely, Greenhouse, Lever, Ashby), normalized into a common schema with freshness/hiring-intent scoring, keyword pre-filtered, then AI-scored by Gemini against a detailed candidate-fit profile with hard rejection gates. Deduplicates and saves the top 10 new highest-priority jobs to Airtable.

**Stack:** n8n · Google Gemini · Airtable

**Flow:**
```
Schedule (9 AM / 5 PM) → 11 parallel feed fetches → Normalize → Keyword pre-filter
→ Gemini AI scoring → Parse & rank → Dedup vs Airtable → Save top 10
```

Paired with a Telegram proposal notifier and an "Applied" status handler.

---

### 7. 🎯 Direct Human Hiring Opportunity Finder
**File:** `workflows/07-direct-human-hiring-finder.json`

Twice-daily scan of Reddit and web search for people directly asking to hire an n8n/automation freelancer — not formal ATS postings. Extracts contact emails/LinkedIn, screens out job-seeker and agency-ad posts, runs each requirement through a strict Gemini evaluator with hard rejection gates, and saves the top 10 highest-fit new opportunities to Airtable.

**Stack:** n8n · Google Gemini · Airtable · Reddit API

**Flow:**
```
Schedule (10 AM / 6 PM) → 6 parallel source searches → Normalize → Pre-filter + extract contacts
→ Gemini fit evaluation → Filter score ≥70 → Dedup vs Airtable → Save top 10
```

---

### 8. 💰 Lead Finder v2 — Linear, No Agent
**File:** `workflows/08-lead-finder-v2-linear.json`

A cost-optimization case study: replaces an earlier AI-agent-based lead finder (~$2.80 per test run) with a straight linear pipeline — 5 rotating local-business searches/day, deduplicated against Airtable, one AI call per lead (~300 tokens) — cutting cost to roughly $0.0002/day (~99.9% cheaper).

**Stack:** n8n · Serper Maps API · Airtable · Telegram

**Flow:**
```
Schedule (8 AM) → Build 5 daily search categories → Maps search → Extract top places
→ Dedup vs Airtable → Save lead → Telegram summary
```

---

### 9. 🧭 High-Intent B2B Lead Gen & AI Qualification
**File:** `workflows/09-b2b-lead-qualification.json`

Zero-cost buyer-intent engine: scans free job-board APIs and subreddits for businesses openly describing manual, repetitive operational pain, keyword-scores the signal, then runs candidates through a two-stage AI pipeline — a primary Gemini qualifier, followed by a deliberately skeptical Gemini "auditor" with veto power — before anything reaches the CRM.

**Stack:** n8n · Google Gemini (dual-model) · Airtable · Reddit API

**Flow:**
```
Trigger → Fetch job feeds + Reddit → Signal scoring → Dedup vs CRM
→ Primary Gemini qualification → Qualification gate → Skeptical Gemini audit
→ Validation gate → Format & enrich → Save to CRM
```

---

### 10. 📬 Email Triage & Auto-Reply System (Daily Mail Router)
**File:** `workflows/10-email-triage-router.json`

Webhook-driven router that receives pre-classified email events and routes them by tier: FYI-only summaries post a Telegram notification; reply-required emails are staged and sent to Telegram with inline Approve/Reject buttons — approving triggers an instant Gmail reply, then cleans up the pending record.

**Stack:** n8n · Telegram · Gmail · n8n Data Tables

**Flow:**
```
Webhook → Route by tier → [Summary: Telegram notify] / [Reply: stage + Telegram approval]
→ Approve → Gmail reply → Update Telegram message → Cleanup
```

Paired with separate Official-inbox and Personal-inbox classification workflows that feed this router.

---

## 🛠️ How to Use

1. Import the `.json` file into your n8n instance
2. Replace all `YOUR_*` placeholder values with your real credentials — **use n8n's built-in credential manager for API keys and bot tokens rather than pasting them into node parameters**
3. Set up required connections in n8n (Google Sheets, Gmail, Airtable, Telegram, Google Gemini, etc.)
4. Activate the workflow

---

## 📬 Contact

**Prasanna Kumar Das**
AI Automation & Data Analytics Professional
🌐 [rindax.com](https://rindax.com)
📧 prasannadas03@gmail.com
📍 Guwahati, Assam, India
