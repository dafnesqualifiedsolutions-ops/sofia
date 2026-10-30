const VAPI_PUBLIC_KEY = "pk-67bd7d4d-e8cf-4afc-b26b-a1a54fd45568";
const VAPI_ASSISTANT_ID = "4c5df6a4-bc7f-47b7-a2fd-7cfae3cfccb1";
// Optional: point this at a form backend (Formspree / Apps Script / etc.) to actually deliver leads to you.
const LEAD_ENDPOINT = "https://formspree.io/f/xaeebgrz";

const LANGS = [
  { code: "en",   flag: "🇺🇸", label: "English" },
  { code: "es-MX", flag: "🇲🇽", label: "Español (MX)" },
  { code: "es-ES", flag: "🇪🇸", label: "Español (ES)" },
  { code: "es-CO", flag: "🇨🇴", label: "Español (CO)" },
  { code: "es-AR", flag: "🇦🇷", label: "Español (AR)" },
  { code: "fr",   flag: "🇫🇷", label: "Français" },
  { code: "de",   flag: "🇩🇪", label: "Deutsch" },
  { code: "nl",   flag: "🇳🇱", label: "Nederlands" },
  { code: "it",   flag: "🇮🇹", label: "Italiano" },
  { code: "pt",   flag: "🇧🇷", label: "Português" }
];

function uiLang(code) { return code.indexOf("es") === 0 ? "es" : code; }

function setLang(code) {
  document.querySelectorAll("[data-i18n]").forEach(function (el) {
    const k = el.getAttribute("data-i18n");
    const v = T[k] && T[k][uiLang(code)];
    if (v !== undefined) el.textContent = v;
  });
  document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
    const k = el.getAttribute("data-i18n-html");
    const v = T[k] && T[k][uiLang(code)];
    if (v !== undefined) el.innerHTML = v;
  });
  document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
    const k = el.getAttribute("data-i18n-ph");
    const v = T[k] && T[k][uiLang(code)];
    if (v !== undefined) el.placeholder = v;
  });
  const pa = document.getElementById("pitchAudio");
  if (pa) pa.src = "./audio/pitch-" + code + ".mp3";
  const pf = document.getElementById("pitchFlag");
  const lang = LANGS.find(function (l) { return l.code === code; });
  if (pf && lang) pf.textContent = lang.flag;
  document.querySelectorAll(".lang-btn").forEach(function (b) {
    b.classList.toggle("active", b.dataset.code === code);
  });
  try { localStorage.setItem("sofia_lang", code); } catch (e) {}
}

(function buildButtons() {
  const row = document.getElementById("langRow");
  LANGS.forEach(function (l) {
    const b = document.createElement("button");
    b.className = "lang-btn";
    b.dataset.code = l.code;
    b.title = l.label;
    b.innerHTML = l.flag + ' <span>' + l.label + "</span>";
    b.onclick = function () { setLang(l.code); };
    row.appendChild(b);
  });
})();

function saveLead(lead) {
  try {
    const all = JSON.parse(localStorage.getItem("sofia_leads") || "[]");
    all.push(lead);
    localStorage.setItem("sofia_leads", JSON.stringify(all));
    renderLeads();
  } catch (e) {}
  if (LEAD_ENDPOINT) {
    fetch(LEAD_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(lead)
    }).catch(function () {});
  }
}

function renderLeads() {
  const el = document.getElementById("leadsList");
  if (!el) return;
  try {
    const all = JSON.parse(localStorage.getItem("sofia_leads") || "[]");
    if (!all.length) { el.textContent = "(none yet)"; return; }
    el.textContent = all.map(function (l) {
      const t = new Date(l.t).toLocaleString();
      return "[" + l.type + "] " + (l.name || "-") + " | " + (l.phone || "-") +
             " | " + (l.intent || "") + " | " + l.lang + " | " + t;
    }).join("\n");
  } catch (e) { el.textContent = "(error)"; }
}
renderLeads();

let vapi = null, inCall = false;
function getLangCode() { try { return localStorage.getItem("sofia_lang") || "en"; } catch (e) { return "en"; } }

function startCall() {
  const status = document.getElementById("statusLine");
  if (!vapi) { status.textContent = "Voice SDK did not load."; return; }
  status.textContent = "Connecting...";
  vapi.start(VAPI_ASSISTANT_ID).catch(function (e) {
    console.error(e);
    status.textContent = "Could not connect. Check microphone permissions.";
  });
}
function endCall() { if (vapi) vapi.stop(); }

document.getElementById("gateForm").addEventListener("submit", function (e) {
  e.preventDefault();
  if (inCall) { endCall(); return; }
  const name = document.getElementById("gateName").value.trim();
  const phone = document.getElementById("gatePhone").value.trim();
  const consent = document.getElementById("gateConsent").checked;
  const status = document.getElementById("statusLine");
  if (!name || !phone) { status.textContent = "Please enter your name and number."; return; }
  if (!consent) { status.textContent = "Please tick the consent box to talk to Sofia."; return; }
  saveLead({ type: "talk", name: name, phone: phone, lang: getLangCode(), consent: true, t: new Date().toISOString() });
  startCall();
});

