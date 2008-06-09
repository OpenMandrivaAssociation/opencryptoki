%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	An Implementation of PKCS#11 (Cryptoki) v2.11 
Name:		opencryptoki 
Version:	2.2.4.1
Release:	%mkrel 1
Group:		System/Servers
License:	CPL 
URL:		http://sourceforge.net/projects/opencryptoki 
Source0:	http://downloads.sourceforge.net/opencryptoki/%{name}-%{version}.tar.bz2 
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel 
Requires:	openssl
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The openCryptoki package implements the PKCS#11 version 2.11: Cryptographic 
Token Interface Standard (Cryptoki).

%package -n	%{libname}
Summary:	An Implementation of PKCS#11 (Cryptoki) v2.11 
Group:          System/Libraries

%description -n	%{libname}
The openCryptoki package implements the PKCS#11 version 2.11: Cryptographic 
Token Interface Standard (Cryptoki).

%package -n	%{develname}
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
The openCryptoki package implements the PKCS#11 version 2.11: Cryptographic 
Token Interface Standard (Cryptoki).

This package contains the static %{name} library and its header files.

%prep

%setup -q -n %{name}-%{version}


%build
rm -rf autom4te.cache
%serverbuild
autoreconf --force --install

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_initrddir}
mv %{buildroot}%{_sysconfdir}/init.d/pkcsslotd %{buildroot}%{_initrddir}/pkcsslotd

# cleanup
rm -f %{buildroot}%{_libdir}/%{name}/*.la
rm -f %{buildroot}%{_libdir}/%{name}/stdll/*.la

%pre
/usr/sbin/groupadd -r pkcs11 2>/dev/null || true
/usr/sbin/usermod -G $(/usr/bin/id --groups --name root | /bin/sed -e '
# add the pkcs group if it is missing
/(^| )pkcs11( |$)/!s/$/ pkcs11/
# replace spaces by commas
y/ /,/
'),pkcs11 root

%post
%_post_service pkcsslotd

%preun
%_preun_service pkcsslotd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}*.conf
%attr(0755,root,root) %{_initrddir}/pkcsslotd
%dir %attr(0770,root,pkcs11) /var/lib/%{name}
%attr(0755,root,root) %{_sbindir}/pkcsslotd
%attr(0755,root,root) %{_sbindir}/pkcsconf
%attr(0755,root,root) %{_sbindir}/pkcs_slot
%attr(0755,root,root) %{_sbindir}/pkcs11_startup

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING COPYRIGHTS FAQ LICENSE README TODO doc/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/stdll
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/methods
%attr(755,root,root) %{_libdir}/%{name}/stdll/libpkcs11_*.so*
# symlinks for backward compatibility
%dir %{_libdir}/pkcs11
%dir %{_libdir}/pkcs11/stdll
%dir %{_libdir}/pkcs11/methods
%{_libdir}/pkcs11/PKCS11_API.so
%{_libdir}/%{name}/PKCS11_API.so
%{_libdir}/pkcs11/libopencryptoki.so
%ifarch s390 s390x
%{_libdir}/%{name}/stdll/PKCS11_ICA.so
%else
%{_libdir}/%{name}/stdll/PKCS11_SW.so
%endif

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/apiclient.h
%{_includedir}/%{name}/pkcs11.h
%{_includedir}/%{name}/pkcs11types.h
