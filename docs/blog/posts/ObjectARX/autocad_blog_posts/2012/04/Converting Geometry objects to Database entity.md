---
title: "Converting Geometry objects to Database entity"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - Database
description: "Most often, you will work with geometry objects (AcGeXXXX classes) to perform common 2D and 3D geometric operations. To convert them to an entity t..."
author: Autodesk
---
# Converting Geometry objects to Database entity

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/converting-geometry-objects-to-database-entity.html

## 文章内容

By Balaji Ramamoorthy
Most often, you will work with geometry objects (AcGeXXXX classes) to perform common 2D and 3D geometric operations. To convert them to an entity that can be appended to the AutoCAD database, there is an ObjectARX / AutoCAD .Net API method that is very handy.
The "acdbConvertGelibCurveToAcDbCurve" is a method that was introduced in AutoCAD 2012 which can do this. The equivalent of this method in the AutoCAD .Net API was introduced in AutoCAD 2013.
Here is an example demonstrating the use of the method in ObjectARX / AutoCAD .Net API :
// This sample uses "acdbConvertGelibCurveToAcDbCurve"
// Other methods that you might be interested in :
// AcDbCurve::getAcGeCurve()
// AcDbCurve::setFromAcGeCurve()
  static void AdskMyTest1_Ge2Db(void)
{
    AcGeEllipArc3d ellipticArc(AcGePoint3d::kOrigin,
        AcGeVector3d::kXAxis,
        AcGeVector3d::kYAxis,
        2.0,
        0.5);
      GetCurveObjectId(ellipticArc);
}
    static AcDbObjectId GetCurveObjectId(AcGeCurve3d &geCurve3d)
{
    AcDbObjectId oid = AcDbObjectId::kNull;
    Acad::ErrorStatus es = Acad::eOk;
    AcDbCurve *pDbCurve = NULL;
    es = acdbConvertGelibCurveToAcDbCurve(geCurve3d, pDbCurve);
    if(es == Acad::eOk)
    {
    postToDb(pDbCurve, oid);
    }
    return oid;
}
       static Acad::ErrorStatus postToDb(
 AcDbEntity* pEnt, AcDbObjectId &oid)
{
    AcDbBlockTable* pBlockTable;
    AcDbDatabase *pDb
    = acdbHostApplicationServices()->workingDatabase();
    pDb = ->getBlockTable(pBlockTable, AcDb::kForRead);
    AcDbBlockTableRecord* pModelSpaceBTR = NULL;
    pBlockTable->getAt(ACDB_MODEL_SPACE,
    pModelSpaceBTR,
    AcDb::kForWrite);
      Acad::ErrorStatus es;
    es = pModelSpaceBTR->appendAcDbEntity(oid, pEnt);
    pEnt->close();
    pModelSpaceBTR->close();
    pBlockTable->close();
      return es;
}
  using Autodesk.AutoCAD.Geometry;
  [CommandMethod("ge2dbnet")]
public void Ge2DbMethod()
{
     EllipticalArc3d arc1 =
         new EllipticalArc3d(Point3d.Origin,
     Vector3d.XAxis,
     Vector3d.YAxis,
     2.0, 0.5);
      GetCurveObjectId(arc1);
}
    static ObjectId GetCurveObjectId(Curve3d geCurve3d)
{
    Document doc  = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
    ObjectId oid = ObjectId.Null;
    try
    {
        Curve dbCurve = Curve.CreateFromGeCurve(geCurve3d);
        if (dbCurve != null)
        {
            using (Transaction tr =
                db.TransactionManager.StartTransaction())
                {
                    BlockTable bt = tr.GetObject(db.BlockTableId,
                        OpenMode.ForRead) as BlockTable;
                BlockTableRecord btr =
                    tr.GetObject(db.CurrentSpaceId,
                    OpenMode.ForWrite) as BlockTableRecord;
                btr.AppendEntity(dbCurve);
                tr.AddNewlyCreatedDBObject(dbCurve, true);
                tr.Commit();
                }
         }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
    return oid;
}

