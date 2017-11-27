# encoding: utf-8

from yast import *
class ShortcutConflict3Client:
    def main(self):
      # Demo for shortcut checking:
      # Deliberately generate a shortcut conflict.

      UI.OpenDialog(
        VBox(
          RadioButtonGroup(
            VBox(
              Left(RadioButton("Instant &Play", True)),
              Left(RadioButton("Demo &Only"))
            )
          ),
          Left(
            ComboBox("Game &Type:", ["Boring", "Full automatic", "Unplayable"])
          ),
          InputField("Nickname for &Player 1:"),
          InputField("Nickname for &Player 2:"),
          IntField("Maximum &Time:", 0, 100, 20),
          PushButton("&OK")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


ShortcutConflict3Client().main()

