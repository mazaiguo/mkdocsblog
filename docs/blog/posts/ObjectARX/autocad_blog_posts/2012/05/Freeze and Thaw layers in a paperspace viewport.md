---
title: "Freeze and Thaw layers in a paperspace viewport"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Layer
description: "This VB.NET example shows how to freeze or thaw a layer in a layout viewport using the FreezeLayersInViewport() and ThawLayersInViewport() methods...."
author: Autodesk
---
# Freeze and Thaw layers in a paperspace viewport

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/freeze-and-thaw-layers-in-a-paperspace-viewport.html

## 文章内容

This VB.NET example shows how to freeze or thaw a layer in a layout viewport using the FreezeLayersInViewport() and ThawLayersInViewport() methods. These methods take an ObjectIdCollection which is a collection of ObjectId for the layers to freeze or thaw.
By Wayne Brill
<CommandMethod("VPFreezeandThaw")> _
Public Sub VPFreezeandThaw()
      Dim doc As Document = _
        Application.DocumentManager.MdiActiveDocument
    Dim ed As Editor = doc.Editor
    Dim db As Database = doc.Database
    Dim idLay As ObjectId
    Dim idLayTblRcd As ObjectId
    Dim lt As LayerTable
      Dim tm As Autodesk.AutoCAD.ApplicationServices. _
           TransactionManager = db.TransactionManager
    Dim ta As Transaction = tm.StartTransaction()
      Try
          idLay = db.LayerTableId
        lt = ta.GetObject(idLay, OpenMode.ForRead)
          If lt.Has("wbtest") Then
            idLayTblRcd = lt.Item("wbtest")
        Else
            ed.WriteMessage _
           ("Layer - wbtest not available")
            Return
        End If
          Dim idCol As ObjectIdCollection = _
                         New ObjectIdCollection
          idCol.Add(idLayTblRcd)
          ' Check that we are in paper space
        Dim vpid As ObjectId = _
                        ed.CurrentViewportObjectId
        If vpid.IsNull() Then
            ed.WriteMessage("No Viewport current.")
            Return
        End If
          'VP need to be open for write
        Dim oViewport As Viewport = _
            tm.GetObject(vpid, OpenMode.ForWrite)
          If Not oViewport.IsLayerFrozenInViewport _
                        (idLayTblRcd) Then
            oViewport.FreezeLayersInViewport _
                            (idCol.GetEnumerator())
        Else
            oViewport.ThawLayersInViewport _
                            (idCol.GetEnumerator())
        End If
        ta.Commit()
    Finally
        ta.Dispose()
    End Try
End Sub

## 评论

**内容**: Larry Daubenspeck said...
Working with the AutoCad 2017 API...what happened to these viewport methods (IsLayerFrozenInViewport, FreezeLayersInViewport, ThawLayersInViewport)? They're not there. Were they replaced?
Reply
04/24/2017 at 07:58 AM

---
**内容**: Brad said...
What if
I have more than 1 Tab? I want to freeze layers in tab1 but a different set of layers in tab2.
This routine is unpredictable as to which layer is frozen/thawed in what layout
Reply
05/10/2018 at 09:11 AM

---
**内容**: Brad said...
Hi Wayne
After some debugging. It seams to ignor the first layer in my selectionset even though upon debug, I watch the function oViewport.ThawLayersInViewport(idCol.GetEnumerator()) and it is operational so, I included layer "0" and it is subsequentially the first layer in the Selectionset, therefor it is the one that gets ignored but I don't care in this case.
Reply
05/10/2018 at 01:20 PM

---
**内容**: Mr Toby Wilson said...
The above code has been very useful in helping me to develop code to freeze layers in all viewports in all layouts except for one chosen viewport. However this is for paperspace of the viewport. I would like to do the same for modelspace for each viewport (reason is I don't want to see some model space entities in some viewports). I have the following code which works for the first layout then doesn't freeze any other viewport model space layers. lcoll is a collection of layouts created before the code, targetviewport is the viewport I don't want layers frozen on, layerEnumerator is for the layers I want frozen.

        For Each l In lcoll
            LayoutManager.Current.CurrentLayout = l.LayoutName
            Dim viewportIds As ObjectIdCollection = l.GetViewports()
            For Each vpId As ObjectId In viewportIds
                Using acTrans As Transaction = db.TransactionManager.StartTransaction()
                    Dim viewport As Viewport = CType(acTrans.GetObject(vpId, OpenMode.ForWrite), Viewport)
                    If viewport.Number <> 1 Then 'ignore the first viewport (look only at floating ones)
                        If viewport <> targetviewport Then
                            viewport.On = True
                            doc.Editor.SwitchToModelSpace() ' need to be in modelspace to freeze model space viewport layer
                            viewport.FreezeLayersInViewport(layerEnumerator)
                            doc.Editor.SwitchToPaperSpace()
                        End If
                    End If
                        acTrans.Commit()
                End Using
            Next
        Next

Any assistance that can be given will be gratefully received.
Reply
04/01/2022 at 08:41 AM

---
