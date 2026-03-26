---
title: "Inserting a block on a layout"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "A Layout object will have a BlockTableRecordId. This is the BlockTableRecord that contains the entities for the layout. You can add the block refer..."
author: Autodesk
---
# Inserting a block on a layout

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/inserting-a-block-on-a-layout.html

## 文章内容

By Virupaksha Aithal
A Layout object will have a BlockTableRecordId. This is the BlockTableRecord that contains the entities for the layout. You can add the block reference to this BlockTableRecord. Below is an example that adds a block named wbtest to the layout named Layout3
<CommandMethod("testBlk")> _
        Public Shared Sub TestBlk()
            Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
            Dim db As Database = _
                        doc.Database
            Dim tr As Transaction = _
                            db.TransactionManager.StartTransaction()
              Dim ed As Editor = doc.Editor
              Using tr
                Try
                    Dim layoutMgr1 As LayoutManager = _
                                            LayoutManager.Current
                    Dim layoutId As ObjectId = _
                                layoutMgr1.GetLayoutId("Layout3")
                    If layoutId.IsNull = True Then
                        tr.Abort()
                        Return
                    End If
                      Dim layoutObj As Layout = _
                                tr.GetObject(layoutId, _
                                            OpenMode.ForWrite, False)
                    Dim layId As ObjectId = _
                        layoutObj.BlockTableRecordId
                    Dim layoutBtr As BlockTableRecord = _
                                    tr.GetObject(layId, _
                                            OpenMode.ForWrite, True)
                      Dim id As ObjectId = Nothing
                    Dim bt As BlockTable = _
                                    tr.GetObject(db.BlockTableId, _
                                        OpenMode.ForRead, True)
                      Dim blkName As String = "wbtest"
                      If bt.Has(blkName) Then
                        id = bt.Item(blkName)
                        Dim insPt As New Point3d(0, 0, 0)
                        Dim bref As BlockReference = _
                                    New BlockReference(insPt, id)
                        layoutBtr.AppendEntity(bref)
                          tr.AddNewlyCreatedDBObject(bref, True)
                        tr.Commit()
                    Else
                        tr.Abort()
                    End If
                  Catch ex As System.Exception
                    ed.WriteMessage(ex.ToString())
                End Try
            End Using
        End Sub

