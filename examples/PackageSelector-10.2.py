# encoding: utf-8

# Package Selector example
from yast import import_module
import_module('UI')
import_module('Pkg')
from yast import *
class PackageSelector102Client:
    def main(self):
      use_installed_system = True

      Pkg.SourceCreate("file:/mounts/dist/full/full-10.2-i386/", "")


      if use_installed_system:
          Pkg.TargetInit("/", False)

      UI.OpenDialog(
        Opt("defaultsize"),
        PackageSelector(Id("selector"), "/dev/fd0")
      )
      button = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Button: %1", button)


PackageSelector102Client().main()

