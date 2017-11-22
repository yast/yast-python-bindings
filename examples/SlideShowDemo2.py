# encoding: utf-8

# SlideShow demo: Using Wizard and MultiProgressMeter
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
import copy
from yast import *
class SlideShowDemo2Client:
    def main(self):

      base_installation_steps = [
        { "id" : "language", "label" : "Language" },
        { "id" : "proposal", "label" : "Installation Settings" },
        { "id" : "do_resize", "label" : "Perform Installation" },
        { "id" : "prepdisk", "label" : "Perform Installation" },
        { "id" : "kickoff", "label" : "Perform Installation" },
        { "id" : "rpmcopy", "label" : "Perform Installation" },
        { "id" : "finish", "label" : "Perform Installation" }
      ]

      config_steps = [
        { "id" : "root", "label" : "Root Password" },
        { "id" : "proposal_net", "label" : "Network" },
        { "id" : "ask_net_test", "label" : "Network" },
        { "id" : "do_net_test", "label" : "Network" },
        { "id" : "you", "label" : "Online Update" },
        { "id" : "auth", "label" : "Users" },
        { "id" : "user", "label" : "Users" },
        { "id" : "suseconfig", "label" : "Clean Up" },
        { "id" : "release_notes", "label" : "Release Notes" },
        { "id" : "proposal_hw", "label" : "Device Configuration" }
      ]

      steps = ycpbuiltins.flatten([base_installation_steps, config_steps])

      self.initialRpms = [600, 150, 30, 100]
      self.rpms = copy.deepcopy(self.initialRpms)
      self.useTimeout = False
      self.currentCd = 1
      self.megaBytesPerSecond = 2


      #
      # ----------------------------- main() ----------------------------------
      #


      if not UI.HasSpecialWidget("Wizard") or not UI.HasSpecialWidget("DumbTab"):
        ycpbuiltins.y2error(
          "This works only with UIs that provide the Wizard and the DumbTab widget!"
        )
        return

      help_text = "<p>Please wait while packages are being installed.</p>"
      slide_text = "\t\t\t\t\t\t\t\t<table cellspacing=\"10\" cellpadding=\"5\">\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t<td width =\"*\">\t\t\t\t\t\t\t\t\t<img src=\"/usr/share/YaST2/theme/current/icons/48x48/apps/yast-sound.png\"\t\talign=\"left\">\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\"*\">\t\t\t\t\t\t\t\t\t<p><font color=\"#00007f\"><b>XMMS and JuK - Powerful Jukeboxes</b></font></p>\t\t<p>XMMS is an excellent sound player for Linux. It is easy to use and supports\t\tvarious formats, including audio CDs. Test the many visualization plug-ins or\t\tdownload your favorite XMMS skins from the web.</p>\t\t\t\t\t<p>New in KDE: JuK, which classifies your MP3s and organizes your music\t\t\tcollection.</p>\t\t\t\t\t\t\t\t\t\t<p><b>Want More?</b></p>\t\t\t\t\t\t\t\t<p>The SUSE distribution features a wide range of applications for playing\t\tyour CDs and MP3 songs. For example, KsCD is a user-friendly CD player. The\t\ttrack information for most CDs is available on the Internet. Simply activate\t\tthe respective function to display the list.</p>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t</table>"



      UI.OpenDialog(
        Opt("defaultsize"),
        YCPWizard(
          Opt("stepsEnabled"),
          Id("back"),
          "&Back",
          Id("abort"),
          "Ab&ort",
          Id("next"),
          "&Next"
        )
      )

      # UI::DumpWidgetTree();

      UI.WizardCommand(
        Term(
          "SetDialogIcon",
          "/usr/share/YaST2/theme/current/icons/22x22/apps/YaST.png"
        )
      )
      UI.WizardCommand(Term("SetDialogHeading", "Package Installation"))
      UI.WizardCommand(Term("SetHelpText", help_text))

      UI.WizardCommand(Term("AddStepHeading", "Base Installation"))

      for step in ycpbuiltins.foreach(base_installation_steps):
        UI.WizardCommand(
          Term(
            "AddStep",
            step["label"],
            step["id"]
          )
        )


      UI.WizardCommand(Term("AddStepHeading", "Configuration"))

      for step in ycpbuiltins.foreach(config_steps):
        UI.WizardCommand(
          Term(
            "AddStep",
            step["label"],
            step["id"]
          )
        )

      UI.WizardCommand(Term("SetCurrentStep", "rpmcopy"))
      UI.WizardCommand(
        #Term("SetNextButtonLabel", useTimeout ? "&Stop" : "&Start")
        Term("SetNextButtonLabel", "&Stop"  if self.useTimeout else "&Start")
      )
      UI.WizardCommand(Term("SetBackButtonLabel", "S&tep"))

      slideShowPage = RichText(Id("slideText"), slide_text),

      cdTable = Table(
        Id("cdTable"),
        Opt("keepSorting"),
        Header("Media", "Size", "Packages", "Time"),
        [
          Item(Id("total"), "Total", "638.1 MB", "485", "23:31"),
          Item(Id("1-1"), "SLES-9 Base CD", "620.7 MB", "480", "20:23"),
          Item(Id("1-1"), "SLES-9 CD 1", "620.7 MB", "480", "20:23"),
          Item(Id("1-2"), "SLES-9 CD 2", "17.4 MB", "5", "3:08"),
          Item(Id("1-3"), "SLES-9 CD 3", "--", "--", "--:--"),
          Item(Id("1-4"), "SLES-9 CD 4", "--", "--", "--:--"),
          Item(Id("1-5"), "SLES-9 CD 5", "--", "--", "--:--"),
          Item(Id("2-1"), "SLES-9 SP 1 CD 1", "--", "--", "--:--"),
          Item(Id("2-2"), "SLES-9 SP 1 CD 2", "--", "--", "--:--"),
          Item(Id("3-1"), "SLES-9 SP 2 CD 1", "--", "--", "--:--")
        ]
      )

      detailsPage = VBox(
        Id("detailsPage"),
        VBox(
          VWeight(1, cdTable),
          VWeight(1, LogView(Id("pkgLog"), "", 6, 100)),
          ProgressBar(
            Id("progressCurrentPackage"),
            "hypercool-1.3.7 (143.3 MB)",
            100,
            42
          )
        )
      )

      UI.ReplaceWidget(
        Id("contents"),
        VBox(
          VWeight(
            1, # lower layout priority
            HBox(
              DumbTab(
                [
                  Item(Id("showSlideShow"), "Slide Sho&w"),
                  Item(Id("showDetails"), "&Details")
                ],
                VBox(
                  VSpacing(0.4),
                  VWeight(
                    1, # lower layout priority
                    HBox(
                      HSpacing(1),
                      ReplacePoint(Id("tabContents"), slideShowPage),
                      HSpacing(0.5)
                    )
                  ),
                  VSpacing(0.4)
                )
              ),
              HSpacing(0.5),
              VBox(
                Label(Id("totalRemaining"), self.totalRemainingTime()),
                VWeight(1, VMultiProgressMeter(Id("progress"), self.rpms))
              )
            )
          ),
          VSpacing(0.3),
          Label(Id("nextMedia"), Opt("hstretch"), "")
        )
      )


      while True:
        button = UI.TimeoutUserInput(100) if self.useTimeout else UI.UserInput()

        if button == "abort":
          break

        delta = 0
        if button == "next":
          self.useTimeout = not self.useTimeout
          UI.WizardCommand(
            Term("SetNextButtonLabel", "&Stop" if self.useTimeout else "&Start")
          )

          if self.currentCd < 0:
            self.currentCd = 1
        if button == "back":
          delta = 10
        elif button == "timeout":
          delta = 100
        elif button == "showSlideShow":
          ycpbuiltins.y2milestone("Switching to slide show")
          UI.ReplaceWidget("tabContents", slideShowPage)
        elif button == "showDetails":
          ycpbuiltins.y2milestone("detailsPage:\n%1", detailsPage)
          # y2debug( "detailsPage:\n%1", detailsPage );

          UI.ReplaceWidget("tabContents", detailsPage)


          UI.ChangeWidget(
            "pkgLog",
            "LastLine",
            self.pkgInfo("ClosedOffice", "0.8.3", 830.7, "The infamouse office suite")
            + "\n"
            + self.pkgInfo("cool-macs", "27.9.1", 250.3, "An editor-like OS") + "\n"
            + self.pkgInfo("hypercool", "1.3.7", 147.3, "A hyper cool gizmofier")
          )
          UI.RecalcLayout()

        if delta > 0:
          self.rpms = self.subtract(self.rpms, 10)
          UI.ChangeWidget("totalRemaining", "Value", self.totalRemainingTime())
          UI.ChangeWidget("nextMedia", "Value", self.nextMedia())
          UI.RecalcLayout()

      UI.CloseDialog()


    def mediaName(self, mediaNo):
      return ycpbuiltins.sformat("SuSE Linux Professional CD %1", mediaNo)


    def mediaChange(self, cdNo):
      UI.ChangeWidget("nextMedia", "Value", "")
      UI.OpenDialog(
        VBox(
          Label(ycpbuiltins.sformat("Please insert \n%1", self.mediaName(cdNo))),
          PushButton(Opt("default"), "&OK")
        )
      )
      # UI::TimeoutUserInput( 5 * 1000 );
      UI.UserInput()
      UI.CloseDialog()
      self.currentCd = cdNo



    def subtract(self, valueList, delta):
      valueList = copy.deepcopy(valueList)
      subtracted = False
      newList = []
      cdNo = 1
      newCd = -1
      total = 0

      for val in ycpbuiltins.foreach(valueList):
        cdNo = cdNo + 1
        total = total + val
        if val > 0 and not subtracted:
          val = val - delta
          subtracted = True

          if val <= 0:
            val = 0
            newCd = cdNo
        newList = ycpbuiltins.add(newList, val)

      UI.ChangeWidget("progress", "Values", newList)

      if newCd > 0 and newCd <= ycpbuiltins.size(valueList):
        self.mediaChange(newCd)

      if total <= 0:
        self.useTimeout = False
        UI.WizardCommand(Term("SetNextButtonLabel", "&Start"))
        newList = copy.deepcopy(self.initialRpms)
        self.currentCd = -1
        ycpbuiltins.y2milestone("Resetting to %1", self.rpms)

      return copy.deepcopy(newList)


    def twoDigits(self,n):
      return ycpbuiltins.sformat("0%1", n) if (n < 10) else ycpbuiltins.sformat("%1", n)

    def formatTime(self, seconds):
      hours = (seconds / 3600)
      minutes = (seconds / 60)
      seconds = (seconds % 60)
      return ycpbuiltins.sformat(
        "%1:%2:%3",
        hours,
        self.twoDigits(minutes),
        self.twoDigits(seconds)
      )


    def totalRemainingTime(self):
      left = 0

      for val in ycpbuiltins.foreach(self.rpms):
          left = left + val

      totalSeconds = left * self.megaBytesPerSecond

      return ycpbuiltins.sformat("Remaining:\n%1", self.formatTime(totalSeconds))


    def nextMedia(self):
      remaining = ""
      mediaType = "CD"

      if self.currentCd > 0 and ycpbuiltins.size(self.rpms) > self.currentCd:
        seconds = self.rpms[(self.currentCd - 1)] * self.megaBytesPerSecond
        remaining = ycpbuiltins.sformat(
          "Next %1: %2  --  %3",
          mediaType,
          self.mediaName(self.currentCd + 1),
          self.formatTime(seconds)
        )

      return remaining


    def pkgInfo(self, pkgName, pkgVersion, pkgSizeMB, pkgSummary):
      pkgSizeMB = copy.deepcopy(pkgSizeMB)
      info = ycpbuiltins.sformat("%1-%2 (%3 MB)", pkgName, pkgVersion, pkgSizeMB)

      if ycpbuiltins.size(pkgSummary) > 0:
        info = info + " - " +pkgSummary

      return info

SlideShowDemo2Client().main()

