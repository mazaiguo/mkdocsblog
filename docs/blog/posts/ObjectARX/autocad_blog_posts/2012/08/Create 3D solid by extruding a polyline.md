---
title: "Create 3D solid by extruding a polyline"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Polyline
  - Solid
description: "3D solid entity can be extruded by region object. So we can create a temporary region according to the boundary information of the existing polylin..."
author: Autodesk
---
# Create 3D solid by extruding a polyline

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/create-3d-solid-by-extruding-a-polyline.html

## 文章内容

By Virupaksha Aithal
3D solid entity can be extruded by region object. So we can create a temporary region according to the boundary information of the existing polyline object.Here we explode the polyline to get the boundary curves, and create a temporary region with these boundary curves.
Please see the code snippet below as a reference.
void CreateExtrude()
{
 Acad::ErrorStatus es;
   ads_name polyName;
 ads_point ptres;
   //select the polyline
 if( acedEntSel(L"Please select a polyline", polyName, ptres) != RTNORM)
 {
  acutPrintf(L"Failed to select a polyline");
  return;
 }
   //get the boundary curves of the polyline
 AcDbObjectId idPoly;
 acdbGetObjectId(idPoly, polyName);
     AcDbEntity *pEntity = NULL;
 if(acdbOpenAcDbEntity(pEntity, idPoly, AcDb::kForRead) != Acad::eOk)
 {
     return;
 }
   AcDbPolyline *pPoly = AcDbPolyline::cast(pEntity);
   if(pPoly == NULL)
 {
     pEntity->close();
     return;
 }
   AcDbVoidPtrArray lines;
 pPoly->explode(lines);
 pPoly->close();
   // Create a region from the set of lines.
 AcDbVoidPtrArray regions;
 es  =  AcDbRegion::createFromCurves(lines, regions);
   if(Acad::eOk != es)
 {
     pPoly->close();
     acutPrintf(L"\nFailed to create region\n");
     return;
 }
   AcDbRegion *pRegion = AcDbRegion::cast((AcRxObject*)regions[0]);
   // Extrude the region to create a solid.
 AcDb3dSolid *pSolid = new AcDb3dSolid();
   es  =  pSolid->extrude(pRegion, 10.0, 0.0);
   for (int i = 0; i < lines.length(); i++)
 {
  delete (AcRxObject*)lines[i];
 }
   for (int ii = 0; ii < regions.length(); ii++)
 {
  delete (AcRxObject*)regions[ii];
 }
   AcDbObjectId savedExtrusionId = AcDbObjectId::kNull;
   if(Acad::eOk == es)
 {
    AcDbDatabase *pDb = curDoc()->database();
    AcDbObjectId modelId;
    modelId = acdbSymUtil()->blockModelSpaceId(pDb);
      AcDbBlockTableRecord *pBlockTableRecord;
    acdbOpenAcDbObject((AcDbObject*&)pBlockTableRecord,
                                    modelId, AcDb::kForWrite);
      pBlockTableRecord->appendAcDbEntity(pSolid);
    pBlockTableRecord->close();
    pSolid->close();
 }
 else
 {
     delete pSolid;
 }
  }

## 评论

**内容**: Oleg said...
Hi, Virupaksha,
Thanks for your example
I have tried to convert it on C#,
seems is working on my machine:
[CommandMethod("extt")]
public void CreateExtrude()
{
Autodesk.AutoCAD.ApplicationServices.Application.SetSystemVariable("delobj", 1);
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
PromptSelectionOptions pso = new PromptSelectionOptions();
pso.SingleOnly = true;
pso.SinglePickInSpace = true;
pso.MessageForAdding = "\nPlease select a polyline: ";
pso.MessageForRemoval = "Failed to select a polyline";
pso.PrepareOptionalDetails = true;
SelectionFilter filter =
new SelectionFilter(
new TypedValue[] { new TypedValue(0, "lwpolyline"),new TypedValue(70, 1) });
//select the polyline
PromptSelectionResult sres = ed.GetSelection(pso,filter);
if (sres.Status != PromptStatus.OK) return;
using (Transaction tr = doc.TransactionManager.StartTransaction())
{
//get the boundary curves of the polyline
ObjectId idPoly = sres.Value[0].ObjectId;
Entity pEntity = tr.GetObject(idPoly, OpenMode.ForRead) as Entity;
Polyline pPoly = pEntity as Polyline; ;
if (pPoly == null) return;
DBObjectCollection lines = new DBObjectCollection();
pPoly.Explode(lines);
// Create a region from the set of lines.
DBObjectCollection regions = new DBObjectCollection();
regions = Region.CreateFromCurves(lines);
if (regions.Count == 0)
{
ed.WriteMessage("\nFailed to create region\n");
return;
}
Region pRegion = (Region)regions[0];
// Extrude the region to create a solid.
Solid3d pSolid = new Solid3d();
pSolid.RecordHistory = true;
pSolid.Extrude(pRegion, 10.0, 0.0);

ObjectId savedExtrusionId = ObjectId.Null;
ObjectId modelId;
modelId = SymbolUtilityServices.GetBlockModelSpaceId(db);
BlockTableRecord btr = tr.GetObject(modelId, OpenMode.ForWrite) as BlockTableRecord;
savedExtrusionId = btr.AppendEntity(pSolid);
tr.AddNewlyCreatedDBObject(pSolid,true);

if (!pPoly.IsWriteEnabled) pPoly.UpgradeOpen();
pPoly.Erase();

tr.Commit();
}
}
Regards,
Oleg
Reply
08/08/2012 at 01:48 PM

---
