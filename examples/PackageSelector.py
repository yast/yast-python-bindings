# encoding: utf-8

# Package Selector example
from yast import import_module
import_module('UI')
import_module('Pkg')
from yast import *
class PackageSelectorClient:
    def main(self):
      # Pkg::SourceCreate( "http://dist.suse.de/install/SLP/SUSE-10.1-Beta7/i386/CD1/", "" );
      # Pkg::SourceCreate( "http://dist.suse.de/install/SLP/SUSE-10.0-RC4/i386/CD1/", "" );
      # Pkg::SourceCreate( "file:/srv/10.1-i386/CD1/", "" );
      Pkg.SourceCreate("file:/srv/10.1-i386/DVD1/", "")
      # Pkg::SourceCreate( "file:/srv/sles-10-i386/CD1/", "" );

      if True:
        Pkg.TargetInit(
          "/", # installed system
          False
        ) # don't create a new RPM database

      UI.OpenDialog(
        Opt("defaultsize"),
        PackageSelector(Id("selector"), "/dev/fd0")
      )
      input = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Input: %1", input)


PackageSelectorClient().main()

