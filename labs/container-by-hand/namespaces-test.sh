#!/usr/bin/env bash
# DRAFT lab for milestone 1 ("container by hand"), namespace half only.
# Verified for real in WSL2 Ubuntu on 2026-10-03: inside the new spaces the shell was PID 1,
# the hostname change stayed inside, only a loopback link existed, and host files were invisible.
# Run inside WSL as root. The cgroup v2 half (memory, CPU, process limits) is NOT written yet;
# it needs cgroup v2 first. See docs/superpowers/plans/2026-10-03-PLAN-NOTES-in-progress.md.
# Test of the namespace part of the "container by hand" lab (no system settings changed).
set -u
LAB=/tmp/mall-lab-test
ROOTFS=$LAB/rootfs
VER=3.24.2
URL=https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-$VER-x86_64.tar.gz
SHA=c5ca053cfe1d85c5b96dff8b9bc57045f7f184a30ffb6b65776409ca90388677

rm -rf "$LAB"; mkdir -p "$ROOTFS"
curl -fsSL "$URL" -o "$LAB/rootfs.tar.gz" || { echo "download failed"; exit 1; }
echo "$SHA  $LAB/rootfs.tar.gz" | sha256sum -c - || exit 1
tar -xzf "$LAB/rootfs.tar.gz" -C "$ROOTFS"
echo "rootfs files: $(ls $ROOTFS | wc -l)"; cat "$ROOTFS/etc/os-release" | head -2

HOST_NAME=$(hostname)
echo "host hostname: $HOST_NAME"

# One command: new PID, mount, UTS, IPC and network namespaces, then chroot into the rootfs
OUT=$(unshare --pid --fork --mount --uts --ipc --net --mount-proc="$ROOTFS/proc" \
  chroot "$ROOTFS" /bin/sh -c '
    hostname mall-flat
    echo "inside-hostname=$(hostname)"
    echo "inside-pid=$$"
    echo "inside-ps-count=$(ps | grep -vc "PID")"
    echo "inside-os=$(. /etc/os-release; echo $ID)"
    echo "inside-links=$(ip -o link | wc -l)"
    echo "inside-link-names=$(ip -o link | cut -d: -f2 | tr -d " " | tr "\n" ",")"
    echo "inside-sees-host-files=$([ -e /mnt/c ] && echo yes || echo no)"
  ' 2>&1)
echo "$OUT"
echo "host hostname after: $(hostname)"
rm -rf "$LAB"
