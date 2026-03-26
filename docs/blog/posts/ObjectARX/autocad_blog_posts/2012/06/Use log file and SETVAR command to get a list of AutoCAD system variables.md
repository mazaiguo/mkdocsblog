---
title: "Use log file and SETVAR command to get a list of AutoCAD system variables"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Unicode
description: "You may want to output the system variables to a text file. This VB.NET example turns the log file on and runs the SETVAR command. The QAFLAGS sett..."
author: Autodesk
---
# Use log file and SETVAR command to get a list of AutoCAD system variables

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-log-file-and-setvar-command-to-get-a-list-of-autocad-system-variables.html

## 文章内容

By Wayne Brill
You may want to output the system variables to a text file. This VB.NET example turns the log file on and runs the SETVAR command. The QAFLAGS setting of 2 enables the command to complete without having to hit Enter multiple times.
<CommandMethod("saveTheVars")> _
Public Sub saveVars()
    Dim strLogFileName As String = _
      Application.GetSystemVariable("LOGFILENAME")
      MsgBox("Varibles saved in " & strLogFileName)
      ' Setting QAFLAGS to 2 allows you to avoid
    ' hitting enter multiple times
    Application.SetSystemVariable("QAFLAGS", 2)
      Application.DocumentManager.MdiActiveDocument _
        .SendStringToExecute _
              ("_.LOGFILEON ", False, False, False)
      Dim strCmd As String
    strCmd = _
"(command" & """_setvar""" & """?""" & """*""" & ")" _
      & vbCrLf
      Application.DocumentManager.MdiActiveDocument. _
        SendStringToExecute _
                        (strCmd, False, False, False)
      Application.DocumentManager.MdiActiveDocument. _
        SendStringToExecute _
               ("_.LOGFILEOFF ", False, False, False)
  End Sub

