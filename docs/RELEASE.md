# Release

`lumid-hooks` publishes one distribution:

| Distribution | Source |
|--------------|--------|
| `lumid-hooks` | `pyproject.toml` |

## PyPI setup

Use PyPI Trusted Publishing instead of long-lived API tokens. Configure pending
or active trusted publishers for `lumid-hooks` on both PyPI and TestPyPI.

Use this publisher configuration:

| Setting | Value |
|---------|-------|
| Owner | `mlsys-io` |
| Repository | `lumid.hooks` |
| Workflow | `release.yml` |
| Environment | `pypi` for PyPI, `testpypi` for TestPyPI |

Create matching GitHub environments named `pypi` and `testpypi`. The `pypi`
environment should require manual approval. The approver should verify the
matching TestPyPI run before approving production publishing.

## Prepare a release

1. Update the package version in `pyproject.toml`.
2. Re-lock:

   ```bash
   uv lock
   ```

3. Validate locally:

   ```bash
   uv sync --group dev --frozen
   uv run pytest -q
   uv build --out-dir dist
   uv run scripts/ci/check_package_build.py --dist dist
   ```

4. Open and merge a release prep PR with the version bump and `uv.lock`.

## Publish to TestPyPI

After the release prep PR lands, create and push a signed or annotated tag:

```bash
git tag -a v0.1.0 -m "chore: release v0.1.0"
git push origin v0.1.0
```

Run the `Release` workflow manually:

```bash
gh workflow run release.yml -f tag=v0.1.0 -f publish_target=testpypi
```

Then verify the published artifact from TestPyPI in a fresh environment:

```bash
python -m venv .venv-testpypi
. .venv-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lumid-hooks
python -c "from lumid_hooks import BaseBindings, HookBindings; assert isinstance(BaseBindings(), HookBindings)"
```

## Publish to PyPI

Create a GitHub Release from the same `vX.Y.Z` tag. Publishing the release
triggers `.github/workflows/release.yml`, which rebuilds from the tag, runs
tests, smoke-tests the wheel, and publishes the uploaded artifact set to PyPI
after the `pypi` environment approval.

Do not move or force-update release tags. The release workflow assumes the tag
already passed PR or main-branch CI.

After publishing, verify PyPI installs in a fresh environment:

```bash
python -m venv .venv-pypi
. .venv-pypi/bin/activate
python -m pip install --upgrade pip
python -m pip install lumid-hooks
python -c "from lumid_hooks import BaseBindings, HookBindings; assert isinstance(BaseBindings(), HookBindings)"
```

## If a release goes wrong

PyPI versions are immutable: once `vX.Y.Z` is published you cannot edit,
re-upload, or replace it. Recovery options:

- **Yank** the bad release on PyPI. `pip install` still installs the version
  when it is explicitly pinned, but resolution skips it otherwise. Use yank
  for security or correctness bugs that warrant skipping the version
  entirely.
- **Cut the next patch.** Bump to `vX.Y.(Z+1)`, fix forward, and publish.
  This is the default path for any non-critical bug.
- **`.postN` re-release** of the same source release when the only change is
  packaging metadata (LICENSE, classifiers, README) and no Python code
  changed. Rare.

Do not delete or reuse a published version number under any circumstance.
