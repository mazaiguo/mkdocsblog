---
title: "Setting the UCS to WCS"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
description: "Below code shows the procedure to set the UCS TO WCS."
author: Autodesk
---
# Setting the UCS to WCS

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/setting-the-ucs-to-wcs.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to set the UCS TO WCS.
        <CommandMethod("restoreWCS")> _
        Public Sub restoreWCS()
            Dim doc As Document = _
                       Application.DocumentManager.MdiActiveDocument
              Dim ed As Editor = doc.Editor
              ed.CurrentUserCoordinateSystem = Matrix3d.Identity
            ed.Regen()
        End Sub

