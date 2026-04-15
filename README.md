# kysc-components

Shared Jinja + Tailwind component library for the kevinsykes.ai ecosystem — powers the main site, demo generator, and per-client exported sites.

**Status:** v0.1.0 — scaffold. Only one trivial block (`nav`) ships; full block set arrives in Sprint 2.

## Ownership

This repo lives under the `kevinhsykes` personal GitHub account for now. A `kysc/` GitHub organization may be created later; when that happens the repo moves via GitHub's transfer flow and consumers update their install URL. All existing tags remain valid — the transfer preserves history.

**Visibility:** public. The library contains no secrets or client data; publishing it openly simplifies `pip install git+https://...` from exported client-site Cloud Run builds (no token plumbing needed).

## Install

Pin to an exact tag — never use `main`:

```bash
pip install git+https://github.com/kevinhsykes/kysc-components.git@v0.1.0
```

In `requirements.txt`:

```
kysc_components @ git+https://github.com/kevinhsykes/kysc-components.git@v0.1.0
```

## Semver discipline

This is the load-bearing contract for every consumer (main site, demo generator, client exports).

| Change type | Bump |
|-------------|------|
| Any block template content change (even whitespace that alters render) | **minor** |
| Adding a new block | **minor** |
| Removing a block, renaming a block, changing a block's required context variables | **major** |
| Tailwind preset additions that don't conflict | **minor** |
| Tailwind preset removals or renames | **major** |
| README / comment / test-only changes | **patch** |

**Hard rule:** no tag is ever force-pushed or deleted. Consumers pin to specific tags and expect them to be immutable. If you ship a broken tag, publish a new one — never mutate.

## Adding a new block

1. Create `kysc_components/blocks/<name>.html` — Jinja template. Accept context variables; document them at the top in a `{# #}` comment.
2. Register in `kysc_components/registry.py` — add the slug to the `blocks()` list.
3. Add a render test in `tests/` that asserts the block renders without error against representative context.
4. Bump the version in `pyproject.toml` AND `kysc_components/__init__.py` (they must match).
5. Tag the release: `git tag vX.Y.Z && git push --tags`. CI publishes a GitHub Release automatically.

## Consumer upgrade path

Consumers (kevinsykes-ai main app, kysc-templates, exported client sites) pin exact versions. To upgrade:

1. Read the release notes for breaking changes.
2. Bump the pin.
3. Run the consumer's test suite against the new pin.
4. If tests pass, deploy. If not, stay on the old pin until reconciled.

Client-exported sites should update ONLY when there's a reason — stability beats currency for paid client work.

## License

MIT — see LICENSE.
