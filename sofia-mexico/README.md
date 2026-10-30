# Sofia — Mexico (Riviera Maya)

## What this is
The multilingual AI phone-receptionist landing page for the Mexico / Riviera Maya market.

## Live
- Main (coral): https://dafnesqualifiedsolutions-ops.github.io/sofia/
- Green/red Mexican theme: https://dafnesqualifiedsolutions-ops.github.io/sofia/?theme=mexico
- Colour previews: gold.html / violet.html / teal.html / lime.html (open them in this folder, or via ?theme= on the live URL)

## Price
- One-time setup: ,899 MXN
- Monthly: ,449 MXN (flat, no per-call fees)

## AI brain (Vapi assistant)
- ID: 4c5df6a4-bc7f-47b7-a2fd-7cfae3cfccb1  (name: "Sofia - Master Sales Caller", Mexican Spanish voice)
- Live "Talk to Sofia" on the page connects to this assistant.

## Leads
- Form (talk-gate + callback) and live calls both go to Formspree -> dafne396396@gmail.com
- Tagged region = MX in the inbox.

## Rebrand a client fast (no code)
Send a URL like:
  https://dafnesqualifiedsolutions-ops.github.io/sofia/?biz=Luigis%20Pizzeria&wa=529987654321&theme=gold
  - biz = page title, wa = WhatsApp line, theme = coral/gold/violet/teal/lime/mexico

## Regenerate the demo audio
  cd this-folder
  PATH=/home/yan/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin:$PATH   /home/yan/ai-agent/venv/bin/python gen_calls.py

## Redeploy
Edit files, then git push in the repo (/tmp/sofia-repo). Pages rebuild on GitHub automatically.
