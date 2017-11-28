# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class PackageSelectorEmptyClient:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        PackageSelector(Id("selector"), Opt("testMode"))
      )
      input = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Input: %1", input)


PackageSelectorEmptyClient().main()

