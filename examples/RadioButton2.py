# encoding: utf-8

from yast import *
class RadioButton2Client:
    def main(self):
      UI.OpenDialog(
        RadioButtonGroup(
          Id("rb"),
          VBox(
            Label("How do you want to crash?"),
            Left(RadioButton(Id(0), Opt("notify"), "No&w")),
            Left(RadioButton(Id(1), Opt("notify"), "&Every now an then")),
            Left(RadioButton(Id(2), Opt("notify"), "Every &five minutes")),
            Left(RadioButton(Id(3), Opt("notify"), "Ne&ver", True)),
            HBox(
              PushButton(Id("next"), "&Next"),
              PushButton(Id("close"), "&Close")
            )
          )
        )
      )

      while True:
        ret = UI.UserInput()

        if ret == "close":
          break
        elif ret == "next":
          # y2milestone("Hit next");
          current = UI.QueryWidget(Id("rb"), "CurrentButton")
          current = ((current + 1) % 4)
          UI.ChangeWidget(Id("rb"), "CurrentButton", current)
        else:
          ycpbuiltins.y2milestone("Hit RadioButton #%1", ret)

      ycpbuiltins.y2milestone("Terminating.")

      UI.CloseDialog()


RadioButton2Client().main()

