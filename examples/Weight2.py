# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Weight2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          HBox(
            HWeight(1, PushButton(Opt("hstretch"), "Weight 1")),
            HWeight(1, PushButton(Opt("hstretch"), "Weight 1"))
          ),
          HBox(
            HWeight(3, PushButton(Opt("hstretch"), "Weight 3")),
            HWeight(2, PushButton(Opt("hstretch"), "Weight 2"))
          ),
          HBox(
            HWeight(2, PushButton(Opt("hstretch"), "Weight 2")),
            HWeight(1, PushButton(Opt("hstretch"), "Weight 1"))
          ),
          HBox(
            HWeight(3, PushButton(Opt("hstretch"), "Weight 3")),
            HWeight(1, PushButton(Opt("hstretch"), "Weight 1"))
          ),
          HBox(
            HWeight(10, PushButton(Opt("hstretch"), "Weight 10")),
            HWeight(1, PushButton(Opt("hstretch"), "Weight 1"))
          )
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Weight2Client().main()

