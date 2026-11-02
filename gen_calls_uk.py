import asyncio, subprocess, os, tempfile

OUT = "/tmp/sofia-repo/audio-uk"
TMP = tempfile.mkdtemp()
os.makedirs(OUT, exist_ok=True)

# pitch samples: one per BUTTON language, UK-framed intro
PITCH = {
    "en":    ("en-GB-SoniaNeural",  "Hi, I'm Sofia. I answer calls for your business across the North West — Liverpool, Manchester and beyond — in English and many other languages, day or night."),
    "es-MX": ("es-MX-DaliaNeural",  "Hola, soy Sofia. Atiendo las llamadas de tu negocio en el norte de Inglaterra — Liverpool, Manchester — en inglés y español, a cualquier hora."),
    "es-ES": ("es-ES-AlvaroNeural", "Hola, soy Sofia. Atiendo las llamadas de tu negocio en el noroeste de Inglaterra — Liverpool, Manchester — en español o inglés, a cualquier hora."),
    "es-CO": ("es-CO-SalomeNeural", "Hola, soy Sofia. Contesto las llamadas de tu negocio en el norte de Inglaterra — Liverpool, Manchester — en español o inglés, a cualquier hora."),
    "es-AR": ("es-AR-ElenaNeural",  "Hola, soy Sofia. Atiendo las llamadas de tu negocio en el noroeste de Inglaterra — Liverpool, Manchester — en español o inglés, a cualquier hora."),
    "fr":    ("fr-FR-DeniseNeural", "Bonjour, je suis Sofia. Je réponds aux appels de votre entreprise dans le nord de l'Angleterre — Liverpool, Manchester — en français ou en anglais, à toute heure."),
    "de":    ("de-DE-KatjaNeural",  "Hallo, ich bin Sofia. Ich nehme Anrufe für Ihr Unternehmen im Nordwesten Englands — Liverpool, Manchester — auf Deutsch oder Englisch entgegen, rund um die Uhr."),
    "nl":    ("nl-NL-FennaNeural",   "Hoi, ik ben Sofia. Ik neem de telefoon aan voor uw bedrijf in het noordwesten van Engeland — Liverpool, Manchester — in het Nederlands of Engels, op elk moment."),
    "it":    ("it-IT-ElsaNeural",    "Ciao, sono Sofia. Rispondo alle chiamate della tua attività nel Nord Ovest dell'Inghilterra — Liverpool, Manchester — in italiano o in inglese, a qualsiasi ora."),
    "pt":    ("pt-BR-FranciscaNeural","Olá, eu sou a Sofia. Atendo as ligações do seu negócio no norte da Inglaterra — Liverpool, Manchester — em português ou inglês, a qualquer hora."),
}

