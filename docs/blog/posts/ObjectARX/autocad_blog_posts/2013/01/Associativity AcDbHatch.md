---
title: "Associativity AcDbHatch"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Database
  - Hatch
description: "After I made a hatch object, added it to the database, set the style, and so on, it is not associative to the object. To make it associative, use t..."
author: Autodesk
---
# Associativity AcDbHatch

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/associativity-acdbhatch.html

## 文章内容

By Augusto Goncalves
After I made a hatch object, added it to the database, set the style, and so on, it is not associative to the object. To make it associative, use the hatch object that was just created as a persistent reactor for the entities to which it is hatching. The following sample demonstrates how to create a hatch and associate it to the boundary entities (a rectangle and a circle).
static void CreateHatch()
{
  AcDbHatch* pHatch = new AcDbHatch();
  // Set hatch plane
  AcGeVector3d normal(0.0, 0.0, 1.0);
  pHatch->setNormal(normal);
  pHatch->setElevation(0.0);
  // Set hatch pattern to ANSI31 predefined type //
  pHatch->setPattern(AcDbHatch::kPreDefined, _T("ANSI31"));
  // Set Associativity
  pHatch->setAssociative(Adesk::kTrue);
  // Construct database AcDbLines
  AcGePoint3d vertexPts[4];
  AcDbObjectId lineId, cirId, hatchId;
  AcDbObjectIdArray dbObjIds;
  AcDbLine *line;
  vertexPts[0].set(2.0, 2.0, 0.0);
  vertexPts[1].set(8.0, 2.0, 0.0);
  vertexPts[2].set(8.0, 8.0, 0.0);
  vertexPts[3].set(2.0, 8.0, 0.0);
  for (int i = 0; i < 4; i++)
  {
    line = new AcDbLine();
    line->setStartPoint(vertexPts[i]);
    line->setEndPoint(vertexPts[(i == 3) ? 0 : i+1]);
    postToDb(line, lineId);
    dbObjIds.append(lineId);
  }
  // Append an external rectangular loop to hatch boundary //
  pHatch->appendLoop(AcDbHatch::kExternal, dbObjIds);
  // Create a AcDbCircle and post it to database //
  AcGePoint3d cenPt(5.0, 5.0, 0.0);
  normal.set(0.0, 0.0, 1.0);
  AcDbCircle *circle = new AcDbCircle();
  circle->setNormal(normal);
  circle->setCenter(cenPt);
  circle->setRadius(1.0);
  postToDb(circle, cirId);
  dbObjIds.setLogicalLength(0);
  dbObjIds.append(cirId);
  // Append an internal loop (circle) to hatch boundary
  pHatch->appendLoop(AcDbHatch::kDefault, dbObjIds);
  // Elaborate hatch lines
  pHatch->evaluateHatch();
  // Get all associative source boundary object Ids for later use.
  dbObjIds.setLogicalLength(0);
  pHatch->getAssocObjIds(dbObjIds);
  // Post hatch entity to database
  postToDb(pHatch, hatchId);
  // Attach hatchId to all source boundary
  // objects for notification.
  AcDbEntity *pEnt;
  int numObjs = dbObjIds.length();
  for (int i = 0; i < numObjs; i++)
  {
    if (acdbOpenAcDbEntity(pEnt, dbObjIds[i],
      AcDb::kForWrite)==Acad::eOk)
    {
      pEnt->addPersistentReactor(hatchId);
      pEnt->close();
    }
  }
}
And here is the commonly used postToDb method:
static Acad::ErrorStatus postToDb(AcDbEntity* ent,
                  AcDbObjectId& objId)
{
  Acad::ErrorStatus es;
  AcDbBlockTable* pBlockTable;
  AcDbBlockTableRecord* pSpaceRecord;
  if (ent==NULL)
    return Acad::eNullObjectPointer;
  if (acdbHostApplicationServices()->workingDatabase()==NULL)
    return Acad::eNoDatabase;
  if ((es = acdbHostApplicationServices()->workingDatabase()->
    getBlockTable(pBlockTable, AcDb::kForRead))!=Acad::eOk)
    return es;
  if ((es =pBlockTable->getAt(ACDB_MODEL_SPACE,
    pSpaceRecord,AcDb::kForWrite)) != Acad::eOk)
  {
    pBlockTable->close();
    return es;
  }
  pBlockTable->close();
  if ((es = pSpaceRecord->appendAcDbEntity(objId, ent))
    != Acad::eOk)
  {
    pSpaceRecord->close();
    return es;
  }
  pSpaceRecord->close();
  return ent->close();
}

## 评论

**内容**: Jorge Renatto said...
Autocad 2013 vba to vb.net migration.
How I can migrate autocad vba to vb.net? Autocad 2013, since the basic migration example shown on this page http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=770215 does not work, your help really appreciate it.
Reply
07/26/2013 at 07:00 AM

---
**内容**: Augusto Goncalves said in reply to Jorge Renatto...
Jorge,
The migration process should work, but note that Visual Basic .NET 2008 must be used. The newer versions, 2010/2012, do not include the migration tool.
What kind of issue are you facing?
Regards,
Augusto Goncalves
Reply
07/26/2013 at 07:05 AM

---
**内容**: Jorge Renatto said...
When running the following code shows me the following error:
1: Imports Autodesk.AutoCAD.Runtime
2: Imports Autodesk.AutoCAD.Interop
3: Imports Autodesk.AutoCAD.Interop.Common
4: Public Class Class1
5: Public ReadOnly Property ThisDrawing() As AcadDocument
6: Get
7: Return Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.activedocument
8: End Get
9: End Property
10: Public Sub COMANDO()
11: Thisdrawing.Utility.Prompt("Hola mundo")
12: End Sub
13: End Class
The error states: 'ActiveDocument' is not a member of' Autodesk.ApplicationServices.Document', in line 7
Reply
07/26/2013 at 07:40 AM

---
**内容**: Augusto Goncalves said in reply to Jorge Renatto...
This is a migration requirement for 2013/2014
Remember to also include reference to AcCoreMgd.dll and replace AcadDocument with GetAcadDocument()
Reply
07/26/2013 at 07:46 AM

---
**内容**: Jorge Renatto said...
Already achieved migrate vba to vb.net your help it was very useful, thank you very much.
Reply
07/27/2013 at 05:16 AM

---
