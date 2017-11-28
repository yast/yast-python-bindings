# encoding: utf-8
from yast import import_module
import_module('UI')
from yast import *

# Create a combo box with three entries.
# All entries have IDs to identify them independent of locale
# (The texts might have to be translated!).
# Entry "Funghi" will be selected by default.
class ComboBoxSetEmptyClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          ComboBox(
            Id("pizza"),
            Opt("editable"),
            "Select your Pizza:",
            [
              Item(Id("nap"), "Napoli"),
              Item(Id("fun"), "Funghi", True),
              Item(Id("sal"), "Salami")
            ]
          ),
          HBox(
            PushButton(Id("empty"), "&Empty"),
            PushButton(Id(42), "42"),
            PushButton(Id("ok"), "&OK")
          )
        )
      )

      button = None
      while True:
        ycpbuiltins.y2debug("Waiting")
        button = UI.UserInput()
        ycpbuiltins.y2debug("button: %s"%button)

        if button == 42:
            UI.ChangeWidget("pizza", "Value", 42)

        if button == "empty":
            UI.ChangeWidget("pizza", "Value", "")
        if button == "ok":
            break


      # Get the input from the selection box.
      #
      # Notice: The return value of UI::UserInput() does NOT return this value!
      # Rather, it returns the ID of the widget (normally the PushButton)
      # that caused UI::UserInput() to return.
      pizza = UI.QueryWidget(Id("pizza"), "Value")
      ycpbuiltins.y2milestone("Selected %s"%pizza)

      UI.CloseDialog()

ComboBoxSetEmptyClient().main()
