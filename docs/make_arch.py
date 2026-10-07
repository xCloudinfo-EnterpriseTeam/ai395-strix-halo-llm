import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/xcloud-visio-diagram"))
from vdiagram import *

W, H = 1600, 1118
p = head("Big models on one desktop box",
         "What you can run on a Ryzen AI Max+ 395, and how fast it answers")
X, R = 50, 1420
x0, cw, gap = 290, 266, 15

# 1 what you do with it  (the only solid band)
y = 150
p.append(rect(X, y, R - X, 170, SOLID, 18))
p += [t(X + 30, y + 78, "What you get", 24, "#FFFFFF", 700),
      t(X + 30, y + 110, "all of it offline", 17, "#D5E3F3")]
items = [("doc", "Chat"), ("chip", "Coding"),
         ("search", "Long docs"), ("cube", "Your apps"),
         ("shield", "Stays local"), ("plug", "Desk sized")]
icw, igap = 172, 15.6
for i, (ic, lab) in enumerate(items):
    cx = x0 + i * (icw + igap)
    p.append(rect(cx, y + 20, icw, 130, "#2B6CB5", 12))
    p.append(icon(ic, cx + icw / 2 - 20, y + 38, 40))
    p.append(t(cx + icw / 2, y + 122, lab, 18, "#FFFFFF", 700, "middle"))

# 2 how fast  (core layer, the headline)
y = 336
p.append(rect(X, y, R - X, 250, CORE, 18))
p += [t(X + 30, y + 46, "How fast", 24, NAVY, 700),
      t(X + 30, y + 76, "measured on one box,", 17, BODY),
      t(X + 30, y + 102, "nothing else running", 17, BODY)]
p.append(rect(X + 30, y + 176, 196, 44, RED, 22))
p.append(t(X + 128, y + 205, "Faster than you read", 18, "#FFFFFF", 700, "middle"))
cards = [("Writes answers", ["39 to 41 words a second", "on the 125B model"]),
         ("Reads your prompt", ["343 to 367 a second", "a long brief in 20 s"]),
         ("Holds the thread", ["32,000 words of context", "speed stays flat"]),
         ("Ready to talk", ["80 seconds from cold", "18 s for the other model"])]
for i, (tt, ls) in enumerate(cards):
    cx = x0 + i * (cw + gap)
    p.append(rect(cx, y + 26, cw, 128, "#FFFFFF", 12, LINE))
    p.append(t(cx + 22, y + 64, tt, 21, LABEL, 700))
    for k, l in enumerate(ls):
        p.append(t(cx + 22, y + 98 + k * 28, l, 17))
pills = ["No subscription", "No per-token bill", "Works with no internet", "You own the weights"]
px = x0
for pl in pills:
    w = len(pl) * 11 + 44
    p.append(rect(px, y + 176, w, 44, "#FFFFFF", 22, "#8FA3B8"))
    p.append(t(px + w / 2, y + 205, pl, 18, NAVY, 700, "middle"))
    px += w + 14

# 3 which models
y = 602
p.append(rect(X, y, R - X, 250, PALE, 18))
p += [t(X + 30, y + 46, "What runs", 24, NAVY, 700),
      t(X + 30, y + 76, "both are open weights", 17, BODY)]
p.append(rect(X + 30, y + 196, 196, 40, RED, 20))
p.append(t(X + 128, y + 223, "Two engines tested", 18, "#FFFFFF", 700, "middle"))
srcs = [("cube", "The bigger one", "284 billion parameters",
         ["13.5 to 15.4 a second", "steady to 32,000 words"]),
        ("chip", "The faster one", "125 billion parameters",
         ["39 to 41 a second", "best for everyday work"]),
        ("doc", "Both fit", "81 and 88 gigabytes",
         ["shrunk to 2 to 4 bits", "quality kept where it counts"]),
        ("shield", "Picture reading", "available, not measured",
         ["vision builds exist", "we only tested text"])]
for i, (ic, tt, sub, ls) in enumerate(srcs):
    cx = x0 + i * (cw + gap)
    p.append(rect(cx, y + 26, cw, 198, "#FFFFFF", 12, LINE))
    p.append(icon(ic, cx + cw - 56, y + 42, 34, LABEL))
    p.append(t(cx + 22, y + 66, tt, 21, LABEL, 700))
    p.append(t(cx + 22, y + 94, sub, 16, MUTED))
    for k, l in enumerate(ls):
        p.append(rect(cx + 18, y + 112 + k * 50, cw - 36, 40, "#EEF3F9", 8))
        p.append(t(cx + cw / 2, y + 138 + k * 50, l, 17, BODY, 400, "middle"))

# 4 the box
y = 868
p.append(rect(X, y, R - X, 200, PALE2, 18))
p += [t(X + 30, y + 46, "The box", 24, NAVY, 700),
      t(X + 30, y + 76, "one you can own", 17, BODY)]
sites = [("chip", "Ryzen AI Max+", "the 395, Radeon 8060S"),
         ("cube", "128 GB", "shared with graphics"),
         ("plug", "Desktop", "no rack, no server room"),
         ("shield", "Linux", "stock packages")]
for i, (ic, tt, sub) in enumerate(sites):
    cx = x0 + i * (cw + gap)
    p.append(rect(cx, y + 26, cw, 112, "#FFFFFF", 12, LINE))
    p.append(icon(ic, cx + 20, y + 44, 38, LABEL))
    p.append(t(cx + 72, y + 70, tt, 21, NAVY, 700))
    p.append(t(cx + 72, y + 104, sub, 16, BODY))
p.append(t(x0, y + 172,
           "Figures are medians from the engines' own benchmarks on this machine; see the tables in the README",
           16, MUTED))

p += vcol(1440, 150, 112, 918, [["U", "S", "E"], ["F", "A", "S", "T"],
                               ["R", "U", "N", "S"], ["B", "O", "X"]])
p.append(t(50, H - 22,
           "xCloudinfo Corp. Limited（云碩科技）　　October 2026　　"
           "Published under CC BY 4.0　　github.com/xCloudinfo-EnterpriseTeam/ai395-strix-halo-llm",
           15, "#9AA7B4"))
save(sys.argv[1], W, H, p)
