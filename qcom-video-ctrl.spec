# RPM packaging for the qcom-video-ctrl prebuilt binary drop.
# Target distro: Fedora / RHEL aarch64 (%%{_libdir} == /usr/lib64).

# Architecture tag used in the vendor tarball file name.
%global vendor_arch     armv8a

%global algs_incdir     %{_includedir}/iot-core-algs

# The tarball contains an already-stripped, vendor-validated aarch64 shared
# object. Let RPM neither strip it again, nor try to extract debuginfo from it,
# nor inject /usr/lib/.build-id/* entries into the payload.
%global debug_package                   %{nil}
%global __strip                         /bin/true
%global __brp_strip                     %{nil}
%global __brp_strip_static_archive      %{nil}
%global __brp_strip_comment_note        %{nil}
%global _build_id_links                 none

Name:           qcom-video-ctrl
Version:        1.0.1
Release:        1%{?dist}
Summary:        QCOM library for smart video codec control logic

# Proprietary; redistribution permitted in binary form only. Full text ships in
# the tarball as LICENSE.qcom-2.
License:        LicenseRef-Qualcomm-nologin-binaries
# TODO: set the canonical upstream URL.
URL:            https://www.qualcomm.com/

# TODO: record the exact fetch location/command for this artifact in README.md.
Source0:        https://softwarecenter.qualcomm.com/nexus/generic/software/chip/component/iot-core-algs.lnx.0.0/260709/prebuilt_yocto/qcom-video-ctrl_1.0.1_armv8a.tar.gz

ExclusiveArch:  aarch64

# No BuildRequires: nothing is compiled; the payload is prebuilt. See README.md
# for the from-source rebuild path and its dependencies.

# libVideoCtrl.so links against libfastcvopt, which is not part of the distro.
# The soname dependency is generated automatically from the prebuilt object, so
# a provider must exist in the build/install repositories.
# TODO: confirm the FastCV runtime RPM name for the target distro (Debian used
# qcom-fastcv-binaries | libfastcvopt).
Requires:       qcom-fastcv-binaries
# Alternative, if FastCV is delivered out-of-band (not as an RPM): drop the
# Requires above and filter the auto-generated soname dependency instead:
#%%global __requires_exclude ^libfastcvopt\\.so.*$

# Compatibility with the Debian binary package name.
Provides:       qcom-video-ctrl1 = %{version}-%{release}

%description
QCOM library for smart video codec control logic.

This package contains the prebuilt shared library (libVideoCtrl) implementing
the bitrate, frame-rate, GOP length, ROI tracking and frame-drop decision logic
used for smart video encoding on Qualcomm platforms, together with its runtime
configuration file.

%package devel
Summary:        QCOM library for smart video codec control logic - Development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       qcom-video-ctrl-dev = %{version}-%{release}

%description devel
Development files (public header, pkg-config file and linker symlink) for the
QCOM smart video codec control library.

%prep
# -c is required: the vendor tarball unpacks a staged rootfs with no top-level
# directory (./etc, ./usr, ./CHANGES, ./LICENSE.qcom-2 at the root).
%autosetup -c -n %{name}-%{version} -p1

# Fail loudly if the vendor tarball layout changed, rather than silently
# producing an empty or partial package.
for f in LICENSE.qcom-2 CHANGES etc/video-ctrl.ini \
         usr/lib/libVideoCtrl.so usr/lib/libVideoCtrl.so.1 \
         usr/lib/pkgconfig/%{name}.pc \
         usr/include/iot-core-algs/videoctrl.h; do
    if [ ! -e "$f" ]; then
        echo "ERROR: expected '$f' in %{name}_%{version}_%{vendor_arch}.tar.gz" >&2
        echo "ERROR: the vendor tarball layout changed; update this spec." >&2
        exit 1
    fi
done

%build
# Nothing to build: the tarball ships prebuilt aarch64 binaries only.

%install
# The tarball is a staged rootfs, so %%install is a straight relocation of that
# tree into %%{buildroot}, honouring RPM's %%{_libdir} (= /usr/lib64 on
# Fedora/RHEL aarch64) instead of the vendor's flat /usr/lib.
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_libdir}/pkgconfig
install -d -m 0755 %{buildroot}%{algs_incdir}

# This MUST stay in /etc: the shared object is compiled with
# VCTRL_CONFIG_FILE="<VIDEO_CTRL_CONFIG_DIR>/video-ctrl.ini" baked in, so the
# path is not relocatable.
install -p -m 0644 etc/video-ctrl.ini %{buildroot}%{_sysconfdir}/video-ctrl.ini

# cp -a preserves the .so -> .so.1 -> .so.1.0 symlink chain and the vendor
# mtimes/permissions.
cp -a usr/lib/libVideoCtrl.so* %{buildroot}%{_libdir}/
# 0755, matching the install PERMISSIONS upstream CMake uses for the target.
find %{buildroot}%{_libdir} -maxdepth 1 -name 'libVideoCtrl.so.*' -type f \
    -exec chmod 0755 {} +

install -p -m 0644 usr/include/iot-core-algs/videoctrl.h %{buildroot}%{algs_incdir}/

# The .pc file is shipped pre-expanded with libdir/includedir hardcoded to
# ${prefix}/lib, which is wrong on a lib64 distro - retarget them.
install -p -m 0644 usr/lib/pkgconfig/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i -e 's|^libdir=.*|libdir=%{_libdir}|' \
       -e 's|^includedir=.*|includedir=%{algs_incdir}|' \
       %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Deliberately NOT copied: usr/share/doc/qcom-video-ctrl/ from the tarball.
# %%doc and %%license below install CHANGES and LICENSE.qcom-2 into RPM's own
# %%{_docdir}/%%{name}-%%{version} and %%{_licensedir} locations; copying the
# vendor tree as well would duplicate both files and leave an unowned directory.

%check
:

# Spelled out instead of using %%ldconfig_scriptlets so the spec also parses on
# rpm builds that do not ship the Fedora macro set.
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.qcom-2
%doc CHANGES
%config(noreplace) %{_sysconfdir}/video-ctrl.ini
%{_libdir}/libVideoCtrl.so.1
%{_libdir}/libVideoCtrl.so.1.0

%files devel
%dir %{algs_incdir}
%{algs_incdir}/videoctrl.h
%{_libdir}/libVideoCtrl.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Aug 06 2026 Viswanath Srikanth Bathina <bathina@qti.qualcomm.com> - 1.0.1-1
- Initial RPM packaging, converted from the Debian packaging in
  iot-core-algs/qti-video-ctrl/debian
- Package the qcom-video-ctrl_1.0.1_armv8a prebuilt binary drop
- Ship /etc/video-ctrl.ini as config(noreplace)
