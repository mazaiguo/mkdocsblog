---
title: "Using Plant3d Project.xml file to obtain data"
date: 2012-09-01
categories:
  - Plant 3D
tags:
  - API
  - AutoCAD
  - Block
  - Plant 3D
description: "If you are new to Plant3d, it’s tempting to quickly obtain project data directly from the Project.xml file."
author: Autodesk
---
# Using Plant3d Project.xml file to obtain data

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/using-plant3d-projectxml-file-to-obtain-data.html

## 文章内容

by Fenton Webb
If you are new to Plant3d, it’s tempting to quickly obtain project data directly from the Project.xml file.
The Project.xml file is an internal project file that should not really be used to extract Plant data. You should always use the API's because the XML file format can change from release to release.
Take, for instance, obtaining the list of P&ID drawings in AutoCAD P&ID. In 2011, you could
1) Read the Project.xml…
<ProjectPart name="PnId" fileName="C:\Fenton\Projects\PnID\Test ISO\PnIdPart.xml" relativeFileName="PnIdPart.xml" uncFileName="\\Fenton\Projects\PnID\Test ISO\PnIdPart.xml" />
2) Then Use the "relativeFileName" value to locate the "PnIdPart.xml" file.
3) Open the "PnIdPart.xml" file and search for the XML block named "<PnpDrawingFiles>"
4) Finally, inside the "<PnpDrawingFiles>" block, all the project drawing files are listed.
However, in P&ID 2013 these elements don’t exist anymore. This is because we had issues with multi-user support, so we moved the file list into the DCF.
The correct way to obtain a list of P&ID DWG files is to use the API
Autodesk.ProcessPower.ProjectManager.Project.GetPnPDrawingFiles()

## 评论

**内容**: Khoa Ho said...
This is my comments:
DCF is SQLite database. If we open ProcessPower.dcf file, the table stores all those drawings is PnPDrawings, and the view is PnPDrawings_PNP.
Since AutoCAD P&ID 2009, it already had table PnPDrawings, but it stores dummy data. The project drawing files are on PnIDPart.xml. But from P&ID 2013, this table has actual real drawing references, and strips all those project drawing files out of PnIDPart.xml. The benefit of database over XML is for multi-user connections.
The API will call SQLite library to query data, so if we can use SQLite instead of AutoCAD P&ID API, it would be really more powerful.
Reply
09/25/2012 at 07:51 PM

---
**内容**: Jorge Lopez said...
Product can be configured to use SQL Server also. Using the APIs allow your customization to be database and schema agnostic.
Reply
10/31/2012 at 11:07 AM

---
**内容**: Khoa Ho said...
That is correct, the API will sync between drawing schema and database. But by learning what behind P&ID project, the actual mapping between database (SQLite or SQL server) and Project/Data Manager in Plant3d is helpful to understand how it works. Working directly with database instead of API is better for SQL Reporting Services.
Reply
11/09/2012 at 12:17 PM

---
