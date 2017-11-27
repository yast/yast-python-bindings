# encoding: utf-8

from yast import *
class Heading3Client:
    def main(self):
      # Build dialog with one label, 4 Beatles buttons and an OK button.
      UI.OpenDialog(
        VBox(
          Label("My favourite Beatle:"),
          # `Heading(`id(`favourite), "Press one of the buttons below"),
          Heading(Id("favourite"), "(please select one)"),
          HBox(
            PushButton(Id("john"), "John"),
            PushButton(Id("paul"), "Paul"),
            PushButton(Id("george"), "George"),
            PushButton(Id("ringo"), "Ringo")
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      # Wait for user input.
      button = None
      while True:
        button = UI.UserInput()

        if button == "john":
          UI.ChangeWidget(Id("favourite"), "Value", "John Lennon")
        elif button == "paul":
          UI.ChangeWidget(Id("favourite"), "Value", "Paul McCartney")
        elif button == "george":
          UI.ChangeWidget(Id("favourite"), "Value", "George Harrison")
        elif button == "ringo":
          UI.ChangeWidget(Id("favourite"), "Value", "Ringo Starr")
        if button == "ok":
          break

      UI.CloseDialog()

Heading3Client().main()

