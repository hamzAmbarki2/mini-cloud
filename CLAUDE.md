# Mini Cloud: handoff notes for Claude

Read this file first in every new session, then the spec in `docs/superpowers/specs/`.

## Where we stopped (2026-10-03)
- **Design approved.** Spec: `docs/superpowers/specs/2026-10-03-mini-cloud-part1-design.md`. Pictures: `docs/pictures/`.
- **Next step:** finish the implementation plan with the `superpowers:writing-plans` skill: a master plan plus detailed plans for milestones 1 and 2. **Start from `docs/superpowers/plans/2026-10-03-PLAN-NOTES-in-progress.md`**: it holds the task outlines, the findings on the owner's old PC, and the list of facts still to verify before writing commands. Then teach milestone 1.
- **Nothing is built yet.** The only code is a verified draft lab script in `labs/container-by-hand/`.
- **The owner is reformatting their PC** (disk was full). Everything lives in this repo. After a fresh install: install Git, clone, open the folder in Claude Code, and check the machine from scratch (WSL2, cgroup v2, Docker).
- **Do not install or download anything on the owner's machine without asking.** A Go download was rejected on 2026-10-03.
- Open items: week-1 technical choices (kind or k3d, Calico or Cilium, SQLite or Postgres for usage and bills, Docker Desktop or Docker Engine in WSL2); re-check tool versions and licences at the start.
- Older material is kept in `archive-from-scratch/` (the superseded from-scratch design, its pictures and its generator script).

## The project in one paragraph
A small multi-tenant platform on the open-source DevOps stack (Docker, Kubernetes via kind, Terraform, GitLab CE and Runner, SonarQube Community, Trivy, Gitleaks, Hadolint, BuildKit, Argo CD, Calico, Traefik, CoreDNS, cert-manager with a private CA, Prometheus, Grafana, Loki, Alertmanager, Kyverno, k6, Chaos Mesh) plus the owner's own Go code: `mall-operator` (Tenant and App custom resources), `mall-api`, the `mall` CLI and `mall-meter`. Story: a mall. Customers rent locked sections (namespaces). Apps live at `https://<tenant>-<app>.mall.hamza`.

## Decisions already made (do not reopen without a reason)
- Real open-source tools plus a Go layer. **Not** from scratch (an earlier from-scratch design is archived).
- Zero budget, no payment card, everything on the owner's own PC (Windows 11, WSL2, Docker).
- Names: the private, invented ending `.hamza`. HTTPS from cert-manager and a private certificate authority. One wildcard name covers every app.
- Version 1 = the CORE and BASIC items of the complete map (57 of 98). Careful updates (canary, Argo Rollouts) is LATER. Payments are simulated.
- Parts 2 to 4 come only after part 1: security guard (Falco, Wazuh), file storage (SeaweedFS or Garage; MinIO community edition is retired), 5G app (Open5GS).
- Plan: 7 milestones, about 6 to 8 months at about 25 hours a week, **no fixed end date**. Checkpoint after milestone 3. Ordered cut list is in the spec.
- Facts checked on 2026-10-03 are in spec section 14 (ingress-nginx retired, kind needs Calico for network policies, GitLab.com free runners need a card, and more). Re-check them.

## How to work with the owner (important)
- **The owner types everything and the assistant teaches**: small exercises, explanations, reviews. Do not silently write the owner's code.
- **Plain words only.** The owner is new to cloud. Explain every technical word simply, with the mall analogy, and give the real technical word next to it. When they say "I didn't understand", re-explain simpler.
- **Answer the literal question first**, then add context.
- **List everything up front**: complete lists with a status for each item beat drip-feeding.
- **Be honest about time and scope.** The owner tends to choose the biggest option. State the cost once, then record the escape plan (checkpoint, cut list) instead of arguing.
- Ask **one question at a time**, with plain option labels.
- Pictures are valued. Render them, look at them, and check that nothing overflows before sending.
- Never publish or push anything external without explicit permission. This repo is **public**: no secrets, no personal data.

## Security rules
- Never commit keys, tokens, kubeconfig files, Terraform state or `.env` files. `.gitignore` covers the usual names.
- The private CA's **root key stays offline** on the owner's machine. Never put it in the repo.
- Commits use GitHub's noreply address, not a personal or school email.

## Regenerate the pictures
```
python tools/make_stack_png.py docs/pictures/mini-cloud-stack-design.png docs/pictures/mini-cloud-stack-map.png
```
The data for the complete map is the `GROUPS` list in that script. The spec's Appendix A mirrors it, so change both together.
