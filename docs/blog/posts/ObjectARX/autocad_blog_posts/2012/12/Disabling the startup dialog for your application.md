---
title: "Disabling the startup dialog for your application"
date: 2012-12-01
categories:
  - AutoCAD VBA
tags:
  - API
  - AutoCAD
  - COM
  - VBA
description: "The setting for controlling the startup dialog is stored in a profile in the system registry. The preferred way to have application-specific settin..."
author: Autodesk
---
# Disabling the startup dialog for your application

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/disabling-the-startup-dialog-for-your-application.html

## 文章内容

By Gopinath Taget
The setting for controlling the startup dialog is stored in a profile in the system registry. The preferred way to have application-specific settings that do not apply to "normal" use of AutoCAD would be to set up a profile for your application. When this profile is active, you can then change the system variables to the values you require, and then set the active profile back to the default one. You can
then make a special shortcut for your application, which calls AutoCAD with the /p switch, specifying your application's profile.
The ActiveX API is the easiest way to achieve this. The following sample code is for a Visual Basic application (which might be called from your installation script):
Dim Acad As Object
Dim strDefaultActiveProfile As String
Set Acad = CreateObject("AutoCAD.Application")
'Get active profile name
strDefaultActiveProfile = Acad.Preferences.Profiles.ActiveProfile
'Set active profile name to ours, then change settings
Acad.Preferences.Profiles.ActiveProfile = "My Application Profile"
Acad.Preferences.System.EnableStartupDialog = False
'Restore the previous active profile
Acad.Preferences.Profiles.ActiveProfile = strDefaultActiveProfile
Acad.Quit
This starts AutoCAD, sets a new profile named "My Application Profile", sets the Start Up dialog to not display, and then resets the profile to the default and exits AutoCAD. Please note that this should be used from your installation program only to create your profile and its settings. Subsequent "real" usage of your application should start AutoCAD with /p "My Application Profile".

