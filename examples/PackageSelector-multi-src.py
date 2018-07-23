from __future__ import unicode_literals
# encoding: utf-8

# Package Selector example
from yast import import_module
import_module('UI')
import_module('Pkg')
from yast import *
class PackageSelectorMultiSrcClient:
    def main(self):
      Pkg.SourceCreate("file:/srv/sles-10-i386/CD1/", "")
      Pkg.SourceCreate("file:/srv/10.1-i386/CD1/", "")
      # Pkg::SourceCreate( "http://ftp.uni-erlangen.de/pub/mirrors/packman/suse/10.0/", "" );
      # Pkg::SourceCreate( "ftp://ftp.gwdg.de/pub/linux/misc/packman/suse/10.0/", "" );
      Pkg.TargetInit("/", False) # installed system

      UI.OpenDialog(
        Opt("defaultsize"),
        PackageSelector(
          Id("selector"),
          Opt("repoMode"),
          # `opt(`testMode),
          "/dev/fd0"
        )
      )
      input = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Input: %1", input)


PackageSelectorMultiSrcClient().main()

