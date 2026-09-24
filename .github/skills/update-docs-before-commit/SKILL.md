---
name: update-docs-before-commit
description: Before committing changes to modules/bridge or modules/integration, check whether user-facing docs (CHANGELOG.md, DOCS.md, README.md, config.yaml version) drifted out of sync with the code change, and update them in the same commit. Use this whenever a change touches backend routes/config.yaml options/demo scenarios, the Home Assistant integration, or the add-on <-> integration connection flow.
---

# Update Docs Before Commit

Docs in this repo drift silently because doc updates are optional and easy to forget in a normal commit flow. This skill makes doc-sync a required step, run right before every commit that touches user-visible behavior.

## When to use this skill

Run this check before committing any change to:
- `modules/bridge/backend/bl_haos/**` (API routes, config options, demo scenarios, recovery actions)
- `modules/bridge/config.yaml` (add-on options, schema, discovery services)
- `modules/integration/custom_components/bl_haos/**` (config flow, entities, services)
- Anything affecting the add-on <-> integration connection/auth flow

Skip it for: test-only changes, CI workflow tweaks, pure refactors with no behavior change, `.planning/` files.

## Files to check, per change

| Change | Update |
|---|---|
| New/changed backend REST or WS endpoint | `modules/bridge/DOCS.md` ("How to Use" section) if user-facing; otherwise no doc change needed |
| New/changed `config.yaml` option or schema | `modules/bridge/DOCS.md` (setup/configuration section) |
| New/changed demo scenario or recovery action | Usually internal-only; update `.github/skills/update-e2e-tests/SKILL.md` coverage instead (see that skill) |
| Change to how the add-on and integration connect/authenticate | `modules/bridge/DOCS.md`, `modules/integration/README.md`, and the root `README.md` if it also describes setup |
| Any user-visible fix or feature in `modules/bridge` | `modules/bridge/CHANGELOG.md` -- new entry, plus a version bump in `modules/bridge/config.yaml` |
| Breaking change to the integration's config entry data/schema | `modules/integration/README.md` and a migration note if existing installs need to reconfigure |

## Procedure

1. **Classify the change.** Read the diff and decide: is this user-visible (behavior, setup steps, options) or purely internal (refactor, test, CI)? Only user-visible changes need doc updates.

2. **Bump the version and changelog (bridge only).** This repo's convention (see `modules/bridge/CHANGELOG.md`) is a patch-style bump for every user-visible change, regardless of whether it's a feature or a fix:
   - Increment `version` in `modules/bridge/config.yaml`.
   - Add a new entry at the **top** of `modules/bridge/CHANGELOG.md` with that version as the header, and one or two concise, technical bullet(s) describing the user-visible effect (not implementation detail). Match the existing terse style -- state what changed and why it matters to the user, skip internal mechanics.

3. **Update DOCS.md / README.md content, not just the changelog.** A changelog entry is not a substitute for updating the actual setup/usage instructions. If the change alters:
   - what a user needs to do during setup (e.g., manual steps that became automatic, or vice versa),
   - what data/permissions the integration requires,
   - what options are available in the add-on configuration,

   then edit the relevant prose in `modules/bridge/DOCS.md`, `modules/integration/README.md`, or the root `README.md` to match. Search for stale phrases first (e.g. `grep` for the old behavior's keywords) rather than assuming where it's described.

4. **Verify docs actually match the code, not just intent.** Before committing, re-read the specific paragraph you touched (or the one describing the feature you changed) and confirm it's still literally true given the new code -- this repo has previously had docs describe a smoother flow ("Home Assistant discovers the add-on... confirm the setup prompt") while the code still required a manual step the docs didn't mention. Don't let that happen the other way either.

5. **Keep it in the same commit as the code change.** Doc updates for a change belong in the same commit, not a follow-up "docs" commit -- this keeps `git blame`/history meaningful and prevents a window where docs and code disagree.

6. **Do not create new markdown files** for this. Update the existing `CHANGELOG.md` / `DOCS.md` / `README.md` files only, unless the user explicitly asks for a new doc.

## Non-goals

- This skill does not cover test-suite documentation. Docker-based integration tests were retired; HAOS end-to-end behavior is validated in a Home Assistant OS virtual machine.
- This skill does not require a doc update for internal-only refactors, dependency bumps, or CI workflow changes that have no user-visible effect.
