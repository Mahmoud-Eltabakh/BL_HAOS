---
name: update-e2e-tests
description: Retired. Docker-based integration tests were removed; validate HAOS behavior in a Home Assistant OS virtual machine and keep module-local SIL tests current.
---

# Retired E2E Test Harness

## When to use this skill

The Docker Compose and live-bridge harness described by this skill has been
removed. Do not add references to its former files. New behavior is covered by
the module-local SIL suites where appropriate, then validated end to end in a
Home Assistant OS virtual machine with the add-on and integration installed.
