"""
Generate MiroFish-Offline change report PDF using ReportLab.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os

OUT = "/home/dolores/mirofish-offline/MiroFish_Changes_Report.pdf"

# ── colour palette ─────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0D1B2A")
BLUE   = colors.HexColor("#1565C0")
TEAL   = colors.HexColor("#00897B")
RED    = colors.HexColor("#C62828")
AMBER  = colors.HexColor("#FF8F00")
LGREY  = colors.HexColor("#F5F5F5")
MGREY  = colors.HexColor("#E0E0E0")
DGREY  = colors.HexColor("#757575")
WHITE  = colors.white
BLACK  = colors.black

ADD_BG    = colors.HexColor("#E8F5E9")
ADD_FG    = colors.HexColor("#1B5E20")
DEL_BG    = colors.HexColor("#FFEBEE")
DEL_FG    = colors.HexColor("#B71C1C")
MOD_BG    = colors.HexColor("#FFF8E1")
MOD_FG    = colors.HexColor("#E65100")
NEW_BG    = colors.HexColor("#E3F2FD")
NEW_FG    = colors.HexColor("#0D47A1")

# ── styles ─────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def s(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = s("CoverTitle",
    fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
    leading=36, alignment=TA_CENTER)

cover_sub = s("CoverSub",
    fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#B0BEC5"),
    leading=20, alignment=TA_CENTER)

cover_meta = s("CoverMeta",
    fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#90A4AE"),
    leading=16, alignment=TA_CENTER)

h1 = s("H1",
    fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
    spaceBefore=18, spaceAfter=6, leading=20,
    borderPad=4)

h2 = s("H2",
    fontName="Helvetica-Bold", fontSize=12, textColor=BLUE,
    spaceBefore=12, spaceAfter=4, leading=16)

h3 = s("H3",
    fontName="Helvetica-Bold", fontSize=10, textColor=TEAL,
    spaceBefore=8, spaceAfter=2, leading=14)

body = s("Body",
    fontName="Helvetica", fontSize=9, textColor=BLACK,
    leading=14, alignment=TA_JUSTIFY, spaceAfter=4)

bullet = s("Bullet",
    fontName="Helvetica", fontSize=9, textColor=BLACK,
    leading=13, leftIndent=14, bulletIndent=4, spaceAfter=2)

code_style = s("Code",
    fontName="Courier", fontSize=8, textColor=colors.HexColor("#1A237E"),
    backColor=colors.HexColor("#F8F9FA"), leading=11,
    leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4)

note_style = s("Note",
    fontName="Helvetica-Oblique", fontSize=8.5, textColor=DGREY,
    leading=13, spaceBefore=2, spaceAfter=6)

# ── helpers ────────────────────────────────────────────────────────────────────
def hr(color=MGREY, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=6, spaceBefore=4)

def sp(h=6):
    return Spacer(1, h)

def p(text, style=body):
    return Paragraph(text, style)

def h(text, level=1):
    return Paragraph(text, [h1, h2, h3][level - 1])

def b(text):
    return Paragraph(f"• {text}", bullet)

def badge(text, bg, fg):
    """Small inline badge rendered as a 1-cell table."""
    t = Table([[Paragraph(f"<b>{text}</b>",
                          s("_b", fontName="Helvetica-Bold", fontSize=7,
                            textColor=fg, leading=9, alignment=TA_CENTER))]],
              colWidths=[2.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [3]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

SYM_HEX = {"ADD": "1B5E20", "DEL": "B71C1C", "MOD": "E65100", "NEW": "0D47A1"}

def diff_table(rows):
    """Renders a before/after diff block."""
    tdata = []
    for kind, before, after in rows:
        bg = {"ADD": ADD_BG, "DEL": DEL_BG, "MOD": MOD_BG, "NEW": NEW_BG}.get(kind, LGREY)
        sym = {"ADD": "+", "DEL": "-", "MOD": "~", "NEW": "*"}.get(kind, " ")
        sym_hex = SYM_HEX.get(kind, "757575")

        sym_para = Paragraph(
            f"<font color='#{sym_hex}'><b>{sym}</b></font>",
            s("_sym", fontName="Courier-Bold", fontSize=10, leading=12, alignment=TA_CENTER))

        before_para = Paragraph(
            f"<font color='#B71C1C'>{before}</font>" if before else "",
            s("_diff", fontName="Courier", fontSize=8, leading=11, textColor=DEL_FG))

        after_para = Paragraph(
            f"<font color='#1B5E20'>{after}</font>" if after else "",
            s("_diff", fontName="Courier", fontSize=8, leading=11, textColor=ADD_FG))

        tdata.append([sym_para, before_para, after_para])

    col_w = [0.5 * cm, 7.5 * cm, 7.5 * cm]
    t = Table(tdata, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LGREY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [ADD_BG, DEL_BG, MOD_BG, NEW_BG, LGREY]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, MGREY),
        ("BOX", (0, 0), (-1, -1), 0.5, MGREY),
    ]))
    # apply per-row background
    for i, (kind, _, __) in enumerate(rows):
        bg = {"ADD": ADD_BG, "DEL": DEL_BG, "MOD": MOD_BG, "NEW": NEW_BG}.get(kind, LGREY)
        t.setStyle(TableStyle([("BACKGROUND", (0, i), (-1, i), bg)]))
    return t

def endpoint_table(rows, headers=("Method", "Endpoint", "Purpose")):
    hrow = [Paragraph(f"<b>{h}</b>", s("_th", fontName="Helvetica-Bold", fontSize=8,
                                        textColor=WHITE, leading=11))
            for h in headers]
    data = [hrow]
    for r in rows:
        data.append([Paragraph(c, s("_td", fontName="Courier" if i < 2 else "Helvetica",
                                     fontSize=8, leading=11, textColor=BLACK))
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=[1.8 * cm, 5.5 * cm, 9.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGREY]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, MGREY),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, MGREY),
    ]))
    return t

# ── cover page ─────────────────────────────────────────────────────────────────
def cover_block():
    bg = Table(
        [[Paragraph("MiroFish-Offline", cover_title)],
         [sp(8)],
         [Paragraph("Change Report", cover_title)],
         [sp(16)],
         [Paragraph("Custom enhancements layered on top of the baseline OASIS simulation engine", cover_sub)],
         [sp(24)],
         [Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", cover_meta)],
         [Paragraph("Author: Dolores · hariharan.m@mu-sigma.com", cover_meta)],
        ],
        colWidths=[16.5 * cm])
    bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 28),
        ("RIGHTPADDING", (0, 0), (-1, -1), 28),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return bg

# ── summary table ───────────────────────────────────────────────────────────────
def summary_table():
    rows = [
        ["File / Component", "Status", "Impact"],
        [".env", "NEW", "Remote Ollama + port config"],
        ["backend/app/config.py", "MODIFIED", "Runtime model & server override"],
        ["backend/app/utils/llm_client.py", "MODIFIED", "Global LLM call logging"],
        ["backend/app/api/settings.py", "NEW", "7 new API endpoints"],
        ["backend/app/api/simulation.py", "MODIFIED", "6 new simulation control endpoints"],
        ["backend/app/api/__init__.py", "MODIFIED", "Blueprint registration"],
        ["backend/app/__init__.py", "MODIFIED", "Blueprint registration"],
        ["frontend/src/api/settings.js", "NEW", "API client for all new endpoints"],
        ["frontend/src/components/ModelChooser.vue", "NEW", "Live model selector UI"],
        ["frontend/src/views/MainView.vue", "MODIFIED", "ModelChooser added to header"],
        ["frontend/src/components/Step3Simulation.vue", "MODIFIED", "Pause/resume, ontology, LLM log UI"],
        ["frontend/vite.config.js", "MODIFIED", "Proxy port 5001→5010"],
        ["frontend/src/api/index.js", "MODIFIED", "Relative baseURL (network fix)"],
        ["docker-compose.yml", "MODIFIED", "Removed local ollama service"],
    ]
    status_colors = {"NEW": (NEW_BG, NEW_FG), "MODIFIED": (MOD_BG, MOD_FG)}
    hrow = [Paragraph(f"<b>{c}</b>",
                      s("_th", fontName="Helvetica-Bold", fontSize=8.5,
                        textColor=WHITE, leading=12))
            for c in rows[0]]
    data = [hrow]
    for r in rows[1:]:
        bg, fg = status_colors.get(r[1], (LGREY, DGREY))
        data.append([
            Paragraph(f"<font name='Courier' size='8'>{r[0]}</font>",
                      s("_f", fontName="Courier", fontSize=8, leading=11)),
            Paragraph(f"<b>{r[1]}</b>",
                      s("_s", fontName="Helvetica-Bold", fontSize=8,
                        textColor=fg, leading=11, alignment=TA_CENTER)),
            Paragraph(r[2], s("_i", fontName="Helvetica", fontSize=8.5, leading=12)),
        ])
    t = Table(data, colWidths=[6.5 * cm, 2.2 * cm, 7.8 * cm])
    for i, r in enumerate(rows[1:], 1):
        bg, _ = status_colors.get(r[1], (LGREY, DGREY))
        alt = LGREY if i % 2 == 0 else WHITE
        t.setStyle(TableStyle([("BACKGROUND", (0, i), (-1, i), alt)]))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, MGREY),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, MGREY),
    ]))
    return t

# ── build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="MiroFish-Offline Change Report",
        author="Dolores")

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [sp(60), cover_block(), sp(40)]

    # ── 1. Executive Summary ───────────────────────────────────────────────────
    story += [
        h("1. Executive Summary"),
        hr(BLUE, 1),
        p("MiroFish-Offline is a multi-agent social simulation engine built on the OASIS/CAMEL-AI "
          "framework with a Neo4j knowledge graph backend and a Vue 3 frontend. The baseline "
          "repository ran with a local Ollama container and offered no runtime model control, no "
          "visibility into LLM calls, no bag-ontology inspection, and no way to pause or reorder "
          "agents mid-simulation."),
        sp(4),
        p("This report documents every change made to introduce four capabilities requested by the "
          "user, plus the network connectivity fix:"),
        sp(4),
        b("<b>Model Chooser</b> — pick any of the 59 models on the remote Ollama server "
          "(172.25.1.70:11434) from the UI header, switch server URLs, all without restarting."),
        b("<b>Transparent Agentic Conversation</b> — every LLM prompt and response is logged "
          "in real-time, visible in an expandable side panel during simulation."),
        b("<b>Bag Ontology Visibility</b> — entity types and edge types from the Neo4j knowledge "
          "graph are surfaced in a live side panel during simulation."),
        b("<b>Pause &amp; Rearrange</b> — pause a running simulation, reorder agents, adjust "
          "influence/activity sliders, inject one-off events, then resume."),
        b("<b>Network Fix</b> — API calls now use relative paths proxied by Vite, so the app "
          "works from any IP/hostname, not just localhost."),
        sp(8),
        h("2. File Change Summary", 2),
        hr(),
        summary_table(),
        sp(16),
    ]

    # ── 2. Infra & Config ──────────────────────────────────────────────────────
    story += [
        h("3. Infrastructure &amp; Configuration"),
        hr(BLUE, 1),

        h("3.1  .env  (NEW FILE)", 2),
        p("The repository originally shipped no .env — environment was baked into docker-compose. "
          "A new .env was created for bare-metal execution pointing all services at the remote "
          "Ollama server instead of a local container:"),
        sp(4),
    ]

    env_rows = [
        ("DEL", "# no .env existed", ""),
        ("ADD", "", "LLM_BASE_URL=http://172.25.1.70:11434/v1"),
        ("ADD", "", "LLM_MODEL_NAME=qwen2.5:32b"),
        ("ADD", "", "OLLAMA_NUM_CTX=8192"),
        ("ADD", "", "NEO4J_URI=bolt://localhost:7687"),
        ("ADD", "", "FLASK_PORT=5010   # avoids collision with :5001"),
        ("ADD", "", "OPENAI_API_BASE_URL=http://172.25.1.70:11434/v1"),
    ]
    story += [diff_table(env_rows), sp(8)]

    story += [
        h("3.2  docker-compose.yml  (MODIFIED)", 2),
        p("The local <font name='Courier'>ollama</font> service and its <font name='Courier'>"
          "depends_on</font> reference were removed. All LLM traffic goes to the remote server. "
          "Only the <font name='Courier'>mirofish</font> app and <font name='Courier'>neo4j</font>"
          " services remain."),
        sp(4),
        diff_table([
            ("DEL", "ollama:", ""),
            ("DEL", "  image: ollama/ollama", ""),
            ("DEL", "  volumes: [ollama_data:/root/.ollama]", ""),
            ("DEL", "  depends_on: [ollama]  # in mirofish service", ""),
        ]),
        sp(12),
    ]

    # ── 3. Backend Changes ─────────────────────────────────────────────────────
    story += [
        h("4. Backend Changes"),
        hr(BLUE, 1),

        h("4.1  backend/app/config.py  (MODIFIED)", 2),
        p("Added class-level runtime override slots so model and server URL can be switched at "
          "runtime via the API — no process restart required. The active URL/model is always "
          "resolved through a getter that prefers the runtime override:"),
        sp(4),
        diff_table([
            ("ADD", "", "from typing import Optional"),
            ("ADD", "", "_runtime_model: Optional[str] = None"),
            ("ADD", "", "_runtime_base_url: Optional[str] = None"),
            ("ADD", "", "get_runtime_model() / set_runtime_model(model)"),
            ("ADD", "", "get_active_base_url() / set_runtime_base_url(url)"),
        ]),
        sp(8),

        h("4.2  backend/app/utils/llm_client.py  (MODIFIED)", 2),
        p("Three additions: (1) the constructor now resolves <font name='Courier'>base_url</font> "
          "and <font name='Courier'>model</font> through Config's runtime getters; "
          "(2) a global in-memory ring buffer (deque, max 200 entries) captures every LLM call; "
          "(3) an optional per-simulation JSONL file is written alongside each call for persistent "
          "retrieval."),
        sp(4),
        diff_table([
            ("ADD", "", "_global_llm_log: deque = deque(maxlen=200)"),
            ("ADD", "", "get_global_llm_log() → List[Dict]"),
            ("MOD", "base_url = base_url or Config.LLM_BASE_URL",
                    "base_url = base_url or Config.get_active_base_url()"),
            ("MOD", "model = model or Config.LLM_MODEL_NAME",
                    "model = model or Config.get_runtime_model() or Config.LLM_MODEL_NAME"),
            ("ADD", "", "call_tag, simulation_log_path params on __init__"),
            ("ADD", "", "_log_call() → appends entry to deque + optional JSONL file"),
            ("ADD", "", "chat() calls self._log_call() after every completion"),
        ]),
        sp(8),

        h("4.3  backend/app/api/settings.py  (NEW FILE)", 2),
        p("New Flask Blueprint registered at <font name='Courier'>/api/settings</font>. Provides "
          "full runtime control over the LLM configuration and exposes the global call log:"),
        sp(4),
        endpoint_table([
            ("GET",    "/api/settings",              "Current model, base_url, override flags"),
            ("GET",    "/api/settings/models",       "Live model list from Ollama (/api/tags). Optional ?url= param to probe a different server without saving"),
            ("POST",   "/api/settings/model",        "Switch active model at runtime. Body: {model}"),
            ("DELETE", "/api/settings/model",        "Reset model to .env default"),
            ("POST",   "/api/settings/server",       "Switch Ollama server URL. Probes server, returns live model list"),
            ("DELETE", "/api/settings/server",       "Revert server URL to .env default"),
            ("GET",    "/api/settings/llm-calls",    "Global LLM transparency log (newest-first, ?limit=N, ?tag=X)"),
        ]),
        sp(8),

        h("4.4  backend/app/api/simulation.py  (MODIFIED)", 2),
        p("Six new endpoints appended to the existing simulation blueprint. These power the "
          "pause/resume, agent rearrangement, event injection, ontology, and per-simulation "
          "LLM call log features:"),
        sp(4),
        endpoint_table([
            ("GET",  "/<id>/ontology",       "Read entity types + edge types from Neo4j storage"),
            ("POST", "/pause",               "Stop simulation subprocess, set status=PAUSED"),
            ("PUT",  "/<id>/agents",         "Patch agent configs and reorder in simulation_config.json"),
            ("POST", "/resume",              "Mark simulation READY, restart subprocess"),
            ("POST", "/<id>/inject-event",   "Prepend a post/event to event_config.initial_posts"),
            ("GET",  "/<id>/llm-calls",      "Stream last N entries from llm_calls.jsonl for this simulation"),
        ]),
        sp(12),
    ]

    # ── 4. Frontend Changes ───────────────────────────────────────────────────
    story += [
        h("5. Frontend Changes"),
        hr(BLUE, 1),

        h("5.1  frontend/src/api/settings.js  (NEW FILE)", 2),
        p("Thin Axios wrapper functions for every new backend endpoint:"),
        sp(4),
        Preformatted(
            "getSettings()                           → GET /api/settings\n"
            "listModels(url?)                        → GET /api/settings/models\n"
            "setModel(model)                         → POST /api/settings/model\n"
            "resetModel()                            → DELETE /api/settings/model\n"
            "setServer(url)                          → POST /api/settings/server\n"
            "resetServer()                           → DELETE /api/settings/server\n"
            "getSimulationOntology(simId)            → GET /api/simulation/:id/ontology\n"
            "pauseSimulation(simId)                  → POST /api/simulation/pause\n"
            "resumeSimulation(simId, opts)           → POST /api/simulation/resume\n"
            "updateAgentConfigs(simId, agents, order)→ PUT /api/simulation/:id/agents\n"
            "injectEvent(simId, content, author)     → POST /api/simulation/:id/inject-event\n"
            "getSimulationLlmCalls(simId, limit)     → GET /api/simulation/:id/llm-calls",
            code_style),
        sp(8),

        h("5.2  frontend/src/components/ModelChooser.vue  (NEW FILE)", 2),
        p("A compact dropdown button added to the app header. Shows the current model name and "
          "a green/red health dot indicating whether the Ollama server is reachable."),
        sp(4),
        b("Clicking the button opens a popover with a server URL input field."),
        b("Hitting <i>Connect</i> calls <font name='Courier'>POST /api/settings/server</font>, "
          "probes the server, and loads the live model list."),
        b("All 59 remote models are shown in a scrollable list; clicking one calls "
          "<font name='Courier'>POST /api/settings/model</font>."),
        b("A custom model name text field allows typing any model name directly."),
        b("State is synced from <font name='Courier'>GET /api/settings</font> on open."),
        sp(8),

        h("5.3  frontend/src/views/MainView.vue  (MODIFIED)", 2),
        p("One-line change — <font name='Courier'>&lt;ModelChooser /&gt;</font> imported and "
          "placed in the <font name='Courier'>header-right</font> slot."),
        sp(4),
        diff_table([
            ("ADD", "", "import ModelChooser from '../components/ModelChooser.vue'"),
            ("ADD", "", "<ModelChooser />  <!-- in header-right div -->"),
        ]),
        sp(8),

        h("5.4  frontend/src/components/Step3Simulation.vue  (MODIFIED)", 2),
        p("The simulation view received the largest frontend change. Four new interactive "
          "capabilities were wired into the existing control bar:"),
        sp(6),

        h("Pause &amp; Rearrange", 3),
        b("A <i>Pause &amp; Rearrange</i> button calls <font name='Courier'>POST /api/simulation/pause</font> "
          "and opens a full-screen overlay modal."),
        b("The overlay lists every agent with influence (slider) and activity (slider) controls "
          "and up/down arrow buttons to reorder the agent execution sequence."),
        b("An <i>Inject Event</i> row lets the user type a message that gets prepended to the "
          "simulation's event queue immediately."),
        b("<i>Save &amp; Resume</i> calls <font name='Courier'>PUT /api/simulation/:id/agents</font> "
          "to persist the new config, then <font name='Courier'>POST /api/simulation/resume</font> "
          "to restart the subprocess."),
        sp(4),

        h("Bag Ontology Panel", 3),
        b("Antenna-icon button toggles a right-side panel."),
        b("Panel calls <font name='Courier'>GET /api/simulation/:id/ontology</font> and renders "
          "entity types (nodes) and edge types (relationships) from the Neo4j knowledge graph."),
        b("Entity types shown as teal badges; edge types shown as amber badges."),
        sp(4),

        h("LLM Call Log Panel", 3),
        b("Chat-bubble-icon button toggles a right-side panel that auto-polls every 5 s."),
        b("Each entry shows model name, tag, elapsed time, and a one-line preview."),
        b("Clicking an entry expands the full prompt messages and model response inline."),
        b("Calls <font name='Courier'>GET /api/simulation/:id/llm-calls</font> for per-simulation "
          "history."),
        sp(12),

        h("5.5  frontend/vite.config.js  (MODIFIED)", 2),
        p("Proxy target updated from the old port to the new one:"),
        sp(4),
        diff_table([
            ("MOD", "target: 'http://localhost:5001'",
                    "target: 'http://localhost:5010'"),
        ]),
        sp(8),

        h("5.6  frontend/src/api/index.js  (MODIFIED) — Network Fix", 2),
        p("The original code hard-coded <font name='Courier'>http://localhost:5001</font> as the "
          "Axios base URL. When the app is opened from another machine (e.g. "
          "<font name='Courier'>http://172.25.2.181:3010</font>), the browser tries to reach "
          "<font name='Courier'>localhost:5001</font> on the <i>user's</i> machine — which fails."),
        sp(4),
        p("Fix: base URL set to an empty string so all <font name='Courier'>/api/*</font> requests "
          "are relative to the page origin. Vite's dev-server proxy intercepts them and forwards "
          "to the backend on <font name='Courier'>localhost:5010</font> server-side:"),
        sp(4),
        diff_table([
            ("MOD", "baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'",
                    "baseURL: ''  // relative — Vite proxies /api/* → :5010"),
        ]),
        sp(12),
    ]

    # ── 5. Running the App ─────────────────────────────────────────────────────
    story += [
        h("6. How to Run"),
        hr(BLUE, 1),
        p("All services run bare-metal (no Docker rebuild needed). Neo4j runs in a "
          "single Docker container."),
        sp(4),
        Preformatted(
            "# 1. Start Neo4j\n"
            "docker run -d --name mirofish-neo4j \\\n"
            "  -p 7474:7474 -p 7687:7687 \\\n"
            "  -e NEO4J_AUTH=neo4j/mirofish \\\n"
            "  neo4j:5.18-community\n\n"
            "# 2. Start Flask backend (from repo root)\n"
            "python3 backend/run.py          # reads .env → port 5010\n\n"
            "# 3. Start Vue frontend (from frontend/)\n"
            "npm install && npm run dev -- --port 3010 --host 0.0.0.0\n\n"
            "# App:     http://<host>:3010\n"
            "# API:     http://<host>:5010\n"
            "# Neo4j:   http://<host>:7474",
            code_style),
        sp(12),
    ]

    # ── 6. Architecture Diagram (text) ─────────────────────────────────────────
    story += [
        h("7. Architecture Overview"),
        hr(BLUE, 1),
        Preformatted(
            "  Browser  ──────────────────────────────────────────────────────\n"
            "    │  http://<host>:3010   (Vue 3 + Vite)\n"
            "    │\n"
            "    │  /api/*  ──── Vite proxy ──▶  Flask :5010\n"
            "    │                                    │\n"
            "    │                            ┌───────┴────────┐\n"
            "    │                            │                │\n"
            "    │                       Neo4j :7687    Ollama :11434\n"
            "    │                    (localhost)    (172.25.1.70)\n"
            "    │\n"
            "    └── ModelChooser  ──── GET /api/settings/models ──▶ Ollama /api/tags\n"
            "    └── Simulation view ── LLM log, ontology, pause/resume, inject",
            code_style),
        sp(12),
    ]

    # ── footer note ────────────────────────────────────────────────────────────
    story += [
        hr(NAVY, 1),
        p(f"MiroFish-Offline Change Report · Generated {datetime.now().strftime('%d %B %Y')} · "
          "hariharan.m@mu-sigma.com", note_style),
    ]

    doc.build(story)
    print(f"PDF written → {OUT}")


if __name__ == "__main__":
    build()
