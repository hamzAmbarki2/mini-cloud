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
PURT = (PUR_F, PUR_B, PUR_T)
TEAT = (TEA_F, TEA_B, TEA_T)
GRYT = (GRY_F, GRY_B, GRY_T)
CORT = (COR_F, COR_B, COR_T)
AMBT = (AMB_F, AMB_B, AMB_T)

img = Image.new('RGB', (W, 20000), BG)
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


def arrow(x1, y1, x2, y2, color=MUTED, width=5, head=22):
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
        fonts = [F(26, True) if (ci == 0 or ci == tech_col) else bodyf for ci in range(len(r))]
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


def subhead(yy, s):
    d.text((M, yy), s, font=F(36, True), fill=INK)
    return yy + 58


# ====================================================================== DATA: the complete map
GROUPS = [
    ('A. What customers touch (your Go code)', [
        ('Command tool "mall"', 'mall CLI (Go)', 'CORE', 'login, deploy, list, logs, delete, rollback'),
        ('Counter', 'mall-api (Go)', 'CORE', 'tokens, per-tenant permissions, audit log'),
        ('Platform words: Tenant and App', 'Custom resources (CRDs)', 'CORE', "the platform's own kinds of objects inside Kubernetes"),
        ('Brain that builds tenants and apps', 'mall-operator (Go)', 'CORE', 'namespace, quota, rules, deployment, route, autoscaler'),
        ('Customer accounts', 'Tenants', 'BASIC', 'created by you, by hand. No sign-up page.'),
        ('App settings', 'Environment variables', 'BASIC', 'plain settings inside the App resource'),
        ('Charts page', 'Bill page + Grafana', 'BASIC', 'bill and status: one small Go page plus dashboards'),
        ('Secret settings', 'Secrets management (Vault)', 'LATER', 'encrypted passwords and keys'),
        ('Teams and roles', 'Roles (RBAC) for customers', 'LATER', 'several people per customer'),
        ('Sign-up page and email', 'Self-service sign-up', 'LATER', 'needs email sending and abuse checks'),
        ('Own web address', 'Custom domains', 'LATER', 'needs a real, paid domain'),
        ('Ready-made database', 'Managed database add-on', 'LATER', 'file storage (part 3) comes first'),
        ('Scheduled jobs', 'CronJobs', 'LATER', 'Kubernetes has them; the platform needs a way to ask for one'),
        ('One home page for developers', 'Developer portal (Backstage)', 'LATER', 'a web home for tenants'),
    ]),
    ('B. The factory line (CI/CD)', [
        ('Code home and pipelines', 'GitLab CE (self-hosted)', 'CORE', 'also holds the registry; wants about 8 GB of RAM'),
        ('Factory worker', 'GitLab Runner', 'CORE', 'runs the pipeline steps'),
        ('Shared pipeline recipe', 'Pipeline template', 'CORE', 'one recipe that every tenant project includes'),
        ('Quality inspector', 'SonarQube Community', 'CORE', 'its quality gate can stop a bad build'),
        ('Recipe checker', 'Hadolint', 'BASIC', 'checks Dockerfiles for mistakes'),
        ('Password finder', 'Gitleaks', 'BASIC', 'finds secrets left inside code'),
        ('Security inspector', 'Trivy', 'BASIC', 'stops builds that have critical security holes'),
        ('Packing machine', 'BuildKit', 'BASIC', 'builds the image'),
        ('Parcel shelf', 'GitLab Container Registry', 'BASIC', 'where images wait; the private certificate must be trusted'),
        ('Caretaker that follows the blueprint', 'Argo CD (GitOps)', 'BASIC', 'keeps add-ons equal to what Git says'),
        ('Pipeline health', 'GitLab and SonarQube numbers in Grafana', 'BASIC', 'build time, failures, quality trends (method to verify)'),
        ('A temporary copy for each change', 'Review environments', 'LATER', 'one per merge request'),
        ('Proof of who built an image', 'Image signing (cosign)', 'LATER', 'signed images'),
    ]),
    ('C. The cluster (the Floors)', [
        ('Blueprint builder', 'Terraform (or OpenTofu)', 'CORE', 'builds the cluster and tools; destroy and rebuild is a proof'),
        ('Floors on your PC', 'Kubernetes nodes (kind)', 'CORE', '1 control plane and 2 workers'),
        ('Locked section per customer', 'Namespaces, quotas, limit ranges', 'CORE', 'the multi-tenancy core'),
        ('Who may do what', 'RBAC', 'CORE', 'per-tenant rights'),
        ('Who may call whom', 'Network policies', 'CORE', 'default deny, allow only the reception desk'),
        ('Delivery boxes', 'Helm', 'BASIC', 'installs ready-made tool bundles'),
        ('Walls and phone lines', 'Calico', 'BASIC', 'kind alone does not enforce network policies'),
        ('House rules', 'Kyverno policies', 'BASIC', 'no root, limits required, images only from the registry'),
        ('Safe pods', 'Pod Security (restricted)', 'BASIC', 'dangerous settings are refused'),
        ('Live gauges', 'metrics-server', 'BASIC', 'needed for autoscaling; kind needs a special flag'),
        ('Grow and shrink', 'Horizontal Pod Autoscaler', 'BASIC', 'copies follow CPU use'),
        ('Self-healing and moving', 'Kubernetes controllers', 'BASIC', 'built in; proven by crash tests'),
        ('Sleep when idle', 'KEDA (scale to zero)', 'LATER', 'wake up on the first visitor'),
        ('Empty a Floor for repair', 'Node drain', 'LATER', 'move its pods away gently first'),
        ('Several control planes', 'High availability', 'LATER', 'removes the single point of failure'),
        ('Backups', 'Velero', 'LATER', 'copy the cluster state somewhere safe'),
        ('Prepare real Linux machines', 'Ansible', 'LATER', 'for real machines instead of kind'),
        ('Many clusters', 'Multi-cluster', 'SKIP', 'one PC, one cluster'),
        ('Heavy hardware', 'GPU scheduling', 'SKIP', 'no such hardware on your PC'),
    ]),
    ('D. The doors (names, padlock, reception)', [
        ('Reception desk', 'Traefik', 'CORE', 'HTTPS entrance; chosen because ingress-nginx was retired in March 2026'),
        ('Mall directory', 'CoreDNS (zone for mall.hamza)', 'CORE', 'one wildcard name covers every app'),
        ('Certificate office', 'cert-manager + private CA', 'CORE', 'makes the wildcard certificate'),
        ('Names like ahmed-shop.mall.hamza', 'DNS names', 'BASIC', 'a private, invented ending; the domain is one setting'),
        ('Padlock', 'HTTPS on every door', 'BASIC', 'your PC and the nodes must trust the private CA once'),
        ('Names that work from everywhere', 'Split DNS: PC, nodes, pipeline', 'BASIC', 'the same name must work from all three; a known pain'),
        ('Names for the tools too', 'gitlab, sonar, grafana under mall.hamza', 'BASIC', 'the tools get names and padlocks as well'),
        ('Spreading visitors', 'Load balancing (Traefik + Services)', 'BASIC', 'built in'),
        ('Automatic DNS entries', 'ExternalDNS', 'LATER', 'not needed while one wildcard name exists'),
        ('Certificates renewed by themselves', 'Short-lived certificates', 'LATER', 'in v1 the certificate lasts long'),
        ('Limit visitors per second', 'Rate limiting (Traefik)', 'LATER', 'protects apps from floods'),
        ('Encryption between pods', 'Service mesh (Linkerd or Istio)', 'LATER', 'parts prove who they are'),
        ('Limit outgoing calls', 'Egress policy', 'LATER', 'pods cannot call the internet freely'),
        ('A real internet domain', 'Public domain and public certificates', 'LATER', 'costs money; only settings change'),
    ]),
    ('E. Watching (monitoring)', [
        ('Meter reader', 'Prometheus', 'CORE', 'collects numbers over time'),
        ('Charts', 'Grafana', 'CORE', 'dashboards and the status page'),
        ('Complaints book', 'Loki (logs)', 'BASIC', 'what each app printed'),
        ('Alarm bells', 'Alertmanager + alert rules', 'BASIC', 'crash loops, node down, error spikes'),
        ('Cluster gauges', 'kube-state-metrics, node-exporter', 'BASIC', 'come with the Prometheus bundle'),
        ('Visitor counts', 'Traefik metrics', 'BASIC', 'visits, errors and slowness per app'),
        ('Platform health', 'Platform dashboards', 'BASIC', 'nodes, control plane and tools'),
        ('Following one visit', 'Tracing (OpenTelemetry, Tempo)', 'LATER', 'find where a slow visit lost time'),
        ('Cost cross-check', 'OpenCost', 'LATER', 'compare with your own meter'),
    ]),
    ('F. Billing (your Go code)', [
        ('Meter', 'mall-meter (Go)', 'CORE', 'reads Prometheus and stores exact usage'),
        ('Bill', 'Usage report per month', 'CORE', 'one per tenant'),
        ('Price list', 'Pricing plan', 'BASIC', 'one simple price list'),
        ('Customer sees own usage', 'Usage view per tenant', 'LATER', '"mall usage" and a page'),
        ('Past bills kept', 'Invoice history', 'LATER', 'one stored bill per customer per month'),
        ('Free allowance', 'Free tier', 'LATER', 'some usage free each month'),
        ('Collecting real money', 'Payments (cards)', 'SKIP', 'needs a payment company and a card; simulated instead'),
    ]),
    ('G. Security', [
        ('Break-in tests', 'Isolation tests', 'CORE', 'Sara cannot reach Ahmed, quotas hold, root is refused'),
        ('ID check and permissions', 'Hashed API tokens, per-tenant permissions', 'BASIC', 'inside mall-api'),
        ('Logbook of who did what', 'Audit log', 'BASIC', 'every action is recorded'),
        ('Secrets vault', 'Vault', 'LATER', 'real secret storage'),
        ('One login for everything', 'Keycloak (single sign-on)', 'LATER', 'one identity for all tools'),
        ('Parts prove who they are', 'mTLS (service mesh)', 'LATER', 'encrypted, identified traffic between pods'),
        ('Signed images and strict checks', 'cosign + Kyverno verification', 'LATER', 'only signed images may run'),
        ('Guard watching for attacks', 'Falco + Wazuh (SOC)', 'PART 2', 'the security-guard part'),
    ]),
    ('H. Storage and data', [
        ('Files that survive a restart', 'Persistent volumes', 'LATER', 'in v1 apps forget everything'),
        ('File storage service', 'Object store (SeaweedFS or Garage)', 'PART 3', 'MinIO community edition is retired; choice to verify'),
        ('Databases', 'Managed databases', 'LATER', 'after storage works'),
        ('Backups for customers', 'Customer backups', 'LATER', 'needs storage first'),
    ]),
    ('I. Building and testing the platform itself', [
        ('Proofs', 'Automated tests (Go tests, scripts)', 'CORE', 'one command runs them all'),
        ('One-command rebuild', 'terraform apply and destroy', 'CORE', 'rebuild the whole platform from nothing'),
        ('Docs and demo video', 'Documentation', 'CORE', 'your portfolio'),
        ('Proofs run on every change', 'GitLab CI for the platform repo', 'BASIC', 'the platform tests itself'),
        ('Fake crowd', 'k6 load tests', 'BASIC', 'drives the autoscaling proof and the meter proof'),
        ('Break things on purpose', 'Chaos Mesh', 'BASIC', 'kill pods and nodes'),
        ('Careful updates', 'Argo Rollouts (canary)', 'LATER', 'cheap with these tools; the hooks are in place'),
    ]),
    ('J. Extra parts and ideas', [
        ('Telecom 5G app on the platform', 'Open5GS on Kubernetes', 'PART 4', 'a showcase app'),
        ('Many platforms joined together', 'Federation', 'LATER', 'place apps by cost, delay or carbon'),
        ('Tiny on-demand functions', 'Serverless (Knative)', 'LATER', 'code that runs only when called'),
    ]),
]

