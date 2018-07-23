from __future__ import unicode_literals
# encoding: utf-8

# Example for a RichText widget
from yast import import_module
import_module('UI')
from yast import *
class RichText4Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          RichText(
            "<h3>RichText example</h3>" +
              "<p>This is a <i>RichText</i> widget.</p>" +
              "<p>It's very much like <i>HTML</i>, but not quite as powerful.</p>" +
              "<p><b>bold</b> and <i>italic</i> you can rely on.<br>" +
              "But in text mode bold and italic it look the same.</p>" +
              "<p>Bold used for status:</p>" + "<p>" + "<pre>" +
              "<b>-i-</b>: keep the installed version ( package locked )<br>" +
              "<b> i </b>: All requirements of this pattern/language are satisfied" + "</pre>" + "</p>" +
              "<p>Italic used for special info:</p>" +
              "<p>Please read the <i>Users Manual</i>.</p>" +
              "<p>The &lt;tt&gt; typewriter tag is interpreted like bold in text mode.</p>" +
              "<p><tt>This is text in &lt;tt&gt;, looks like bold text in text mode.</tt></p>" +
              "<p>The product name is automatically replaced by the UI. " +
              "Use the special macro <b>&amp;product;</b> for that." + "</p>" +
              "<p>The current product name is <b>&product;</b>.</p>"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


RichText4Client().main()

