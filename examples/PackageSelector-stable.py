# encoding: utf-8

# Package Selector example
from yast import *
class PackageSelectorStableClient:
    def main(self):
      Pkg.SourceCreate("file:/mounts/machcd/CDs/openSUSE-10.2-RC5-FTP-OSS", "")
      useInstalledSystem = True

      if useInstalledSystem:
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


PackageSelectorStableClient().main()

