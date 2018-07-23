from __future__ import unicode_literals
# encoding: utf-8

# stupid puzzle
# $Id$
from yast import import_module
import_module('UI')
from yast import *
import copy

def is_int(numstr):
    try:
      int(numstr)
    except:
      return False
    return True

class PuzzleClient:
    def main(self):
      self.line_len = 4


      # ==== main

      # define this global variable to provide nxn puzzle table

      # create buttons with space at num
      buttons = self.generate_buttons(5)

      # play puzzle
      self.PuzzleWindow(buttons)


    def DebugDialog(self, str):
      str = copy.deepcopy(str)
      UI.OpenDialog(
        VBox(RichText(ycpbuiltins.sformat("%1", str)), PushButton("&OK"))
      )
      r = UI.UserInput()
      UI.CloseDialog()



    def buttons_table(self, buttons):
      buttons = copy.deepcopy(buttons)
      tabl = VBox()
      line = HBox()

      i = 0
      j = 0
      label = ""

      while ((i + self.line_len) - 1) < ycpbuiltins.size(buttons):
        j = 0
        line = HBox()

        while j < self.line_len:
          label = buttons[i + j]

          if ycpbuiltins.size(label) > 0:
            line = ycpbuiltins.add(
              line,
              ReplacePoint(
                Id(ycpbuiltins.sformat("rp%1", (i + j))),
                PushButton(Id(str(i + j)), label)
              )
            )
          else:
            line = ycpbuiltins.add(
              line,
              ReplacePoint(
                Id(ycpbuiltins.sformat("rp%1", (i + j))),
                HStretch()
              )
            )

          j = j + 1

        tabl = ycpbuiltins.add(tabl, line)

        i = i + j

      #return copy.deepcopy(tabl)
      return tabl


    def isRight(self, buttons, pos):
      buttons = copy.deepcopy(buttons)
      if (pos + 1) < ycpbuiltins.size(buttons):
        return str(buttons[pos + 1]) == ""
      return False


    def isLeft(self, buttons, pos):
      buttons = copy.deepcopy(buttons)
      if (pos - 1) >= 0:
        return str(buttons[(pos - 1)]) == ""
      return False


    def isDown(self, buttons, pos):
      buttons = copy.deepcopy(buttons)
      if (pos + self.line_len) <  ycpbuiltins.size(buttons):
        return str(buttons[pos + self.line_len]) == ""
      return False


    def isUp(self, buttons, pos):
      buttons = copy.deepcopy(buttons)
      if (pos - self.line_len) >=  0:
        return str(buttons[pos - self.line_len]) == ""
      return False


    # do the move
    def move(self, buttons, pos, m):
      buttons = copy.deepcopy(buttons)
      ret = []
      i = 0

      while i < ycpbuiltins.size(buttons):
        if i == pos:
          #Ops.set(ret, ycpbuiltins.size(ret), Ops.get(buttons, Ops.add(i, m)))
          ret.append(buttons[i + m])
        elif i == (pos + m):
          #Ops.set(ret, ycpbuiltins.size(ret), Ops.get(buttons, Ops.subtract(i, m)))
          ret.append(buttons[i - m])
        else:
          ret.append(buttons[i])

        i = i + 1

      UI.ReplaceWidget(Id(ycpbuiltins.sformat("rp%1", pos)), HStretch())
      UI.ReplaceWidget(
        Id(ycpbuiltins.sformat("rp%1", (pos + m))),
        PushButton(Id(str(pos + m)), buttons[pos])
      )


      ret = copy.deepcopy(ret)
      return ret

    # generate list of buttons
    # TODO: needs to be randomized

    def generate_buttons(self, space):
      buttons = []
      i = 1

      while (i <= (self.line_len * self.line_len)):
        if i == space:
          buttons.append("")
        else:
          if i < space:
            buttons.append(ycpbuiltins.sformat("%1", i))
          else:
            buttons.append(ycpbuiltins.sformat("%1", (i - 1)))

        i = i + 1

      return copy.deepcopy(buttons)

    def PuzzleWindow(self, buttons):
      buttons = copy.deepcopy(buttons)
      UI.OpenDialog(
        HBox(
          HSpacing(3),
          VBox(
            VSpacing(),
            Frame("Puzzle", self.buttons_table(buttons)),
            VSpacing(5),
            PushButton(Id("quit"), "&Quit")
          ),
          HSpacing()
        )
      )

      ui = None
      while True:
        ui = UI.UserInput()

        if is_int(ui):
          if self.isLeft(buttons, int(ui)):
            buttons = self.move(buttons, int(ui), -1)
          elif self.isRight(buttons, int(ui)):
            buttons = self.move(buttons, int(ui), 1)
          elif self.isUp(buttons, int(ui)):
            buttons = self.move(
              buttons,
              int(ui),
              -self.line_len)
          elif self.isDown(buttons, int(ui)):
            buttons = self.move(buttons, int(ui), self.line_len)
        if ui == "cancel" or ui == "quit":
          break

      UI.CloseDialog()


PuzzleClient().main()

