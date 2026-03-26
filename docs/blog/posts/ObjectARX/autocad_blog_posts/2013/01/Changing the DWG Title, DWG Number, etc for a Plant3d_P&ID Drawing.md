---
title: "Changing the DWG Title, DWG Number, etc for a Plant3d/P&ID Drawing"
date: 2013-01-01
categories:
  - Plant 3D
tags:
  - API
  - DWG
  - Plant 3D
  - Plugin
description: "I had a question come up about how to set the DWG Title, DWG Number, etc when adding new files to the project via the API."
author: Autodesk
---
# Changing the DWG Title, DWG Number, etc for a Plant3d/P&ID Drawing

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/changing-the-dwg-title-dwg-number-etc-for-a-plant3dpid-drawing.html

## 文章内容

By Fenton Webb
I had a question come up about how to set the DWG Title, DWG Number, etc when adding new files to the project via the API.
You can add the files using:
Autodesk.ProcessPower.ProjectManager.Project.AddPnPDrawingFile()
once added, you can utilize these functions to do what you want with the properties…
Autodesk.ProcessPower.ProjectManager.Project.GetDrawingPropertyValue()Autodesk.ProcessPower.ProjectManager.Project.SetDrawingPropertyValue()
Autodesk.ProcessPower.ProjectManager.Project.GetDrawingProperties()
Autodesk.ProcessPower.ProjectManager.Project.SetDrawingProperties()
then call this function to commit the changes…
Autodesk.ProcessPower.ProjectManager.Project.AcceptDrawingProperties()

## 评论

**内容**: dennis said...
For Plant 2015 VB.NET, could you provide an example of reading and writing using the GetDrawingProperties, SetDrawingProperties and AcceptDrawingProperties. For example, changing the DWG Number.
Reply
07/25/2014 at 08:19 AM

---
**内容**: Alan Shanley said...
Hi - I'm looking for some direction on how to use C# to edit the fields added to custom category under Drawing Properties. I would like to edit the fields in the active drawing but also run it as a batch process.
Thanks
Reply
06/06/2018 at 06:49 PM

---
