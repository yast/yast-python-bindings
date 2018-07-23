from __future__ import unicode_literals
# encoding: utf-8

# -*- coding: utf-8 -*-
from yast import import_module
import_module('UI')
from yast import *
class SetLanguageClient:
    def main(self):
      # Example for UI::SetLanguage() UI::GetLanguage()

      UI.OpenDialog(
        VBox(
          InputField(Id("lang_field"), "&Language:"),
          HBox(
            Label("Current language:"),
            Label(
              Id("lang_label"),
              Opt("outputField", "hstretch"),
              UI.GetLanguage(False)
            )
          ),
          HBox(
            PushButton(Id("set"), "UI::&SetLanguage()\n"),
            PushButton(Id("get_strip"), "UI::&GetLanguage()\nstrip encoding"),
            PushButton(Id("get_nostrip"), "&UI::GetLanguage()\n&with encoding"),
            PushButton(Id("test_dialog"), "&Test Dialog"),
            HSpacing(3),
            PushButton(Id("close"), "&Close")
          )
        )
      )

      UI.SetFocus(Id("lang_field"))

      while True:
        id = UI.UserInput()

        if id == "close":
          UI.CloseDialog()
          return
        elif id == "get_strip":
          UI.ChangeWidget(Id("lang_field"), "Value", UI.GetLanguage(True))
        elif id == "get_nostrip":
          UI.ChangeWidget(Id("lang_field"), "Value", UI.GetLanguage(False))
        elif id == "set":
          UI.SetLanguage(
            UI.QueryWidget(Id("lang_field"), "Value"))
          UI.ChangeWidget(Id("lang_label"), "Value", UI.GetLanguage(False))
        elif id == "test_dialog":
          UI.OpenDialog(
            VBox(
              Heading("Test Dialog"),
              Label(
                "Fonts may have changed\n" +
                  "Gr\u00FC\u00DF Gott\n" +
                  "Czech (\u010Desky)\n" +
                  "Greek (\u0395\u03BB\u03BB\u03B7\u03BD\u03B9\u03BA\u03AC)\n" +
                  "Russian (\u0420\u0443\u0441\u0441\u043A\u0438\u0439)\n" +
                  "\u6F22\u5B57\u304B\u306A\u76F4\n" +
                  "Hangul (\uD55C\uAE00)"
              ),
              PushButton(Opt("default"), "&OK")
            )
          )
          UI.UserInput()
          UI.CloseDialog()


SetLanguageClient().main()

