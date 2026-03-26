---
title: "Access AutoCAD Group subsystem via .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Like other object, Groups also have ObjectId, and it can be accessed through its dictionary. This code sample shows how read the dictionary and wha..."
author: Autodesk
---
# Access AutoCAD Group subsystem via .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/access-autocad-group-subsystem-via-net.html

## 文章内容

By Augusto Goncalves
Like other object, Groups also have ObjectId, and it can be accessed through its dictionary. This code sample shows how read the dictionary and what is inside.
<CommandMethod("getGroupIds")> _
Public Sub CmdGetGroupIds()
  ' input the group name we want to list
  Dim ed As Editor = Application.DocumentManager.
    MdiActiveDocument.Editor
  Dim groupName As PromptResult =
    ed.GetString("Enter Group name to list : ")
  ' get the working database
  Dim db As Database = Application.DocumentManager.
    MdiActiveDocument.Database
  ' start a transaction
  Using trans As Transaction =
    db.TransactionManager.StartTransaction()
    ' now try the read
    Try
      ' now get the ACAD_GROUP dictionary entry,
      ' this contains all of the Groups defined in the drawing
      Dim acadGroup As DBDictionary =
        trans.GetObject(db.GroupDictionaryId, OpenMode.ForRead)
      ' next, find the group name that was entered above
      Dim groupRequired As Group =
        trans.GetObject(acadGroup(groupName.StringResult),
                        OpenMode.ForRead)
      ' we now have the group required, lets find out what's inside
      Dim entityIds As ObjectId() = groupRequired.GetAllEntityIds()
      Dim id As ObjectId
      For Each id In entityIds
        ' open the entity for read
        Dim ent As Entity = trans.GetObject(id, OpenMode.ForRead)
        ' create the highlight path
        Dim path As FullSubentityPath = New  _
          FullSubentityPath(New ObjectId(0) _
                            {id},
                            New SubentityId(SubentityType.Null, 0))
        ' now highlight it
        ent.Highlight(path, True)
      Next
      trans.Commit()
    Catch
      End Try
  End Using
End Sub

