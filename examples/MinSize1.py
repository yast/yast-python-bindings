from __future__ import unicode_literals
# encoding: utf-8

# Simple example for MinSize
from yast import import_module
import_module('UI')
from yast import *
class MinSize1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MinSize(
            50,
            12,
            RichText(
              "<h3MinSize example</h3>" +
                "<p>MinSize is particularly useful in connection with widgets" +
                " that can scroll, such as" + "<ul>" + "<li>RichText" + "<li>SelectionBox" + "<li>Table" +
                "<li>MultiLineEdit" + "</ul>" +
                "since those widgets don't have a reasonable default size." + "</p>"
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MinSize1Client().main()

