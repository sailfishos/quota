Name:       quota
Version:    4.05
Release:    1
Summary:    System administration tools for monitoring users' disk usage
# quota_nld.c, quotaio_xfs.h:       GPLv2
# bylabel.c copied from util-linux: GPLv2+
# doc/quotas.ms, edquota.c:         BSD
# COPYING:                          GPLv2 text and license declaration
## Unpackaged in Sailfish
# warnquota.c:                      GPLv2+
# rquota_server.c:                  GPLv2+
# rquota_svc.c:                     GPLv2+
# svc_socket.c copied from glibc:   LGPLv2+
# po/cs.po:                         GPLv2+
## Not involved in any binary package
# aclocal.m4:                       FSFULLR and (GPLv2+ with exception)
# ar-lib:                           GPLv2 with exception
# depcomp:                          GPLv2+ with exception
# compile:                          GPLv2+ with exception
# config.guess:                     GPLv3+ with exception
# config.rpath:                     GPLv2+ with exception
# config.sub:                       GPLv3+ with exception
# configure:                        FSFUL
# install-sh:                       MIT and Public Domain
# m4/gettext.m4:                    GPL with exception
# m4/iconv.m4:                      GPL with exception
# m4/lib-ld.m4:                     GPL with exception
# m4/lib-link.m4:                   GPL with exception
# m4/lib-prefix.m4:                 GPL with exception
# m4/nls.m4:                        GPL with exception
# m4/po.m4:                         GPL with exception
# m4/progtest.m4:                   GPL with exception
# Makefile.in:                      FSFULLR
# missing:                          GPLv2+ with exception
# mkinstalldirs:                    Public Domain
License: BSD and GPLv2 and GPLv2+
URL: https://github.com/sailfishos/quota
Source0: %{name}-%{version}.tar.gz
Source1: quota_nld.service
Source2: 01-start-before-services.conf

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bash
BuildRequires: coreutils
BuildRequires: e2fsprogs-devel
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: make
BuildRequires: pkgconfig(com_err)
BuildRequires: pkgconfig(ext2fs)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libnl-3.0) >= 3.1
BuildRequires: pkgconfig(libnl-genl-3.0)

Requires: %{name}-minimal = %{version}-%{release}

%description
The quota package contains system administration tools for monitoring
and limiting user and or group disk usage per file system.

%package minimal
Summary: Minimal set of quota tools

%description minimal
Allows to create and update quota files and enable quota on filesystem. See
%{name} for a full set of quota tools.

%package nld
Summary:    quota_nld daemon
License:    GPLv2 and GPLv2+
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description nld
Daemon that listens on netlink socket and processes received quota warnings.
The daemon supports forwarding warning messages to the system D-Bus (so that
desktop manager can display a dialog) and writing them to the terminal user
has last accessed.

%package doc
Summary:    Additional documentation for disk quotas
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch
AutoReq:    0

%description doc
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream
# Regenerate build scripts
autoreconf -f -i

%build
%global _hardened_build 1
%configure \
    --enable-bsd-behaviour \
    --enable-ext2direct=yes \
    --enable-ldapmail=no \
    --disable-libwrap \
    --enable-netlink=yes \
    --disable-nls \
    --disable-rpath \
    --disable-rpc \
    --disable-rpcsetquota \
    --disable-silent-rules \
    --disable-xfs-roothack
%{make_build}

%install
%{make_install}
rm -rf %{buildroot}/%{_docdir}/%{name}

install -p -m644 -D %{SOURCE1} %{buildroot}/%{_unitdir}/quota_nld.service
install -p -d %{buildroot}/%{_unitdir}/multi-user.target.wants/
ln -s ../quota_nld.service %{buildroot}/%{_unitdir}/multi-user.target.wants/

mkdir -p %{buildroot}/%{_unitdir}/quota@home.service.d
install -p -m644 -D %{SOURCE2} %{buildroot}/%{_unitdir}/quota@home.service.d/

mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m644 -t %{buildroot}/%{_docdir}/%{name}-%{version} Changelog doc/*

%post nld
%systemd_post quota_nld.service

%preun nld
%systemd_preun quota_nld.service

%postun nld
%systemd_postun_with_restart quota_nld.service

%files
%{_bindir}/quota
%{_bindir}/quotasync
%{_sbindir}/convertquota
%{_sbindir}/edquota
%{_sbindir}/quotastats
%{_sbindir}/repquota
%{_sbindir}/setquota
%{_sbindir}/xqmstats
# Skip warnquota
%exclude %{_sysconfdir}/quotagrpadmins
%exclude %{_sysconfdir}/quotatab
%exclude %{_sysconfdir}/warnquota.conf
%exclude %{_sbindir}/warnquota

%files minimal
%license COPYING
%{_sbindir}/quotacheck
%{_sbindir}/quotaon
%{_sbindir}/quotaoff
%{_unitdir}/quota@home.service.d/01-start-before-services.conf

%files nld
%license COPYING
%{_unitdir}/quota_nld.service
%{_unitdir}/multi-user.target.wants/quota_nld.service
%{_sbindir}/quota_nld

%files doc
%doc %{_docdir}/%{name}-%{version}
%{_mandir}/man?/*
