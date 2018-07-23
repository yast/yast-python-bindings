from __future__ import unicode_literals
# encoding: utf-8

# NCurses SlideShow demo: No Wizard or MultiProgressMeter widget available,
# thus using simpler layout
from yast import import_module
import_module('Wizard')
import_module('UI')
from yast import *
import copy

class NCursesSlideShowDemoClient:
    def main(self):

      self.initialRpms = [600, 150, 30, 100]
      self.rpms = copy.deepcopy(self.initialRpms)
      self.totalToInstall = 0
      self.useTimeout = False
      self.currentCd = 1
      megaBytesPerSecond = 2



      #
      # ----------------------------- main() ----------------------------------
      #



      help_text = "<p>Please wait while packages are being installed.</p>"
      slide_text = "\t\t\t\t\t\t\t\t<table cellspacing=\"10\" cellpadding=\"5\">\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t<td width =\"*\">\t\t\t\t\t\t\t\t\t<img src=\"/opt/kde3/share/icons/crystalsvg/128x128/apps/kscd.png\"  width=\"100\"\talign=\"left\">\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\"*\">\t\t\t\t\t\t\t\t\t<p><font color=\"#00007f\"><b>XMMS and JuK - Powerful Jukeboxes</b></font></p>\t\t<p>XMMS is an excellent sound player for Linux. It is easy to use and supports\t\tvarious formats, including audio CDs. Test the many visualization plug-ins or\t\tdownload your favorite XMMS skins from the web.</p>\t\t\t\t\t<p>New in KDE: JuK, which classifies your MP3s and organizes your music\t\t\tcollection.</p>\t\t\t\t\t\t\t\t\t\t<p><b>Want More?</b></p>\t\t\t\t\t\t\t\t<p>The SUSE distribution features a wide range of applications for playing\t\tyour CDs and MP3 songs. For example, KsCD is a user-friendly CD player. The\t\ttrack information for most CDs is available on the Internet. Simply activate\t\tthe respective function to display the list.</p>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t</table>"


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

      self.totalToInstall = self.listSum(self.initialRpms)

      detailsPage = VBox(
        Id("detailsPage"), #, `VSpacing( 0.3 ),
        # `Label(`id(`nextMedia ), `opt( `hstretch), "" ) // Reserve space
        VWeight(1, cdTable),
        VWeight(1, LogView(Id("pkgLog"), "", 6, 100)),
        ProgressBar(
          Id("progressCurrentPackage"),
          "hypercool-1.3.7 (143.3 MB)",
          100,
          42
        ),
        ProgressBar(Id("progressTotal"), "Total", self.totalToInstall, 0)
      )


      contents = VBox(
        VSpacing(0.4),
        VWeight(
          1, # lower layout priority
          HBox(HSpacing(1), detailsPage, HSpacing(0.5))
        ),
        VSpacing(0.4)
      )

      Wizard.OpenNextBackDialog()
      Wizard.SetContents(
        "Package Installation",
        contents,
        help_text,
        True,
        True
      )
      Wizard.SetNextButton("startStop", "&Stop" if self.useTimeout else "&Start")
      Wizard.SetBackButton("step", "S&tep")

      #	UI::ChangeWidget(`nextMedia, `Value, nextMedia() + "      " ); // Reserve space
      #	UI::RecalcLayout();
      #	UI::ChangeWidget(`nextMedia, `Value, "" );	//
      #	// Intentionally omitting UI::RecalcLayout() so the reserved space remains


      while True:
        button = UI.TimeoutUserInput(100) if self.useTimeout else UI.UserInput()

        if button == "abort":
          break 

        delta = 0
        if button == "startStop":
          self.useTimeout = not self.useTimeout
          Wizard.SetNextButton("startStop", "&Stop" if self.useTimeout else "&Start")
          UI.RecalcLayout()

          if self.currentCd < 0:
            self.currentCd = 1
        if button == "step":
          delta = 10
        elif button == "timeout":
          delta = 100
        if delta > 0:
          self.rpms = self.install(self.rpms, 10)

          if UI.WidgetExists("nextMedia"):
            UI.ChangeWidget("nextMedia", "Value", nextMedia)
            UI.RecalcLayout()

      UI.CloseDialog()


    def mediaName(self, mediaNo):
      return ycpbuiltins.sformat("SuSE Linux Professional CD %1", mediaNo)


    def mediaChange(self, cdNo):
      if UI.WidgetExists("nextMedia"):
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



    def listSum(self, valueList):
      valueList = copy.deepcopy(valueList)
      sum = 0

      for val in ycpbuiltins.foreach(valueList):
         sum = sum + val

      return sum


    def install(self, valueList, delta):
      valueList = copy.deepcopy(valueList)
      subtracted = False
      newList = []
      cdNo = 1
      newCd = -1
      totalRemaining = 0

      for val in ycpbuiltins.foreach(valueList):
        cdNo = cdNo + 1
        totalRemaining = totalRemaining + val
        if val > 0 and not subtracted:
          val = val - delta
          subtracted = True

          if val <= 0:
            val = 0
            newCd = cdNo
        newList = ycpbuiltins.add(newList, val)

      UI.ChangeWidget(
        "progressTotal",
        "Value",
        self.totalToInstall - totalRemaining
      )

      if newCd > 0 and (newCd <= ycpbuiltins.size(valueList)):
        self.mediaChange(newCd)

      if totalRemaining <= 0:
        self.useTimeout = False
        Wizard.SetNextButton("startStop", "&Start")
        newList = copy.deepcopy(self.initialRpms)
        self.currentCd = -1
        ycpbuiltins.y2milestone("Resetting to %1", self.rpms)

      return copy.deepcopy(newList)


    def twoDigits(self, n):
      result = ycpbuiltins.sformat("0%1", n)  if n < 10 else ycpbuiltins.sformat("%1", n)
      return result


    def formatTime(self, seconds):
      hours = seconds / 3600
      minutes = seconds / 60
      seconds = seconds % 60
      result = ycpbuiltins.sformat(
        "%1:%2:%3",
        hours,
        twoDigits(minutes),
        twoDigits(seconds)
      )
      return result


    def nextMedia(self):
      remaining = ""
      mediaType = "CD"

      if self.currentCd > 0 and ycpbuiltins.size(self.rpms) > self.currentCd:
        seconds = self.pms * self.pms[self.currentCd - 1] * megaBytesPerSecond
        remaining = ycpbuiltins.sformat(
          "Next %1: %2  --  %3",
          mediaType,
          self.mediaName(self.currentCd + 1),
          formatTime(seconds)
        )

      return remaining


def pkgInfo(pkgName, pkgVersion, pkgSizeMB, pkgSummary):
      pkgSizeMB = deep_copy(pkgSizeMB)
      info = ycpbuiltins.sformat("%1-%2 (%3 MB)", pkgName, pkgVersion, pkgSizeMB)

      if ycpbuiltins.size(pkgSummary) > 0:
        info = info + " - " + pkgSummary

      return info

NCursesSlideShowDemoClient().main()

