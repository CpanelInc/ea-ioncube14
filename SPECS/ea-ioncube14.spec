%global _missing_build_ids_terminate_build 0

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _parent_prefix %ns_dir

%global inifile 01-ioncube.ini

Name:    %{parent_prefix}php-ioncube14
Vendor:  cPanel, Inc.
Summary: v14 Loader for ionCube-encoded PHP files
Version: 14.0.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 2
Release: %{release_prefix}%{?dist}.cpanel
License: Redistributable
Group:   Development/Languages
URL:     http://www.ioncube.com/loaders.php

# 1. See `perldoc find-latest-version` for info on the tarball.
# 2. The archive contains the license file, so no need to have it as a
#    separate source file.
Source: ioncube_loaders_lin_x86-64.tar.gz

Provides:      %{parent_prefix}ioncube = 14
Conflicts:     %{parent_prefix}php-ioncube
Conflicts:     %{?parent_prefix}ioncube

# Don't provide extensions as shared library resources
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}

%description
The v14 ionCube Loader enables use of ionCube-encoded PHP files running
under PHP %{php_version}.

%prep
%setup -q -n ioncube

%build
# Nothing to do here, since it's a binary distribution.

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -d -m 755 $RPM_BUILD_ROOT%{php_docdir}

install -m 755 ioncube_loader_lin_%{php_version}.so $RPM_BUILD_ROOT%{php_extdir}
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{php_docdir}
install -m 644 README.txt $RPM_BUILD_ROOT%{php_docdir}

# The ini snippet
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
cat > $RPM_BUILD_ROOT%{php_inidir}/%{inifile} <<EOF
; Enable v12 IonCube Loader extension module
zend_extension="%{php_extdir}/ioncube_loader_lin_%{php_version}.so"
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{php_docdir}
%dir %{php_docdir}
%config(noreplace) %{php_inidir}/%{inifile}
%{php_extdir}/ioncube_loader_lin_%{php_version}.so

%changelog
* Mon Jan 06 2025 Chris Castillo <c.castillo@cpanel.net> - 14.0.0-2
- ZC-12409: Fix conflicts with other ionCube versions.

* Wed Sep 11 2024 Julian Brown <julian.brown@cpanel.net> - 14.0.0-1
- ZC-12253: Initial Release

