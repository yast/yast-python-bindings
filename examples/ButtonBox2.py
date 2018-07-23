from __future__ import unicode_literals
# encoding: utf-8

# Demo for common ButtonBox-based dialogs
import copy
from yast import import_module
import_module('UI')
from yast import *

class ButtonBox2Client:
    def main(self):




      buttons = VBox(
        PushButton(Id("okCancel"), Opt("hstretch"), "&OK / Cancel"),
        PushButton(Id("yesNo"), Opt("hstretch"), "&Yes / No"),
        PushButton(Id("continueCancel"), Opt("hstretch"), "C&ontinue / Cancel"),
        PushButton(Id("okApply"), Opt("hstretch"), "OK / &Apply / Cancel"),
        PushButton(
          Id("okEtcHelp"),
          Opt("hstretch"),
          "OK / Apply / Cancel / &Help"
        ),
        PushButton(
          Id("okCustom"),
          Opt("hstretch"),
          "OK / Apply / Cancel / C&ustom / Help"
        ),
        PushButton(Id("okOnly"), Opt("hstretch"), "O&K"),
        PushButton(Id("okRetry"), Opt("hstretch"), "OK / Re&try (Error!)"),
        PushButton(Id("retryCancel"), Opt("hstretch"), "&Retry / Cancel")
      )

      UI.OpenDialog(
        MarginBox(
          1.0,
          0.5,
          VBox(
            Heading("ButtonBox Examples"),
            VSpacing(0.5),
            HVCenter(HSquash(buttons)),
            VSpacing(0.5),
            Right(PushButton(Id("close"), "&Close"))
          )
        )
      )

      button = None
      while True:
        button = UI.UserInput()

        if button == "okCancel":
            okCancelDialog()
        if button == "yesNo":
            yesNoDialog()
        if button == "continueCancel":
            continueCancelDialog()
        if button == "okApply":
            okApplyCancelDialog()
        if button == "okEtcHelp":
            okApplyCancelHelpDialog()
        if button == "okCustom":
            okApplyCancelCustomHelpDialog()
        if button == "okOnly":
            okDialog()
        if button == "okRetry":
            okRetryDialog()
        if button == "retryCancel":
            retryCancelDialog()
        if button == "close" or button == "cancel": # [Close] button # WM_CLOSE
            break
      UI.CloseDialog()

def showDialog(buttonBox):
      #buttonBox = copy.deepcopy(buttonBox)
      success = UI.OpenDialog(VBox(HVCenter(Label("Hello, World!")), buttonBox))

      # Most YCP developers never use the return value of UI::OpenDialog().
      # Many of them probably don't even know that it has a return value.
      #
      # Used properly, that return value can be used to recover from error
      # situations that would otherwise abort the program - like in this case.

      if success:
        UI.UserInput()
        UI.CloseDialog()

def okCancelDialog():
      showDialog(
        ButtonBox(
          PushButton(Id("ok"), "&OK"),
          PushButton(Id("cancel"), "&Cancel")
        )
      )


def yesNoDialog():
      showDialog(
        ButtonBox(PushButton(Id("yes"), "&Yes"), PushButton(Id("no"), "&No"))
      )


def continueCancelDialog():
      showDialog(
        ButtonBox(
          PushButton(Id("continue"), "C&ontinue"),
          PushButton(Id("cancel"), "&Cancel")
        )
      )

def okApplyCancelDialog():
      showDialog(
        ButtonBox(
          PushButton(Id("ok"), "&OK"),
          PushButton(Id("apply"), "&Apply"),
          PushButton(Id("cancel"), "&Cancel")
        )
      )


def okApplyCancelHelpDialog():
      showDialog(
        ButtonBox(
          PushButton(Id("ok"), "&OK"),
          PushButton(Id("apply"), "&Apply"),
          PushButton(Id("cancel"), "&Cancel"),
          PushButton(Id("help"), "&Help")
        )
      )


def okApplyCancelCustomHelpDialog():
      showDialog(
        ButtonBox(
          PushButton(Id("ok"), "&OK"),
          PushButton(Id("apply"), "&Apply"),
          PushButton(Id("cancel"), "&Cancel"),
          PushButton(Id("custom1"), "&Do Something"),
          PushButton(Id("custom2"), "Do &More"),
          PushButton(Id("help"), "&Help")
        )
      )


def okDialog():
      showDialog(ButtonBox(PushButton(Id("ok"), "&OK")))


def okRetryDialog():
      # This will throw an error:
      # If there is more than one button in a button box, one of them must
      # have the [OK] role and one must have the [Cancel] role.

      showDialog(
        ButtonBox(PushButton(Id("ok"), "&OK"), PushButton(Id("retry"), "&Retry"))
      )


def retryCancelDialog():
      # Explicitly assigning the [OK] role to the [Retry] button

      showDialog(
        ButtonBox(
          PushButton(Id("retry"), Opt("okButton"), "&Retry"),
          PushButton(Id("cancel"), "&Cancel")
        )
      )

ButtonBox2Client().main()
