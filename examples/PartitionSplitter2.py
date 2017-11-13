# encoding: utf-8

from yast import *
class PartitionSplitter2Client:
    def main(self):
      if not UI.HasSpecialWidget("Slider") or not UI.HasSpecialWidget("BarGraph"):
        UI.OpenDialog(
          VBox(
            Label(
              "Error: This UI doesn't support the required special widgets!"
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
          Left(Label("Now:")),
          BarGraph(
            Opt("vstretch"),
            [win_used, total_free],
            [
              "Windows\nused\n%1 " + unit,
              "Windows\nfree\n%1 " + unit
            ]
          ),
          VSpacing(1),
          Left(Label("After installation:")),
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
            "Linux (" +  unit + ")"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


PartitionSplitter2Client().main()

