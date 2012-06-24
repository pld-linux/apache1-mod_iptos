%define		mod_name	iptos
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: assign IPTOS bits to different vhosts or directories
Summary(pl):	Modu� Apache'a: przypisywanie bit�w IPTOS do r�nych vhost�w i katalog�w
Name:		apache1-mod_%{mod_name}
Version:	1.1
Release:	0.1
License:	Apache 1.1
Group:		Networking/Daemons
Source0:	http://www.arctic.org/~dean/mod_iptos/libapache-mod-%{mod_name}_%{version}.orig.tar.gz
# Source0-md5:	1e5582acf63b6fabf567ecb79e57bdd5
URL:		http://www.arctic.org/~dean/mod_iptos/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Modify IPTOS bits on outbound data for fine-tuned traffic shaping.
mod_iptos is a module for Apache 1.3.x which allows the admin to
assign different IPTOS bits to different vhosts or directories. This
can be used in combination with traffic shaping to give much better
control (than other userland-only solutions such as mod_bandwidth)
over the bandwidth for various portions of a website.

%description -l pl
Modu� ten ma na celu modyfikowanie bit�w IPTOS danych wychodz�cych w
celu poprawienia mo�liwo�ci ograniczania pasma. mod_iptos to modu� dla
Apache'a 1.3.x umo�liwiaj�cy przypisywanie r�nych bit�w IPTOS do
r�nych vhost�w i katalog�w. Mo�na to wykorzysta� w po��czeniu z
ograniczaniem ruchu w celu lepszej kontroli (ni� inne rozwi�zania
dzia�aj�ce wy��cznie w przestrzeni u�ytkownika, takie jak
mod_bandwidth) nad pasmem dla r�nych cz�ci serwisu WWW.

%prep
%setup -q -n libapache-mod-%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README debian/changelog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