SOFIA = "en-GB-SoniaNeural"
scenarios = [
    {  # Holiday-let guest, Manchester
        "id": "airbnb",
        "turns": [
            ("en-GB-RyanNeural", "Hi, I've booked your Manchester city-centre flat for next weekend — is there parking nearby, and can we check in a bit early, say 2pm?"),
            (SOFIA, "Hi! Yes, there's a paid car park two minutes away, and I can note an early 2pm check-in for you. Shall I send the arrival details by text?"),
            ("en-GB-RyanNeural", "Please, yes."),
            (SOFIA, "Done — I'll text the check-in info and door code now. Enjoy your weekend in Manchester!"),
        ],
    },
    {  # Barber, Manchester
        "id": "barber",
        "turns": [
            ("en-GB-ThomasNeural", "Alright Sofia, can I get a skin fade and a beard trim at your Manchester shop, Saturday morning?"),
            (SOFIA, "Sorted — we've got Saturday at 10am with our barber. Skin fade and beard trim, that right?"),
            ("en-GB-ThomasNeural", "Yeah, and my lad's six — can he come for a simple cut?"),
            (SOFIA, "Of course, we do kids from age three, gentle and quick. I'll book you both in — see you Saturday."),
        ],
    },
    {  # Dry cleaner, Manchester
        "id": "lavanderia",
        "turns": [
            ("en-GB-RyanNeural", "Hi, do you do dry cleaning for suits and a big duvet? And do you use a hypoallergenic detergent? My daughter is asthmatic."),
            (SOFIA, "Yes, we clean suits and king-size duvets, and we use a hypoallergenic solvent at no extra charge for your daughter. Shall I schedule a pickup tomorrow?"),
            ("en-GB-RyanNeural", "Yes please, morning."),
            (SOFIA, "Brilliant, we'll collect tomorrow morning. All booked in!"),
        ],
    },
    {  # Liverpool stadium tour (accessible)
        "id": "tours",
        "turns": [
            ("en-GB-RyanNeural", "Hi, can I book the Liverpool stadium tour for four, and is it wheelchair accessible for my mum?"),
            (SOFIA, "Absolutely — the stadium tour runs daily and has step-free access and wheelchair spaces for your mum. Shall I book four tickets?"),
            ("en-GB-RyanNeural", "Yes please."),
            (SOFIA, "Booked — four stadium tour tickets, accessible entry noted. Details on the way!"),
        ],
    },
    {  # Mid-call language switch PL -> EN (Polish community in the NW)
        "id": "langswitch",
        "turns": [
            ("pl-PL-MarekNeural", "Dzień dobry, chciałbym zapisać auto na przegląd w Manchesterze na poniedziałek rano."),
            ("pl-PL-ZofiaNeural", "Dzień dobry! Oczywiście, mamy wolny termin w poniedziałek rano. Samochód do przeglądu, zgadza się?"),
            ("en-GB-RyanNeural", "Actually, could you confirm that back in English for my wife?"),
            ("en-GB-SoniaNeural", "Of course — Monday morning for your car service in Manchester, all confirmed. I'll text the details."),
            ("en-GB-ThomasNeural", "Thank you!"),
            ("en-GB-SoniaNeural", "You're very welcome! See you Monday."),
        ],
    },
]

async def gen(voice, text, out_mp3, tries=8):
    import edge_tts
    last = None
    for i in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice)
            await comm.save(out_mp3)
            return
        except Exception as e:
            last = e
            await asyncio.sleep(3 + i * 3)
    raise last

def to_wav(mp3, wav):
    subprocess.run(["ffmpeg", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def silence(path, dur=0.6):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono:d={dur}",
                    "-t", str(dur), path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def phoneify(wav_in, mp3_out):
    noise = os.path.join(TMP, "noise.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=d=20:color=brown:amplitude=0.02",
                    "-ar", "24000", "-ac", "1", noise], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    filt = ("[0:a]highpass=f=300,lowpass=f=3400,volume=1.1[main];"
            "[1:a]volume=0.012[ns];"
            "[main][ns]amix=inputs=2:duration=first:dropout_transition=0")
    tmp = os.path.join(TMP, "phone.wav")
    subprocess.run(["ffmpeg", "-y", "-i", wav_in, "-i", noise, "-filter_complex", filt, tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["ffmpeg", "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "128k", mp3_out],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def build_call(scn):
    out = os.path.join(OUT, f"call-{scn['id']}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print("skip", out); return
    parts = []
    for i, (voice, text) in enumerate(scn["turns"]):
        mp3 = os.path.join(TMP, f"{scn['id']}_{i}.mp3")
        wav = os.path.join(TMP, f"{scn['id']}_{i}.wav")
        asyncio.run(gen(voice, text, mp3))
        to_wav(mp3, wav)
        parts.append(wav)
    sil = os.path.join(TMP, "sil.wav")
    silence(sil, 0.6)
    files = []
    for p in parts:
        files.append(p); files.append(sil)
    files = files[:-1]
    listfile = os.path.join(TMP, scn["id"] + ".txt")
    with open(listfile, "w") as f:
        for fn in files:
            f.write(f"file '{fn}'\n")
    merged = os.path.join(TMP, scn["id"] + ".wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c:a", "pcm_s16le", merged],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    out = os.path.join(OUT, f"call-{scn['id']}.mp3")
    phoneify(merged, out)
    print("built", out, os.path.getsize(out), "bytes")

def build_pitch(code, voice, text):
    mp3 = os.path.join(OUT, f"pitch-{code}.mp3")
    if os.path.exists(mp3) and os.path.getsize(mp3) > 1000:
        print("skip", mp3); return
    asyncio.run(gen(voice, text, mp3))
    print("built", mp3, os.path.getsize(mp3), "bytes")

for code, (voice, text) in PITCH.items():
    build_pitch(code, voice, text)

for scn in scenarios:
    build_call(scn)

print("ALL DONE")
