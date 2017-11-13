# encoding: utf-8

# Input field width under different layout constraints
from yast import *
class TextEntryLayoutClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          TextEntry("Normal", "normal width"),
          TextEntry(Opt("shrinkable"), "Sml", "shrinkable"),
          VBox(
            MarginBox(
              1,
              0.2,
              Frame(
                "Useless Frame",
                VBox(
                  Heading("Very Wide and Very Useless Heading"),
                  TextEntry("Normal 1"),
                  TextEntry("Normal 2"),
                  TextEntry("Normal 3"),
                  TextEntry("Unusually &wide field caption to make it wider"),
                  TextEntry("Normal 4"),
                  TextEntry(Opt("hstretch"), "Stretch", "stretchable"),
                  TextEntry(Opt("shrinkable"), "Sml", "shrinkable"),
                  Left(TextEntry("Left", "left aligned")),
                  HSquash(TextEntry("HSquashed", "hquashed"))
                )
              )
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


TextEntryLayoutClient().main()

