# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class WidgetExistsClient:
    def main(self):


      # main
      #

      UI.OpenDialog(
        VBox(
          ReplacePoint(Id("rp_top"), PushButton(Id("top"), "Top Button")),
          ReplacePoint(Id("rp_center"), PushButton(Id("center"), "Center Button")),
          ReplacePoint(Id("rp_bottom"), PushButton(Id("bottom"), "Bottom Button")),
          VSpacing(1),
          Label(Id("summary"), ""),
          VSpacing(1),
          PushButton(Id("close"), "&Close")
        )
      )

      # Better wait until now before doing the summary - it isn't much use before UI::OpenDialog()
      # since of course all UI::WidgetExists() calls return False until then.
      UI.ChangeWidget(Id("summary"), "Value", Summary())
      UI.RecalcLayout()

      button = None
      while True:
        button = UI.UserInput()

        if button == "top":
          RemoveButton(Id("rp_top"))
        elif button == "center":
          RemoveButton(Id("rp_center"))
        elif button == "bottom":
          RemoveButton(Id("rp_bottom"))
        if button == "close":
          break

      UI.CloseDialog()


    # Return a text summary of existing buttons.
    #
def Summary():
      summary = ""
      if UI.WidgetExists(Id("top")):
        summary = summary + "Top button exists"
      else:
        summary = summary + "No top button"
      if UI.WidgetExists(Id("center")):
        summary = summary + "\nCenter button exists"
      else:
        summary = summary + "\nNo center button"
      if UI.WidgetExists(Id("bottom")):
        summary = summary + "\nBottom button exists" 
      else:
        summary = summary + "\nNo bottom button"
      print ("returning \n%s"%summary)
      return summary

    # Remove button with given id and update summary.
    #
def RemoveButton(id):
      # can't deepcoy Id
      #id = deep_copy(id)
      UI.ReplaceWidget(id, Empty())
      UI.ChangeWidget(Id("summary"), "Value", Summary())
      UI.RecalcLayout()


WidgetExistsClient().main()

