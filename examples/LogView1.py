# encoding: utf-8

from yast import *
class LogView1Client:
    def main(self):
      part1 = "They sought it with thimbles, they sought it with care;\n"
      part1 = part1 + "They pursued it with forks and hope;\n"
      part1 = part1 + "They threatened its life with a railway-share;\n"
      part1 = part1 + "They charmed it with smiles and soap. \n" + "\n"

      part2 = "Then the Butcher contrived an ingenious plan\n"
      part2 = part2 +  "For making a separate sally;\n"
      part2 = part2 +  "And fixed on a spot unfrequented by man,\n"
      part2 = part2 +  "A dismal and desolate valley. \n" + "\n"

      part3 = "But the very same plan to the Beaver occurred:\n"
      part3 = part3 +  "It had chosen the very same place:\n"
      part3 = part3 +  "Yet neither betrayed, by a sign or a word,\n"
      part3 = part3 + "The disgust that appeared in his face. \n" + "\n"

      part4 = "Each thought he was thinking of nothing but \"Snark\"\n"
      part4 = part4 +  "And the glorious work of the day;\n"
      part4 = part4 +  "And each tried to pretend that he did not remark\n"
      part4 = part4 +  "That the other was going that way. \n" + "\n"

      part5 = "But the valley grew narrow and narrower still,\n"
      part5 = part5 +  "And the evening got darker and colder,\n"
      part5 = part5 +  "Till (merely from nervousness, not from goodwill)\n"
      part5 = part5 +  "They marched along shoulder to shoulder. \n" + "\n"

      part6 = "Then a scream, shrill and high, rent the shuddering sky,\n"
      part6 = part6 +  "And they knew that some danger was near:\n"
      part6 = part6 +  "The Beaver turned pale to the tip of its tail,\n"
      part6 = part6 +  "And even the Butcher felt queer. \n" + "\n"

      part7 = "He thought of his childhood, left far far behind--\n"
      part7 = part7 +  "That blissful and innocent state--\n"
      part7 = part7 +  "The sound so exactly recalled to his mind\n"
      part7 = part7 +  "A pencil that squeaks on a slate! \n" + "\n"

      part8 = "\"'Tis the voice of the Jubjub!\" he suddenly cried.\n"
      part8 = part8 +  "(This man, that they used to call \"Dunce.\")\n"
      part8 = part8 +  "\"As the Bellman would tell you,\" he added with pride,\n"
      part8 = part8 +  "\"I have uttered that sentiment once.\n" + "\n"

      thats_it = "\n\n*** Press [OK] once more to exit. ***"


      UI.OpenDialog(
        VBox(
          LogView(
            Id("log"),
            "&Excerpt from \"The Hunting Of The Snark\" by Lewis Carroll",
            5, # visible lines
            10
          ), # lines to store
          PushButton(Opt("default"), "&OK")
        )
      )

      UI.ChangeWidget(Id("log"), "LastLine", part1)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part2)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part3)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part4)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part5)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part6)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part7)
      UI.UserInput()
      UI.ChangeWidget(Id("log"), "LastLine", part8)
      UI.UserInput()

      UI.ChangeWidget(Id("log"), "Value", thats_it)
      UI.UserInput()
      UI.CloseDialog()


LogView1Client().main()

