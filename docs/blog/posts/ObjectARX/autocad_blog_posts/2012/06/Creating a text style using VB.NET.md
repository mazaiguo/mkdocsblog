---
title: "Creating a text style using VB.NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Unicode
description: "Below code shows the procedure to add a new text style to database. Also, the code makes the newly added text style as active/current text style by..."
author: Autodesk
---
# Creating a text style using VB.NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/creating-a-text-style-using-vbnet.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to add a new text style to database. Also, the code makes the newly added text style as active/current text style by setting the database property “Database.Textstyle”
       <CommandMethod("TestFont")> _
      Public Shared Sub TestFont()
              Dim doc As Document = _
                       Application.DocumentManager.MdiActiveDocument
            Dim db As Database = _
                        doc.Database
            Dim tm As Transaction = _
                            db.TransactionManager.StartTransaction()
              Dim ed As Editor = doc.Editor
              Using tm
                Dim st As TextStyleTable = CType(tm.GetObject( _
                                db.TextStyleTableId, _
                                OpenMode.ForWrite, False),  _
                                                 TextStyleTable)
                Dim str As TextStyleTableRecord = _
                                        New TextStyleTableRecord()
                str.Name = "MyStyle"
                st.Add(str)
                  'Following are properties to set by default,
                'you can also modify them
                  'str.FileName = "txt.shx"
                'str.PriorSize = 0.2               
                'str.ObliquingAngle = 0.0
                'str.XScale = 1.0
                'str.TextSize = 0.0
                'str.IsVertical = False
                'str.IsShapeFile = False
                  'using the font descriptor to set the new font style
                'Imports Autodesk.AutoCAD.GraphicsInterface
                str.Font = New FontDescriptor("Times New Roman", _
                                        True, True, Nothing, Nothing)
                tm.AddNewlyCreatedDBObject(str, True)
                  'make as current
                db.Textstyle = str.ObjectId
                tm.Commit()
            End Using
          End Sub

## 评论

**内容**: Steve Hill said...
Thanks for posting this. I have a couple of questions.
1. Where do you set the Upside down and backwords values? These are shown on the dialog but not in vb.net from what I can see.
2. Using the FontDescriptor, it asks for a string, you have entered "Times New Roman". I have a variable dimed as a string called 'FontName' that I want to place here. Each time I try, I get an error saying invalid input. But it works if I put it in the FileName setting. This happens even on True type fonts. And if I want to set a true type font and it's styles how would I with this method?
Thanks.
Reply
06/27/2012 at 06:42 AM

---
**内容**: Pos Indonesia said...
Thank you for share text style code.. it works for my project.
Reply
04/22/2018 at 04:03 AM

---
