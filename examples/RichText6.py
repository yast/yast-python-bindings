# encoding: utf-8

# Example for a RichText widget
from yast import *
class RichText6Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          RichText(
            "<h1>The big headline (level 1)</h1>" +
              "<p>This is a <i>RichText</i> widget.</p>" +
              "<p>It's very much like <i>HTML</i>, but not quite as powerful.</p>" +
              "<p><b>bold</b> and <i>italic</i> you can rely on.</p>" + "<p>" +
              "<h2>An ordered list (headline level 2)</h2>" + "<ol>" +
              "<li>First list entry</li>" +
              "<li>Second one \t</li>" + "<ol>" +
              "<li>and more info</li>" +
              "<li>and more and more</li>" + "</ol>" +
              "<li>And so on</li>" +
              "<li>and even more</li>" + "</ol>" +
              "<h2>An unordered list</h2>" + "<ul>" +
              "<li>An unordered list entry </li>" +
              "<li>and another...</li>" + "<ul>" +
              "<li>Argumets are these:</li>" + "<ol>" +
              "<li>first point is...</li>" +
              "<li>second point is that</li>" + "</ol>" +
              "<li>and another argument</li>" + "</ul>" +
              "<li>and last entry</li>" + "</ul>" +
              "<h2>Text mode ignores:</h2>" + "<pre>" +
              "&lt;big&gt;      &lt;small&gt;     &lt;font&gt;\n" +
              " <big>big</big>        <small>small</small>       <font>font</font>" + "</pre>"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


RichText6Client().main()

