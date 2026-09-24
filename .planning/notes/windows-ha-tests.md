---
title: Windows Home Assistant test strategy
date: 2026-09-24
context: gsd-explore making Home Assistant integration tests runnable on Windows
---

Native Windows remains the fast developer loop for bridge, frontend, and package-level integration checks. Full Home Assistant SIL/config-entry tests should run in Linux CI because Home Assistant Core imports Unix-only modules such as `fcntl` and the official development guidance supports WSL 2 or devcontainers on Windows.

The CI lane should use a pinned Home Assistant Core version for reproducibility. Upgrade that pin deliberately, then run a separate compatibility check before accepting a new Core release. WSL 2 is an optional local reproduction path, not a repository-managed prerequisite. Docker and live Bluetooth hardware remain separate validation concerns.
