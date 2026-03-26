---
title: "Quick tip: Get the dwg file path from AcDbDatabase object"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "You might have noticed that on occasion the "acdbHostApplicationServices()->workingDatabase()->getFilename( pFileName )" returns the name of the te..."
author: Autodesk
---
# Quick tip: Get the dwg file path from AcDbDatabase object

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/quick-tip-get-the-dwg-file-path-from-acdbdatabase-object.html

## 文章内容

By Gopinath Taget
You might have noticed that on occasion the "acdbHostApplicationServices()->workingDatabase()->getFilename( pFileName )" returns the name of the temporary save file rather than the name of actual file that is open. This is as designed.
AcDbDatabase::originalFileName() function retrieves the file name under which the drawing is originally opened. In addition, AcApDocument::fileName() function also can retrieve the actual file full path.

## 评论

**内容**: CAD bloke said...
...until AutoCAD does another autosave but you have changed the file name in the meantime, then it gives you the old filename before you changed it. See https://forums.autodesk.com/t5/net/database-filename-return-autosave-filename-sv/td-p/4401703 and https://forums.autodesk.com/t5/net/workingdatabase-vs-mdiactivedocument-database/td-p/2455039
Spoiler: get the Name from the MdiActiveDocument
Reply
03/18/2020 at 04:16 PM

---