STATUS = {
    'CORE': (PUR_B, 'An essential piece of version 1'),
    'BASIC': (TEA_B, 'A smaller supporting piece of version 1'),
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
V1 = cnt['CORE'] + cnt['BASIC']


def legend(yy):
    for key in ('CORE', 'BASIC', 'LATER', 'PART 2', 'SKIP'):
        color, meaning = STATUS[key]
        label = 'PART 2-4' if key == 'PART 2' else key
        n = parts_n if key == 'PART 2' else cnt[key]
        pill(M, yy, label, color)
        d.text((M + 210, yy + 2), f'{n} items', font=F(28, True), fill=INK)
        d.text((M + 380, yy + 2), meaning if key != 'PART 2' else 'Follow-up parts: security guard (2), file storage (3), 5G app (4)', font=F(28), fill=MUTED)
        yy += 56
    return yy


# ====================================================================== PICTURE 1: the design
y = 70
d.text((M, y), 'Mini Cloud', font=F(86, True), fill=INK)
d.text((M + 4, y + 104), 'Design overview: a multi-tenant platform built on the open-source DevOps stack', font=F(36), fill=MUTED)
bw, _ = badge(M, y + 170, 'DRAFT v8: working style set', COR_F, COR_T, F(28, True))
bw2, _ = badge(M + bw + 20, y + 170, 'Part 1 of 4: the platform', PUR_F, PUR_T, F(28, True))
badge(M + bw + bw2 + 40, y + 170, 'Nothing is built yet', GRY_F, GRY_T, F(28, True))
y += 290

# ---------------------------------------------------------------- 1 big picture
y = section_head(y, 1, 'The big picture', 'Read it from top to bottom. Colors tell you who does the work.')
lx = M
for tone, label in ((PURT, 'You write it (Go)'), (TEAT, 'Ready-made open-source tool, configured by you'), (GRYT, 'People and your PC')):
    rbox(lx, y, 40, 40, tone[0], tone[1], r=8)
    d.text((lx + 56, y + 3), label, font=F(26), fill=INK)
    lx += 56 + int(F(26).getlength(label)) + 50
y += 70


def band(y, label, boxes, arrows=False, note=None):
    n = len(boxes)
    pad = 30
    gap = 40
    bwid = (CW - 2 * pad - (n - 1) * gap) // n
    bh = 150
    h = 64 + bh + 30 + (46 if note else 0)
    d.rounded_rectangle([M, y, M + CW, y + h], radius=18, outline=LINE, width=3, fill=(252, 252, 250))
    d.text((M + pad, y + 16), label, font=F(28, True), fill=MUTED)
    bx = M + pad
    by = y + 64
    for i, (title, sub, tone) in enumerate(boxes):
        fill, border, ink = tone
        rbox(bx, by, bwid, bh, fill, border, r=14)
        cx = bx + bwid // 2
        d.text((cx, by + 16), title, font=F(32, True), fill=ink, anchor='ma')
        yy = by + 64
        for ln in wrap(sub, F(24), bwid - 30)[:3]:
            d.text((cx, yy), ln, font=F(24), fill=border, anchor='ma')
            yy += 30
        if arrows and i < n - 1:
            arrow(bx + bwid + 4, by + bh // 2, bx + bwid + gap - 4, by + bh // 2)
        bx += bwid + gap
    if note:
        d.text((M + pad, y + 64 + bh + 22), note, font=F(26, False, True), fill=MUTED)
    return y + h + 26


y = band(y, 'Factory line (GitLab CI/CD): code goes in, a checked and scanned image comes out', [
    ('Ahmed', 'developer, pushes code', GRYT),
    ('GitLab', 'code and pipelines', TEAT),
    ('Checks', 'Hadolint, Gitleaks, tests, SonarQube', TEAT),
    ('Build and scan', 'BuildKit, Trivy', TEAT),
    ('Registry', 'GitLab registry = parcel shelf', TEAT),
], arrows=True)
y = band(y, 'Your Go brain: the part you write', [
    ('mall CLI', 'login, deploy, logs', PURT),
    ('mall-api', 'tokens, permissions, audit', PURT),
    ('mall-operator', 'Tenant and App resources', PURT),
    ('mall-meter', 'usage and the bill', PURT),
], arrows=False)
y = band(y, 'Doors: names, padlock and reception', [
    ('Visitor', 'opens the shop', GRYT),
    ('CoreDNS', 'names for mall.hamza', TEAT),
    ('cert-manager', 'private certificate office', TEAT),
    ('Traefik', 'reception desk, HTTPS', TEAT),
])
y = band(y, 'Kubernetes cluster = the Floors (kind: 1 control plane, 2 workers)', [
    ('Control plane', 'API, scheduler, memory', TEAT),
    ("Ahmed's namespace", 'pods, quota, rules', TEAT),
    ("Sara's namespace", 'pods, quota, rules', TEAT),
    ("Youssef's namespace", 'pods, quota, rules', TEAT),
], note='Add-ons: Calico (network rules), Kyverno (house rules), metrics-server (live gauges for autoscaling)')
y = band(y, 'Watching: numbers, logs and alarms', [
    ('Prometheus', 'collects the numbers', TEAT),
    ('Grafana', 'dashboards, status page', TEAT),
    ('Loki', 'logs of every app', TEAT),
    ('Alertmanager', 'alarm bells', TEAT),
])
y = band(y, 'Foundation: builds and keeps everything', [
    ('Terraform', 'builds the cluster and tools', TEAT),
    ('Argo CD', 'keeps add-ons equal to Git', TEAT),
    ('Private CA', 'root certificate, kept offline', TEAT),
    ('Your PC', 'Windows, WSL2, Docker', GRYT),
])
y += 40

# ---------------------------------------------------------------- 2 mall words to tools
y = section_head(y, 2, 'The mall, translated into real tools', 'The mall story stays. Each mall part now has a real tool behind it.')
DW = [380, 560, CW - 940]
y = table(M, y, DW, ['Mall word', 'Real tool', 'What it does here'], [
    ['Floors (worker nodes)', 'Kubernetes nodes (kind)', '1 control plane and 2 workers, all inside Docker on your PC'],
    ['Flat', 'Container (Docker image), running in a pod', 'One copy of a customer app, in its own locked space'],
    ['Parcel', 'Docker image', 'The app packed once; never runs by itself'],
    ['Parcel shelf', 'GitLab Container Registry', 'Where images wait for Kubernetes to fetch them'],
    ['Manager (control plane)', 'Kubernetes control plane + your Go operator', 'Kubernetes keeps things running; your operator builds tenants and apps'],
    ["Manager's notebook", 'etcd (inside Kubernetes) + your own small database', 'Cluster memory; plus usage and bills'],
    ['Counter and mall CLI', 'mall-api and the mall CLI (Go)', 'Tokens, permissions, audit log; deploy, list, logs'],
    ['Reception desk', 'Traefik', 'Receives HTTPS visits and forwards them to the right app'],
    ['Mall directory', 'CoreDNS', 'One wildcard name: every app under mall.hamza'],
    ['Certificate office', 'cert-manager + a private certificate authority', 'Makes the wildcard certificate for the padlock'],
    ['Meter', 'Prometheus + mall-meter (Go)', 'Prometheus collects; your meter stores exact usage'],
    ['Health board', 'Grafana, Loki, Alertmanager', 'Dashboards, logs, alarms'],
    ['Customers kept separate', 'Namespaces, quotas, network policies, RBAC', 'The multi-tenancy core'],
    ['Grow and shrink', 'Horizontal Pod Autoscaler + metrics-server', 'Copies follow CPU use'],
    ['Careful updates (later)', 'Argo Rollouts', 'Cheap now: 5% of visitors first, automatic return'],
    ['NEW: the factory line', 'GitLab, Runner, SonarQube, Trivy, Gitleaks, Hadolint, BuildKit', 'Code in, a checked and scanned image out'],
    ['NEW: the blueprint', 'Terraform and Argo CD', 'Builds the cluster; keeps it equal to Git'],
], tech_col=1) + 90

# ---------------------------------------------------------------- 3 toolbox
y = section_head(y, 3, 'The toolbox in plain words', 'Every tool in version 1, what it does, and its mall word.')
TW = [330, 1000, CW - 1330]
y = table(M, y, TW, ['Tool', 'In plain words', 'Mall word'], [
    ['Linux + WSL2', 'The operating system that has the container locks. WSL2 runs Linux inside Windows.', 'The ground under the mall'],
    ['Docker', 'Packs an app into an image and runs images as containers.', 'Parcel and flat'],
    ['Kubernetes', 'Runs and keeps alive many containers across several computers.', 'Manager and Floors'],
    ['kind', 'Kubernetes inside Docker: several pretend computers on one PC.', 'The Floors on your PC'],
    ['Helm', 'Installs ready-made bundles of Kubernetes parts with one command.', 'Delivery boxes'],
    ['Terraform', 'Builds the cluster and the tools from text files, the same way every time.', 'The blueprint builder'],
    ['Argo CD', 'Watches a Git repository and makes the cluster match it.', 'The caretaker that follows the blueprint'],
    ['GitLab CE', 'Stores code, runs pipelines and holds images.', 'Factory line and parcel shelf'],
    ['GitLab Runner', 'The worker that executes the pipeline steps.', 'Factory worker'],
    ['SonarQube', 'Reads code, grades its quality and bugs, and can stop a bad build.', 'Quality inspector'],
    ['Trivy', 'Scans images and files for known security holes.', 'Security inspector'],
    ['Gitleaks', 'Finds passwords and keys accidentally left in code.', 'Password finder'],
    ['Hadolint', 'Checks Dockerfiles for mistakes.', 'Recipe checker'],
    ['BuildKit', 'Builds images quickly inside the pipeline.', 'Packing machine'],
    ['Calico', 'Enforces network rules between pods, so Sara cannot reach Ahmed.', 'Walls and phone lines'],
    ['Kyverno', 'Enforces rules: no root, limits required, images only from the registry.', 'House rules'],
    ['Traefik', 'Receives visitors on HTTPS and forwards them to the right app.', 'Reception desk'],
    ['CoreDNS', 'Turns a name into an address. One wildcard covers every app.', 'Mall directory'],
    ['cert-manager', 'Creates certificates for the padlock, here from your private certificate authority.', 'Certificate office'],
    ['metrics-server', 'Live CPU and memory numbers that autoscaling needs.', 'Live gauges'],
    ['Prometheus', 'Collects and stores numbers over time.', 'Meter reader'],
    ['Alertmanager', 'Sends alarms when a rule fires.', 'Alarm bells'],
    ['Grafana', 'Draws dashboards from the numbers and logs.', 'Charts page'],
    ['Loki', 'Stores and searches the logs of every app.', 'Complaints book'],
    ['k6', 'Sends a fake crowd of visitors to test the platform.', 'Fake crowd'],
    ['Chaos Mesh', 'Breaks things on purpose to prove the platform recovers.', 'Test saboteur'],
    ['Go (your code)', 'The operator, the API, the CLI and the meter.', 'Your brain'],
], tech_col=0) + 90

y = subhead(y, 'Kubernetes words in plain words')
y = table(M, y, [330, 1000, CW - 1330], ['Kubernetes word', 'In plain words', 'Mall word'], [
    ['Node', 'One computer that belongs to the cluster.', 'Floor'],
    ['Pod', 'One or more containers that run together. The smallest thing Kubernetes runs.', 'Flat'],
    ['Namespace', 'A named, separated area inside the cluster.', "A customer's locked section"],
    ['Deployment', 'A standing order: "keep 3 copies of this app running".', 'Standing order'],
    ['Service', 'A stable address in front of a group of pods.', 'A door number that never changes'],
    ['Ingress route', 'A rule: this name goes to that Service.', 'Reception rule'],
    ['Custom resource (CRD)', 'A new kind of object you invent. Yours are Tenant and App.', "The platform's own forms"],
    ['Operator', 'A program that watches those objects and makes the cluster match them.', 'Your Go brain'],
    ['ResourceQuota', 'A cap on how much a namespace may use.', 'Electricity limit'],
    ['NetworkPolicy', 'A rule about who may call whom.', 'Phone-line rules'],
    ['RBAC', 'Rules about who may do what.', 'Staff badges'],
], tech_col=0) + 90

# ---------------------------------------------------------------- 4 flows
y = section_head(y, 4, 'What happens, step by step', 'Technical words in brackets.')
colw = (CW - 40) // 2
hA = card(M, y, colw, 'A. Ahmed deploys his app (push to GitLab)', [
    "Ahmed pushes code to his project in GitLab. The shared pipeline recipe starts on the GitLab Runner.",
    'Checks run first: Hadolint (Dockerfile), Gitleaks (secrets in code), the tests, and the SonarQube quality gate. Any failure stops the pipeline.',
    'BuildKit builds the image. Trivy scans it. Critical security holes stop the pipeline.',
    'The image is pushed to the registry (the parcel shelf).',
    'The pipeline calls "mall deploy". mall-api checks the API token and permissions, writes the audit log, and creates or updates the App resource in Ahmed\'s namespace.',
    'The operator sees the App and creates the Deployment, the Service, the Traefik route and the autoscaler. Kyverno checks the house rules. Kubernetes places the pods on a worker (Floor).',
    'Health checks (probes) keep it alive. The name ahmed-shop.mall.hamza already works because one wildcard name covers every app.',
], PURT)
x2 = M + colw + 40
h1 = card(x2, y, colw, 'B. A visitor opens the shop', [
    'The visitor types https://ahmed-shop.mall.hamza. CoreDNS answers with the address of Traefik.',
    'Traefik sets up the padlock with the wildcard certificate from cert-manager.',
    'Traefik forwards the request to one of the app\'s pods (load balancing) and counts the visit, any error and the time taken.',
], TEAT)
h2 = card(x2, y + h1 + 28, colw, 'C. A new customer joins', [
    'The admin runs "mall admin tenant create sara". That creates a Tenant resource.',
    'The operator creates her namespace, quota, limits, network rules, RBAC and Pod Security label.',
    'The admin gives her a GitLab project and a deploy token by hand in version 1. Her API token is shown once.',
], TEAT)
h3 = card(x2, y + h1 + h2 + 56, colw, 'D. Meter, monitoring and breakdowns', [
    'Prometheus collects CPU, memory and visit counts. mall-meter reads them every minute and stores exact usage per tenant for the bill.',
    'Grafana shows dashboards. Loki keeps logs. Alertmanager rings when a pod crash-loops or a node goes down.',
    'A pod crashes: Kubernetes restarts it. A node dies: its pods move to another node. A bad pipeline: it stops before anything is deployed.',
], AMBT, numbered=False)
y += max(hA, h1 + h2 + h3 + 56) + 28
h = card(M, y, CW, 'Limits that keep version 1 small (written down openly)', [
    'One control plane only. If it dies, running apps keep running, but nothing can change until it is back.',
    'Apps are stateless web programs (HTTP). They forget everything when restarted. File storage is part 3.',
    'Names and the padlock are private. Only devices that ask your DNS and trust your certificate authority see them without warnings.',
    'The bill counts CPU, memory and requests. Not disk or network. Payments are simulated.',
    'GitLab is self-hosted because the free shared runners on GitLab.com ask for a card. Self-hosting costs about 8 GB of RAM.',
    'Everything runs on one PC, so it shows how the platform works. It does not prove real-world scale.',
], GRYT, numbered=False)
y += h + 90

# ---------------------------------------------------------------- 5 proofs
y = section_head(y, 5, 'The proofs', 'No piece is "done" until its proof runs by itself with one command.')
y = table(M, y, [440, CW - 440], ['Piece', 'The proof'], [
    ['Customers kept separate', "Break-in tests: Sara's pod cannot reach Ahmed's. A pod asking for more than its quota is refused. A pod that runs as root is refused."],
    ['Factory line', 'A failing test, a weak quality gate, a leaked password, a bad Dockerfile and a vulnerable image each stop the pipeline. A good push reaches the cluster.'],
    ['Names and padlock', 'ahmed-shop.mall.hamza resolves through your DNS and the browser shows the padlock. The CLI refuses a wrong certificate.'],
    ['Self-healing', 'Kill a pod and it returns. Stop a worker node and its pods move.'],
    ['Meter and bill', 'A known load (k6) gives usage numbers that match. Restart the meter and nothing is lost.'],
    ['Autoscaling', 'A fake crowd makes the copies go up. A quiet period brings them down.'],
    ['Monitoring', 'A crashing app turns the dashboard red, the logs say why, and an alarm fires.'],
    ['Reproducible', 'terraform destroy and apply rebuild the whole platform from nothing with one command.'],
]) + 90

# ---------------------------------------------------------------- 6 plan
y = section_head(y, 6, 'The plan: milestones, about 6 to 8 months', 'No fixed end date. You type, the assistant teaches. Every milestone ends with a demo.')
y = table(M, y, [310, 880, 430, CW - 1620], ['Milestone', 'What you do', 'Demo moment', 'Rough time'], [
    ['1. Foundations', 'Prepare the PC (free disk space, WSL2 memory). Linux and Docker basics. Build one container by hand with Linux commands. Go basics.', 'A locked room made by hand', '3-4 weeks'],
    ['2. Cluster, names, padlock', 'Terraform builds the kind cluster (1 control plane, 2 workers) with Calico, Traefik, cert-manager, CoreDNS for mall.hamza and the private CA. A sample app answers at https://hello.mall.hamza.', 'The padlock on your own name', '4-5 weeks'],
    ['3. Factory line', 'GitLab CE, Runner and registry. First pipeline: build, push, deploy. Then the SonarQube, Trivy, Gitleaks and Hadolint gates.', 'Push code and the app updates. A bad push is stopped.', '4-5 weeks'],
    ['4. Watching and GitOps', 'Prometheus, Alertmanager, Grafana, Loki, pipeline-health dashboards. Argo CD keeps the add-ons equal to Git.', 'Kill a pod: red, then green', '3 weeks'],
    ['5. The Go brain', 'Operator with Tenant and App, namespaces, quotas, network policies, RBAC, Kyverno rules. mall-api and the mall CLI with tokens, permissions and audit log.', 'mall deploy works. Sara cannot reach Ahmed.', '6-8 weeks'],
    ['6. Meter, bill, autoscaling', 'mall-meter and the bill page. Autoscaling with metrics-server and a fake crowd.', 'Ahmed sees his bill. The crowd makes copies rise.', '3-4 weeks'],
    ['7. Proofs and polish', 'Chaos tests. Isolation proofs run in CI. Destroy and rebuild everything. Documentation and the demo video. Careful updates only if you want them.', 'The platform rebuilt in one command, and the demo video', '3 weeks'],
    ['Total', '', '', 'about 26-32 weeks'],
]) + 36
h = card(M, y, CW, 'Checkpoint after milestone 3, and the cut list', [
    'After milestone 3 (about month 3), "push code, the pipeline passes, the app answers at an https name" must work. If it takes much longer than planned, we pause and simplify before going on.',
    'There is no deadline, so cutting is your choice, not a necessity. For a shorter project, drop in this order: (1) Argo CD, (2) Loki, (3) the bill page, (4) self-hosted GitLab becomes GitLab.com with your own runner, (5) autoscaling becomes a manual "mall scale" command.',
    'Every milestone has a target date and a monthly review, so "no deadline" does not turn into "never finished".',
], CORT, numbered=False)
y += h + 90

# ---------------------------------------------------------------- 7 complete map summary
y = section_head(y, 7, 'The complete map, in short', 'Everything the platform has or could have, sorted. The full list is the second picture.')
y = legend(y) + 30
summary_rows = []
for gname, rs in GROUPS:
    c = Counter(r[2] for r in rs)
    summary_rows.append([gname, str(c['CORE']), str(c['BASIC']), str(c['LATER']), str(c['PART 2'] + c['PART 3'] + c['PART 4']), str(c['SKIP'])])
summary_rows.append(['Total', str(cnt['CORE']), str(cnt['BASIC']), str(cnt['LATER']), str(parts_n), str(cnt['SKIP'])])
y = table(M, y, [820, 200, 200, 200, 220, 200], ['Group', 'CORE', 'BASIC', 'LATER', 'PART 2-4', 'SKIP'], summary_rows, center_cols=(1, 2, 3, 4, 5)) + 90

# ---------------------------------------------------------------- 8 risks and decisions
y = section_head(y, 8, 'Risks and decisions')
hr = card(M, y, CW, 'Honest risks', [
    f'Tool sprawl. Version 1 has {V1} items. Most are "install and configure", but each one can fight back. Each tool must earn its place, and there is one golden path.',
    'Trusting your private certificate authority everywhere (your PC, the Kubernetes nodes, the pipeline) and making one name work from all three is the classic pain. It is timeboxed inside milestones 2 and 3.',
    'No deadline can turn into never finished. Every milestone has a demo, a target date and a monthly review.',
    'Your PC: GitLab alone wants about 8 GB of RAM, and the whole stack needs tens of GB of free disk. You have about 14 GB free on C:, so cleaning up comes first in week 1.',
    'Versions and licences move. Examples already found: ingress-nginx was retired in March 2026, MinIO community edition is retired, Terraform changed its licence in 2023 (OpenTofu is the community fork). All versions are pinned and re-checked in week 1.',
    'Docker Desktop is free for personal use, education and small companies. A large employer may require a paid licence. Docker Engine inside WSL2 is the free alternative.',
], CORT, numbered=False)
y += hr + 28
h = card(M, y, CW, 'Locked in', [
    'Goal: one flagship project for the job hunt, current-role credibility, product potential and learning.',
    'Direction: real open-source tools (Docker, Kubernetes, Terraform, GitLab, SonarQube and more) with your own Go brain on top. Not from scratch.',
    'Language of your own code: Go. Budget: zero, no card, everything on your own PC.',
    'Working style: you type everything and the assistant teaches. About 25 hours a week with no fixed end date: learning the foundations and finishing professionally matter more than speed. My guess is 6 to 8 months.',
    'Names and HTTPS: the private, invented ending .hamza (names like ahmed-shop.mall.hamza), CoreDNS, and a private certificate authority with cert-manager.',
    f'Version 1 scope: the {cnt["CORE"]} CORE and {cnt["BASIC"]} BASIC items. The {cnt["LATER"]} LATER items are future work, listed up front. Careful updates is LATER.',
    'Later parts, only after part 1 works: (2) security guard (Falco and Wazuh), (3) file storage (SeaweedFS or Garage), (4) a 5G telecom app (Open5GS).',
], PURT, numbered=False)
y += h + 28
h = card(M, y, CW, 'Still open', [
    'Where the real project lives: a permanent folder and git repository. This session\'s folder is temporary.',
    'Small technical choices for week 1: kind or k3d, Calico or Cilium, SQLite or Postgres for the bill, Docker Desktop or Docker Engine in WSL2.',
], AMBT, numbered=False)
y += h + 70

img.crop((0, 0, W, y)).save(OUT_DESIGN, optimize=True)
print('design saved', W, y)

# ====================================================================== PICTURE 2: the complete map
new_canvas(16000)
y = 70
d.text((M, y), 'Mini Cloud: the complete map', font=F(78, True), fill=INK)
d.text((M + 4, y + 96), f'Everything the platform has or could have: {TOTAL} items, each marked with what happens to it', font=F(34), fill=MUTED)
y += 190
y = legend(y) + 40

MW = [380, 500, 190, CW - 1070]
pad = 18
hf = F(26, True)
hh = lh(hf) + 2 * pad - 6
tx = M
d.rounded_rectangle([tx, y, tx + CW, y + hh], radius=12, fill=PUR_F)
cx = tx
for cw_, hd in zip(MW, ['Mall word', 'Real tool', 'Status', 'Note']):
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
print('map saved', W, y, dict(cnt), TOTAL, 'v1 =', V1)
