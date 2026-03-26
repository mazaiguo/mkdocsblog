---
title: "How to insert a RasterImage using the .NET API?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "To insert a RasterImage we also need to create a image definition for it, as the image we can see at the drawing is just a reference to this defini..."
author: Autodesk
---
# How to insert a RasterImage using the .NET API?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-insert-a-rasterimage-using-the-net-api.html

## 文章内容

By Augusto Goncalves
To insert a RasterImage we also need to create a image definition for it, as the image we can see at the drawing is just a reference to this definition. This sample code demonstrate how open an existing definition (e.g. MY_IMAGE_NAME), if exists, or create if it doesn’t, and finally place a reference.
<CommandMethod("customRasterImage")> _
Public Sub CmdInsertImage()
  ' Image dictionary name constant
  Dim dictName As String = "MY_IMAGE_NAME"
  Dim imageDef As RasterImageDef
  Dim imageDefId As ObjectId
    Dim db As Database =
    Application.DocumentManager.MdiActiveDocument.Database
  Dim ed As Editor =
    Application.DocumentManager.MdiActiveDocument.Editor
  Using trans As Transaction = db.TransactionManager.StartTransaction
    Try
      Dim imageDictId As ObjectId =
        RasterImageDef.GetImageDictionary(db)
        If imageDictId.IsNull Then
        ' Image dictionary doesn't exist, create new
        imageDictId = RasterImageDef.CreateImageDictionary(db)
      End If
        ' Open the image dictionary
      Dim imageDict As DBDictionary = trans.GetObject( _
        imageDictId, OpenMode.ForRead)
        ' See if our raster def in the image dict exists,
      ' if not, create new
      If imageDict.Contains(dictName) Then
        ' Get the raster image def
        imageDefId = imageDict.GetAt(dictName)
        imageDef = trans.GetObject(imageDefId, OpenMode.ForWrite)
      Else
        ' Create a raster image definition
        ' Get the file name of the image
        Dim fileDia As New Autodesk.AutoCAD.Windows.OpenFileDialog(
          "Open an Image file", Nothing,
          "jpg; gif; tif; bmp", "Image File",
          Autodesk.AutoCAD.Windows.
                OpenFileDialog.OpenFileDialogFlags.NoUrls)
          ' Show the dialog and test the result
        Dim res As System.Windows.Forms.DialogResult =
          fileDia.ShowDialog()
        If res <> System.Windows.Forms.DialogResult.OK Then Return
          ' Create a new image definition
        imageDef = New RasterImageDef()
        ' And set its source image
        imageDef.SourceFileName = fileDia.Filename()
        ' finally load it
        imageDef.Load()
        imageDict.UpgradeOpen()
        imageDefId = imageDict.SetAt(dictName, imageDef)
        trans.AddNewlyCreatedDBObject(imageDef, True)
      End If
        ' Now create the raster image that references the definition
      Dim image As New RasterImage()
      image.ImageDefId = imageDefId
        ' Prepare the orientation
      Dim uCorner As New Vector3d(1.5, 0, 0)
      Dim vOnPlane As New Vector3d(0, 1, 0)
      Dim coordinateSystem As New CoordinateSystem3d( _
        Point3d.Origin, uCorner, vOnPlane)
      image.Orientation = coordinateSystem
        ' And some other properties
      image.ImageTransparency = True
      image.ShowImage = True
        ' Add the image to ModelSpace
      Dim bt As BlockTable = trans.GetObject( _
        db.BlockTableId, OpenMode.ForRead)
      Dim msBtr As BlockTableRecord = trans.GetObject( _
        bt(BlockTableRecord.ModelSpace), _
        OpenMode.ForWrite)
      msBtr.AppendEntity(image)
      trans.AddNewlyCreatedDBObject(image, True)
        ' Create a reactor between the RasterImage
      ' and the RasterImageDef to avoid the "Unreferenced"
      ' warning the XRef palette
      RasterImage.EnableReactors(True)
      image.AssociateRasterDef(imageDef)
        trans.Commit()
    Catch
    End Try
  End Using
End Sub

## 评论

**内容**: Greg said...
Thanks, that last bit of code solved my Unreferenced problem. Not having that code also prevents Unload/Reload, FYI.
Reply
08/22/2017 at 01:48 PM

---
**内容**: Ben said...
Hi Augusto
do you know how to insert an image without it being an XRef?
i.e. the image should be located in the AutoCAD drawing itself.
any advice much appreciated.
rgds

Ben
Reply
09/09/2018 at 10:51 PM

---
**内容**: Augusto Goncalves said in reply to Ben...
Ben,
I believe the other way would be to PASTE SPECIAL, which creates an OLE object. I'm afraid this is not exposed as an API, you may be able to use P/Invoke as shown here http://adndevblog.typepad.com/autocad/2012/04/update-linked-ole-object-from-net.html
Regards,
Augusto Goncalves
Reply
09/12/2018 at 06:37 AM

---
**内容**: Jeremy said...
Greetings Augusto,
When I use the 'MapIInsert' command to bring in a MrSid image, it gets the insertion point from the image file. I am having trouble getting the insertion point using the .Net API. I was able to set the correct width and height of the image (1/(ResolutionMMPerPixel.X * Size.LengthSquared / 10000)) * Size.X. Any help with the insertion point would be greatly appreciated.
Thanks,
Jeremy
Reply
02/20/2024 at 07:44 PM

---
