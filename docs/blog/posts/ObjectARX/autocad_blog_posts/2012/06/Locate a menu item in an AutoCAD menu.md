---
title: "Locate a menu item in an AutoCAD menu"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "With classic UI, if you want to add a item AutoCAD menu at run time, you can locate the menu by Application.MenuBar and call AddMenuItem. AddMenuIt..."
author: Autodesk
---
# Locate a menu item in an AutoCAD menu

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/locate-a-menu-item-in-an-autocad-menu.html

## 文章内容

By Xiaodong Liang
With classic UI, if you want to add a item AutoCAD menu at run time, you can locate the menu by Application.MenuBar and call AddMenuItem. AddMenuItem specifies the index of your item and its corresponding macro to execute.
The following code finds the menu of File, and adds one custom item as the first one in the list of File menu. It provides a macro to execute Open.
' This procedure finds a menu item in a pull down menu
' and inserts a new menu item above it
Public Sub findMenuItem()
     Dim aMenuGrp As AcadMenuGroup
   Dim aPupMenu As AcadPopupMenu
   Dim aPupMenuItem As AcadPopupMenuItem
   Dim newMenuItem As AcadPopupMenuItem
   Dim int1 As Integer
   Dim aPupName As String
   Dim strTestTag As String
   Dim openMacro As String
     int1 = -1
   ' Change the value to the Tag of the menu Item
   ' You want to insert above in the pull down menu
   'strTestTag = "ID_AcadWeb" 'Only for AutoCAD 2000
    strTestTag = "ID_New"     'for All AutoCAD version
   ' Iterate through each menu group
   For Each aMenuGrp In App.MenuGroups 
      ' Iterate through each popup menu
    For Each aPupMenu In aMenuGrp.Menus
          ' Iterate through each popup menu item
        For Each aPupMenuItem In aPupMenu
          ' Get the index of the object based on the TagString
        ' and the name of the parent (a Popup Menu) if the
        ' TagString is equal to the value in strTestTag
            If aPupMenuItem.TagString = strTestTag Then
                  ' Get the name of the Popup menu
                aPupName = aPupMenuItem.Parent.Name
                  ' Get the index of the menu item
                int1 = aPupMenuItem.Index
                Exit For
            End If
        Next
        If int1 <> -1 Then Exit For
      Next
      If int1 <> -1 Then Exit For
   Next
     If aPupName <> "" Then
        ' Assign the macro the equivalent of "ESC ESC _open "
        openMacro = Chr(3) + Chr(3) +  _
            Chr(16) + Chr(95) + "open" + Chr(32)
          ' Insert a new menu Item above the item found above
         newMenuItem = app.MenuBar(aPupName).AddMenuItem(int1, _
                        "&Test3...", openMacro)
   End If
  End Sub

## 评论

**内容**: Sanjay Kulkarni said...
Hello,
When 'Option strict' is On, the following code two lines of code give me error
1. For Each aMenuGrp In App.MenuGroups
2. newMenuItem = app.MenuBar(aPupName).AddMenuItem(int1, _
"&Test3...", openMacro)
I was able to overcome the first error using DirectCast.
But I am not able to overcome the second error - Option strict does not allow late binding'
Can you help?
Also I had to replace app with Application at two places.
Reply
08/14/2012 at 03:22 AM

---
**内容**: Craig said...
Hi
What are the references required to access the classes AcadMenuGroup etc. ?
Reply
05/02/2014 at 05:51 AM

---
**内容**: YASSER MAHMOUD said...
Hi,
can any one tell me how to add a new menu to the menu bar, then i can add my menu items in it??
please help me with a piece of code in vb.net
Reply
10/26/2015 at 02:19 AM

---
