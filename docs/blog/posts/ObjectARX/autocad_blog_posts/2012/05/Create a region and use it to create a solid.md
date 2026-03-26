---
title: "Create a region and use it to create a solid"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Polyline
  - Solid
description: "How can I use points to use as vertices for creating a solid extrusion? After the solid is created, how can I manipulate it?"
author: Autodesk
---
# Create a region and use it to create a solid

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/create-a-region-and-use-it-to-create-a-solid.html

## 文章内容

By Xiaodong Liang
Issue
How can I use points to use as vertices for creating a solid extrusion? After the solid is created, how can I manipulate it?
Solution
To create a solid extrusion you have to provide a region as input. You can then use points to create a polyline for creating a region. After the region is created, use it to create the solid extrusion. After the solid is created, manipulate it as you would any other AcDbEntity. The sample below uses a set of points to create a polyline that creates a region. A solid extrusion is then created from the region. Lastly, it demonstrates how to manipulate the solid by moving it. 
// main function
 void createSolid()
{
    // Assign the set of points that will define the vertices
    // of the region used to create the solid extrusion.  The
    // points are defined and loaded in an AcGePoint3dArray.
    // The first and last point are the same so a close
    // region will be created.
    AcGePoint3dArray pointArray;
    AcGePoint3d VertexPoint(0.0, 0.0, 0.0);
    pointArray.append(VertexPoint);
      VertexPoint.set(4.0, 0.0, 0.0);
    pointArray.append(VertexPoint);
      VertexPoint.set(4.0, 3.0, 0.0);
    pointArray.append(VertexPoint);
      VertexPoint.set(2.0, 2.0, 0.0);
    pointArray.append(VertexPoint);
      VertexPoint.set(0.0, 3.0, 0.0);
    pointArray.append(VertexPoint);
      VertexPoint.set(0.0, 0.0, 0.0);
    pointArray.append(VertexPoint);
      // Create a region using the point array.
    AcDbObjectId RegionId;
    RegionId = CreateRegionFromPoints(pointArray);
      // Create a solid extrusion using the region. 
    // The depth of the
    // protrusion will be 2 units with a taper of 5 degrees.
    AcDbObjectId SolidId;
    SolidId = CreateSolidExtrusion(RegionId, 2.0,
                     3.14159256359/36.0);
      // Demonstrate manipulating the solid by moving it.
    MoveObject(SolidId, AcGeVector3d(5.0, 0.0, 0.0));
}
  // Given an AcDbObjectId, move the object.
 void MoveObject(AcDbObjectId ObjectId,
                AcGeVector3d MoveVector)
{
    // Open the object for write.
    AcDbEntity* pEnt;
    acdbOpenObject(pEnt, ObjectId, AcDb::kForWrite);
      AcGeMatrix3d transMatrix;
    transMatrix = transMatrix.setTranslation(MoveVector);
    pEnt->transformBy(transMatrix);
     // Force the entity to draw.
    pEnt->draw();
      // Close the object.
    pEnt->close();  
      // Force the update of the display.
    acedUpdateDisplay();
}
    // Given a region create a solid extrusion.
 AcDbObjectId CreateSolidExtrusion(
     AcDbObjectId RegionId,
     double Height,
     double Taper)
{
    AcDbObjectId solidId;
      // Get the AcDbEntity for the input region.
    AcDbEntity* pRegion;
    acdbOpenAcDbEntity(pRegion, RegionId, AcDb::kForRead);
      // Create a solid using the region.
    AcDb3dSolid* solid = new AcDb3dSolid;
    assert(solid != NULL);
    solid->extrude(static_cast<AcDbRegion*>(pRegion),
                Height, Taper);
    pRegion->close();
      // Add the solid to the database
    AcDbBlockTable* pBlockTable;
    acdbHostApplicationServices()->workingDatabase()->
        getBlockTable(pBlockTable, AcDb::kForRead);
    AcDbBlockTableRecord* pBlockTableRecord;
      // get model space
    pBlockTable->getAt(ACDB_MODEL_SPACE,
        pBlockTableRecord,
        AcDb::kForWrite);
    pBlockTable->close();
      pBlockTableRecord->appendAcDbEntity(solidId, solid);
      pBlockTableRecord->close();
    solid->close();
      // Return the ID of the solid.
    return solidId;
}
  // Given an AcGePoint3dArray, create a region that
