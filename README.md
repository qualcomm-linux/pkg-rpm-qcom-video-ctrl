<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-qcom-video-ctrl

RPM packaging for the Qualcomm® Linux smart video codec control library and
development files.

This repository contains RPM packaging rules for the `qcom-video-ctrl`
prebuilt release. The package provides the `libVideoCtrl` runtime library,
public `videoctrl.h` header, `pkg-config` metadata, and the
`/etc/video-ctrl.ini` runtime configuration used by Qualcomm Linux smart video
encoding consumers.

The prebuilt archive is fetched during the RPM build from Qualcomm Software
Center. This repository contains no compiled libraries, binaries, or source
archives.

The `main` branch contains repository documentation and workflow support files.

## License

This project is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.
