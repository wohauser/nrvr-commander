#!/usr/bin/python

"""nrvr.distros.el.util - Utilities for manipulating Ubuntu

Class provided by this module is ElUtil.

Idea and first implementation - Leo Baschy <srguiwiz12 AT nrvr DOT com>

Public repository - https://github.com/srguiwiz/nrvr-commander

Copyright (c) Nirvana Research 2006-2015.
Simplified BSD License"""

import re

import nrvr.distros.common.util

class UbUtil(nrvr.distros.common.util.LinuxUtil):
    """Utilities for manipulating an Ubuntu installation."""

    @classmethod
    def ubReleaseVersion(cls, isoImagePath):
        """Return release version from isoImagePath."""
        return re.search(r'ubuntu-([0-9]{2}\.[0-9]{2}(?:\.[0-9]+)?)[^/]*\.iso', isoImagePath).group(1);

    @classmethod
    def ubCommandToOpenFirewallPort(cls, port):
        """Build command to open a firewall TCP port.
        
        Must be root to succeed.
        
        As implemented does not check whether firewall is enabled.
        
        Return command to open a firewall TCP port."""
        port = int(port) # precaution
        port = str(port)
        command = "ufw allow " + port + "/tcp"
        return command

    @classmethod
    def _ubCommandToHaveLightDMConfiguration(cls, username=None):
        """Build command to enable configuration of LightDM.
        
        Must be root to succeed.
        
        Return command to enable configuration of LightDM."""
        # in Ubuntu 14.04 LTS first must ensure there is a file /etc/lightdm/lightdm.conf with a section [SeatDefaults]
        return r"if [ ! -f /etc/lightdm/lightdm.conf ] ; then mkdir -p /etc/lightdm ; echo '[SeatDefaults]' > /etc/lightdm/lightdm.conf ; fi"

    @classmethod
    def ubCommandToEnableAutoLogin(cls, username=None):
        """Build command to enable auto-login with LightDM.
        
        Must be root to succeed.
        
        username
            defaults to None, which effects disabling auto-login.
        
        Return command to enable auto-login with LightDM."""
        # see http://www.tuxgarage.com/2011/09/setting-lightdm-to-auto-login-oneiric.html
        command = cls.ubCommandToDisableAutoLogin()
        if username:
            username = re.escape(username) # precaution
            # autologin-user-timeout=0 to avoid https://bugs.launchpad.net/ubuntu/+source/lightdm/+bug/902852
            command += r" ; sed -i -e '/^\[SeatDefaults\]/ a \autologin-user=" + username + r"\nautologin-user-timeout=0' /etc/lightdm/lightdm.conf"
        return command

    @classmethod
    def ubCommandToDisableAutoLogin(cls):
        """Build command to disable auto-login with LightDM.
        
        Must be root to succeed.
        
        Return command to disable auto-login with LightDM."""
        command = cls._ubCommandToHaveLightDMConfiguration()
        command += r" ; sed -i -e '/^\s*autologin-user\s*=/ d' -e '/^\s*autologin-user-timeout\s*=/ d' /etc/lightdm/lightdm.conf"
        return command

    @classmethod
    def ubCommandToDisableGuestLogin(cls):
        """Build command to disable guest login with LightDM.
        
        Must be root to succeed.
        
        Return command to disable guest login with LightDM."""
        command = cls._ubCommandToHaveLightDMConfiguration()
        command += r" ; sed -i -e '/^\s*allow-guest\s*=/ d'  -e '/^\[SeatDefaults\]/ a \allow-guest=false' /etc/lightdm/lightdm.conf"
        return command

    @classmethod
    def ubCommandToEnableGuestLogin(cls):
        """Build command to enable guest login with LightDM.
        
        Must be root to succeed.
        
        Return command to enable guest login with LightDM."""
        command = cls._ubCommandToHaveLightDMConfiguration()
        command += r" ; sed -i -e '/^\s*allow-guest\s*=/ d'  -e '/^\[SeatDefaults\]/ a \allow-guest=true' /etc/lightdm/lightdm.conf"
        return command

if __name__ == "__main__":
    print UbUtil.ubReleaseVersion("/mnt/isos/ubuntu-12.04.4-alternate-i386.iso")
    print UbUtil.commandToAppendAddressNameLineToEtcHosts("127.0.0.1", "myself")
    print UbUtil.ubCommandToOpenFirewallPort(80)
    print UbUtil.ubCommandToOpenFirewallPort("80")
    print UbUtil.commandToWaitForNetworkDevice("eth1",30)
    print UbUtil.ubCommandToEnableAutoLogin("joe")
    print UbUtil.ubCommandToDisableAutoLogin()
    print UbUtil.ubCommandToEnableAutoLogin()
    print UbUtil.ubCommandToDisableGuestLogin()
    print UbUtil.ubCommandToEnableGuestLogin()
