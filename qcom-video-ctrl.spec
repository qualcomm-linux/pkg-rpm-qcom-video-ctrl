%global vendor_arch     armv8a

%global algs_incdir     %{_includedir}/iot-core-algs

# The tarball contains an already-stripped shared object.
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

License:        BSD-3-Clause-Clear

Source0:        https://softwarecenter.qualcomm.com/nexus/generic/software/chip/component/iot-core-algs.lnx.0.0/260709/prebuilt_yocto/qcom-video-ctrl_1.0.1_armv8a.tar.gz

ExclusiveArch:  aarch64

# libVideoCtrl.so requires the FastCV runtime.
Requires:       qcom-fastcv-binaries

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
# The vendor archive is a staged rootfs with no top-level directory.
%autosetup -c -n %{name}-%{version} -p1

# Verify the expected payload layout.
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

%install
# Install the staged rootfs under RPM's standard paths.
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_libdir}/pkgconfig
install -d -m 0755 %{buildroot}%{algs_incdir}

# The library has /etc/video-ctrl.ini embedded as its config path.
install -p -m 0644 etc/video-ctrl.ini %{buildroot}%{_sysconfdir}/video-ctrl.ini

cp -a usr/lib/libVideoCtrl.so* %{buildroot}%{_libdir}/
find %{buildroot}%{_libdir} -maxdepth 1 -name 'libVideoCtrl.so.*' -type f \
    -exec chmod 0755 {} +

install -p -m 0644 usr/include/iot-core-algs/videoctrl.h %{buildroot}%{algs_incdir}/

# Repoint the pre-expanded pkg-config paths.
install -p -m 0644 usr/lib/pkgconfig/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i -e 's|^libdir=.*|libdir=%{_libdir}|' \
       -e 's|^includedir=.*|includedir=%{algs_incdir}|' \
       %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%check
:

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
- Initial RPM packaging, qcom-video-ctrl_1.0.1_armv8a prebuilt binary drop
- Ship /etc/video-ctrl.ini as config(noreplace)
