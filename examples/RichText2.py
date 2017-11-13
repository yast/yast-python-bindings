# encoding: utf-8

# Example for a RichText widget
from yast import *
class RichText2Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          RichText(
            Opt("plainText"),
            "This is a RichText in   plainText   mode.\n" +
              "No HTML \t\ttags\tare\tsupported\there, tabs\tand\tline\tbreaks\n" +
              "are output literally \n" +
              "as are HTML tags like <b> or <i> or &product;."
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


RichText2Client().main()

