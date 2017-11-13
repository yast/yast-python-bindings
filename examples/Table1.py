# encoding: utf-8

from yast import *
class Table1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            25,
            7,
            Table(
              Header("Name", "Price"),
              [
                Item(Id(1), "Chili", 6),
                Item(Id(2), "Salami Baguette", None),
                Item(Id(3), "Spaghetti", 8),
                Item(Id(4), "Steak Sandwich", 12)
              ]
            )
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Table1Client().main()

