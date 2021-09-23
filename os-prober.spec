%define _libexecdir %{_prefix}/libexec
%define lprob linux-boot-prober

Summary:	Probes disks on the system for installed operating systems
Name:		os-prober
Version:	1.78
Release:	1
Group:		System/Configuration/Boot and Init
License:	GPLv2+
Url:		http://kitenet.net/~joey/code/os-prober/
Source0:	http://ftp.de.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.xz
Source1:	%{name}-pamd
# move newns binary outside of os-prober subdirectory, so that debuginfo
# can be automatically generated for it
Patch0:         os-prober-files-path-fix.patch
Patch1:		os-prober-no-dummy-mach-kernel.patch
# Fixes OMA Bug 2300
Patch2:		os-prober-fix-grub-utility-naming.patch
# Sent upstream
Patch3:		os-prober-mdraidfix.patch
#Redundant already upstream Patch4:		os-prober-usrmovefix.patch
Patch7:         os-prober-btrfsfix.patch
Patch8:		os-prober-bootpart-name-fix.patch
Patch9:		os-prober-mounted-partitions-fix.patch
Patch10:	os-prober-factor-out-logger.patch
# To be sent upstream
Patch11:	os-prober-factored-logger-efi-fix.patch
Patch12:	os-prober-umount-fix.patch
Patch13:        os-prober-grub2-parsefix.patch
Patch14:	os-prober-grepfix.patch
Patch15:	os-prober-gentoo-fix.patch
# (tpg) SUSE patches
Patch20:	os-prober-dont-load-all-fs-module-and-dont-test-mount.patch
Patch21:	os-prober-linux-distro-avoid-expensive-ld-file-test.patch
Patch22:	os-prober-linux-distro-parse-os-release.patch
#Fixes OMA bug 2234
Patch23:	microcode-initrd-line-fix.patch
Requires:	coreutils
Requires:	grep
Requires:	sed
Requires:	udev
Requires:	util-linux
Requires:	kmod
%if %mdvver < 201500
Requires:	kmod-compat
%endif

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%autosetup -p1

#find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;
#sed -i -e 's|grub-probe|grub2-probe|g' os-probes/common/50mounted-tests \
#     linux-boot-probes/common/50mounted-tests

%build
%make_build CC=%{__cc} CFLAGS="%{optflags} -Os" LDFLAGS="%{ldflags}"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_sbindir}
install -m 0755 -d %{buildroot}%{_sysconfdir}/pam.d
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}

install -m 0755 -p %{name} %{lprob} %{buildroot}%{_sbindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/os-prober/newns
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