// uses these points at the vertices of the region.
AcDbObjectId CreateRegionFromPoints(
        AcGePoint3dArray InPoints)
{
    // Create the the polyline.
    AcDbObjectId polylineID = NULL;
    polylineID = createPolyline(InPoints);
      // Get the AcDbEntity for the polyline.
    AcDbEntity* pPolyline;
    AcDbObjectId regionId;
    acdbOpenAcDbEntity(pPolyline,
        polylineID, AcDb::kForRead);
      // Create a region using the polyline.
    AcDbVoidPtrArray polylineArray;
    polylineArray.append(static_cast<void*>(pPolyline));
    AcDbVoidPtrArray regions;
    AcDbRegion::createFromCurves(polylineArray, regions);
    AcDbRegion *pRegion = NULL;
    pRegion = AcDbRegion::cast((AcRxObject*)regions[0]);
      pPolyline->close();
      // Add the region to the database.
    AcDbBlockTable* pBlockTable;
    acdbHostApplicationServices()->workingDatabase()->
        getBlockTable(pBlockTable, AcDb::kForRead);
      // get model space
    AcDbBlockTableRecord* pBlockTableRecord;
    pBlockTable->getAt(ACDB_MODEL_SPACE,
        pBlockTableRecord,
        AcDb::kForWrite);
    pBlockTable->close();
      AcDbRegion* regionObj =
        static_cast<AcDbRegion*>(regions[0]);
    pBlockTableRecord->appendAcDbEntity(
                regionId,
                regionObj);
      pBlockTableRecord->close();
    regionObj->close();
      // Return the ID of the region.
    return regionId;
}
  // Given an AcGePoint3dArray, create a polyline that
// uses these points at the vertices of the region.
 AcDbObjectId createPolyline(AcGePoint3dArray Vertices)
{
    // Create the polyline.
    AcDb3dPolyline* pPolyline =
        new AcDb3dPolyline(AcDb::k3dSimplePoly,
                        Vertices);
      // Add the polyline to the databse.
    AcDbBlockTable* pBlockTable;
    acdbHostApplicationServices()->workingDatabase()->
        getBlockTable(pBlockTable,
                AcDb::kForRead);
      AcDbBlockTableRecord* pBlockTableRecord;
    pBlockTable->getAt(ACDB_MODEL_SPACE,
        pBlockTableRecord,
        AcDb::kForWrite);
    pBlockTable->close();
      AcDbObjectId polylineId;
    pBlockTableRecord->appendAcDbEntity(
        polylineId, pPolyline);
      pBlockTableRecord->close();
    pPolyline->close();
      // Return the ID of the polyline.
    return polylineId;
}

## 评论

**内容**: Account Deleted said...
Hi, Xiaodong!
Are you sure that it is permissible to call first pEnt->close(); and then pEnt->draw(); ???
As far as I know no manipulations with closed entity are not allowed.
Reply
05/30/2012 at 10:08 PM

---
**内容**: Xiaodong Liang said in reply to Account Deleted...
Hi Alex, you are right. It did not pop out error when I tested. Thanks spotting this. -Xiaodong
Reply
06/01/2012 at 03:10 AM

---
**内容**: passion Pham said...
Hi.
I have applied your code.
But, I have a bug.
On CreateRegionFromPoints Function
command "return regionId" is failed.
Detail: The app is break.

I have check, when I don't used createFromCurves(). This bug don't occur.
can you support for me.
thank you so much
Reply
09/10/2014 at 08:40 PM

---
**内容**: Chao Han said...
We try to use your code to create a solid object. But we found the same bug -- "return regionId" is failed.
Please told us how to solve this bug?
Reply
02/05/2016 at 10:23 AM

---
