* Decide on a new version number following semantic versioning
* Update `dqmj1_info/meta_info.py`
* Update `pyproject.toml`
* Update `CHANGELOG.md`
* Create a new tag and push it
```bash
git tag vX.Y.Z -a "vX.Y.Z"
git push origin vX.Y.Z
```
* Create a new release cotnaining the compiled binaries from the GitHub Actions run