# encoding: utf-8

# Example for a RichText widget
from yast import *
class RichText3Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          RichText(
            "<h3>RichText example</h3>" +
              "<p>This is a <i>RichText</i> widget. Lines are wrapped automatically, this is a very very very very long long long long long long line .</p>" +
              "<p>It's very much like <i>HTML</i>, but not quite as powerful.</p>" +
              "<p>Text in <b>pre</b> tags preserves newlines and spaces.</p>" + "<pre>" + "Table in pre\n" +
              "\t\thost\tip adress       info      description\n" +
              "\t\tsturm\t10.10.0.159     old       work station\n\n" +
              "Lines are    <i>not</i>      wrapped but HTML tags are <b>interpreted</b>" +
              " and entities like product: &product; are filtered and shown correctly." + "</pre>" +
              "<p>After   <b>/pre</b>    the  text is <i>HTML</i> text like before.</p>" +
              "<p>Much much more text .............. continous" +
              " much much more text .... follows " +
              " much much more text .................</p>" +
              "<pre><small>another    pre      t\tt\t</small></pre>" +
              "<p>and more text after pre is closed, now <b>HTML</b> text,\n" +
              "newlines are removed." + "</p>" +
              "<pre>Another text in pre preserving spaces and newlines\n" +
              "     host     ip adress       host     ip adress\n" +
              "     sturm    10.10.0.159     sturm    10.10.0.159\n" +
              "Lines are not wrapped; in newest version HTML tags are <b>interpreted</b> \tif the pre tag is used.\n" + "</pre>" +
              "<p>And after closing pre tag  much more text - <b>long</b> long long long long lines are now wrapped again, this is a very very very very long long long long long long line <i>Even</i> longer and longer, line is wrapped again</p>" +
              "<p><pre>And   another  short  pre</pre></p>"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


RichText3Client().main()

