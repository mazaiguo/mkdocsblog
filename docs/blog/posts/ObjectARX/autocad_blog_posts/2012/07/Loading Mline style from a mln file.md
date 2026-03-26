---
title: "Loading Mline style from a mln file"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
description: "You need to use database API “LoadMlineStyleFile” passing mline style and the file name to load the mline style from a external mln file. But this ..."
author: Autodesk
---
# Loading Mline style from a mln file

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/loading-mline-style-from-a-mln-file.html

## 文章内容

By Virupaksha Aithal
You need to use database API “LoadMlineStyleFile” passing mline style and the file name to load the mline style from a external mln file. But this API expects and loads files from AutoCAD support path only at present. So to address this issue, in below code, the path of the file is temporarily added to AutoCAD support path.
       <CommandMethod("LoadMlineStyle")> _
      Public Shared Sub LoadMlineStyle()
              Dim doc As Document = _
                    Application.DocumentManager.MdiActiveDocument
            Dim ed As Editor = doc.Editor
            Dim db As Database = doc.Database
              If Not System.IO.File.Exists("c:\temp\Test.mln") Then
                ed.WriteMessage("File missing at c:\temp\test.mln")
                Return
            End If
              'check if c:\temp is in acad supported path.
            Dim acadApp As Object = Application.AcadApplication
            Dim preferences As Object = acadApp.Preferences
            Dim files As Object = preferences.Files
            Dim path As String = files.SupportPath
              Dim bPathFound As Boolean = False
            Dim strList As String() = path.Split(";"c)
              For Each str As String In strList
                If String.Compare(str, "c:\temp", True) = 0 Then
                    bPathFound = True
                    Exit For
                End If
            Next
              If Not bPathFound Then
                files.SupportPath = path + ";" + "c:\Temp"
            End If
              'Style name and the file name..
            db.LoadMlineStyleFile("TEST", "c:\temp\Test.mln")
              If Not bPathFound Then
                files.SupportPath = path
            End If
          End Sub

