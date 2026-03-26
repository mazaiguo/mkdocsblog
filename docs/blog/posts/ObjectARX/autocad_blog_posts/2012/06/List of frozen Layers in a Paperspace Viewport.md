---
title: "List of frozen Layers in a Paperspace Viewport"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Layer
description: "The names of frozen layers in a paperspace viewport are stored with xdata. Below is a VB.Net example that gets the xdata attached to the paperspace..."
author: Autodesk
---
# List of frozen Layers in a Paperspace Viewport

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/list-of-frozen-layers-in-a-paperspace-viewport.html

## 文章内容

By Balaji Ramamoorthy
The names of frozen layers in a paperspace viewport are stored with xdata. Below is a VB.Net example that gets the xdata attached to the paperspace viewport you select. If the xdata contains a group code 1003 then there are frozen layers for the pspace vport. A message is displayed listing the frozen layers.
<CommandMethod("ListFrozenLayers", CommandFlags.NoTileMode)> _
Sub ListFrozenLayersMethod()
    Dim doc As Document = Application.DocumentManager.MdiActiveDocument
    Dim ed As Editor = doc.Editor
    Dim db As Database = doc.Database
      Dim peo As New PromptEntityOptions("Select a viewport : ")
    peo.SetRejectMessage("Sorry, Not a viewport")
    peo.AddAllowedClass(GetType(Viewport), True)
    Dim per As PromptEntityResult = ed.GetEntity(peo)
    If per.Status <> PromptStatus.OK Then
        Return
    End If
    Dim vpid As ObjectId = per.ObjectId
      Using tr As Transaction = db.TransactionManager.StartTransaction()
        Dim vp As Viewport = tr.GetObject(vpid, OpenMode.ForWrite)
          Dim resBuf As ResultBuffer
        resBuf = vp.XData()
        If resBuf Is Nothing Then
            ed.WriteMessage("No layers frozen in this viewport")
        Else
            For Each tv As TypedValue In resBuf
                Dim typeCode As Short
                typeCode = tv.TypeCode
                  If typeCode = 1003 Then
                    ed.WriteMessage( _
                                    String.Format("{0}{1}", _
                                    Environment.NewLine, _
                                    tv.Value.ToString))
                End If
            Next
        End If
          tr.Commit()
    End Using
End Sub

## 评论

**内容**: Anonymoose said...
Please remove this sample, or correct it to not use IEnumerator. foreach() is the correct way to iterate over items in an IEnumerable, and ensures that if the IEnumerator implements IDisposable, it's Dispose() method is called.
Reply
07/05/2012 at 03:05 PM

---
**内容**: Balaji said in reply to Anonymoose...
I have made the changes.
Thank you.
Reply
07/05/2012 at 10:05 PM

---
