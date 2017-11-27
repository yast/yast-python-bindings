# encoding: utf-8

# Popup stress test: Pop up dialogs and close them all the time
from yast import *
class PopupStressTestClient:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          Heading("Pop-up Stress Test"),
          VSpacing(5),
          Label(
            "Sit back and watch the pop-up dialogs.\n" + "\n" +
              "Experiment with minimizing this application\n" +
              "and with working with some other application\n" +
              "while this is running."
          ),
          Bottom(Right(PushButton(Id("cancel"), Opt("default"), "&Close")))
        )
      )

      while True:
        if UI.TimeoutUserInput(3 * 1000) == "cancel":
          break

        UI.OpenDialog(
          VBox(
            Heading("Annoying pop-up #1"),
            PushButton(Id("cancel"), Opt("default"), "&Cancel")
          )
        )

        if UI.TimeoutUserInput(3 * 1000) == "cancel":
          UI.CloseDialog()
          break

        UI.OpenDialog(
          VBox(
            Heading("Annoying pop-up #2"),
            PushButton(Id("cancel"), Opt("default"), "&Cancel")
          )
        )

        if UI.TimeoutUserInput(3 * 1000) == "cancel":
          UI.CloseDialog()
          UI.CloseDialog()
          break

        UI.CloseDialog() # close pop-up #2

        if UI.TimeoutUserInput(3 * 1000) == "cancel":
          UI.CloseDialog()
          break

        UI.CloseDialog() # close pop-up #1

      UI.CloseDialog()


PopupStressTestClient().main()

