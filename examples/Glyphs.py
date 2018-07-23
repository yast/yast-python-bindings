from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class GlyphsClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("Glyphs"),
          Left(Label(UI.Glyph("ArrowLeft") + " ArrowLeft")),
          Left(Label(UI.Glyph("ArrowRight") + " ArrowRight")),
          Left(Label(UI.Glyph("ArrowUp") + " ArrowUp")),
          Left(Label(UI.Glyph("ArrowDown") + " ArrowDown")),
          Left(Label(UI.Glyph("CheckMark") + " CheckMark")),
          Left(Label(UI.Glyph("BulletArrowRight") + " BulletArrowRight")),
          Left(Label(UI.Glyph("BulletCircle") + " BulletCircle")),
          Left(Label(UI.Glyph("BulletSquare") + " BulletSquare")),
          VSpacing(),
          Left(
            Label(
              "If you see only question marks,\n" +
                "maybe you forgot to start this example\n" +
                "with the correct font -\n" +
                "use the 'start_glyphs' script!"
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


GlyphsClient().main()

