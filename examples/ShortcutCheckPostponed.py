from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class ShortcutCheckPostponedClient:
    def main(self):
      # Demo for postponed shortcut checking

      b_kilroy = PushButton(Opt("hstretch"), "&Kilroy")
      b_was = PushButton(Opt("hstretch"), "&was")
      b_here = PushButton(Opt("hstretch"), "&here")


      UI.OpenDialog(
        VBox(
          VSpacing(0.3),
          HBox(
            HSpacing(),
            Label("Click on one of the upper buttons\n" + "to exchange them."),
            HSpacing()
          ),
          VSpacing(0.3),
          ReplacePoint(Id(1), b_kilroy),
          ReplacePoint(Id(2), b_was),
          ReplacePoint(Id(3), b_here),
          VSpacing(Opt("vstretch")),
          Right(PushButton(Id("cancel"), "&Quit"))
        )
      )


      button = None

      ycpbuiltins.y2milestone("Initial state: 'Kilroy was here'")
      button = UI.UserInput()
      if button == "cancel":
        return 

      UI.PostponeShortcutCheck # "&Kilroy" "&was" "&here"
      UI.ReplaceWidget(Id(1), b_was) # "&was" "&was" "&here"
      UI.ReplaceWidget(Id(2), b_kilroy) # "&was" "&Kilroy" "&here"
      UI.CheckShortcuts()

      ycpbuiltins.y2milestone("After change: 'was Kilroy here'")
      button = UI.UserInput()
      if button == "cancel":
        return

      UI.PostponeShortcutCheck # "&was" "&Kilroy" "&here"
      UI.ReplaceWidget(Id(1), b_here) # "&here" "&Kilroy" "&here"
      UI.ReplaceWidget(Id(2), b_was) # "&here" "&was" "&here"
      UI.ReplaceWidget(Id(3), b_kilroy) # "&here" "&was" "&Kilroy"
      UI.CheckShortcuts()

      ycpbuiltins.y2milestone("After change: 'here was Kilroy'")
      button = UI.UserInput()
      if button == "cancel":
        return

      UI.PostponeShortcutCheck # "&here" "&was" "&Kilroy"
      UI.ReplaceWidget(Id(1), b_kilroy) # "&Kilroy" "&was" "&Kilroy"
      UI.ReplaceWidget(Id(3), b_here) # "&Kilroy" "&was" "&here"
      # Omitting UI::CheckShortcuts();

      ycpbuiltins.y2milestone("After change: back to 'Kilroy was here'")
      ycpbuiltins.y2milestone(
        "Expect complaint about missing UI::CheckShortcuts()"
      )
      button = UI.UserInput()
      if button == "cancel":
        return


      ycpbuiltins.y2milestone("Expect shortcut conflict: '&was' vs. '&was'")
      UI.ReplaceWidget(Id(1), b_was) # "&was" "&was" "&here"
      UI.ReplaceWidget(Id(2), b_kilroy) # "&was" "&Kilroy" "&here"
      ycpbuiltins.y2milestone("Expect complaint about excess UI::CheckShortcuts()")
      UI.CheckShortcuts()

      ycpbuiltins.y2milestone("After change: 'was Kilroy here'")
      button = UI.UserInput()
      if button == "cancel":
        return


      UI.CloseDialog()


ShortcutCheckPostponedClient().main()

