#!/usr/bin/python

"""To use in developing and testing of cloning and modifying an .iso disk image.

Idea and first implementation - Leo Baschy <srguiwiz12 AT nrvr DOT com>

Public repository - https://github.com/srguiwiz/nrvr-commander

Copyright (c) Nirvana Research 2006-2013.
Modified BSD License"""

from optparse import OptionParser, OptionError
import os.path

from nrvr.diskimage.isoimage import IsoImage

optionsParser = OptionParser(usage="%prog [options] isofile",
                             description=
"""Utility to use in developing and testing of cloning and modifying an .iso disk image.
Exercises nrvr.diskimage.isoimage.IsoImage.cloneWithModifications() without any modifications.""",
                             version="%prog 1.0")
optionsParser.add_option("-j", "--dont-ignore-joliet", action="store_true", dest="dontIgnoreJoliet",
                         help="don't ignore Joliet-extension information, default %default", default=False)
optionsParser.add_option("-k", "--keep-clone", action="store_true", dest="keepClone",
                         help="keep clone when exiting, which uses disk space, default %default", default=False)
(options, args) = optionsParser.parse_args()
if len(args) is not 1:
    raise OptionError("needs exactly one argument, a .iso file")

try:
    isoFile = args[0]
    isoImage = IsoImage(isoFile)
    isoImageClone = isoImage.cloneWithModifications(modifications=[],
                                                    ignoreJoliet=not options.dontIgnoreJoliet)
    print "cloned into %s" % (isoImageClone.isoImagePath)
finally:
    if os.path.exists(isoImageClone.isoImagePath):
        if not options.keepClone:
            print "avoiding disk clogging, now deleting cloned %s" % (isoImageClone.isoImagePath)
            isoImageClone.remove()
        else:
            print "watch your disk space, per --keep-clone nowkeeping cloned %s" % (isoImageClone.isoImagePath)