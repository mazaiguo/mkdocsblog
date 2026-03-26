---
title: "DIESEL expression in menu label not evaluated when used with AddMenuItem()"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Question: I use the following VB.NET code and instead of the label displaying "Full Screen On" or "Full Screen Off", the DIESEL string is displayed..."
author: Autodesk
---
# DIESEL expression in menu label not evaluated when used with AddMenuItem()

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/diesel-expression-in-menu-label-not-evaluated-when-used-with-addmenuitem.html

## 文章内容

By Barbara Han
Question: I use the following VB.NET code and instead of the label displaying "Full Screen On" or "Full Screen Off", the DIESEL string is displayed in AutoCAD Classic menu.
  Sub DIESEL_problem()
    Dim currMenuGroup As AcadMenuGroup
    currMenuGroup = ThisDrawing.Application.MenuGroups.Item(0)
      ' Create the new menu
    Dim newMenu As AcadPopupMenu
    Try
      newMenu = currMenuGroup.Menus.Item("DIESEL_Problem")
    Catch ex As Exception
      newMenu = currMenuGroup.Menus.Add("DIESEL_Problem")
    End Try
    Dim CommandName As String
    CommandName = "($if,$(=,$(getvar,tilemode),0),Full &Screen ON,Full &Screen OFF)"
      ' Add a menu item to the new menu
    Dim newMenuItem As AcadPopupMenuItem
    Dim openMacro As String
    ' Assign the macro string the VB equivalent of "ESC ESC _open "
    openMacro = Chr(3) & Chr(3) & Chr(95) & "open" & Chr(32)
    newMenuItem = newMenu.AddMenuItem(newMenu.Count + 1, CommandName, openMacro)
      ' Display the menu on the menu bar
    newMenu.InsertInMenuBar(ThisDrawing.Application.MenuBar.Count + 1)
    End Sub
Solution: The work around is to use the label property. Here is an example that shows this. After creating the menu Item, the label property is set using the DIESEL expression.
  Sub DIESEL_fix()
    Dim currMenuGroup As AcadMenuGroup
    currMenuGroup = ThisDrawing.Application.MenuGroups.Item(0)
      ' Create the new menu
    Dim newMenu As AcadPopupMenu
    Try
      newMenu = currMenuGroup.Menus.Item("DIESEL_fix")
    Catch ex As Exception
      newMenu = currMenuGroup.Menus.Add("DIESEL_fix")
    End Try
      ' Add a menu item to the new menu
    Dim newMenuItem As AcadPopupMenuItem
    Dim openMacro As String
    ' Assign the macro string the VB equivalent of "ESC ESC _open "
    openMacro = Chr(3) & Chr(3) & Chr(95) & "open" & Chr(32)
      newMenuItem = newMenu.AddMenuItem(newMenu.Count + 1, "placeHolder", openMacro)
      newMenuItem.Label = "$(if,$(=,$(getvar,tilemode),0),Full &Screen ON,Full &Screen OFF)"
      ' Display the menu on the menu bar
    newMenu.InsertInMenuBar(ThisDrawing.Application.MenuBar.Count + 1)
    End Sub
Addendum: Please refer to below sample to get the AutoCAD document which is used in above code:
Imports Autodesk.AutoCAD.Interop
Imports Autodesk.AutoCAD.Interop.Common
……
  Private ThisDrawing As Object
  Private Sub Button1_Click(sender As System.Object, e As System.EventArgs) Handles Button1.Click
    Dim acadApp As AcadApplication = Nothing
      Try
      acadApp = GetObject(, "AutoCAD.Application")
      acadApp.Visible = Visible
      Catch ex As Exception
      Try
        acadApp = CreateObject("AutoCAD.Application.18.2")
        acadApp.Visible = Visible
      Catch ex1 As Exception
        MsgBox(ex1.Message)
      End Try
    End Try
    ThisDrawing = acadApp.ActiveDocument
    'DIESEL_problem()
    DIESEL_fix()
  End Sub

## 评论

**内容**: Tunnel Rush said...
"The work Around is to use the label property." I am looking for this remedy to complete my work. Thank.
Reply
04/19/2023 at 09:16 PM

---
