from __future__ import unicode_literals
# encoding: utf-8

# SetDesktopTitle Example
#
# Set the window title that is shown by the window manager
# Searches for the desktop file and uses its name attribute
# Note: this works in qt and gtk only, ncurses doesn't have a window title
from yast import import_module
import_module('Wizard')
from yast import *
class WizardSetDesktopTitleClient:
    def main(self):

      Wizard.CreateDialog()
      Wizard.SetContentsButtons(
        "SetDesktopTitle Example",
        Label(
          "Read 'Network Settings' from the lan.desktop file and set this string as window title"
        ),
        "Help",
        #Label.BackButton,
        #Label.NextButton
        "Back",
        "Next"
      )

      Wizard.SetDesktopTitle("lan") # use "lan" as an example

      Wizard.UserInput()
      Wizard.CloseDialog()


WizardSetDesktopTitleClient().main()

