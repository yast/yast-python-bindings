from __future__ import unicode_literals
# encoding: utf-8

# Full-fledged simple patch selection
from yast import import_module
import_module('UI')
import_module('Pkg')
from yast import *
class SimplePatchSelectorStableClient:
    def main(self):

      # Initialize RPM DB as pkg src
      Pkg.TargetInit(
        "/", # installed system
        False
      ) # don't create a new RPM database

      # Pkg::SourceCreate( "file:/mounts/dist/install/stable-x86/", "" );
      Pkg.SourceCreate("ftp://ftp.gwdg.de/pub/suse/update/10.2", "")



      if not UI.HasSpecialWidget("SimplePatchSelector"):
        self.detailedSelection() # Fallback: Do detailed selection right away
        return


      UI.OpenDialog(
        Opt("defaultsize"),
        Term("SimplePatchSelector", Id("selector"))
      )

      button = None
      while True:
        button = UI.RunPkgSelection(Id("selector"))
        ycpbuiltins.y2milestone(
          "SimplePatchSelector selector returned %1",
          button
        )

        if button == "details":
          self.detailedSelection()
        if button == "cancel" or button == "accept":
          break

      UI.CloseDialog()


    def detailedSelection(self):

      # Open empty dialog for instant feedback

      UI.OpenDialog(
        Opt("defaultsize"),
        ReplacePoint(Id("rep"), Label("Reading package database..."))
      )

      # This will take a while: Detailed package data are retrieved
      # while the package manager is initialized
      UI.ReplaceWidget(
        "rep",
        PackageSelector(Id("packages"), Opt("youMode"), "/dev/fd0")
      )

      input = UI.RunPkgSelection(Id("packages"))
      ycpbuiltins.y2milestone("Package selector returned  %1", input)
      UI.CloseDialog()


SimplePatchSelectorStableClient().main()

