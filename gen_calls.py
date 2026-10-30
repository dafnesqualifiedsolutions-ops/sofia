import asyncio, subprocess, os, tempfile

OUT = "/tmp/sofia-repo/audio"
TMP = tempfile.mkdtemp()
os.makedirs(OUT, exist_ok=True)

# ---- pitch samples: one per BUTTON language (Spanish dialects get their own voice) ----
# key = exact button code used on the page
PITCH = {
    "en":    ("en-US-AriaNeural",    "Hi, I'm Sofia. I answer calls for your business in English or Spanish, any time, day or night."),
    "es-MX": ("es-MX-DaliaNeural",   "Hola, soy Sofia. Contesto las llamadas de tu negocio en inglés o español, a cualquier hora."),
    "es-ES": ("es-ES-AlvaroNeural",  "Hola, soy Sofia. Atiendo las llamadas de tu negocio en español o inglés, a cualquier hora."),
    "es-CO": ("es-CO-SalomeNeural",  "Hola, soy Sofia. Contesto las llamadas de tu negocio en español o inglés, a cualquier hora."),
    "es-AR": ("es-AR-ElenaNeural",   "Hola, soy Sofia. Atiendo las llamadas de tu negocio en español o inglés, a cualquier hora."),
    "fr":    ("fr-FR-DeniseNeural",  "Bonjour, je suis Sofia. Je réponds aux appels de votre entreprise en français ou en anglais, à toute heure."),
    "de":    ("de-DE-KatjaNeural",   "Hallo, ich bin Sofia. Ich nehme Anrufe für Ihr Unternehmen auf Deutsch oder Englisch an, rund um die Uhr."),
    "nl":    ("nl-NL-FennaNeural",    "Hoi, ik ben Sofia. Ik neem de telefoon aan voor uw bedrijf in het Nederlands of Engels, op elk moment."),
    "it":    ("it-IT-ElsaNeural",     "Ciao, sono Sofia. Rispondo alle chiamate della tua attività in italiano o in inglese, a qualsiasi ora."),
    "pt":    ("pt-BR-FranciscaNeural","Olá, eu sou a Sofia. Atendo as ligações do seu negócio em português ou inglês, a qualquer hora."),
}

SOFIA = "es-MX-DaliaNeural"
scenarios = [
    {  # Airbnb — English tourist, casual, throws a weird question
        "id": "airbnb",
        "turns": [
            ("en-US-ChristopherNeural", "Yeah hi — I'm looking at that beach condo in Playa, the one that sleeps six? For next week. Quick thing, is the rooftop pool heated? We're coming in February."),
            (SOFIA, "¡Hola! Sí, el condo acepta hasta seis personas. La alberca del rooftop está climatizada todo el año, en febrero va a estar perfecta. ¿Quieres que anote tu check-in?"),
            ("en-US-ChristopherNeural", "Awesome. Oh — one more, can I bring my dog? He's a golden retriever, like a service dog, y'know?"),
            (SOFIA, "Claro, los perros de servicio son bienvenidos sin costo extra. Anoto a tu golden retriever. ¿Reservo ya?"),
            ("en-US-ChristopherNeural", "Yeah go ahead, book it."),
            (SOFIA, "Listo, agendé tu estancia. Te mando los detalles por WhatsApp. ¡Que la disfrutes!"),
        ],
    },
    {  # Barber — local Spanish, colloquial, odd request
        "id": "barber",
        "turns": [
            ("es-MX-JorgeNeural", "Quisiera agendar una cita para un fade, ¿tienen libre el sábado por la mañana?"),
            (SOFIA, "¡Órale! Tenemos sitio el sábado a las diez de la mañana. ¿Corte fade y barba?"),
            ("es-MX-JorgeNeural", "Sí, fade y barba. Ah, y una duda rara — ¿cortan a niños? Porque quiero llevar a mi sobrino de cuatro añitos."),
            (SOFIA, "Sí, cortamos desde los tres años, con paciencia y tijeras chiquitas. Agendamos a los dos juntos, ¿te va?"),
            ("es-MX-JorgeNeural", "Perfecto, los dos entonces."),
            (SOFIA, "Listo, cita para ti y tu sobrino el sábado a las diez. Te confirmamos por mensaje."),
        ],
    },
    {  # Laundry — English expat, specific needs
        "id": "lavanderia",
        "turns": [
            ("en-US-JennyNeural", "Hi Sofia, do you guys do laundry pickup from Airbnbs? I'm near Fifth Avenue."),
            (SOFIA, "¡Hola! Sí, recogemos y entregamos en Airbnb sin problema. ¿Qué necesitas lavar?"),
            ("en-US-JennyNeural", "Mostly clothes, but also a king-size comforter. And — this matters — do you use hypoallergenic detergent? My son has eczema."),
            (SOFIA, "Sí, lavamos edredones king size y usamos detergente hipoalergénico sin costo extra por tu hijo. ¿Agendo la recolección mañana?"),
            ("en-US-JennyNeural", "Yes please, tomorrow morning."),
            (SOFIA, "Perfecto, pasamos mañana por tu Airbnb. ¡Quedó agendado!"),
        ],
    },
    {  # Tours — English tourist, accessibility twist
        "id": "tours",
        "turns": [
            ("en-US-AvaNeural", "Hey, I wanna book the dolphin swim and maybe a yacht for the family."),
            (SOFIA, "¡Hola! Con gusto. El nado con delfines sale a las nueve y la carta de yate es media jornada. ¿Para cuántas personas?"),
            ("en-US-AvaNeural", "Four of us. Oh — my mom's in a wheelchair. Is the yacht accessible?"),
            (SOFIA, "Sí, tenemos yates con rampa y espacio para silla de ruedas. Tu mamá viene sin problema. ¿Reservo para cuatro?"),
            ("en-US-AvaNeural", "Yes please."),
            (SOFIA, "Listo, reservé delfines y yate accesible para cuatro. ¡Los detalles por WhatsApp!"),
        ],
    },
    {  # Mid-call language switch ES -> EN -> ES
        "id": "langswitch",
        "turns": [
            ("es-MX-JorgeNeural", "Hola Sofia, quiero preguntar sobre el tour de Tulum."),
            (SOFIA, "¡Hola! Con gusto, ¿qué te gustaría saber de los tours de Tulum?"),
            ("en-US-BrianNeural", "Actually, do you have the cenote tour, and is it good for kids?"),
            (SOFIA, "Sí, tenemos el tour de cenotes y es familiar, ideal para niños. ¿Quieres que agende tu visita?"),
            ("es-MX-JorgeNeural", "Sí, para el sábado por favor."),
            (SOFIA, "¡Perfecto! Agendé tu tour de cenotes para el sábado. Te mando confirmación."),
        ],
    },
]

async def gen(voice, text, out_mp3, tries=4):
    import edge_tts
    last = None
    for i in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice)
            await comm.save(out_mp3)
            return
        except Exception as e:
            last = e
            await asyncio.sleep(2 + i * 2)
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
    asyncio.run(gen(voice, text, mp3))
    print("built", mp3, os.path.getsize(mp3), "bytes")

for code, (voice, text) in PITCH.items():
    build_pitch(code, voice, text)

for scn in scenarios:
    build_call(scn)

print("ALL DONE")
