# Mini Cloud

A small **multi-tenant platform** built on the open-source DevOps stack (Docker, Kubernetes, Terraform, GitLab, SonarQube, Prometheus, Grafana and more), plus an original layer written in **Go**.

Think of a **mall**. The customers are people who make apps. They get locked sections of a shared Kubernetes cluster. They push code to GitLab, a pipeline checks, scans and builds it, and the platform runs it at `https://<customer>-<app>.mall.hamza` with a padlock, watches it, and sends a monthly bill. The project builds the mall around the shops, not the shops.

**Status:** design phase. The design is approved. The implementation plan is next. Nothing is built yet.

## Read this first

| What | Where |
|---|---|
| The approved design (spec) | [docs/superpowers/specs/2026-10-03-mini-cloud-part1-design.md](docs/superpowers/specs/2026-10-03-mini-cloud-part1-design.md) |
| The design as a picture | [docs/pictures/mini-cloud-stack-design.png](docs/pictures/mini-cloud-stack-design.png) |
| Everything the platform has or could have (98 items) | [docs/pictures/mini-cloud-stack-map.png](docs/pictures/mini-cloud-stack-map.png) |
| The earlier "from scratch" design (superseded, kept for history) | [archive-from-scratch/](archive-from-scratch/) |

## The plan in one table

| Milestone | What | Rough time |
|---|---|---|
| 1. Foundations | Linux, Docker, Go basics, a container made by hand | 3-4 weeks |
| 2. Cluster, names, padlock | Terraform, kind, Calico, Traefik, CoreDNS, cert-manager, private CA | 4-5 weeks |
| 3. Factory line | GitLab, Runner, registry, pipeline with SonarQube, Trivy, Gitleaks, Hadolint | 4-5 weeks |
| 4. Watching and GitOps | Prometheus, Grafana, Loki, Alertmanager, Argo CD | 3 weeks |
| 5. The Go brain | Kubernetes operator, API, CLI, multi-tenancy, policies | 6-8 weeks |
| 6. Meter, bill, autoscaling | Usage metering, the bill, autoscaling, load tests | 3-4 weeks |
| 7. Proofs and polish | Chaos tests, rebuild from nothing, docs, demo video | 3 weeks |

No fixed end date. Learning the foundations and finishing professionally matter more than speed.

## Resume on a new machine

1. Install Git and Claude, and sign in.
2. `git clone https://github.com/hamzAmbarki2/mini-cloud.git`
3. Open the folder in Claude Code. [CLAUDE.md](CLAUDE.md) loads by itself and tells Claude where we stopped and how we work.
4. Say "continue".

## Regenerate the pictures

The two pictures are drawn by a script. It needs Python with Pillow and the Windows font Segoe UI.

```
python tools/make_stack_png.py docs/pictures/mini-cloud-stack-design.png docs/pictures/mini-cloud-stack-map.png
```

## Safety

No keys, tokens, kubeconfig files or Terraform state are ever committed. `.gitignore` blocks the usual names. The private certificate authority's root key stays offline on the author's machine.

No licence has been chosen yet.
