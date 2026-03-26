---
title: "Creating cylinder (Solid3d object) using .NET API."
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Solid
description: "To insert a cylindrical solid object into the AutoCAD database, you can use a Solid3d database object. To define a cylinder, you use the Solid3d.Cr..."
author: Autodesk
---
# Creating cylinder (Solid3d object) using .NET API.

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-cylinder-solid3d-object-using-net-api.html

## 文章内容

By Virupaksha Aithal
 To insert a cylindrical solid object into the AutoCAD database, you can use a Solid3d database object. To define a cylinder, you use the Solid3d.CreateFrustum() method. Remember to call RecordHistory to record solid history.
<CommandMethod("CreateCylinder")> _
       Public Shared Sub CreateCylinder()
            Dim radius As Double = 1.2345
            Dim height As Double = 2.3456
              Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
            Dim db As Database = _
                        doc.Database
            Dim tm As Transaction = _
                            db.TransactionManager.StartTransaction()
            Using tm
                Dim solid As New Solid3d()
                solid.RecordHistory = True
                solid.CreateFrustum(height, radius, radius, radius)
                  Dim bt As BlockTable = _
                    tm.GetObject(db.BlockTableId, OpenMode.ForRead)
                Dim btr As BlockTableRecord = _
                    tm.GetObject(bt(BlockTableRecord.ModelSpace), _
                                        OpenMode.ForWrite)
                btr.AppendEntity(solid)
                tm.AddNewlyCreatedDBObject(solid, True)
                tm.Commit()
            End Using
        End Sub

## 评论

**内容**: Tilo said...
One remark: If you like to insert cylinders with a certain start point and direction you would need to
a) define an appropriate UCS before creating the cylinder or
b) transform the entity to reflect these parameters after creating the cylinder
Reply
05/04/2012 at 04:48 AM

---
**内容**: Virupaksha aithal said...
Thanks for the comments. I will update the post with your remarks
Reply
05/04/2012 at 05:37 AM

---
