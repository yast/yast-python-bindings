# encoding: utf-8

# YOU mode
from yast import *
class PackageSelectorYOUClient:
    def main(self):
      Pkg.SourceCreate(
        "http://armstrong.suse.de/download/Code/10/update/i386.ro/",
        "/"
      )

      if True:
        Pkg.TargetInit(
          "/", # installed system
          False
        ) # don't create a new RPM database

      UI.OpenDialog(
        Opt("defaultsize"),
        PackageSelector(Id("selector"), Opt("testMode", "youMode"))
      )
      #				    `opt(`testMode ) ) );
      UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()


PackageSelectorYOUClient().main()

