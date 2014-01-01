#!/usr/bin/python

"""nrvr.distros.el.kickstarttemplates - Templates for creating Enterprise Linux kickstart files

The main class provided by this module is ElKickstartTemplates.

To be expanded as needed.

Idea and first implementation - Leo Baschy <srguiwiz12 AT nrvr DOT com>

Contributor - Nora Baschy

Public repository - https://github.com/srguiwiz/nrvr-commander

Copyright (c) Nirvana Research 2006-2014.
Modified BSD License"""

class ElKickstartTemplates(object):
    """Generally usable templates for Enterprise Linux."""

    # a kickstart file template known to work well with Scientific Linux 6.1 (tested up to 6.4)
    # for creating generally usable servers
    #
    # good chance it will work with other brand Enterprise Linux distributions
    #
    # see http://docs.redhat.com/docs/en-US/Red_Hat_Enterprise_Linux/6/html/Installation_Guide/s1-kickstart2-options.html
    # and http://fedoraproject.org/wiki/Anaconda/Kickstart
    usableElKickstartTemplate001 = r"""# A kickstart file automatically has been generated by anaconda
# from Scientific Linux 6.1, SL-61-i386-2011-07-27-Install-DVD.iso .
#
# Edited manually as needed.
# Could use further automated configuration as needed.
#
install
cdrom
lang en_US.UTF-8
keyboard us
#
# All static networking configuration information must be specified on one line; you cannot wrap lines.
# Could be set to either
# network --device=eth0 --bootproto=static --ip=10.123.45.67 --netmask=255.255.255.0 --gateway=10.123.45.1 --nameserver=10.123.45.1 --hostname=replacethis --noipv6 --onboot=yes --activate
# or
# network --device=eth0 --bootproto=dhcp --hostname=replacethis --noipv6 --onboot=yes --activate
# The "--activate" option has been introduced in Enterprise Linux 6.1.
# Without "--activate" there had been an automation stopping "Select network interface"
# dialog in the installer.
# Hope you don't need to read http://fedoraproject.org/wiki/Anaconda/NetworkIssues.
network --device=eth0 --bootproto=static --ip=10.123.45.67 --netmask=255.255.255.0 --gateway=10.123.45.1 --nameserver=10.123.45.1 --hostname=replacethis --noipv6 --onboot=yes --activate
#
# Should be set.
rootpw --iscrypted $1$sodiumch$UqZCYecJ/y5M5pp1x.7C4/
#
authconfig --enableshadow --enablemd5
#
firewall --enabled --service=ssh
#
selinux --enforcing
#
# Consider whether it needs to be timezone --utc Etc/UTC
timezone --utc Etc/UTC
#
# Inserted to make it work.
zerombr
#
bootloader --location=mbr --driveorder=sda,sdb --append="crashkernel=auto rhgb quiet"
#
# The following is the partition information you requested.
#
# Uncommented and edited to make it work better.
clearpart --all --drives=sda,sdb --initlabel
part /boot --fstype=ext4 --size=500 --ondisk=sda
part swap --size=1 --grow --ondisk=sdb
part pv.008002 --size=1 --grow --ondisk=sda
volgroup VolGroup00 --pesize=4096 pv.008002
logvol / --fstype=ext4 --fsoptions="noatime" --name=LogVol00root --vgname=VolGroup00 --size=1 --grow
#
# Inserted to be sure.
firstboot --disabled
#
# Inserted for automation.
# Else kickstart would display a message and wait for user to press a key for rebooting.
poweroff
#
services --enabled sshd
#
%packages
@base
@client-mgmt-tools
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@misc-sl
@network-file-system-client
@performance
@perl-runtime
@scalable-file-systems
@server-platform
pax
oddjob
sgpio
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
#
%end
#
# Inserted for automation.
%post
#!/bin/bash
#
# Start sshd to trigger initial key generation now.
service sshd on
#
%end"""

    # list of packages and package groups from Scientific Linux 6.4 (generated by anaconda)
    # for creating generally usable machines
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfSL64Minimal = filter(None, """
@client-mgmt-tools
@core
@misc-sl
""".splitlines())

    # list of packages and package groups from Scientific Linux 6.4 (generated by anaconda)
    # for creating generally usable servers
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfSL64BasicServer = filter(None, """
@base
@client-mgmt-tools
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@misc-sl
@network-file-system-client
@performance
@perl-runtime
@server-platform
pax
oddjob
sgpio
device-mapper-persistent-data
samba-winbind
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
""".splitlines())

    # list of packages and package groups from Scientific Linux 6.4 (generated by anaconda)
    # for creating generally usable workstations
    #
    # to boot into graphical login use with kickstart command
    # xconfig --startxonboot
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfSL64MinimalDesktop = filter(None, """
@ice-desktop
@base
@client-mgmt-tools
@core
@basic-desktop
@desktop-platform
@directory-client
@fonts
@input-methods
@internet-browser
@legacy-x
@misc-sl
@network-file-system-client
@print-client
@remote-desktop-clients
@x11
mtools
pax
oddjob
sgpio
device-mapper-persistent-data
samba-winbind
certmonger
pam_krb5
krb5-workstation
xterm
libXmu
""".splitlines())

    # list of packages and package groups from Scientific Linux 6.4 (generated by anaconda)
    # for creating generally usable workstations
    #
    # to boot into graphical login use with kickstart command
    # xconfig --startxonboot
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfSL64Desktop = filter(None, """
@base
@client-mgmt-tools
@core
@debugging
@basic-desktop
@desktop-debugging
@desktop-platform
@directory-client
@fonts
@general-desktop
@graphical-admin-tools
@input-methods
@internet-applications
@internet-browser
@java-platform
@legacy-x
@misc-sl
@network-file-system-client
@office-suite
@print-client
@remote-desktop-clients
@server-platform
@x11
mtools
pax
oddjob
wodim
sgpio
genisoimage
device-mapper-persistent-data
samba-winbind
certmonger
pam_krb5
krb5-workstation
gnome-pilot
libXmu
SL_desktop_tweaks
""".splitlines())

    # list of packages and package groups from Scientific Linux 6.1 (generated by anaconda)
    # for creating generally usable servers
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfTraditionalNrvrCommanderServer = filter(None, """
@base
@client-mgmt-tools
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@misc-sl
@network-file-system-client
@performance
@perl-runtime
@scalable-file-systems
@server-platform
pax
oddjob
sgpio
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
""".splitlines())

    # list of packages and package groups from Scientific Linux 6.1 (generated by anaconda and modified)
    # for creating generally usable servers with GUI
    #
    # to boot into graphical login use with kickstart command
    # xconfig --startxonboot
    #
    # some chance it will work with other brand Enterprise Linux distributions,
    # but watch out for e.g. any names that contain "sl"
    packagesOfTraditionalNrvrCommanderServerWithGui = filter(None, """
@base
@client-mgmt-tools
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@misc-sl
@network-file-system-client
@performance
@perl-runtime
@scalable-file-systems
@server-platform
pax
oddjob
sgpio
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
#
# desktop GUI
@basic-desktop
@desktop-platform
@general-desktop
@x11
#
# some apps
@internet-browser
@office-suite
""".splitlines())
