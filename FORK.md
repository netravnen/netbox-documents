# Fork branch model

This repository is a fork of
[jasonyates/netbox-documents](https://github.com/jasonyates/netbox-documents).

| Branch | Content |
| --- | --- |
| `main` | Identical to upstream `main`. Never commit to it. |
| `patches/main` | Our patch set, rebased on top of upstream `main`. |

All our changes go into `patches/main` as a linear series of commits on
top of upstream `main`. Open topic branches from `patches/main` and open
pull requests into `patches/main`. Merge them with "Rebase and merge", so
the series stays linear.

## Automatic sync

`.github/workflows/upstream-sync.yml` runs every day and on demand:

1. It rebases `patches/main` onto upstream `main`. Patches that upstream
   has merged drop out of the series.
2. It runs the plugin tests against each NetBox version in its matrix.
3. If the tests pass, it force-pushes the rebased `patches/main`.
4. It moves `main` to upstream `main`.

If the rebase or the tests fail, the run fails and nothing is pushed.
GitHub sends a failure notification for the scheduled run.

The push steps use the `SYNC_TOKEN` secret when it exists. It must be a
token with Contents and Workflows write access to this repository.
`GITHUB_TOKEN` cannot push commits that change `.github/workflows/`.

## Manual sync

Do this when the automatic rebase fails:

```bash
git fetch upstream
git switch patches/main
git rebase upstream/main
git push --force-with-lease origin patches/main
```

Rebase open topic branches onto the new `patches/main` after each sync.
