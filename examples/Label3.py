# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Label3Client:
    def main(self):
      # Build dialog with one label, 4 Beatles buttons and an OK button.
      UI.OpenDialog(
        VBox(
          Label("Select your favourite Beatle:"),
          Label(Id("beatle"), Opt("outputField"), "   "),
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
          UI.ChangeWidget(Id("beatle"), "Value", "John Lennon")
        elif button == "paul":
          UI.ChangeWidget(Id("beatle"), "Value", "Paul McCartney")
        elif button == "george":
          UI.ChangeWidget(Id("beatle"), "Value", "George Harrison")
        elif button == "ringo":
          UI.ChangeWidget(Id("beatle"), "Value", "Ringo Starr")

        # Recalculate the layout - this is necessary since the label widget
        # doesn't recompute its size upon changing its value.
        UI.RecalcLayout()
        if button == "ok":
          break


      # Retrieve the label's value.
      name = UI.QueryWidget(Id("beatle"), "Value")

      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()

      # Pop up a new dialog to echo the input.
      UI.OpenDialog(
        VBox(
          VSpacing(),
          HBox(
            Label("You selected:"),
            Label(Opt("outputField"), name),
            HSpacing()
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Label3Client().main()

