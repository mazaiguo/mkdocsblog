---
title: "Access raster image variables using the .NET API"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
  - Plot
description: "The variables for raster images are stored in the Named Object Dictionary (NOD) in the database with the key name "ACADIMAGEVARS". Using the .NET A..."
author: Autodesk
---
# Access raster image variables using the .NET API

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/access-raster-image-variables-using-the-net-api.html

## 文章内容

By Augusto Goncalves
The variables for raster images are stored in the Named Object Dictionary (NOD) in the database with the key name "ACAD_IMAGE_VARS". Using the .NET API, you can open this entry in the NOD as RasterVariables object.
Here is a VB.NET example that sets the IMAGEFRAME variable to zero (Image frames are not displayed and not plotted).
<CommandMethod("ImageFrameOff")> _
Public Sub CmdImageFrameOff()
  Dim db As Database = Application.DocumentManager.
    MdiActiveDocument.Database
  Using trans As Transaction=db.TransactionManager.StartTransaction()
    Try
      Dim theNOD As DBDictionary = trans.GetObject(
        db.NamedObjectsDictionaryId, OpenMode.ForRead)
      Dim rasterVars As RasterVariables
      'get variables dictionary
      Dim kImageVars As String = "ACAD_IMAGE_VARS"
      If theNOD.Contains(kImageVars) Then
        Dim rastVarsId As ObjectId = theNOD.GetAt(kImageVars)
        rasterVars = trans.GetObject(rastVarsId, OpenMode.ForWrite)
      Else
        ' or create it
        rasterVars = New RasterVariables()
        theNOD.UpgradeOpen()
        theNOD.SetAt(kImageVars, rasterVars)
        trans.AddNewlyCreatedDBObject(rasterVars, True)
      End If
        rasterVars.ImageFrame = FrameSetting.ImageFrameOff
      trans.Commit()
    Catch 
    End Try
  End Using
End Sub

