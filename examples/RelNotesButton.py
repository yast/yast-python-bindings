# encoding: utf-8

# Trivial example for Release Notes button 
from yast import *

class RelNotesButtonClient:
    def main(self):
      
      rel_notes_file =  "./RELEASE-NOTES.en.txt" if UI.TextMode() else "./RELEASE-NOTES.en.rtf"       
      rel_notes_text = SCR.Read(path(".target.string"), rel_notes_file)
      rel_notes = {"SLES12" : rel_notes_text, "Some-Add-On" : "some text" }

      UI.SetReleaseNotes(rel_notes)
    
      UI.OpenDialog(
        VBox(
          Right(PushButton(Id("relNotes"), Opt("relNotesButton"), "&Release Notes")),
          VSpacing(2.0),
          Heading("Expert Dialog"),
          VSpacing(2.0),
          MinSize(
            60,
            15,
            MarginBox(
              1.0,
              0.5,
              CheckBoxFrame(
                "E&xpert Settings",
                True,
                VBox(
                  HBox(
                    InputField("&Server"),
                    ComboBox("&Mode", ["Automatic", "Manual", "Debug"])
                  ),
                  Left(CheckBox("&Logging")),
                  InputField("&Connections")
                )
              )
           )
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      while True:
        id = UI.UserInput()
        if id == "ok" or id == "cancel":
          break

      UI.CloseDialog()


RelNotesButtonClient().main()

