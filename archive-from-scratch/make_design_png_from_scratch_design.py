from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import math, sys

OUT_DESIGN = sys.argv[1]
OUT_MAP = sys.argv[2]
W, M = 2000, 80
CW = W - 2 * M
FD = 'C:/Windows/Fonts/'


def F(size, bold=False, italic=False):
    name = 'segoeuiz.ttf' if (bold and italic) else 'segoeuib.ttf' if bold else 'segoeuii.ttf' if italic else 'segoeui.ttf'
    return ImageFont.truetype(FD + name, size)


BG = (250, 250, 247); INK = (31, 31, 30); MUTED = (95, 94, 90); LINE = (211, 209, 199)
PUR_F = (238, 237, 254); PUR_B = (83, 74, 183); PUR_T = (60, 52, 137)
GRY_F = (241, 239, 232); GRY_B = (136, 135, 128); GRY_T = (68, 68, 65)
TEA_F = (225, 245, 238); TEA_B = (15, 110, 86); TEA_T = (8, 80, 65)
COR_F = (250, 236, 231); COR_B = (153, 60, 29); COR_T = (113, 43, 19)
AMB_F = (250, 238, 218); AMB_B = (133, 79, 11); AMB_T = (99, 56, 6)
WHITE = (255, 255, 255)

img = Image.new('RGB', (W, 18000), BG)
d = ImageDraw.Draw(img)


def new_canvas(h):
    global img, d
    img = Image.new('RGB', (W, h), BG)
    d = ImageDraw.Draw(img)


def wrap(s, font, maxw):
    lines = []
    for para in s.split('\n'):
        cur = ''
        for w in para.split(' '):
            t = (cur + ' ' + w).strip()
            if font.getlength(t) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def lh(font, k=1.38):
    return int(font.size * k)


def para_h(s, font, maxw):
    return len(wrap(s, font, maxw)) * lh(font)


