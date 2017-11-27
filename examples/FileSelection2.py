# encoding: utf-8

# Example for the file selection builtins
from yast import import_module
import_module('UI')
from yast import *
class FileSelection2Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          Heading("YaST2 File Selector Demo"),
          VStretch(),
          HBox(
            HStretch(),
            HWeight(
              1,
              VBox(
                PushButton(Id("askDir"), Opt("hstretch"), "Select &Directory..."),
                PushButton(Id("dir"), Opt("hstretch"), "&Select File..."),
                PushButton(Id("load"), Opt("hstretch"), "&Load File..."),
                PushButton(Id("saveAs"), Opt("hstretch"), "Save &As...")
              )
            ),
            HSpacing(2)
          ),
          VSpacing(),
          HBox(
            Label("Selected: "),
            Label(Id("name"), Opt("outputField", "hstretch"), "<nothing selected>")
          ),
          VSpacing(),
          Right(PushButton(Id("close"), "&Close"))
        )
      )

      button = None
      name = ""
      while True:
        update = True
        button = UI.UserInput()

        if button == "askDir":
          name = UI.AskForExistingDirectory("/tmp", "")
        elif button == "dir":
          name = UI.AskForExistingFile("", "*", "")
        elif button == "load":
          name = UI.AskForExistingFile("/tmp", "*png", "")
        elif button == "saveAs":
          name = UI.AskForSaveFileName("/tmp", "*", "")

        if name == None:
          name = "<canceled>"

        if name != "": # Label update necessary?
          UI.ChangeWidget(Id("name"), "Value", name)
          UI.RecalcLayout()
          name = ""
        if button == "close" or button == "cancel":
            break

      UI.CloseDialog()


FileSelection2Client().main()

