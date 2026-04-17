# Vantage Intelligence — Deployment Guide

## What you need before starting
- A Claude API key from console.anthropic.com (paid account required)
- A GitHub account (free at github.com)
- A Streamlit Community Cloud account (free at share.streamlit.io — sign in with GitHub)

---

## Step 1 — Get your Claude API key

1. Go to console.anthropic.com
2. Sign up or log in
3. Go to API Keys → Create Key
4. Copy the key (starts with `sk-ant-...`)
5. Keep it safe — you only see it once

---

## Step 2 — Put the app on GitHub

1. Go to github.com → New repository
2. Name it: `vantage-intelligence` (or any name)
3. Set to **Private**
4. Click Create repository

Upload these four files to the repo:
- `app.py`
- `prompts.py`
- `requirements.txt`
- `DEPLOY.md` (this file — optional)

The easiest way to upload: on your new GitHub repo page, click **Add file → Upload files**
and drag all four files in at once.

---

## Step 3 — Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io
2. Sign in with your GitHub account
3. Click **New app**
4. Select:
   - Repository: `vantage-intelligence` (the one you just created)
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Deploy**

The app will start building. This takes about 2 minutes.

---

## Step 4 — Add your API key as a secret

This is critical — without this, the app will not run.

1. Once the app is deployed, click the **⋮ menu** (top right of your app on Streamlit Cloud)
2. Click **Settings → Secrets**
3. Add this exactly:

```
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

Replace `sk-ant-your-key-here` with your actual API key.

4. Click **Save**
5. The app will restart automatically

---

## Step 5 — Test it

1. Your app now has a shareable URL that looks like:
   `https://your-app-name.streamlit.app`

2. Open the URL and enter:
   - Company: `littlefish`
   - URL: `littlefishapp.com`
   - Brief type: `Funder Brief`

3. Click **Run Vantage Brief**

4. The pipeline takes approximately 4–7 minutes to complete.
   You will see each role progress on screen.

---

## Step 6 — Share with testers

Send testers the URL. They need nothing else — no install, no account, no API key.

Ask them to test with a company they know well so they can evaluate the accuracy
of the Brief against their own knowledge.

---

## Costs

Each Brief costs approximately $0.15–0.40 in Claude API credits depending on
the company's available signal. Running 20 test Briefs costs approximately $4–8.

Monitor usage at console.anthropic.com → Usage.

---

## Updating the app

When you make changes to `app.py` or `prompts.py`:
1. Upload the new file to GitHub (same repo, same filename — it replaces the old one)
2. Streamlit Cloud detects the change and redeploys automatically within 1–2 minutes

---

## Troubleshooting

**"API key not found" error**
→ Check Streamlit secrets. Make sure the key is entered exactly as:
`ANTHROPIC_API_KEY = "sk-ant-..."`

**App times out or freezes**
→ The pipeline takes 4–7 minutes. This is normal. Do not refresh the page mid-run.

**Brief quality is thin**
→ Add additional context in the "Additional context" field — paste in any relevant
information about the company you want to include.

**Model error**
→ Check console.anthropic.com to confirm your account has active credits.
