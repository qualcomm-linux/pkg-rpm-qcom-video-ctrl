%global vendor_arch     armv8a

%global algs_incdir     %{_includedir}/qimsdk-smartvenc

# The tarball contains an already-stripped shared object.
%global debug_package                   %{nil}
%global __strip                         /bin/true
%global __brp_strip                     %{nil}
%global __brp_strip_static_archive      %{nil}
%global __brp_strip_comment_note        %{nil}
%global _build_id_links                 none

Name:           qcom-video-ctrl
Version:        1.0.2
Release:        1%{?dist}
Summary:        QCOM library for smart video codec control logic

License:        BSD-3-Clause-Clear

Source0:        https://softwarecenter.qualcomm.com/nexus/generic/software/chip/component/iot-core-algs.lnx.0.0/260814/prebuilt_yocto/qcom-video-ctrl_1.0.2_armv8a.tar.gz

ExclusiveArch:  aarch64

# libqimsdk-smartvenc.so requires the FastCV runtime.
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
for f in LICENSE.qcom-2 CHANGES etc/qimsdk-smartvenc.ini \
         usr/lib/libqimsdk-smartvenc.so usr/lib/libqimsdk-smartvenc.so.1 \
         usr/lib/pkgconfig/qimsdk-smartvenc.pc \
         usr/include/qimsdk-smartvenc/videoctrl.h; do
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

# The library has /etc/qimsdk-smartvenc.ini embedded as its config path.
install -p -m 0644 etc/qimsdk-smartvenc.ini %{buildroot}%{_sysconfdir}/qimsdk-smartvenc.ini

cp -a usr/lib/libqimsdk-smartvenc.so* %{buildroot}%{_libdir}/
find %{buildroot}%{_libdir} -maxdepth 1 -name 'libqimsdk-smartvenc.so.*' -type f \
    -exec chmod 0755 {} +

install -p -m 0644 usr/include/qimsdk-smartvenc/videoctrl.h %{buildroot}%{algs_incdir}/

# Repoint the pre-expanded pkg-config paths.
install -p -m 0644 usr/lib/pkgconfig/qimsdk-smartvenc.pc \
    %{buildroot}%{_libdir}/pkgconfig/qimsdk-smartvenc.pc
sed -i -e 's|^libdir=.*|libdir=%{_libdir}|' \
       -e 's|^includedir=.*|includedir=%{algs_incdir}|' \
       %{buildroot}%{_libdir}/pkgconfig/qimsdk-smartvenc.pc

%check
:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.qcom-2
%doc CHANGES
%config(noreplace) %{_sysconfdir}/qimsdk-smartvenc.ini
%{_libdir}/libqimsdk-smartvenc.so.1
%{_libdir}/libqimsdk-smartvenc.so.1.0

%files devel
%dir %{algs_incdir}
%{algs_incdir}/videoctrl.h
%{_libdir}/libqimsdk-smartvenc.so
%{_libdir}/pkgconfig/qimsdk-smartvenc.pc


%changelog
* Mon Oct 05 2026 Viswanath Srikanth Bathina <bathina@qti.qualcomm.com> - 1.0.2-1
- Initial RPM packaging
- Package the qcom-video-ctrl_1.0.2_armv8a prebuilt binary drop
- Ship /etc/qimsdk-smartvenc.ini as config(noreplace)
