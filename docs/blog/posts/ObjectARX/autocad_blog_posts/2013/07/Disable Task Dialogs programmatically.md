---
title: "Disable Task Dialogs programmatically"
date: 2013-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - Unicode
  - XREF
description: "I didn’t realize how tricky it was to disable task dialogs programmatically until a developer asked me recently about it. What I’m talking about ar..."
author: Autodesk
---
# Disable Task Dialogs programmatically

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/disable-task-dialogs-programmatically.html

## 文章内容

by Fenton Webb
I didn’t realize how tricky it was to disable task dialogs programmatically until a developer asked me recently about it. What I’m talking about are these pesky dialogs that appear with either the “Do not show me this message again” or “Always use this choice in the future” texts…
These ‘hide dialog’ settings are stored in your %APPDATA%\Autodesk\AutoCAD 2014\R19.1\enu\Support\Profiles\Unnamed Profile\fixedprofile.aws under the HideableDialogs section.
You can access the previously ‘hidden’ dialogs (to bring them back) inside of AutoCAD via Options->System->Hidden Messages Settings button.
We currently only have an undocumented C++ API for accessing these settings. (by the way here’s the AdTaskDialog.h header file for accessing the below API)
1) Gain access to the hideable dialog settings object
AdHideableDialogSettingsDictionary* pDict = AdTaskDialog::GetHideableDialogSettingsDictionary();
2) To disable/enable a specific dialog, look at the FixedProfile.aws and extract the id string, e.g. for the XRef unresolved XRefs task dialog…
<HideableDialogs>
  <HideableDialog id="Acad.UnresolvedReferenceFiles" title="Always ignore unresolved references and continue"
now call
pDict->SetResult("Acad.UnresolvedReferenceFiles", true);

## 评论

**内容**: Tim said...
Dim HideDic As Autodesk.Internal.Windows.HideableDialogSettingsDictionary = Autodesk.Windows.TaskDialog.HideableDialogSettingsDictionary
HideDic.GetResult("MainFrame.CommandLineHideWindow")
HideDic.SetResult("MainFrame.CommandLineHideWindow", 6)
Will set the result if it already exist.
I need to be able to create a new one if it does not already exist.
So I am not too fluent in C++

Reply
01/24/2018 at 09:56 AM

---
**内容**: Tim said in reply to Tim...
Dim CmdLin As New Autodesk.Internal.Windows.HideableDialogSettings
CmdLin.Id = "MainFrame.CommandLineHideWindow
CmdLin.Result = 6
HideDic.Add(CmdLin)
Autodesk.AutoCAD.Internal.Windows.ProfileManager.SaveHideableDialogSettingsDictionary()
Reply
01/24/2018 at 04:37 PM

---
**内容**: Serge Camire said...
Hi,
There are 2 situations where you want to hide or stop hiding hideable dialog boxes programmatically:
1) You pick them one at the time because, as a CAD manager, you want to standardize your environment in some ways for some reasons. This would correspond the most to what Fenton suggested. To use an image, it’s like turning a breaker off in an electrical panel, one at a time.
2) You want to process thousands of drawings in batch and you don’t want to be interrupted by these dialog boxes. I will discuss about this case. To use an image, it’s like cutting the electricity with the main interrupter before the panel box. It is radical but this is what we need.
Said so, what do we do now since nothing is documented? My solution is this one. Read the embedded resources either from the AcTaskDialogs.dll file or the localized AcTaskDialogs.resources.dll located in the AutoCAD directory. They both contain the same crucial information you need like the dialog box keys (always in English). The ressources of these 2 files consist of a dictionary with 5 entries. One of them is named hideabletaskdialogs.baml. It’s a XML like file (hereafter called then BAML file). How to extract it is way beyond this intervention. To help you make it very short, you could start using ILSpy.exe and you’ll see the file in a snap of the fingers.
Please find a short excerpt from the file (the localized one):

x:Uid="TaskDialog_1" AllowDialogCancellation="True"
VerificationHandlerData="Ligne de commande"
VerificationText="Toujours fermer la fenêtre de la ligne de commande" … />
I counted from 94 to 149 different dialog boxes respectively for the versions of AutoCAD 2009 to 2021. Not only you find new ones in each new version of AutoCAD but sometimes, some of them may be withdrawn. Also, there are not only 2 possibilities of checkbox “Do not ...” or “Always …” but more than 50. This mean you have to understand the content of this file. Anyway, since it’s not documented, you will always be guilty is something wrong appends to you.
What is interesting in the BAML file is the attribute AllowDialogCancellation. Some dialogs have this attribute but some don’t. Those who have it may have a value of True or False. Does it mean that with should only populate the HideableDialogSettingsDictionary with those having “AllowDialogCancellation=True”? You won’t get any error message if you add them all. Will it crash AutoCAD on runtime?
The other interesting thing is the DefaultButton attribute. It may take one of the following values: 1, 5, 6, 7, 8, 1001, 1002 and 2001. Since there is no documentation, how to guess that the value 6 will always prevent AutoCAD from bringing up the dialog box and not 1001? I don't have tons of drawings to open that would allow me to find an example of each box and find my answers. For the moment, we will have to fall back on the value 6 for lack of anything better.
Needless to remind that the dialog boxes do not open without a reason. If you choose to turn them off for the duration of the batch file, it would be wise to reset the initial state. A copy of the FixedProfile.aws won’t do because AutoCAD will rewrite it at the closing time.
If ever Autodesk decides to make an API to hide these dialog boxes, it would be important to also have a new callback function that would pass the drawing full filename, the reason that would have caused the dialog box to open in normal time and the severity. This way, we could write a log file.
Reply
05/22/2020 at 03:02 PM

---
