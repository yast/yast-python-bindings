# encoding: utf-8

import copy
from yast import import_module
import_module('UI')
from yast import *

class ContextMenuClient:
    def main(self):

      event_display = "<i>No event yet - click something (or wait for timeout)</i>"

      if not UI.HasSpecialWidget("ContextMenu"):
        UI.OpenDialog(
          VBox(
            Label("ContextMenu not supported!"),
            PushButton(Opt("default"), "&Oops!")
          )
        )
        UI.UserInput()
        UI.CloseDialog()
        return

      UI.OpenDialog(
        VBox(
          SelectionBox(
            Id("sport"),
            Opt("notify", "immediate", "notifyContextMenu"),
            "Select your sport:",
            ["Swimming", "Cycling", "Running"]
          ),
          RichText(Id("event_display"), event_display),
          PushButton(Id("close"), "&OK")
        )
      )

      # Event loop

      event = {}
      while True:
        event = UI.WaitForEvent(100000)
        if event != None:
          UI.ChangeWidget("event_display", "Value", formatEvent(event))

        if (event != None) and (event.get("EventReason", "") == "ContextMenuActivated"):
          UI.OpenContextMenu(
            Term(
              "menu",
              [
                Item(Id("instruct"), "Instruc&tions"),
                Term(
                  "menu",
                  "&Execute",
                  [Item(Id("training"), "&Training"), Item(Id("race"), "&Race")]
                )
              ]
            )
          )
        if event["ID"] == "close":
            break

      UI.CloseDialog()

def formatEvent(event):
      event = copy.deepcopy(event)
      html = "<h3>Event:</h3><p>"
      ycpbuiltins.y2milestone("formatEvent(%1)", event)
      for key, value in ycpbuiltins.foreach(event).iteritems():
        html = html + "<font color=blue>" + key + "</font>: " + ycpbuiltins.tostring(value) + "<br>"
      html = html + "</p>"
      return html

ContextMenuClient().main()
