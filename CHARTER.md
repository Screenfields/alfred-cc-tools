## Repo owner
alfred-cc-tools

## Objective
O2, A way of working that is enforced and improves itself

## Business case
One catalog pins the plugin versions that every platform agent loads, so a method change reaches every platform agent through a single gated pin.

## Merge rule
The hub merges every change after its gate (AP-ADR0024, amended by AP-ADR0031).

## Scope
In: the marketplace catalog (`.claude-plugin/marketplace.json`), the GitHub Actions workflows and checks that guard it, the reusable `path-acl` workflow, README and LICENSE.
Also in: the public Agent Skills repo `Screenfields/agent-skills` and its private development repo `Screenfields/agent-skills-dev` (CC-118, https://github.com/Screenfields/alfred-cc-tools/issues/118).
Out: the `ccplugin-*` plugin source repos, and any cluster or GitOps change.

## Public-facing work
Public-facing functionality always goes through the owner: every public release and every new public function needs the owner's approval first. Owner decision of 2026-11-08: https://github.com/Screenfields/alfred-cc-tools/issues/118#issuecomment-6718303941
