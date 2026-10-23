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
Out: plugin source, which lives in the `ccplugin-*` repos, and any cluster or GitOps change.
