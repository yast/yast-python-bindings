#!/usr/bin/env python
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

class Alignment:
  def main(self):
      UI.OpenDialog(
        VBox(
          PushButton(
            "This is a very long button - it reserves extra space for the label."
          ),
          HBox(
            PushButton(Opt("hstretch"), "Stretchable button"),
            ReplacePoint(Id("rp"), Label("Label"))
          )
        )
      )
      UI.UserInput()

      UI.ReplaceWidget(Id("rp"), Left(Label("Left")))
      UI.UserInput()

      UI.ReplaceWidget(Id("rp"), Right(Label("Right")))
      UI.UserInput()

      UI.ReplaceWidget(Id("rp"), HCenter(Label("HCenter")))
      UI.UserInput()
      UI.CloseDialog()

Alignment().main()
