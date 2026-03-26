---
title: "Embedding an image in a drawing"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How do I embed an image in my drawing file so that it I don't have to include a"
author: Autodesk
---
# Embedding an image in a drawing

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/embedding-an-image-in-a-drawing.html

## 文章内容

By Philippe Leefsma
Q:
How do I embed an image in my drawing file so that it I don't have to include a
separate image file with the drawing?
A:
This can be done in two ways. The method you choose depends on your
requirements.
* As an OLE Insert -
You can insert an image using Insert -> OLE Object to create an AcDbOle2Frame
that has its image data embedded in the drawing. A disadvantage to this approach
is that you cannot create an AcDbOle2Frame programmatically - user interaction
is required to create it.
* Using a custom object - (two options)
An AcDbRasterImageDef/AcDbRasterImage pair can be created and inserted
programatically, but the AcDbRasterImageDef requires an external file to store
its image data. To avoid this, you can either:
1. derive your own custom object from AcDbRasterImageDef, or
2. store your image data in a separate custom object that creates a temporary
file when it is opened, and sets this file to be the image file used by its
associated AcDbRasterImageDef.
The attached sample project demonstrate the second approach. It takes the original image file
and stores it in a custom object, AsdkBindObject.
When AsdkBindImage is opened, it creates a temporary file that is a copy of the original image file
and calls the setActiveFileName() function of the AcDbRasterImageDef, so that
this temporary file is used by the AcDbRasterImageDef, rather than the one
specified by setSourceFileName.
arxbindimage.zip

