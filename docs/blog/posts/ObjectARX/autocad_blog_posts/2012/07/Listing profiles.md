---
title: "Listing profiles"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Below code shows the procedure to get the profiles in the AutoCAD. Code also list the current profile and can set the current profile."
author: Autodesk
---
# Listing profiles

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/listing-profiles.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to get the profiles in the AutoCAD. Code also list the current profile and can set the current profile.
       <CommandMethod("ListProfiles")> _
       Public Shared Sub ListProfiles()
            Dim doc As Document = _
                    Application.DocumentManager.MdiActiveDocument
            Dim ed As Editor = doc.Editor
              Dim acadApp As Object = Application.AcadApplication
            Dim preferences As Object = acadApp.Preferences
            Dim profiles As Object = preferences.Profiles
              ed.WriteMessage("Current profile is " _
                                     + profiles.ActiveProfile + vbLf)
              'list the profiles
            Dim names As String() = Nothing
            profiles.GetAllProfileNames(names)
              For Each name As String In names
                ed.WriteMessage(name + vbLf)
            Next
              'to make the profile current, call ActiveProfile
            'profiles.ActiveProfile = "Test"
          End Sub

