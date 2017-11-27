# encoding: utf-8

from yast import *

# Advanced ComboBox / SelecionBox example:
# Dialog with a ComboBox and a SelectionBox
# where selecting an item in one will also select it in the other
class ComboBox5Client:
    def main(self):
      items = [
        Item(Id("Napoli"), "Napoli"),
        Item(Id("Funghi"), "Funghi", True),
        Item(Id("Salami"), "Salami")
      ]

      UI.OpenDialog(
        VBox(
          MinSize(
            30,
            5,
            HBox(
              Top(ComboBox(Id("pizzaComboBox"), Opt("notify"), "Pizza:", items)),
              SelectionBox(Id("pizzaSelBox"), Opt("notify"), "Pizza:", items)
            )
          ),
          Right(PushButton(Id("cancel"), "&Close"))
        )
      )

      widget = None
      while True:
        widget = UI.UserInput()
        # y2debug( "Event widget: %1", widget );

        if widget == "pizzaComboBox" or widget == "pizzaSelBox":
          pizza = UI.QueryWidget(widget, "Value")
          ycpbuiltins.y2debug("Pizza: %1", pizza)

          UI.ChangeWidget(
            "pizzaSelBox" if widget == "pizzaComboBox" else "pizzaComboBox",
            "Value",
            Id(pizza)
          )

          ycpbuiltins.y2debug(
            "ComboBox: %1",
            UI.QueryWidget("pizzaComboBox", "Items")
          )
          ycpbuiltins.y2debug("SelBox  : %1", UI.QueryWidget("pizzaSelBox", "Items"))
        if widget == "cancel":
            break

      UI.CloseDialog()

ComboBox5Client().main()
