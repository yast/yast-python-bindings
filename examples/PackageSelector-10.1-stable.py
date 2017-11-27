# encoding: utf-8

# Package Selector example
from yast import import_module
import_module('UI')
import_module('Pkg')
from yast import *

class PackageSelector101StableClient:
    def main(self):
      Pkg.SourceCreate(
        "file:/mounts/machcd2/CDs/SUSE-Linux-10.1-RC5-DVD-Retail-i386/DVD1",
        ""
      )


      if False:
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


PackageSelector101StableClient().main()

