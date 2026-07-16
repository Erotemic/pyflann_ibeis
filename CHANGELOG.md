# Changelog

We are currently working on porting this changelog to the specifications in
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version 2.5.1 - Unreleased


## Version 2.5.0 - Released 2026-07-16

### Added
* Python 3.14 support (wheels, classifiers, and CI)

### Changed
* Deployment moved out of `tests.yml` into an xcookie-generated
  `.github/workflows/release.yml` (the workflow filename the PyPI/TestPyPI
  trusted publishers are registered against). Releases are cut by pushing to
  the `release` branch; CI tags `v$VERSION` on success. `tests.yml` now only
  lints, builds, and tests on `main` and PRs.
* Wheels are now built once per platform and tagged `py3-none`. The bindings
  are pure ctypes (no extension module), so the binaries never depended on the
  Python version; previously an identical wheel was rebuilt for each CPython.
* Wheels no longer bundle the unused C++ library (`libflann_cpp*`), static
  archives, or duplicate SOVERSION copies of `libflann`; only the shared
  C-bindings library that the ctypes layer loads is shipped. This roughly
  quarters the uncompressed wheel size and halves native compile time
  (which was doubled again on MSVC by the static+shared rebuild).
* CI: pushes to PR branches no longer trigger a second duplicate run; vcpkg
  lz4 binaries are cached on Windows; the full test suite runs once per wheel
  in the dedicated test jobs instead of also inside cibuildwheel, which now
  runs a quick import/load smoke test instead.
* PyPI uploads now use trusted publishing (OIDC via `gh-action-pypi-publish`
  and the `pypi`/`testpypi` GitHub environments) instead of encrypted twine
  API tokens. Artifacts are still GPG signed, but the signing keys now live
  as environment-scoped GitHub secrets (`ci_gpg_secret_transport =
  "direct_ci"`); the encrypted key files were removed from `dev/` and the
  imported key is verified against the fingerprint pinned in
  `dev/public_gpg_key` before signing.

### Fixed
* Restored the `tests-strict`, `runtime-strict`, and `optional-strict` extras
  that were lost in the move from dynamic setup.py metadata to static
  pyproject metadata. The strict CI legs had been silently installing no test
  dependencies and failing with "No module named pytest".

### Removed
* Dropped support for Python 3.9 and 3.10; the minimum supported Python is now 3.11


## Version 2.4.2 - Released 2026-01-21

### Fixed:
* CI on windows
* respect `centers_init` in kmeans


## [Version 2.4.1] - Released 202x-xx-xx

### Fixed
* Seed random numbers in tests

## [Version 2.4.0] - Released 2024-04-18

### Added
* Python 3.12 support.

### Fixed:
* Removed codecov from test req


## [Version 2.3.0] - Released 2023-01-28

### Changed
* Added Python 3.11 support

## [Version 0.0.1] -

### Added
* Initial version
