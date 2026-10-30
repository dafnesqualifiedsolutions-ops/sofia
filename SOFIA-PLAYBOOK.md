# Sofia — Operating Playbook

> One document to refresh the whole motion: what we sell, what it costs, how reps get paid, how we spin up a client, and how the page works. Edit freely; this is the source of truth between sessions.

## 1. What we sell
**Sofia** — a multilingual AI phone receptionist for small businesses in the Riviera Maya (Puerto Morelos, Playa del Carmen, Cancún). She answers calls in **English and Spanish** (plus more languages on the demo page), 24/7, books/captures, and never misses a caller. Pitch in one line: *"She answers your phone in both languages, any time, so you stop losing customers."*

## 2. The demo is the pitch
The page has a **live "Talk to Sofia" button**. The killer move when knocking doors:
1. Open the page on your phone.
2. Tap **Talk to Sofia**, hit speaker.
3. Ask a real question ("Do you take bookings in English?"). The owner hears Sofia answer live.
Nothing else sells it. Have one scripted question ready so it always lands.

## 3. Pricing (MXN)
- **One-time setup: $1,899**
- **Monthly: $1,449 / month** — flat, no per-call fees.
- **Up-front incentive:** pay a **full year up front → 2 months free** (client pays 10 months, gets 12). Use this to pull cash forward.

## 4. Sales rep commission
Reps keep **50% of everything they sign**, including the recurring monthly (or the yearly up-front) revenue. Setup fee is also 50% unless we decide otherwise.

Worked examples (per client):
- **Monthly plan:** client pays $1,449/mo. Rep earns **$724.50/mo** + **$949.50** setup = ongoing.
- **Yearly up-front:** client pays 10 × $1,449 = **$14,490** (gets 12 months). Rep earns **$7,245** once + **$949.50** setup = **$8,194.50** up front.
  - The 2-free-months is the *client's* discount to choose yearly; rep's 50% is on what's actually paid.

Yan keeps the other 50%. We do **not** need many clients to be cash-positive.

## 5. Who to pitch (verticals)
The four that already demo best on the page — keep these, add more as we learn:
- 🏠 Real Estate & Airbnb
- 💈 Barber Shops
- 🧺 Laundromats
- 🛥️ Tours & Excursions

Good additions: restaurants/cafés, dental/medical spas, gyms, vacation-rental managers. **Best first targets:** businesses that visibly lose calls — Airbnb hosts, tour desks, busy restaurants, barbers. Open with *"How many calls do you miss when you're closed or busy?"*

## 6. Onboarding a client (template)
The page is **config-driven** so spinning up a client is fast:
- **Fastest:** send them (or the rep) a branded URL — no code:
  `https://dafnesqualifiedsolutions-ops.github.io/sofia/?biz=Luigis%20Pizzeria&wa=529987654321&theme=gold`
  - `biz` → page title. `wa` → WhatsApp contact line. `theme` → recolor (coral/gold/violet/teal/lime). `accent=#hex` → custom color.
- **Or** edit `config.js` (`businessName`, `whatsapp`, `accent`) and redeploy.
- **Spoken name:** right now Sofia's script is one global assistant. To have her say *their* business name live, we clone the assistant per client (copy the assistant, drop the name into the prompt). Page branding works today; per-client *voice* name is the next step — flag it when we onboard the first real client.

## 7. Design direction (don't look like "AI slop")
- Distinctive **voice/signal** identity: near-black canvas, one confident accent, editorial type + mono micro-labels, a living **waveform** motif (the product *is* sound), and **custom waveform audio players** (no default browser bars).
- Deliberately **away** from dark + neon-cyan glass — that's the template look everyone ships.
- Compare palettes live via `?theme=` (coral = current default).

## 8. Lead flow (where leads land)
- **Page forms** (talk-gate + callback) → Formspree → **dafne396396@gmail.com** (verified test email received).
- **Live calls** → Sofia calls the `capture_lead` tool → same Formspree → same inbox. (Tool created + attached; live firing needs a real call to confirm — no credits spent yet.)
- Reps can also use the callback form on the spot to drop a prospect's number into the inbox before leaving.

## 9. Open items / next steps
- Pick the winning color (`?theme=`) → bake as default, delete the rest.
- Add a visible phone/WhatsApp line if we want the page to capture on its own (currently sent separately).
- First real client → clone assistant per business so Sofia says their name.
- Rotate the Vapi API key once this is finished (it has sat in chat).
- Cartoon Sofia face is in the hero; illustrated explainer strips can follow if wanted.
