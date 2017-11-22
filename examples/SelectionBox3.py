# encoding: utf-8

from yast import *
class SelectionBox3Client:
    def main(self):
      # Create a selection box with three entries.
      # All entries have IDs to identify them independent of locale
      # (The texts might have to be translated!).
      # Entry "Funghi" will be selected by default.
      #
      # There are two buttons to select a "Today's special" and a
      # "veggie" pizza to demonstrate how to select list entries
      # programmatically.
      UI.OpenDialog(
        VBox(
          SelectionBox(
            Id("pizza"),
            "Select your Pizza:",
            [
              Item(Id("nap"), "Napoli"),
              Item(Id("fun"), "Funghi", True),
              Item(Id("sal"), "Salami")
            ]
          ),
          HBox(
            PushButton(Id("todays_special"), Opt("hstretch"), "&Today's special"),
            PushButton(Id("veggie"), Opt("hstretch"), "&Veggie"),
            PushButton(Id("none"), Opt("hstretch"), "&Nothing")
          ),
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      id = None
      while True:
        id = UI.UserInput()

        if id == "todays_special":
          UI.ChangeWidget("pizza", "CurrentItem", Id("nap"))
        elif id == "veggie":
          UI.ChangeWidget("pizza", "CurrentItem", Id("fun"))
        elif id == "none":
          UI.ChangeWidget("pizza", "CurrentItem", None)
        if id == "ok":
          break

      # Get the input from the selection box.
      #
      # Notice: The return value of UI::UserInput() does NOT return this value!
      # Rather, it returns the ID of the widget (normally the PushButton)
      # that caused UI::UserInput() to return.
      pizza = UI.QueryWidget(Id("pizza"), "CurrentItem")

      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()

      # Evaluate selection

      toppings = "nothing"

      if pizza == "nap":
        toppings = "Tomatoes, Cheese"
      elif pizza == "fun":
        toppings = "Tomatoes, Cheese, Mushrooms"
      elif pizza == "sal":
        toppings = "Tomatoes, Cheese, Sausage"

      # Pop up a new dialog to echo the selection.
      UI.OpenDialog(
        VBox(
          Label("You will get a pizza with:"),
          Label(toppings),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()

      UI.CloseDialog()


SelectionBox3Client().main()

