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
