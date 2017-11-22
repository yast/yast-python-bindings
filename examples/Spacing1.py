# encoding: utf-8

from yast import *
class Spacing1Client:
    def main(self):
      # Build dialog with one input field field, 4 Beatles buttons and an OK button.
      UI.OpenDialog(
        VBox(
          VSpacing(),
          HBox(Label("Name:"), InputField(Id("name"), "")),
          VSpacing(0.2),
          HBox(
            PushButton(Id("john"), "&John"),
            HSpacing(0.5),
            PushButton(Id("paul"), "&Paul"),
            HSpacing(3),
            PushButton(Id("george"), "&George"),
            HSpacing(0.5),
            PushButton(Id("ringo"), "&Ringo")
          ),
          VSpacing(0.5),
          PushButton(Id("ok"), "&OK")
        )
      )

      # Wait for user input.
      button = None
      while True:
        button = UI.UserInput()

        if button == "john":
          UI.ChangeWidget(Id("name"), "Value", "John Lennon")
        elif button == "paul":
          UI.ChangeWidget(Id("name"), "Value", "Paul McCartney")
        elif button == "george":
          UI.ChangeWidget(Id("name"), "Value", "George Harrison")
        elif button == "ringo":
          UI.ChangeWidget(Id("name"), "Value", "Ringo Starr")
        if button == "ok":
          break

      UI.CloseDialog()


Spacing1Client().main()