def para(x, y, s, font, fill, maxw):
    for ln in wrap(s, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh(font)
    return y


def rbox(x, y, w, h, fill, outline, r=18, width=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)


def arrow(x1, y1, x2, y2, color=MUTED, width=5, head=24):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        a = ang + math.pi + s * 0.5
        d.line([x2, y2, x2 + head * math.cos(a), y2 + head * math.sin(a)], fill=color, width=width)


def badge(x, y, s, fill, ink, font):
    w = int(font.getlength(s)) + 36
    h = font.size + 18
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    d.text((x + 18, y + 7), s, font=font, fill=ink)
    return w, h


def section_head(y, n, title, sub=None):
    d.ellipse([M, y, M + 76, y + 76], fill=PUR_B)
    d.text((M + 38, y + 38), str(n), font=F(44, True), fill=WHITE, anchor='mm')
    d.text((M + 104, y - 2), title, font=F(54, True), fill=INK)
    yy = y + 70
    if sub:
        d.text((M + 104, yy - 6), sub, font=F(30), fill=MUTED)
        yy += 36
    d.line([M, yy + 14, W - M, yy + 14], fill=LINE, width=3)
    return yy + 50


def card(x, y, w, title, items, tone, numbered=True, body=F(28), pad=34):
    fill, border, ink = tone
    tf = F(34, True)
    inner = w - 2 * pad
    ind = 62 if numbered else 34
    h = pad + lh(tf, 1.3) + 14
    for it in items:
        h += para_h(it, body, inner - ind) + 14
    h += pad - 14
    rbox(x, y, w, h, fill, border)
    d.text((x + pad, y + pad), title, font=tf, fill=ink)
    yy = y + pad + lh(tf, 1.3) + 14
    for i, it in enumerate(items, 1):
        if numbered:
            d.ellipse([x + pad, yy + 2, x + pad + 40, yy + 42], fill=border)
            d.text((x + pad + 20, yy + 22), str(i), font=F(25, True), fill=WHITE, anchor='mm')
        else:
            d.ellipse([x + pad + 4, yy + 12, x + pad + 18, yy + 26], fill=border)
        yy = para(x + pad + ind, yy, it, body, INK, inner - ind) + 14
    return h


def table(x, y, colw, headers, rows, hfill=PUR_F, hink=PUR_T, bodyf=F(26), tech_col=None, center_cols=()):
    pad = 18
    hf = F(26, True)
    hh = lh(hf) + 2 * pad - 6
    tw = sum(colw)
    d.rounded_rectangle([x, y, x + tw, y + hh], radius=12, fill=hfill)
    cx = x
    for ci, (cw, hd) in enumerate(zip(colw, headers)):
        if ci in center_cols:
            d.text((cx + cw // 2, y + pad - 3), hd, font=hf, fill=hink, anchor='ma')
        else:
            d.text((cx + pad, y + pad - 3), hd, font=hf, fill=hink)
        cx += cw
    yy = y + hh
    for ri, r in enumerate(rows):
        fonts = []
        for ci in range(len(r)):
            fonts.append(F(26, True) if (ci == 0 or ci == tech_col) else bodyf)
        rh = max(para_h(c, f, cw - 2 * pad) for c, f, cw in zip(r, fonts, colw)) + 2 * pad - 6
        if ri % 2 == 0:
            d.rectangle([x, yy, x + tw, yy + rh], fill=WHITE)
        cx = x
        for ci, (c, f, cw) in enumerate(zip(r, fonts, colw)):
            col = PUR_T if ci == tech_col else INK
            if ci in center_cols:
                d.text((cx + cw // 2, yy + pad - 3), c, font=f, fill=col, anchor='ma')
            else:
                para(cx + pad, yy + pad - 3, c, f, col, cw - 2 * pad)
            cx += cw
        yy += rh
    d.rounded_rectangle([x, y, x + tw, yy], radius=12, outline=LINE, width=3)
    return yy


# ====================================================================== DATA: the complete map
GROUPS = [
    ('A. What customers touch', [
        ('Command tool "mall"', 'CLI', 'BUILD', 'login, push, list, logs, delete, rollback'),
        ("Counter's open door", 'HTTP API', 'BUILD', 'the CLI and the dashboard both talk to it'),
        ('Charts page', 'Web dashboard', 'BASIC', 'bill, status and logs on one simple page'),
        ('Customer accounts', 'Tenants and accounts', 'BASIC', 'created by you, by hand. No sign-up page.'),
        ('App settings', 'Environment variables', 'BASIC', 'plain-text settings such as a port or a mode'),
        ('Teams and roles', 'Roles (RBAC)', 'LATER', 'several people per customer, with different rights'),
        ('Sign-up page and email', 'Self-service sign-up', 'LATER', 'needs email sending and abuse checks'),
        ('Secret settings', 'Secrets management', 'LATER', 'encrypted storage for passwords and keys'),
        ('Own web address', 'Custom domains', 'LATER', 'needs a real, paid domain name'),
        ('Ready-made database', 'Managed database add-on', 'LATER', 'file storage (part 3) comes first'),
        ('Scheduled jobs', 'Cron jobs', 'LATER', 'run an app every night, for example'),
        ('Background workers', 'Worker processes', 'LATER', 'apps that do not answer visitors'),
    ]),
    ('B. The Manager (the brain)', [
        ('Brain', 'Control plane', 'BUILD', 'keeps what runs equal to what should run'),
        ("Manager's notebook", 'State store (SQLite)', 'BASIC', 'remembers customers, apps and addresses'),
        ('Choosing a Floor', 'Scheduling', 'BUILD', 'simple rule: the least busy Floor wins'),
        ('Restart a crashed flat', 'Self-healing', 'BUILD', 'needs the health checks'),
        ('Move flats off a dead Floor', 'Failover', 'BUILD', 'needs the Floor heartbeats'),
        ('Version history', 'Releases', 'BASIC', 'v1, v2, v3 and go back'),
        ('Grow and shrink', 'Autoscaling', 'BASIC', 'based on visitors per second'),
        ('Limits per customer', 'Tenant quotas', 'BASIC', 'maximum apps and maximum total power'),
        ('Cleanup', 'Deletion and garbage collection', 'BASIC', 'remove an app and free everything it used'),
        ('Sleep when idle', 'Scale to zero', 'LATER', 'wake up on the first visitor'),
        ('Slow, safe updates', 'Canary deployment + rollback', 'LATER', 'version history and traffic count prepare it'),
        ('Several Managers', 'High availability', 'LATER', 'removes the single point of failure'),
        ('Notebook backups', 'State backups', 'LATER', 'copy the notebook somewhere safe'),
        ('Upgrading the platform', 'Rolling upgrade', 'LATER', 'update parts without downtime'),
    ]),
    ('C. The Floors (where flats run)', [
        ('Floor', 'Worker node', 'BUILD', '2 or 3 pretend Linux machines'),
        ('Floor caretaker', 'Node agent', 'BUILD', 'obeys the Manager'),
        ('Flat', 'Container runtime', 'BUILD', 'your Go program starts apps in locked rooms'),
        ('The five locks', 'Isolation', 'BUILD', 'namespaces, root swap, cgroups, network, capabilities'),
        ('Parcel shelf', 'Parcel store (registry)', 'BASIC', 'where parcels wait until a Floor fetches them'),
        ('Own parcel format', 'App bundle format', 'BASIC', 'becomes the standard OCI image if time runs short'),
        ('"Are you alive?" question', 'Health checks', 'BASIC', 'the Floor caretaker asks every few seconds and reports to the Manager'),
        ('Floor heartbeat', 'Node heartbeat', 'BASIC', 'tells the Manager a Floor is alive'),
        ('Empty a Floor for repair', 'Node drain', 'LATER', 'move its flats away gently first'),
        ('Build from source code', 'Build service (buildpacks)', 'LATER', 'in v1 customers hand in a ready program'),
        ('Heavy hardware', 'GPU scheduling', 'SKIP', 'no such hardware on your PC'),
    ]),
    ('D. Network and names', [
        ('Reception desk', 'Reverse proxy', 'BUILD', 'sends each visitor to the right flat'),
        ('Names like ahmed-shop.mall.hamza', 'DNS names', 'BASIC', 'a private, invented ending; the domain is one setting'),
        ('Spread visitors over copies', 'Load balancing', 'BASIC', 'simple round-robin'),
        ('Private phone lines', 'Virtual networks', 'BUILD', 'one private line per flat'),
        ('Floor-to-Floor lines', 'Cross-node networking', 'BUILD', 'visitors reach flats on any Floor'),
        ('Mall directory (your own DNS server)', 'DNS server', 'BASIC', 'answers for mall.hamza; names come from the Notebook'),
        ('Flats calling each other', 'Service discovery', 'LATER', 'in v1 flats cannot call each other'),
        ('Padlock (HTTPS)', 'TLS (HTTPS)', 'BASIC', 'one wildcard certificate; HTTPS on the Reception desk and the Counter'),
        ('Certificate office', 'Private certificate authority (CA)', 'BASIC', 'makes the certificates; your PC must trust it once'),
        ('Certificates renewed by themselves', 'Automatic renewal', 'LATER', 'in v1 certificates last long and are made by hand'),
        ('A real internet domain', 'Public domain and registrar records', 'LATER', 'costs money; the DNS server and certificates only need new settings'),
        ('Limit visitors per second', 'Rate limiting', 'LATER', 'protects apps from floods'),
        ('Limit outgoing calls', 'Egress policy', 'LATER', 'flats cannot call the internet freely'),
    ]),
    ('E. Storage and data', [
        ('Files that survive a restart', 'Persistent volumes', 'LATER', 'in v1 apps forget everything'),
        ('File storage service', 'Object store', 'PART 3', 'erasure coding and self-repair'),
        ('Databases', 'Managed databases', 'LATER', 'after storage works'),
        ('Backups for customers', 'Customer backups', 'LATER', 'needs storage first'),
    ]),
    ('F. Security', [
        ('ID check at the Counter', 'Authentication (hashed API tokens)', 'BASIC', 'tokens are never stored in plain text'),
        ('Who may touch what', 'Authorization (per-tenant permissions)', 'BASIC', "Ahmed cannot touch Sara's app"),
        ('Seal on the parcel', 'Parcel checksum', 'BASIC', 'a tampered parcel is refused'),
        ('Badge for caretakers', 'Node join token', 'BASIC', 'a fake Floor cannot join'),
        ('Logbook of who did what', 'Audit log', 'BASIC', 'every action is recorded'),
        ('Parts prove who they are', 'mTLS', 'LATER', 'parts identify themselves to each other'),
        ('Signed parcels', 'Signing', 'LATER', 'proof of who made a parcel'),
        ('Scan parcels for known holes', 'Vulnerability scanning', 'LATER', 'check parcels against known problems'),
        ('Refuse suspicious parcels', 'Admission policy', 'LATER', 'rules that reject dangerous requests'),
        ('Guard watching for attacks', 'SOC (detection and response)', 'PART 2', 'the security-guard part'),
    ]),
    ('G. Monitoring', [
        ('Health board', 'Metrics', 'BASIC', 'visitors, errors, slowness per app; CPU and memory per flat'),
        ('Complaints book', 'Logs per flat', 'BASIC', '"mall logs" shows what the app printed'),
        ('Status page', 'Status page', 'BASIC', 'green and red lights'),
        ("Platform's own health", 'Platform metrics', 'BASIC', 'the Manager and caretakers report too'),
        ('Alarm bells', 'Alerts', 'LATER', 'a message when something is wrong'),
        ('Follow one visit through every part', 'Tracing', 'LATER', 'find where a slow visit lost time'),
    ]),
    ('H. Billing', [
        ('Meter', 'Metering', 'BUILD', 'exact usage numbers, nothing lost in a crash'),
        ('Bill', 'Usage report', 'BUILD', 'totals per customer per month'),
        ('Price list', 'Pricing plan', 'BASIC', 'one simple price list'),
        ('Customer sees own usage', 'Usage view per tenant', 'LATER', '"mall usage" and a dashboard page'),
        ('Past bills kept', 'Invoice history', 'LATER', 'one stored bill per customer per month'),
        ('Free allowance', 'Free tier', 'LATER', 'some usage free each month'),
        ('Collecting real money', 'Payments (cards)', 'SKIP', 'needs a payment company and a card. The bill shows a total and "paid" is simulated.'),
    ]),
    ('I. Building and running the platform itself', [
        ('Proofs', 'Automated tests', 'BUILD', 'one command runs them all'),
        ('Docs and demo video', 'Documentation', 'BUILD', 'your portfolio'),
        ('Proofs run on every change', 'CI (GitHub Actions)', 'BASIC', 'free for public projects'),
        ('Fake crowd', 'Load tests', 'BASIC', 'drives the grow-and-shrink proof'),
        ('Break things on purpose', 'Chaos tests', 'BASIC', 'kill apps and Floors'),
        ('One-command install', 'Installer script', 'BASIC', 'set up the whole platform quickly'),
        ('Infrastructure as code', 'Terraform', 'LATER', 'create the Floors by script'),
        ('Many regions', 'Multi-region', 'SKIP', 'one PC, one place'),
    ]),
    ('J. Extra parts and ideas', [
        ('Telecom 5G app on the platform', 'Telco workload', 'PART 4', 'a showcase app running on your platform'),
        ('Many platforms joined together', 'Federation', 'LATER', 'place apps by cost, delay or carbon'),
        ('Tiny on-demand functions', 'Serverless', 'LATER', 'code that runs only when called'),
    ]),
]

STATUS = {
    'BUILD': (PUR_B, 'The core you build in version 1'),
    'BASIC': (TEA_B, 'A small version inside version 1'),
    'LATER': (GRY_B, 'Future work. The design leaves room for it.'),
    'PART 2': (AMB_B, 'A follow-up part, only after part 1 works'),
    'PART 3': (AMB_B, ''),
    'PART 4': (AMB_B, ''),
    'SKIP': (COR_B, 'Not realistic with zero budget and one PC'),
}


def pill(x, y, s, color):
    f = F(22, True)
    w = int(f.getlength(s)) + 30
    d.rounded_rectangle([x, y, x + w, y + 36], radius=18, fill=color)
    d.text((x + w // 2, y + 18), s, font=f, fill=WHITE, anchor='mm')
    return w


all_rows = [r for _, rs in GROUPS for r in rs]
cnt = Counter(r[2] for r in all_rows)
parts_n = cnt['PART 2'] + cnt['PART 3'] + cnt['PART 4']
TOTAL = len(all_rows)

# ====================================================================== PICTURE 1: the design
y = 70
d.text((M, y), 'Mini Cloud', font=F(86, True), fill=INK)
d.text((M + 4, y + 104), 'Design overview: a tiny cloud provider, built from scratch in Go', font=F(36), fill=MUTED)
bw, _ = badge(M, y + 170, 'DRAFT v6 for your review', COR_F, COR_T, F(28, True))
bw2, _ = badge(M + bw + 20, y + 170, 'Part 1 of 4: the platform (the mall)', PUR_F, PUR_T, F(28, True))
badge(M + bw + bw2 + 40, y + 170, 'Nothing is built yet', GRY_F, GRY_T, F(28, True))
y += 290

# ---------------------------------------------------------------- 1 big picture
y = section_head(y, 1, 'The big picture', 'Each box shows the mall word on top and the technical word below it, after the "=".')
S = 2.6
OX = 220
Y0 = y


def X(v):
    return int(OX + (v - 40) * S)


def Y(v):
    return int(Y0 + (v - 30) * S)


def node(x, yy, w, h, title, sub, tech, tone):
    fill, border, ink = tone
    rbox(X(x), Y(yy), int(w * S), int(h * S), fill, border, r=14, width=3)
    cx = X(x) + int(w * S) // 2
    d.text((cx, Y(yy) + 14), title, font=F(34, True), fill=ink, anchor='ma')
    d.text((cx, Y(yy) + 60), sub, font=F(26), fill=border, anchor='ma')
    d.text((cx, Y(yy) + 102), '= ' + tech, font=F(26, True, True), fill=ink, anchor='ma')


P = (PUR_F, PUR_B, PUR_T)
G = (GRY_F, GRY_B, GRY_T)

d.rounded_rectangle([X(40), Y(270), X(640), Y(396)], radius=18, outline=GRY_B, width=3)
d.text((X(40) + 24, Y(270) + 12), 'Floors = worker nodes (Linux machines only). Each has a caretaker program = node agent.', font=F(26, False, True), fill=MUTED)

node(40, 30, 150, 64, 'Ahmed', 'shop owner', 'tenant (customer)', G)
node(265, 30, 150, 64, 'Notebook', "the Manager's memory", 'state store', P)
node(490, 30, 150, 64, 'Visitor', "opens Ahmed's shop", 'end user (client)', G)
node(40, 146, 150, 64, 'Counter', "takes Ahmed's app", 'API server', P)
node(265, 146, 150, 64, 'Manager', 'the brain', 'control plane', P)
node(490, 146, 150, 64, 'Reception desk', 'guides visitors', 'reverse proxy', P)
node(70, 316, 150, 64, "Ahmed's flat", 'locked, own limit', 'container', P)
node(265, 316, 150, 64, "Sara's flat", 'locked, own limit', 'container', P)
node(460, 316, 150, 64, "Youssef's flat", 'locked, own limit', 'container', P)
node(40, 444, 150, 64, 'Parcel shelf', 'where parcels wait', 'parcel store', P)
node(245, 444, 190, 64, 'Meter', 'counts use, makes bill', 'metering service', P)
node(490, 444, 150, 64, 'Health board', 'shows what is wrong', 'monitoring', P)

arrow(X(115), Y(94), X(115), Y(146) - 4)
arrow(X(565), Y(94), X(565), Y(146) - 4)
arrow(X(190), Y(178), X(265) - 4, Y(178))
arrow(X(340), Y(210), X(340), Y(270) - 4)
arrow(X(565), Y(210), X(565), Y(270) - 4)
arrow(X(340), Y(146), X(340), Y(94) + 4)
arrow(X(340), Y(94), X(340), Y(146) - 4)
arrow(X(115), Y(444), X(115), Y(396) + 4)
arrow(X(340), Y(444), X(340), Y(396) + 4)
arrow(X(565), Y(444), X(565), Y(396) + 4)

cap = F(25)
d.text((X(115) + 18, Y(94) + 36), 'hands in his app (CLI, HTTPS)', font=cap, fill=MUTED)
d.text((X(565) - 18, Y(94) + 22), 'asks the directory (DNS) for', font=cap, fill=MUTED, anchor='ra')
d.text((X(565) - 18, Y(94) + 58), 'ahmed-shop.mall.hamza, then HTTPS', font=cap, fill=MUTED, anchor='ra')
d.text(((X(190) + X(265)) // 2, Y(178) - 38), 'passes it on', font=cap, fill=MUTED, anchor='ma')
d.text((X(340) - 18, Y(94) + 44), 'remembers', font=cap, fill=MUTED, anchor='ra')
d.text((X(340) + 18, Y(210) + 54), 'schedules a container', font=cap, fill=MUTED)
d.text((X(565) + 18, Y(210) + 54), 'forwards the request', font=cap, fill=MUTED)
d.text((X(115) + 18, Y(396) + 36), 'supplies parcels', font=cap, fill=MUTED)
d.text((X(340) + 18, Y(396) + 36), 'reads usage counters', font=cap, fill=MUTED)
d.text((X(565) - 18, Y(396) + 36), 'reads health and logs', font=cap, fill=MUTED, anchor='ra')

# security bar
sy = Y(444) + int(64 * S) + 50
rbox(X(40), sy, int(600 * S), 150, COR_F, COR_B, r=14, width=3)
d.text((X(40) + 30, sy + 20), 'Security basics guard every arrow above', font=F(32, True), fill=COR_T)
d.text((X(40) + 30, sy + 74), 'API tokens, per-customer permissions, parcel checksum, caretaker join token, audit log', font=F(28), fill=COR_T)
sy2 = sy + 150 + 30
rbox(X(40), sy2, int(600 * S), 150, TEA_F, TEA_B, r=14, width=3)
d.text((X(40) + 30, sy2 + 20), 'Names and padlock', font=F(32, True), fill=TEA_T)
d.text((X(40) + 30, sy2 + 74), 'Your own DNS server answers for mall.hamza. Your own certificate office makes the HTTPS certificates.', font=F(28), fill=TEA_T)
y = sy2 + 150 + 100

# ---------------------------------------------------------------- 2 dictionary
y = section_head(y, 2, 'The dictionary: mall word to technical word', 'Learn the middle column. Those are the words used in jobs and interviews.')
DW = [330, 470, CW - 800]


def subhead(yy, s):
    d.text((M, yy), s, font=F(36, True), fill=INK)
    return yy + 58


y = subhead(y, 'Who and what')
y = table(M, y, DW, ['Mall word', 'Technical word', 'What it is in your project'], [
    ['The mall', 'PaaS (Platform as a Service)', 'The whole thing you build. Real examples: Heroku, Google Cloud Run.'],
    ['Ahmed', 'Tenant (a customer)', 'Anyone who runs apps on your platform. Each tenant has an account.'],
    ["Ahmed's shop", 'Workload (application)', 'The program a customer wants to run. Here: a small web service.'],
    ['Visitor', 'End user (client)', "A person or program sending requests to the customer's app."],
    ['Parcel', 'App bundle (image)', 'A sealed file: the app plus its manifest. It sits on the shelf and never runs. Your own format; the standard one is called an OCI image.'],
    ['Note inside the parcel', 'Manifest', 'Start command, how much CPU and memory, which network port.'],
], tech_col=1) + 46

y = subhead(y, 'Parcel versus flat: two different things')
y = table(M, y, [330, 755, CW - 1085], ['', 'Parcel (image)', 'Flat (container)'], [
    ['What it is', 'A sealed file: the app plus its note (manifest)', 'A running, locked room with the app alive inside'],
    ['Where it lives', "On Ahmed's PC, then on the parcel shelf", 'On a Floor'],
    ['Does it run?', 'No. It just sits there.', 'Yes.'],
    ['Can it change?', 'No. Fixed once packed.', 'It starts, crashes, restarts and is thrown away.'],
    ['How many?', 'One per version of the app', 'Many: one per copy of the app'],
    ['Life of one app', '"mall push" packs it, then it waits on the shelf', 'A Floor caretaker builds it from the parcel. A crashed flat is replaced by a fresh one from the same parcel.'],
]) + 46

y = subhead(y, 'The parts you build')
y = table(M, y, DW, ['Mall word', 'Technical word', 'What it is in your project'], [
    ['Counter', 'API server', 'The front door for customers. Accepts commands over HTTP and checks who is calling. Plus the command-line tool "mall push".'],
    ['Secret key', 'API token', 'Proves who is calling, so the Counter can tell Ahmed from Sara.'],
    ['Manager', 'Control plane', 'The brain. Remembers what should be running and keeps reality equal to it. Real example: the Kubernetes control plane.'],
    ["Manager's notebook", 'State store', 'A small database file. Without it, a restart makes the Manager forget everything.'],
    ["Manager's choice of Floor", 'Scheduling', 'Picking which worker node has room for a new flat.'],
    ['Floor', 'Worker node', 'A Linux machine that runs flats. You use 2 or 3 pretend ones on your PC.'],
    ['Floor caretaker', 'Node agent', 'A small program on each Floor that obeys the Manager: builds, stops and restarts flats. Real example: kubelet.'],
    ['Flat', 'Container', 'The running, locked room built from a parcel. Not the same thing as the parcel. An ordinary Linux process wrapped in locks (namespaces, cgroups). Docker does the same thing.'],
    ['Electricity limit', 'Resource limits (quotas)', 'CPU and memory caps, enforced by the Linux feature called cgroups.'],
    ['Parcel shelf', 'Parcel store (registry)', 'A folder where parcels wait until a Floor fetches them.'],
    ['Reception desk', 'Reverse proxy (router)', 'Receives visitor requests and forwards each to the right flat. Real examples: Nginx, Traefik.'],
    ['Spreading visitors', 'Load balancing', 'When an app has several copies, the Reception desk shares visitors between them.'],
    ['Mall directory', 'DNS server (Domain Name System)', 'Turns a name into a door number. You build a small DNS server for your own domain, mall.hamza. New apps get their name automatically from the Notebook.'],
    ['Address "ahmed-shop"', 'DNS name and route', 'A name such as ahmed-shop.mall.hamza that leads to the Reception desk, which then finds the flat.'],
    ['Padlock', 'HTTPS (TLS)', 'The browser shows a padlock when the connection is encrypted and the certificate is trusted.'],
    ['Certificate', 'TLS certificate (wildcard)', 'An ID card for a name. One wildcard certificate covers every *.mall.hamza name.'],
    ['Certificate office', 'Private certificate authority (CA)', 'Your own small office that signs the certificates. Your PC must be told once to trust it.'],
    ['"Are you alive?"', 'Health check', 'The Manager asks each flat every few seconds. No answer means restart.'],
    ['Meter', 'Metering service', 'Reads CPU and memory counters every few seconds and stores exact numbers for the bill.'],
    ['Health board', 'Monitoring', 'Visitors, errors, slowness, logs and a status page. Fast and approximate, unlike the Meter.'],
    ['Bill and charts page', 'Billing report and dashboard', 'Totals per customer, plus a web page that draws them.'],
], tech_col=1) + 46

y = subhead(y, 'The extras')
y = table(M, y, DW, ['Mall word', 'Technical word', 'What it is in your project'], [
    ['Customers kept separate', 'Multi-tenancy', 'Isolation (locks) plus quotas (limits) so one customer cannot harm another.'],
    ['Restarts a crashed flat', 'Self-healing', 'The Manager compares "wanted" with "actual" and fixes the gap. The pattern is called a reconciliation loop.'],
    ['Moves flats off a dead Floor', 'Failover (rescheduling)', 'When a worker node dies, its containers start again on another node.'],
    ['Grow and shrink', 'Autoscaling', 'Adds or removes copies (replicas) of an app as traffic changes.'],
    ['Careful updates', 'Canary deployment + rollback', 'FUTURE. New version gets 5% of traffic first; automatic return if errors rise.'],
], tech_col=1) + 90

# ---------------------------------------------------------------- 3 step by step
y = section_head(y, 3, 'What happens, step by step', 'Technical words in brackets.')
colw = (CW - 40) // 2
hA = card(M, y, colw, 'A. Ahmed hands in his app (a "deploy")', [
    'Ahmed types one command, for example "mall push" (a CLI command). It packs his app into a parcel (app bundle, an "image") with a small note (manifest).',
    'The Counter (API server) checks his secret key (API token), checks he may deploy here (permissions), checks the parcel seal (checksum), and writes the action in the logbook (audit log).',
    'The parcel goes on the Parcel shelf (parcel store). The Manager (control plane) writes "Ahmed\'s shop, version 1, should run" in its Notebook (state store).',
    'The Manager finds a Floor (worker node) with free room (scheduling).',
    "That Floor's caretaker (node agent) fetches the parcel, checks the seal again, and builds a locked flat (container) from it, with a power limit. The parcel itself never runs.",
    'The Manager tells the Reception desk (reverse proxy): "the name ahmed-shop.mall.hamza goes to this flat". The mall directory (DNS server) learns the new name from the Notebook.',
    'From then on, the Manager asks the flat "are you alive?" every few seconds (health check).',
], (PUR_F, PUR_B, PUR_T))
x2 = M + colw + 40
h1 = card(x2, y, colw, 'B. A visitor opens the shop (a "request")', [
    'The visitor types "https://ahmed-shop.mall.hamza". The mall directory (DNS server) says where the Reception desk is, and the padlock (HTTPS) is set up with the certificate.',
    'The Reception desk (reverse proxy) picks one of the shop\'s copies (load balancing) and forwards the request.',
    'The shop page (the response) comes back. The Reception desk counts the visit and any error (request metrics).',
], (TEA_F, TEA_B, TEA_T))
h2 = card(x2, y + h1 + 28, colw, 'C. The Meter and the Health board', [
    'The Meter (metering) reads CPU and memory counters every few seconds and stores exact numbers for the bill.',
    'The Health board (monitoring) shows visitors, errors and slowness per app, keeps what each flat printed (logs), and feeds a status page.',
], (AMB_F, AMB_B, AMB_T), numbered=False)
h3 = card(x2, y + h1 + h2 + 56, colw, 'D. When things break', [
    'A flat crashes or stops answering: the Manager notices (health check) and starts it again (self-healing).',
    'A whole Floor goes silent: no heartbeat, so the Manager moves its flats to another Floor (failover).',
], (COR_F, COR_B, COR_T), numbered=False)
y += max(hA, h1 + h2 + h3 + 56) + 28
h = card(M, y, CW, 'Limits that keep version 1 small (written down openly)', [
    "Simple apps first: customers' apps are single self-contained web programs (static Go binaries, HTTP only).",
    'Apps forget everything when restarted. No database or file storage for customers yet (file storage is part 3).',
    'One Manager only. If it dies, running apps keep running, but nothing can change until it restarts.',
    'Floors must be Linux, because the locks are Linux features. Your Windows PC runs 2 or 3 pretend Floors as small Linux machines. Virtual machines or WSL copies: decided in week 1.',
    'The bill counts CPU, memory and requests. Not disk or network. Payments are simulated.',
    'Names and padlock are private: only devices that ask your DNS server and trust your certificate office see the platform without warnings. A real internet name comes later, as a setting change.',
    'Inside the mall (Reception desk to flat) the traffic is plain HTTP over the private line. Encryption between all the parts comes later.',
], (GRY_F, GRY_B, GRY_T), numbered=False)
y += h + 90

# ---------------------------------------------------------------- 4 locks
y = section_head(y, 4, 'How a locked flat (container) works inside', 'Linux already has the locks built in. Your Go program switches them on for each flat.')
y = table(M, y, [250, 640, 560, 390],
          ['Lock', 'In plain words', 'What it stops', 'Technical name'], [
              ['Blindfold', 'The app can only see itself. It thinks it is alone on the computer.', "Sara's app can't see Ahmed's programs", 'namespaces'],
              ['Own empty room', "The app's whole world is just what is in its parcel.", "It can't read the computer's real files", 'root swap (pivot_root)'],
              ['Electricity limit', 'Linux counts and caps the power each flat uses. Over the limit, only that flat is stopped.', "One greedy flat can't slow the others", 'cgroups'],
              ['Private phone line', 'Each flat gets its own line, connected to the Reception desk only.', "Flats can't call each other", 'virtual network'],
              ['Fewer powers', "Even inside, the app can't do dangerous admin actions.", "It can't break out of its room", 'capabilities + seccomp'],
          ], tech_col=3) + 36
hb = card(M, y, colw, 'Bonus', ['Linux already counts the electricity each flat uses, so the Meter just reads those counters.'], (TEA_F, TEA_B, TEA_T), numbered=False)
hc = card(M + colw + 40, y, colw, 'Honest limit', ['Strong walls, not a bank vault. All flats share the same Linux kernel underneath. Fine for a learning platform, and we write the limit down openly.'], (COR_F, COR_B, COR_T), numbered=False)
y += max(hb, hc) + 90

# ---------------------------------------------------------------- 5 extras, proofs, timeline
y = section_head(y, 5, 'Extras, proofs and the 16-week plan', 'No piece is "done" until its proof runs by itself with one command.')
cw4 = (CW - 40) // 2
extras = [
    ('1. Customers kept separate', 'A locked flat and a power limit per customer, plus accounts and permissions at the Counter.', 'multi-tenancy', 'COMMITTED  |  small to medium', (TEA_F, TEA_B, TEA_T)),
    ('2. Meter and bill', 'Counts what each customer used and shows a simple bill.', 'usage metering and billing', 'COMMITTED  |  small to medium', (TEA_F, TEA_B, TEA_T)),
    ('3. Grow and shrink', 'More visitors means more copies of the flat. Fewer visitors, fewer copies.', 'autoscaling', 'COMMITTED  |  small', (TEA_F, TEA_B, TEA_T)),
    ('4. Careful updates', 'A new version goes to 5 visitors first. If it breaks, the platform goes back by itself.', 'canary deployment + rollback', 'FUTURE WORK  |  hooks built in: versions + traffic count', (GRY_F, GRY_B, GRY_T)),
]
ey = y
for i, (t, body, tech, tag, tone) in enumerate(extras):
    ex_x = M + (i % 2) * (cw4 + 40)
    ex_y = ey + (i // 2) * 290
    rbox(ex_x, ex_y, cw4, 260, tone[0], tone[1])
    d.text((ex_x + 34, ex_y + 26), t, font=F(34, True), fill=tone[2])
    para(ex_x + 34, ex_y + 78, body, F(28), INK, cw4 - 68)
    d.text((ex_x + 34, ex_y + 168), 'Technical name: ' + tech, font=F(26, True, True), fill=tone[2])
    d.text((ex_x + 34, ex_y + 210), tag, font=F(24, True), fill=tone[1])
y = ey + 2 * 290 + 20

d.text((M, y), 'The proofs', font=F(40, True), fill=INK)
y += 66
y = table(M, y, [440, CW - 440], ['Piece', 'The proof'], [
    ['Flats (containers)', "Break-in tests (isolation tests): peeking at a neighbor, eating all memory, calling a neighbor directly. Every attempt fails."],
    ['Manager (control plane)', 'Crash tests (failure injection): kill an app and it restarts. Kill a whole Floor and its flats move. Restart the Manager and it remembers everything.'],
    ['Reception desk (reverse proxy)', 'Names reach the right flat, even after a restart. Visitors are shared between copies.'],
    ['Names and padlock', 'The name ahmed-shop.mall.hamza is answered by your own DNS server and the browser shows the padlock. The CLI refuses a wrong or expired certificate.'],
    ['Security basics', "Attack tests: no token or a stolen token is refused, Ahmed can't touch Sara's app, a tampered parcel is refused, a fake Floor can't join."],
    ['Monitoring basics', 'Kill an app on purpose: the health board turns red, the logs show why, the status page turns green after the restart.'],
    ['Meter (metering)', 'A known workload gives numbers that match. No numbers are lost in a crash.'],
    ['Grow and shrink (autoscaling)', 'A fake crowd (load test) makes the copies go up. A quiet night brings them down.'],
]) + 56

d.text((M, y), 'The plan: every step starts with a tiny experiment before real code', font=F(40, True), fill=INK)
y += 66
y = table(M, y, [190, 960, CW - 1150], ['Weeks', 'What you build', 'Demo moment'], [
    ['1 - 2', 'Warm-up: Go basics, a locked room made by hand in Linux commands, and the decision how to run the Floors', "The room can't see outside"],
    ['3 - 5', 'Box runner (container runtime): your Go program starts an app in a locked flat, with limits and a private line', 'Break-in tests all fail'],
    ['6 - 8', 'Manager and notebook (control plane, state store), parcel shelf, node agents, Reception desk, your own DNS server for mall.hamza, health checks', 'Apps get a name and survive crashes'],
    ['9 - 10', 'Customers kept separate (multi-tenancy), security basics (permissions, hashed API tokens, parcel checksum, join token, audit log) and HTTPS (your own certificate office, wildcard certificate)', "Sara can't hurt Ahmed. A fake Floor is refused. The browser shows the padlock."],
    ['11 - 12', 'Meter and bill, monitoring basics (logs, request counts, status page), your own charts page (dashboard)', 'Ahmed sees his bill and his logs'],
    ['13 - 14', 'Grow and shrink (autoscaling) with load balancing, version history, cleanup', 'The fake crowd makes copies rise'],
    ['15 - 16', 'Catch up on anything that slipped, then documentation and the demo video. DNS and HTTPS used up the spare time, so careful updates stay future work.', 'The full demo video'],
]) + 36
h = card(M, y, CW, 'Safety net, agreed in advance', [
    'Checkpoint at week 6. If you are behind, the ready-made manager (Kubernetes) replaces your home-made control plane and everything else stays.',
    'If time runs short, drop in this order: (1) your own charts become the free charts tool (Grafana), (2) your own parcel format becomes the standard one (OCI image), (3) your own DNS server becomes a script that writes name entries by hand, (4) autoscaling becomes a manual "mall scale" command.',
], (COR_F, COR_B, COR_T), numbered=False)
y += h + 90

# ---------------------------------------------------------------- 6 complete map summary
y = section_head(y, 6, 'The complete map, in short', 'Everything a cloud platform has, sorted. The full list is in the second picture.')
leg_y = y
yy = leg_y
for key in ('BUILD', 'BASIC', 'LATER', 'PART 2', 'SKIP'):
    color, meaning = STATUS[key]
    label = 'PART 2-4' if key == 'PART 2' else key
    n = parts_n if key == 'PART 2' else cnt[key]
    pill(M, yy, label, color)
    d.text((M + 210, yy + 2), f'{n} items', font=F(28, True), fill=INK)
    d.text((M + 380, yy + 2), meaning if key != 'PART 2' else 'Follow-up parts: security guard (2), file storage (3), 5G app (4)', font=F(28), fill=MUTED)
    yy += 56
y = yy + 30

summary_rows = []
for gname, rs in GROUPS:
    c = Counter(r[2] for r in rs)
    summary_rows.append([gname, str(c['BUILD']), str(c['BASIC']), str(c['LATER']), str(c['PART 2'] + c['PART 3'] + c['PART 4']), str(c['SKIP'])])
summary_rows.append(['Total', str(cnt['BUILD']), str(cnt['BASIC']), str(cnt['LATER']), str(parts_n), str(cnt['SKIP'])])
y = table(M, y, [820, 200, 200, 200, 220, 200], ['Group', 'BUILD', 'BASIC', 'LATER', 'PART 2-4', 'SKIP'], summary_rows, center_cols=(1, 2, 3, 4, 5)) + 90

# ---------------------------------------------------------------- 7 decisions
y = section_head(y, 7, 'Decisions made so far')
h = card(M, y, CW, 'Locked in', [
    'Goal: one flagship project for the job hunt, current-role credibility, product potential and learning.',
    'Language: Go.   Budget: zero, no card, everything runs on your own PC.   Time: about 25 hours a week, 16 weeks.',
    'Approach: from scratch. You build the container runtime, control plane, reverse proxy, metering, monitoring and dashboard, plus your own parcel format.',
    f'Version 1 scope: the {cnt["BUILD"]} BUILD and {cnt["BASIC"]} BASIC items on the complete map. The {cnt["LATER"]} LATER items are future work, listed up front so nothing is a surprise.',
    'Names and HTTPS: the private, invented ending .hamza (names like ahmed-shop.mall.hamza), answered by your own DNS server, with HTTPS from your own certificate office. A real internet domain comes later as a setting.',
    'Floors must be Linux. How to run them on your Windows PC (virtual machines or WSL) is decided in week 1.',
    'Later parts, only after part 1 works: (2) security guard (SOC), (3) file storage (object store), (4) a 5G telecom app running on the platform.',
], (PUR_F, PUR_B, PUR_T), numbered=False)
y += h + 70

img.crop((0, 0, W, y)).save(OUT_DESIGN, optimize=True)
print('design saved', OUT_DESIGN, W, y)

# ====================================================================== PICTURE 2: the complete map
new_canvas(14000)
y = 70
d.text((M, y), 'Mini Cloud: the complete map', font=F(78, True), fill=INK)
d.text((M + 4, y + 96), f'Everything a cloud platform has: {TOTAL} items, each marked with what happens to it', font=F(34), fill=MUTED)
y += 190
yy = y
for key in ('BUILD', 'BASIC', 'LATER', 'PART 2', 'SKIP'):
    color, meaning = STATUS[key]
    label = 'PART 2-4' if key == 'PART 2' else key
    n = parts_n if key == 'PART 2' else cnt[key]
    pill(M, yy, label, color)
    d.text((M + 210, yy + 2), f'{n} items', font=F(28, True), fill=INK)
    d.text((M + 380, yy + 2), meaning if key != 'PART 2' else 'Follow-up parts: security guard (2), file storage (3), 5G app (4)', font=F(28), fill=MUTED)
    yy += 56
y = yy + 40

MW = [360, 470, 200, CW - 1030]
pad = 18
hf = F(26, True)
hh = lh(hf) + 2 * pad - 6
tx = M
d.rounded_rectangle([tx, y, tx + CW, y + hh], radius=12, fill=PUR_F)
cx = tx
for cw_, hd in zip(MW, ['Mall word', 'Technical word', 'Status', 'Note']):
    d.text((cx + pad, y + pad - 3), hd, font=hf, fill=PUR_T)
    cx += cw_
top = y
yy = y + hh
f_b = F(26, True)
f_n = F(26)
for gname, rs in GROUPS:
    d.rectangle([tx, yy, tx + CW, yy + 60], fill=PUR_B)
    d.text((tx + pad, yy + 12), gname, font=F(30, True), fill=WHITE)
    yy += 60
    for ri, (mall, tech, st, note) in enumerate(rs):
        rh = max(para_h(mall, f_b, MW[0] - 2 * pad), para_h(tech, f_b, MW[1] - 2 * pad), para_h(note, f_n, MW[3] - 2 * pad), 44) + 2 * pad - 6
        d.rectangle([tx, yy, tx + CW, yy + rh], fill=WHITE if ri % 2 == 0 else (248, 248, 244))
        cx = tx
        para(cx + pad, yy + pad - 3, mall, f_b, INK, MW[0] - 2 * pad)
        cx += MW[0]
        para(cx + pad, yy + pad - 3, tech, f_b, PUR_T, MW[1] - 2 * pad)
        cx += MW[1]
        pill(cx + pad, yy + (rh - 36) // 2, st, STATUS[st][0])
        cx += MW[2]
        para(cx + pad, yy + pad - 3, note, f_n, INK, MW[3] - 2 * pad)
        yy += rh
d.rounded_rectangle([tx, top, tx + CW, yy], radius=12, outline=LINE, width=3)
y = yy + 70
img.crop((0, 0, W, y)).save(OUT_MAP, optimize=True)
print('map saved', OUT_MAP, W, y, dict(cnt), TOTAL)
