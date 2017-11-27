# encoding: utf-8

# Advanced MultiSelectionBox example:
#
# Retrieve the list of selected items and output it.
from yast import *
class MultiSelectionBox5Client:
    def main(self):

      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            55,
            10,
            HBox(
              Table(
                Id("pizza"),
                Opt("notify"),
                Header("Pizza", "Price"),
                [
                  Item(Id("vege"), "Vegetarian", 6),
                  Item(Id("capri"), "Capricciosa", 7),
                  Item(Id("meat"), "Meat and more", 8)
                ]
              ),
              MultiSelectionBox(
                Id("toppings"),
                "Select pizza toppings:",
                [
                  Item(Id("cheese"), "Cheese", True),
                  Item(Id("tomatoes"), "Tomatoes", True),
                  Item(Id("mushroom"), "Mushrooms", False),
                  Item(Id("onions"), "Onions")
                ]
              )
            )
          ),
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      vege = [
        Item(Id("cheese"), "Cheese", True),
        Item(Id("tomatoes"), "Tomatoes", True),
        Item(Id("mushroom"), "Mushrooms", False),
        Item(Id("onions"), "Onions")
      ]
      meat = [Item(Id("sausage"), "Salami", True), Item(Id("pork"), "Ham")]
      capri = ycpbuiltins.merge(vege, meat)

      ret = None
      while True:
        ret = UI.UserInput()

        if ret == "pizza":
          item = UI.QueryWidget("pizza", "CurrentItem")
          if item == "vege":
            UI.ChangeWidget("toppings", "Items", vege)
          elif item == "capri":
            UI.ChangeWidget("toppings", "Items", capri)
          elif item == "meat":
            UI.ChangeWidget("toppings", "Items", meat)
        if ret == "ok":
          break

      selected_items = UI.QueryWidget(Id("toppings"), "SelectedItems")

      ycpbuiltins.y2debug("Selected items: %1", selected_items)

      # Remember to retrieve the widget's data _before_ the dialog is closed,
      # i.e. before it is destroyed!

      UI.CloseDialog()



      # Concatenate the list of selected toppings to one multi-line string.

      pizza_description = ""

      for topping in ycpbuiltins.foreach(selected_items):
        pizza_description = ycpbuiltins.sformat(
          "%1\n%2",
          pizza_description,
          topping
        )


      # Open a new dialog to echo the selection.

      UI.OpenDialog(
        VBox(
          Label("Your pizza will come with:\n"),
          Label(pizza_description),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MultiSelectionBox5Client().main()