document.getElementById("cbForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const name = document.getElementById("cbName").value.trim();
  const phone = document.getElementById("cbPhone").value.trim();
  const intent = document.getElementById("cbIntent").value;
  const status = document.getElementById("cbStatus");
  if (!phone) { status.textContent = "Please enter a number."; return; }
  saveLead({ type: "callback", name: name || "-", phone: phone, intent: intent, lang: getLangCode(), t: new Date().toISOString() });
  status.textContent = (T.cbThanks && T.cbThanks[uiLang(getLangCode())]) || "Got it — we'll be in touch.";
  e.target.reset();
});

window.addEventListener("load", function () {
  if (!window.vapiSDK) return;
  try {
    vapi = window.vapiSDK.run({
      apiKey: VAPI_PUBLIC_KEY,
      assistant: VAPI_ASSISTANT_ID,
      config: {
        position: "bottom-right",
        offset: "24px",
        idle: { type: "round", color: "rgb(255,90,60)", icon: "https://unpkg.com/lucide-static@0.321.0/icons/phone.svg" },
        loading: { type: "round", color: "rgb(245,158,11)", icon: "https://unpkg.com/lucide-static@0.321.0/icons/loader-2.svg" },
        active: { type: "round", color: "rgb(239,68,68)", icon: "https://unpkg.com/lucide-static@0.321.0/icons/phone-off.svg" }
      }
    });
  } catch (e) { console.error("vapiSDK.run failed", e); return; }
  if (vapi && vapi.on) {
    vapi.on("call-start", function () {
      inCall = true;
      document.getElementById("gateBtn").textContent = "Hang up";
      document.getElementById("statusLine").textContent = "Connected — talk to Sofia now.";
    });
    vapi.on("call-end", function () {
      inCall = false;
      document.getElementById("gateBtn").textContent = (T.gateBtn && T.gateBtn[uiLang(getLangCode())]) || "Start call with Sofia";
      document.getElementById("statusLine").textContent = "Call ended.";
    });
    vapi.on("error", function (e) { console.error("Vapi error", e); });
  }
});

try { setLang(getLangCode()); } catch (e) { setLang("en"); }

/* === Custom waveform audio players === */
(function () {
  var COUNT = 32;
  document.querySelectorAll('audio').forEach(function (a) {
    var wrap = document.createElement('div'); wrap.className = 'player';
    var btn = document.createElement('button'); btn.className = 'play'; btn.type = 'button'; btn.innerHTML = '<span class="ic">▶</span>';
    var eq = document.createElement('div'); eq.className = 'peq'; var bars = [];
    for (var i = 0; i < COUNT; i++) { var b = document.createElement('span'); b.style.setProperty('--h', (18 + Math.random() * 70) + '%'); eq.appendChild(b); bars.push(b); }
    var time = document.createElement('span'); time.className = 'ptime'; time.textContent = '0:00';
    wrap.appendChild(btn); wrap.appendChild(eq); wrap.appendChild(time);
    a.parentNode.insertBefore(wrap, a); a.style.display = 'none';
    function fmt(s) { if (!isFinite(s)) return '0:00'; s = Math.floor(s); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
    function upd() { var d = a.duration || 1; var r = (a.currentTime || 0) / d; bars.forEach(function (b, i) { b.classList.toggle('on', (i + 0.5) / COUNT <= r); }); time.textContent = fmt(a.currentTime) + (isFinite(a.duration) ? ' / ' + fmt(a.duration) : ''); }
    btn.addEventListener('click', function () { if (a.paused) a.play(); else a.pause(); });
    a.addEventListener('play', function () { wrap.classList.add('playing'); btn.querySelector('.ic').textContent = '❚❚'; });
    a.addEventListener('pause', function () { wrap.classList.remove('playing'); btn.querySelector('.ic').textContent = '▶'; });
    a.addEventListener('ended', function () { wrap.classList.remove('playing'); btn.querySelector('.ic').textContent = '▶'; });
    a.addEventListener('timeupdate', upd);
    a.addEventListener('loadedmetadata', upd);
  });
})();
/* === Hero waveform === */
(function () { var el = document.getElementById('heroWave'); if (!el) return; for (var i = 0; i < 56; i++) { var s = document.createElement('span'); s.style.animationDelay = (i * 0.05) + 's'; s.style.setProperty('--h', (20 + Math.random() * 70) + '%'); el.appendChild(s); } })();
/* === Section kickers === */
(function () {
  var map = [
    ['.listen', '01 — Hear Sofia'], ['.gate', '02 — Talk Live'], ['.callback', '03 — Callback'],
    ['.calls-demo', '04 — Real Calls'], ['.cards', '05 — Who It Helps'],
    ['.how-it-works', '06 — How It Works'], ['.pricing', '07 — Pricing']
  ];
  map.forEach(function (m) { var s = document.querySelector(m[0]); if (s) { var k = document.createElement('div'); k.className = 'kicker'; k.textContent = m[1]; s.parentNode.insertBefore(k, s); } });
})();
