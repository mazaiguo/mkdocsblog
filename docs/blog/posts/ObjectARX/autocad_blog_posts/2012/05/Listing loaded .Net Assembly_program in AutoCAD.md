---
title: "Listing loaded .Net Assembly/program in AutoCAD"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "There is no direct AutoCAD API to determine this. Using .NET API’s, you can list all the loaded assemblies in AutoCAD."
author: Autodesk
---
# Listing loaded .Net Assembly/program in AutoCAD

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/listing-loaded-net-assemblyprogram-in-autocad.html

## 文章内容

By Virupaksha Aithal
There is no direct AutoCAD API to determine this. Using .NET API’s, you can list all the loaded assemblies in AutoCAD.
        <Autodesk.AutoCAD.Runtime.CommandMethod("MYDLLS", "MYDLLS", _
                Autodesk.AutoCAD.Runtime.CommandFlags.Transparent)> _
        Public Shared Sub MYDLLS()
            Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
              Dim ed As Editor = doc.Editor
              Dim Asmbly As System.Reflection.Assembly
            Dim strAssem As String = ""
            Dim strAssemName As String = ""
            'following for loop shows list of assembly details
            For Each Asmbly In _
                        System.AppDomain.CurrentDomain.GetAssemblies()
                strAssem += Asmbly.FullName() + vbCrLf
            Next
            ed.WriteMessage(strAssem)
              'following for loop shows list assembly names only
            For Each Asmbly In _
                        System.AppDomain.CurrentDomain.GetAssemblies()
                Dim strDll As String()
                Dim strDllLocation As String
                strDllLocation = Asmbly.Location.ToString
                strDll = Asmbly.Location.Split("\\")
                strDllLocation = strDll.GetValue(strDll.Length() - 1)
                strAssemName += strDllLocation + vbCrLf
            Next
            ed.WriteMessage(strAssemName)
        End Sub

