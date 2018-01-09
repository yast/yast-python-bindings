# encoding: utf-8

# Example for a RichText widget
# Purpose: Have a possibility to see whether files (.txt, .rtf)
#          such as licenses, release-notes are displayed correctly
#          in text mode (ncurses) or graphical UI (qt).
from yast import import_module
import_module('UI')
from yast import *
import cgi
class RichTextLicenseClient:
    def main(self):

      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          Label("HTML text or text in <pre>...</pre> tags"),
          RichText(Id("text"), ""),
          Label("Plain text (`opt(`plainText))"),
          RichText(Id("plaintext"), Opt("plainText"), ""),
          HBox(
            PushButton(Id("load"), "&Load File"),
            PushButton(Id("close"), "&Close")
          )
        )
      )
      button = None
      name = ""
      text = ""
      if UI.TextMode():
        file_ext = "*.txt *orig"
      else:
        file_ext = "*.txt *orig *rtf"

      while True:
        button = UI.UserInput()

        if button == "load":
          name = UI.AskForExistingFile(".", file_ext, "Select text file")
          text2 = SCR.Read(Path(".target.string"), name)

          if text2 == None:
            text2 = ""

          if ycpbuiltins.regexpmatch(text2, "</.*>"):
            # HTML text (or RichText)
            UI.ChangeWidget(Id("text"), "Value", text2)
          else:
            # plain text
            UI.ChangeWidget(
              Id("text"),
              "Value",
              "<pre>" + cgi.escape(text2) + "</pre>")

          UI.ChangeWidget(Id("plaintext"), "Value", text2)
        if button == "close":
          break

      UI.CloseDialog()


RichTextLicenseClient().main()

