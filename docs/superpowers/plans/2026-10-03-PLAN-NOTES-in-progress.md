# Plan notes (work in progress)

**Date:** 2026-10-03
**Status:** the implementation plan is **not written yet**. Planning started, then the owner asked to stop installing things and save everything, because the PC is about to be reformatted. This file preserves the planning work so the next session can continue straight away.

**Spec this plan implements:** [../specs/2026-10-03-mini-cloud-part1-design.md](../specs/2026-10-03-mini-cloud-part1-design.md)

## How the plan should be written (the agreed shape)

Use the `superpowers:writing-plans` skill. Because the spec covers seven milestones, write separate plans, as that skill advises:

| File to create | Content |
|---|---|
| `docs/superpowers/plans/<date>-master-plan.md` | The 7 milestones, the target repository layout, global constraints, the review focus, and what "done" means per milestone |
| `docs/superpowers/plans/<date>-m1-foundations.md` | Milestone 1 in detail, bite-sized steps |
| `docs/superpowers/plans/<date>-m2-cluster-names-padlock.md` | Milestone 2 in detail, bite-sized steps |
| later plans | One detailed plan per later milestone, written when we reach it, because they depend on what we learn |

**Working mode:** the owner types everything and the assistant teaches (small exercises, explanations, reviews). Test-first becomes **proof-first**: write the proof, watch it fail, build, watch it pass, commit. Execution method is already decided (teaching mode), so the hand-off after writing is "please review the plan", not a choice between subagents and native.

**Rules for the plan text:** plain words, every technical word explained, real commands with the output the owner should see, no placeholders, exact versions.

## Milestone 1 outline: Foundations (3-4 weeks)

1. **Prepare the (freshly formatted) machine.** WSL2 with Ubuntu, Git (repo-local noreply identity), Docker, a `.wslconfig` with memory limits **and cgroup v2** (see "Findings"), a proof script that checks versions, RAM and free disk.
2. **Linux survival lab.** Processes, files, permissions, networking commands, with observations the owner writes in their own words.
3. **Container by hand.** Alpine mini root filesystem, then `unshare` for new PID, mount, UTS, IPC and network spaces plus `chroot`, then a cgroup v2 group with memory, CPU and process limits. A `proof.sh` asserts: PID 1 inside, hostname isolated, only a loopback link, no host files, memory hog is killed. The namespace half is already verified (`labs/container-by-hand/namespaces-test.sh`).
4. **Go basics through the sample app `apps/hello`.** Endpoints `/` and `/healthz`, settings from `APP_NAME` and `PORT`. Tests first: health returns `{"status":"ok"}`, root greets, unknown paths return 404. Draft only, not yet run.
5. **Docker basics.** Multi-stage Dockerfile for `apps/hello` (static binary, non-root user), build, run, `curl` the health endpoint.
6. **Wrap-up.** Notes in the owner's words, tag `m1-done`, push, demo: the container made by hand.

## Milestone 2 outline: Cluster, names, padlock (4-5 weeks)

1. **Install the tools inside WSL:** kubectl, kind, Helm, Terraform, with pinned versions in one `versions.env`.
2. **Terraform builds the kind cluster** (1 control plane, 2 workers) with the default network disabled, then installs **Calico**. Proof: nodes Ready, a network policy is really enforced.
3. **Private certificate authority.** A script makes a root key and certificate with **name constraints** limited to `.hamza`. The root key stays outside the repo and outside Terraform state. Windows trusts the root certificate once.
4. **cert-manager** with a CA issuer built from that root, and a wildcard certificate `*.mall.hamza`.
5. **Traefik** through Helm, as a NodePort mapped to the host's ports 80 and 443 by kind's port mappings, with the wildcard certificate as its default.
6. **CoreDNS** in a Docker container serving `mall.hamza` with one wildcard record to `127.0.0.1`, published on port 53. A Windows name-resolution rule sends `.hamza` to it.
7. **Sample app on the cluster:** manifests for `apps/hello` (non-root, health probes, Service, route for `hello.mall.hamza`), loaded into kind with `kind load docker-image` because there is no registry until milestone 3. Proof: `curl` with the CA works, `curl` without it fails, the browser shows the padlock.
8. **Rebuild proof and wrap-up:** `terraform destroy` then `apply` rebuilds everything. Notes, tag `m2-done`, push.

