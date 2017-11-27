# encoding: utf-8

# Multiple Main Dialogs
from yast import *
class MainDialogPopupClient:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          Heading("Main Dialog"),
          VStretch(),
          PushButton(Id("doit1"), "&Do Something"),
          PushButton(Id("doit2"), "Do &More"),
          PushButton(Id("popup"), "&Popup Main Dialog"),
          VStretch(),
          Right(PushButton(Id("close"), "&Close"))
        )
      )

      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        widget = event.get("ID", "None")

        if widget == "close":
          break

        if widget == "popup":
          UI.OpenDialog(
            Opt("defaultsize"),
            VBox(
              Id("popupDialog"),
              Heading("Popup Main Dialog"),
              VStretch(),
              PushButton(Id("doit11"), "&Do Something"),
              PushButton(Id("doit12"), "Do &More"),
              VStretch(),
              Right(PushButton(Id("popdown"), "&Back"))
            )
          )

        if widget == "popdown" and UI.WidgetExists("popupDialog"):
          UI.CloseDialog()

      UI.CloseDialog()


MainDialogPopupClient().main()

