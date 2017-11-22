# encoding: utf-8

from yast import *
class WindowIDClient:
    def main(self):

      image = Convert.convert(
        SCR.Read(path(".target.byte"), "empty.gif"),
        "from" : "any",
        "to"   : "byteblock"
      )

      Wizard.CreateDialog()

      help = "Help"
      caption = "Penguins"
      penguins = Frame("Penguins", Image(Id("img"), image, "Penguins"))
      Wizard.SetContentsButtons(
        caption,
        penguins,
        help,
        Label.BackButton,
        Label.NextButton
      )

      windowID = UI.QueryWidget(Id("img"), "WindowID")
      ycpbuiltins.y2debug("windowID=%1", windowID)

      run = ycpbuiltins.sformat("/usr/bin/xpenguins --id %1", windowID)
      # string run = sformat ("/usr/X11R6/lib/xscreensaver/xmatrix -window-id %1", windowID);
      # string run = sformat ("/usr/X11R6/lib/xscreensaver/xflame -window-id %1", windowID);
      # string run = sformat ("/usr/X11R6/lib/xscreensaver/atlantis -window-id %1", windowID);
      ycpbuiltins.y2debug("run=%1", run)

      SCR.Execute(path(".target.bash_background"), run)

      UI.UserInput()
      UI.CloseDialog()


WindowIDClient().main()