## Findings on the owner's PC (before the reformat)

These may not hold after a fresh install.

- **WSL2 Ubuntu:** kernel `5.15.167.4-microsoft-standard-WSL2`, systemd is PID 1.
- **cgroups:** the layout is **hybrid**. Version 1 controllers are mounted under `/sys/fs/cgroup`, and version 2 sits empty at `/sys/fs/cgroup/unified`. There was **no `.wslconfig`**.
  - Modern Kubernetes and the planned lab want **cgroup v2 only**. Kubernetes has been moving away from cgroup v1; check how far in the chosen kind node version.
  - The planned fix, **not yet applied or verified**: in `%UserProfile%\.wslconfig` add `[wsl2]` and `kernelCommandLine = cgroup_no_v1=all`, then `wsl --shutdown`. Proof: `stat -fc %T /sys/fs/cgroup` prints `cgroup2fs`.
  - The owner must make this change themselves (it is a system setting). A fresh WSL install may already ship a newer kernel, so look first.
- **Tools present before the reformat:** git 2.48.1, terraform 1.9.8, kubectl 1.31.4, node 20, python 3.13, java 17, dotnet 10, Docker Desktop (installed, stopped). **Missing:** go, kind, helm.
- **Git identity:** the machine's global git email is a school address. For this public repo use the repo-local noreply identity `168687736+hamzAmbarki2@users.noreply.github.com`.
- **Disk:** only about 14 GB free on C: before the reformat. That was the reason for the reformat.
- **Namespace lab, verified for real in WSL Ubuntu:** inside the new spaces the shell had PID 1, the hostname changed only inside, `ip link` showed only `lo`, the OS was Alpine, `/mnt/c` was not visible, and the host's hostname was unchanged afterwards.
- **Alpine mini root filesystem:** version `3.24.2`, file `alpine-minirootfs-3.24.2-x86_64.tar.gz` from `https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/`, sha256 `c5ca053cfe1d85c5b96dff8b9bc57045f7f184a30ffb6b65776409ca90388677` (re-check; "latest-stable" moves).
- **Go:** the current stable release on 2026-10-03 was **1.27.1** (previous line 1.26.8). The Linux amd64 archive `go1.27.1.linux-amd64.tar.gz` has sha256 `63d339f0da5ab53635a56f2490a7984dfe12dfcff22ad749f63edaf590168445` (from the go.dev download list). Nothing was downloaded or tested.

## Still to verify before writing the commands (do not guess)

- kind configuration: disabling the default network, `extraPortMappings`, and the current kind node image for the chosen Kubernetes version.
- Installing Calico on kind (operator or manifest, current version).
- Traefik Helm values for NodePort with fixed node ports, and its default TLS store.
- cert-manager `ClusterIssuer` of type CA from a Secret, and the current chart version.
- CoreDNS zone file with a wildcard record, and running it in Docker on port 53.
- Windows name-resolution rule (`Add-DnsClientNrptRule`) pointing at `127.0.0.1`, and whether another process already uses port 53.
- OpenSSL name-constraints command (can be tested locally with the Git for Windows OpenSSL).
- Docker Desktop's cgroup version (`docker info`).
- Terraform's `kind` provider versus calling the `kind` CLI from Terraform.
- Current versions of everything above. Pin them in one file.

## Rules for the next session

- **Do not install or download anything on the owner's machine without asking.** A Go download was rejected on 2026-10-03.
- The repo is public. No secrets, keys, tokens or personal data in any file or commit.
- Keep the spec's Appendix A and the `GROUPS` list in `tools/make_stack_png.py` in sync.
