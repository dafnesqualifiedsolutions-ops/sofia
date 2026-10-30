# Sofia — UK (North West England)

## What this is
The UK clone of the Sofia page: contact at the end, GBP pricing, British AI voice, blue/white/red edge.

## Live
- https://dafnesqualifiedsolutions-ops.github.io/sofia/uk.html

## Price (GBP)
- One-time setup: £199
- Monthly: £149 (flat, no per-call fees)
- Up-front year = 2 months free (same as Mexico).

## AI brain (Vapi assistant)
- ID: 6933946a-8b14-4881-9725-3e4505d3a1eb  (name: "Sofia - UK North West", British voice en-GB-SoniaNeural)
- Localized to Liverpool/Manchester, multi-language for Polish/Urdu/Arabic communities.
- The page auto-routes its "Talk to Sofia" button to this assistant.

## Leads
- Same Formspree inbox (dafne396396@gmail.com) but tagged region = UK, so MX and UK leads are separable.
- UK live-call tool ID: d1b5608f-4beb-42b9-ab1b-6df67f00d3a2 (capture_lead_uk).

## Not done yet (flag when ready)
- UK phone number (Twilio) for inbound SMS/calls — web "Talk to Sofia" already works without one.
- UK WhatsApp number: button is inert until you set ?wa=44... on the URL.

## Regenerate the UK demo audio
  cd this-folder
  PATH=/home/yan/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin:$PATH   /home/yan/ai-agent/venv/bin/python gen_calls_uk.py

## Redeploy
Edit files, then git push in the repo (/tmp/sofia-repo).

## Standalone deploy note
This folder's entry file is uk.html (app.js detects "UK mode" by that filename). If you ever host this
folder as its own website, rename uk.html -> index.html and ask to flip the detection in app.js.
