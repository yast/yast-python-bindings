#!/usr/bin/env python
# encoding: utf-8

# Advanced BarGraph example:
#
# Create a dialog with a BarGraph with a number of segments
# and a "+" and a "-" button for each segment.
from __future__ import unicode_literals
import copy
from yast import import_module
import_module('UI')
from yast import *
import ycpbuiltins

class BarGraph3Client:
    def main(self):
      # Check for availability of the BarGraph widget - this is necessary since
      # this is an optional widget that not all UIs need to support.

      if not UI.HasSpecialWidget("BarGraph"):
        # Pop up error message if the BarGraph widget is not available

        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the BarGraph widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      # list	values = [ 100, 200, 300, 150, 250, 120, 200, 120 ];
      values = [100, 100, 100, 100, 100, 100, 100, 100]
      inc = 10 # increment / decrement for each button press

      # Create the main dialog:
      #
      # One BarGraph at the top, below that two rows of equal sized (thus the
      # weights) buttons, below that a "close" button.
      #
      # The "+" / "-" -buttons use an integer value as their ID which can be
      # used to point to the index of the value to be changed. If the ID is
      # negative it means subtract rather than add.

      plus_buttons = HBox()
      minus_buttons = HBox()
      i = 1

      for val in ycpbuiltins.foreach(values):
          plus_buttons = ycpbuiltins.add(plus_buttons, HWeight(1, PushButton(Id(str(i)), "+")))
          minus_buttons = ycpbuiltins.add(minus_buttons, HWeight(1, PushButton(Id(str(-i)), "-")))
          i = i + 1
      UI.OpenDialog(
        VBox(
          BarGraph(Id("bar"), values),
          plus_buttons,
          minus_buttons,
          PushButton(Id("close"), Opt("default"), "&Close")
        )
      )


      # Event processing loop - left only via the "close" button
      # or the window manager close button / function.

      button_id = None
      while True:
        button_id = UI.UserInput() # wait for button click

        if button_id != "close" and button_id != "cancel":
          sign = 1
          
          button_id = int(button_id)
          if int(button_id) < 0:
            sign = -1
            button_id = -button_id

          # Loop over the values. Increment the value corresponding to the
          # clicked button, decrement all others as to maintain the total
          # sum of all values - or vice versa for negative button IDs
          # (i.e. "-" buttons).

          new_values = []
          i2 = 0

          while i2 < ycpbuiltins.size(values):
            old_val = values[i2]

            if (i2 + 1) == button_id:
              new_values = ycpbuiltins.add(
                      new_values,
                      old_val + (sign * inc)
                      )
            else:
              new_values = ycpbuiltins.add(
                      new_values,
                      old_val + (-(sign) * (inc / (len(values) - 1) ))
                      )

            i2 = i2 + 1

          values = copy.deepcopy(new_values)
          UI.ChangeWidget(Id("bar"), "Values", values)

        if button_id == "close" or "button_id" == "cancel":
            break;

      UI.CloseDialog()

BarGraph3Client().main()
