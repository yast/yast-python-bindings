# encoding: utf-8

# PollInput.ycp
#
# Example for common usage of UI::PollInput()
from yast import *
class PollInputClient:
    def main(self):
      # Build dialog with two labels and a "stop" button.

      count = 0
      count_max = 10000

      UI.OpenDialog(
        VBox(
          Label("Calculating..."),
          Label(Id("count"), ycpbuiltins.sformat("%1 of %2", count, count_max)),
          PushButton(Id("stop"), "&Stop")
        )
      )

      widget_id = None
      while True:
        widget_id = UI.PollInput()


        # Simulate heavy calculation

        ycpbuiltins.sleep(200) # milliseconds

        # Update screen to show that the program is really busy
        count = count + 1
        UI.ChangeWidget(
          Id("count"),
          "Value",
          ycpbuiltins.sformat("%1 of %2", count, count_max)
        )
        UI.RecalcLayout() # Might be necessary when the label becomes wider
        if widget_id == "stop" or count > count_max:
          break

      UI.CloseDialog()


PollInputClient().main()

