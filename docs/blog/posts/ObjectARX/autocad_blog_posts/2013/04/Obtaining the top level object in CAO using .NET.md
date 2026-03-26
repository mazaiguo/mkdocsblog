---
title: "Obtaining the top level object in CAO using .NET"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - AutoLISP
  - COM
description: "The other blog post introduces how to access CAD by VBA or LISP."
author: Autodesk
---
# Obtaining the top level object in CAO using .NET

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/obtaining-the-top-level-object-in-cao-using-net.html

## 文章内容

By Xiaodong Liang
The other blog post introduces how to access CAD by VBA or LISP.
http://adndevblog.typepad.com/autocad/2012/12/creating-link-templates-using-activex-api-in-vba-and-lisp.html
The following .NET code is converted from the VBA demo directly. Firstly, you need to add the library of CAO by adding
C:\Program Files\Common Files\Autodesk Shared\cao16***.tlb.
where *** is the language. e.g. cao16deu.tlb is for English version.
     Sub fCreateLinkTemplate()
          ' assume AutoCAD 2013 is running
        Const progID As String = "AutoCAD.Application"
        Dim acType As Type = Type.GetTypeFromProgID(progID)
        Dim AcadApp As AcadApplication = Nothing
        AcadApp = Marshal.GetActiveObject(progID)
          'get active document
        Dim ThisDrawing As AcadDocument
        ThisDrawing = AcadApp.ActiveDocument
          Try
            'get the DBCONNECT object
            Dim pDB As CAO.DbConnect =
                ThisDrawing.Application.
                    GetInterfaceObject
                        ("CAO.DBConnect.16")
            ' get LinkTemplates
            Dim pLTs As CAO.LinkTemplates =
                pDB.GetLinkTemplates(ThisDrawing)
                Dim pKeyDescs As CAO.KeyDescriptions 
            'prepare the keydescriptions
            pKeyDescs =
                ThisDrawing.Application.
              GetInterfaceObject 
                 ("CAO.KeyDescriptions.16")
            pKeyDescs.Add("TAG_NUMBER",
                 CAO.CaoDataType.kCaoTypeInteger)
            pKeyDescs.Add("Manufacturer",
                  CAO.CaoDataType.kCaoTypeText)
                Dim psDataSrc As String = "jet_dbsamples"
            Dim psLinkTempName1 As String =  
                           "LTCreatedByVBNetCAO"
            Dim psLinkTempName2 As String =  
                            "LTtobeDeleted"
                'create two Link Templates
            Dim pLT1 As CAO.LinkTemplate = pLTs.Add(
                                            psDataSrc,
                                           "Catalog1",
                                            "Schema1",
                                           "Computer",
                                           psLinkTempName1,
                                            pKeyDescs)
              Dim pLT2 As CAO.LinkTemplate = pLTs.Add(
                                            psDataSrc,
                                            Catalog2",
                                            "Schema2",
                                            Computer",
                                      psLinkTempName2,
                                            pKeyDescs)
                'created Link Templates
            MsgBox("Created Link Templates : " &  _
                        Chr(13) & "1) " &
              pLTs.Item(psLinkTempName1).Name _
            & Chr(13) & "2) " & pLTs.Item
                      (psLinkTempName2).Name)
              'connect to the datasource
            pDB.Connect(psDataSrc)
            'delete the second linktemplate.
            'Comment the following statement if
            'you want to see both the link templates
            pLTs.Delete(psLinkTempName2)
        Catch ex As Exception
            MsgBox(ex.ToString())
        End Try
    End Sub

## 评论

**内容**: Hanauer said...
Sorry for my bad English.
A basic introduction. Wait a more useful example, perhaps the example "caotest.dvb" converted to C #. NET and logical with enhancements.Example that should be tested and working properly.
It seems to me that the library "CAO" was forgotten. It's hard to find any example in fruitful .NET.
Anyway thank you.
Reply
04/01/2013 at 05:42 PM

---
