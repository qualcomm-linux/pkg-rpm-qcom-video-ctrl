<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-qcom-video-ctrl

RPM packaging for the Qualcomm Linux smart video codec control library and
development files.

This repository contains RPM packaging rules for the `qcom-video-ctrl`
prebuilt binary release. It builds the `libVideoCtrl` runtime library, the
public `videoctrl.h` header, `pkg-config` metadata, and the
`/etc/video-ctrl.ini` runtime configuration used by Qualcomm Linux smart video
encoding consumers.

The prebuilt archive is fetched during the RPM build from Qualcomm Software
Center. This repository contains no compiled libraries, binaries, or source
archives. The `c10s` branch contains the RPM packaging files, while the `main`
branch contains repository documentation and workflow support files.

## Repository Layout

| File | Purpose |
|---|---|
| `qcom-video-ctrl.spec` | Builds the runtime and development RPM packages. |
| `sources` | SHA-512 checksum for the prebuilt `qcom-video-ctrl` archive. |
| `.github/workflows/build-on-pr.yml` | Builds the RPM packages for pull requests. |
| `.github/workflows/pkg-release.yml` | Builds and publishes release RPMs. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

The vendor archive is not committed to this repository. `Source0` in the spec
points to the Qualcomm Software Center artifact, and the checksum in `sources`
is verified before the RPM is built.

## Packages

### `qcom-video-ctrl`

Runtime package containing the `libVideoCtrl` shared library, its
`/etc/video-ctrl.ini` configuration file, and the package documentation. The
library implements bitrate, frame-rate, GOP-length, ROI-tracking, and frame-drop
decision logic used by Qualcomm smart video encoding consumers.

The package is built for `aarch64` and depends on `qcom-fastcv-binaries` for the
FastCV runtime required by `libVideoCtrl`.

### `qcom-video-ctrl-devel`

Development package providing the public
`/usr/include/iot-core-algs/videoctrl.h` header, the
`/usr/lib64/pkgconfig/qcom-video-ctrl.pc` file, and the unversioned linker
symlink needed to build applications against `libVideoCtrl`.

The packages contain prebuilt vendor binaries; the RPM build does not compile
the library or generate debug symbols.

## Installation

Install the runtime and development packages from the configured CentOS Stream
10 repository:

```bash
sudo dnf install -y qcom-video-ctrl qcom-video-ctrl-devel
```

## Local usage

The `build-on-pr.yml` build can be reproduced on an **aarch64** host with
`docker`, `git`, `curl`, and `bash`. The steps below mirror the
`pkg-build-reusable-workflow.yml` job in
[`qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils). Step 1
checks out the `c10s` branch; run the later steps from the **repository root**.

1. Clone this repository, check out the `c10s` packaging branch, then fetch the
   build tooling and build the builder image. CI pulls the same image from GHCR;
   building it locally avoids the GHCR login:

   ```sh
   git clone https://github.com/qualcomm-linux/pkg-rpm-qcom-video-ctrl.git
   cd pkg-rpm-qcom-video-ctrl
   git checkout c10s
   git clone https://github.com/qualcomm-linux/qcom-rpm-utils.git tool
   docker build -f tool/docker/Dockerfile.rpm-builder -t rpm-builder:centos10 tool/docker/
   ```

2. Resolve the source archive against `sources`. `resolve-sources.sh` appends
   to `$GITHUB_OUTPUT`, so start from an empty file:

   ```sh
   export GITHUB_OUTPUT="$PWD/resolve_sources_output.env"
   : > "$GITHUB_OUTPUT"
   tool/scripts/resolve-sources.sh \
     --sources sources \
     --spec qcom-video-ctrl.spec \
     --cache-base-url https://dummy_url \
     --dest "$PWD/sources-cache"
   # tarballs= is an unquoted, space-separated list; sourcing the file would
   # run every path after the first as a command, so read the values instead.
   tarball="$(sed -n 's/^tarball=//p' "$GITHUB_OUTPUT")"
   tarballs="$(sed -n 's/^tarballs=//p' "$GITHUB_OUTPUT")"
   ```

   The lookaside cache is tried first. On a miss, the archive is downloaded from
   the spec's `Source0` (Qualcomm Software Center), and in both cases it is verified against
   the checksum in `sources`.

3. Build:

   ```sh
   tool/scripts/build-rpm.sh \
     --tarball "$tarballs" \
     --spec qcom-video-ctrl.spec \
     --output output \
     --builder-image rpm-builder:centos10
   ```

   The package has no cross-package `BuildRequires`. `qcom-fastcv-binaries` is
   only a runtime `Requires`, so it is not needed to build.

   `build-rpm.sh` copies every file beside the spec into the build workspace,
   so the spec can be built straight from the repository root.

Binary and source RPMs are written to `output/`. Nothing is uploaded; publishing
happens only through `pkg-release.yml`. The build leaves `tool/`,
`sources-cache/`, `output/`, and `resolve_sources_output.env` in the repository
root; they are not part of the package and can be deleted.

## Updating the Package Version

1. Update `Version:` in `qcom-video-ctrl.spec` and update `Source0` if the
   vendor archive path changes. The archive filename must remain
   `qcom-video-ctrl_<version>_armv8a.tar.gz`.
2. Confirm that the staged archive still contains the files validated by the
   `%prep` checks in the spec.
3. Regenerate the source checksum:

   ```bash
   sha512sum --tag qcom-video-ctrl_<version>_armv8a.tar.gz > sources
   ```

4. Commit the spec and `sources`, then open a pull request against `c10s`.
5. After the pull request is merged, run `pkg-release.yml` to publish the
   RPMs.

## License

This packaging repository is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.

The vendor binary payload is distributed under Qualcomm's binary license. The
`LICENSE.qcom-2` file from the vendor archive is included in the runtime RPM.
