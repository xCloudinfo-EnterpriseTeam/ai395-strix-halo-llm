# 使用者操作流程圖產生器（定稿範本：x360 巡檢平台）。改節點與箭頭即可，樣式與字級不要動。
# 用法：python3 user_flow.py  → 產出 out.svg / out.png（zoom=3）
import sys; sys.path.insert(0, "/Users/jeff/.claude/skills/arch-diagram-style")
from arch_diagram import Diagram, BLUE, GREEN, VIOLET, ORANGE, CYAN
from msicons import ms_icon

W, H = 1400, 780
d = Diagram(width=W, height=H)
RED = "#bf181f"; INK = "#16202a"; GR = "#64748b"
BLUEC, GREENC, VIOC, ORC = "#2563eb", "#059669", "#7c3aed", "#ea580c"
T, N, S, A = 25, 20, 18, 20      # 標題／名稱／小字／箭頭字（簡報用，比網頁版大一級）

def node(x, y, icon, color, title, name, size=80, lines=()):
    d.parts.append(ms_icon(icon, x - size / 2, y - size / 2, size, color))
    if title: d.text(x, y - size / 2 - 14, title, size=T, fill=RED, bold=True, anchor="middle")
    if name: d.text(x, y + size / 2 + 26, name, size=N, fill=INK, bold=True, anchor="middle")
    for i, ln in enumerate(lines): d.text(x, y + size / 2 + 50 + i * 21, ln, size=S, fill=GR, anchor="middle")

def arrow(path, color, label="", lx=0, ly=0, anchor="middle"):
    hue = {BLUEC: BLUE, GREENC: GREEN, VIOC: VIOLET, ORC: ORANGE}[color]
    d.arrow(0, 0, 0, 0, hue, path=path)
    for i, ln in enumerate(label.split("\n") if label else []):
        d.text(lx, ly + i * (A + 4), ln, size=A, fill=INK, bold=True, anchor=anchor)

def dashed_box(x, y, w, h, label):
    d.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="10 6"/>')
    d.text(x + w - 14, y + h - 14, label, size=T, fill=RED, bold=True, anchor="end")

# 左：資料源 → 後台 → 平台

# ── set up once (bottom left) ───────────────────────────────────────────────
node(170, 430, "Cluster server", GREENC, "The engine", "built from source",
     lines=("one make command",))
arrow("M236 430 H 668", GREENC, "2. compiled for this chip", 440, 412)

node(170, 640, "Internet", GREENC, "Model weights", "open, MIT licensed",
     lines=("81 GB, one file",))
arrow("M236 640 H 678 V 496", GREENC, "3. downloaded once", 440, 622)

dashed_box(58, 352, 380, 368, "set up once")

# ── the box (centre); all of its text sits below it, where nothing else is ──
node(740, 430, "Server (generic)", VIOC, "", "", size=100)
d.text(740, 560, "Your desktop box", size=T, fill=RED, bold=True, anchor="middle")
d.text(740, 590, "Ryzen AI Max+ 395", size=N, fill=INK, bold=True, anchor="middle")

# ── you (top) ───────────────────────────────────────────────────────────────
node(440, 140, "User", BLUEC, "You", "at your desk", size=72)
arrow("M482 140 H 726", BLUEC, "1. pick a size\nthat fits", 604, 96)
node(780, 140, "Monitor", BLUEC, "Chat page", "in the browser", size=72)
arrow("M722 212 V 376", BLUEC, "4. you ask", 704, 300, anchor="end")
arrow("M770 376 V 212", BLUEC, "5. words stream back", 788, 300, anchor="start")

dashed_box(390, 70, 470, 212, "you, at the keyboard")

# ── anything else that calls it (right) ─────────────────────────────────────
node(1180, 140, "Application server", ORC, "Your own app", "same endpoint", size=72)
arrow("M812 398 H 1040 V 140 H 1136", ORC, "6. one ordinary chat endpoint", 926, 382)
node(1180, 660, "Workstation client", ORC, "Coding tools", "editor plug-ins", size=72)
arrow("M812 470 H 1040 V 660 H 1136", ORC, "7. or any tool that speaks it", 926, 454)

d.text(58, 756, "Steps 2 and 3 happen once. After that the box answers at "
                "13 to 41 words a second, and nothing leaves the machine.",
       size=N, fill=INK, bold=True)
d.save(sys.argv[1] if len(sys.argv) > 1 else "flow.svg")
