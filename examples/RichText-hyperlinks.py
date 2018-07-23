from __future__ import unicode_literals
# encoding: utf-8

# Example for a RichText widget with hyperlinks
from yast import import_module
import_module('UI')
from yast import *
class RichTextHyperlinksClient:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          RichText(
            "<h3>RichText example</h3>" +
              "<p>RichText may contain <a href=\"hyper\">hyperlinks</a>," +
              "very much like HTML.</p>" +
              "<p>Clicking on a <a href=\"link\">link</a> will make " +
              "<a href=\"user_input\">UI::UserInput()</a> return " +
              "with the <i>href</i> part of the hyperlink " +
              "as a (string) return value.</p>" +
              "<h3>Known (HTML-like) entities</h3>" + "<ul>" +
              "<li><b>&amp;product;</b> for the product name (<b>&product;</b>)" +
              "<li><b>&amp;amp;</b> for <b>&amp;</b>" +
              "<li><b>&amp;lt;</b> for <b>&lt;</b>" +
              "<li><b>&amp;gt;</b> for <b>&gt;</b>" + "</ul>"
          ),
          HBox(
            Label("You clicked: "),
            Label(Id("val"), Opt("outputField", "hstretch"), "")
          ),
          PushButton(Id("close"), Opt("default"), "&Close")
        )
      )


      ret = None
      while True:
        ret = UI.UserInput()

        if ret != None:
          val = ycpbuiltins.sformat("%1", ret)
          UI.ChangeWidget(Id("val"), "Value", val)
        if ret == "close":
          break

      UI.CloseDialog()


RichTextHyperlinksClient().main()

