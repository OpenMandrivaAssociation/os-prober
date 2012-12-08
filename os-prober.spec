%define _libexecdir %{_prefix}/libexec
%define lprob linux-boot-prober

Name:           os-prober
Version:        1.56
Release:        4
Summary:        Probes disks on the system for installed operating systems

Group:          System/Configuration/Boot and Init
License:        GPL+
URL:            http://kitenet.net/~joey/code/os-prober/
Source0:        http://ftp.de.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.gz
Source1:        %{name}-pamd
# move newns binary outside of os-prober subdirectory, so that debuginfo
# can be automatically generated for it
Patch0:         os-prober-newnsdirfix.patch
Patch1:         os-prober-bsd-detection.patch
Patch2:         os-prober-linux-detection.patch
Patch3:		os-prober-missed-os-fix.patch

Requires:       udev coreutils util-linux
Requires:       grep
Requires:		sed
Requires:		module-init-tools

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;

%build
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_sbindir}
install -m 0755 -d %{buildroot}%{_sysconfdir}/pam.d
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}

install -m 0755 -p %{name} %{lprob} %{buildroot}%{_sbindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/newns
install -m 0644 -Dp common.sh %{buildroot}%{_datadir}/%{name}/common.sh

for probes in os-probes os-probes/mounted os-probes/init \
              linux-boot-probes linux-boot-probes/mounted; do
        install -m 755 -d %{buildroot}%{_libexecdir}/$probes 
        cp -a $probes/common/* %{buildroot}%{_libexecdir}/$probes
        if [ -e "$probes/x86" ]; then
    	    cp -a $probes/x86/* %{buildroot}%{_libexecdir}/$probes 
	fi
done
install -m 755 -p os-probes/mounted/powerpc/20macosx \
    %{buildroot}%{_libexecdir}/os-probes/mounted

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{lprob}

ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{lprob}

%files
%doc README TODO debian/copyright debian/changelog
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}
%{_var}/lib/%{name}
%{_sysconfdir}/pam.d/*

