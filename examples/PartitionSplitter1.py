from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class PartitionSplitter1Client:
    def main(self):
      if not UI.HasSpecialWidget("PartitionSplitter"):
        UI.OpenDialog(
          VBox(
            Label(
              "Error: This UI doesn't support the PartitionSplitter widget!"
            ),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return

      unit = "MB"
      win_used = 350
      total_free = 1500
      min_free = 50
      linux_min = 300
      linux_size = 800

      UI.OpenDialog(
        VBox(
          HSpacing(60), # wider default size
          PartitionSplitter(
            win_used,
            total_free,
            linux_size,
            linux_min,
            min_free,
            "Windows\nused\n%1 " + unit,
            "Windows\nfree\n%1 " + unit,
            "Linux\n%1 " + unit,
            "Windows free (" + unit + ")",
            "Linux (" + unit + ")"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


PartitionSplitter1Client().main()

