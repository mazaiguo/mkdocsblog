---
title: "Using Transient graphics"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "In this post we looked at using graphics functions provided by AutoCAD API to show temporary graphics. In this post we will look at using the trans..."
author: Autodesk
---
# Using Transient graphics

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/using-transient-graphics.html

## 文章内容

By Balaji Ramamoorthy
In this post we looked at using graphics functions provided by AutoCAD API to show temporary graphics. In this post we will look at using the transient graphics API to draw temporary graphics. This API provides us much better control over the display of the graphics as compared to the graphics functions.
Here is a sample code that uses transient graphics to mark the intersection points of rectangle and a ray. To try this, draw a rectangle and select an internal point and the ray direction when prompted.
Using ObjectARX :
static AcArray<AcDbEntity*> _markers;
static AcArray<int> viewportNumbers;
  static void ArxProject_Test(void)
{
    Acad::ErrorStatus es;
    AcDbDatabase *pDb =
        acdbHostApplicationServices()->workingDatabase();
      ads_point pickPnt;
    ads_name ent_name;
    int ret = acedEntSel(
                            ACRX_T("\n Select a polyline\n"),
                            ent_name,
                            pickPnt
                        );
    if(ret != RTNORM)
        return;
      AcDbObjectId plOid;
    es = acdbGetObjectId(plOid, ent_name);
    if (es != Acad::eOk)
        return;
      ads_point adsTestPoint;
    ret = acedGetPoint
                (
                    NULL,
                    ACRX_T("\n Select an internal point\n"),
                    adsTestPoint
                ) ;
    if(ret != RTNORM)
        return;
    AcGePoint3d testPoint = asPnt3d(adsTestPoint);
      ads_real rayAngle = 0.0;
    ret = acedGetAngle(
                        asDblArray(testPoint),
                        ACRX_T("Specify ray direction"),
                        &rayAngle
                      );
    if(ret != RTNORM)
        return;
      AcGePoint3d tempPoint = testPoint + AcGeVector3d::kXAxis;
    tempPoint = tempPoint.rotateBy(
                                    rayAngle,
                                    AcGeVector3d::kZAxis,
                                    testPoint
                                  );
    AcGeVector3d rayDir = tempPoint - testPoint;
      ClearTransientGraphics();
      AcDbTransactionManager* pTM = pDb->transactionManager();
    AcTransaction *pTransaction = pTM->startTransaction();
    AcDbObject *pCurveObj = NULL;
      es = pTransaction->getObject(
                                    pCurveObj,
                                    plOid,
                                    AcDb::kForRead
                                );
    AcDbCurve *pCurve = AcDbCurve::cast(pCurveObj);
      AcGiTransientManager* pTransientManager
                                = acgiGetTransientManager();
      viewportNumbers.removeAll();
    struct resbuf res;
    acedGetVar(L"CVPORT", &res);
    viewportNumbers.append(res.resval.rint);
      if(pCurve != NULL)
    {
        for (int cnt = 0; cnt < 2; cnt++)
        {
            if (cnt == 1)
                rayDir = rayDir.negate();
              AcDbRay ray;
            ray.setBasePoint(testPoint);
            ray.setUnitDir(rayDir);
              AcGePoint3dArray IntersectionPoints;
            es = pCurve->intersectWith(
                                        &ray,
                                        AcDb::kOnBothOperands,
                                        IntersectionPoints
                                      );
            if(es == Acad::eOk)
            {
                int numberOfInters = 0;
                numberOfInters = IntersectionPoints.length();
                for(int i=0; i < numberOfInters; ++i)
                {
                    AcGePoint3d pt = IntersectionPoints[i];
                    AcDbCircle *marker
                        = new AcDbCircle
                                    (
                                        pt,
                                        AcGeVector3d::kZAxis,
                                        0.2
                                    );
                    AcCmColor color;
                    color.setColor(2);
                    marker->setColor(color);
                    _markers.append(marker);
                      pTransientManager->addTransient
                                        (
                                            marker,
                                            kAcGiDirectShortTerm,
                                            0,
                                            viewportNumbers
                                        );
                      acutPrintf(
                                ACRX_T("\n Point : %lf %lf"),
                                pt.x,
                                pt.y
                              );
                }
            }
        }
    }
    pTM->endTransaction();
}
  static void ClearTransientGraphics()
{
    AcGiTransientManager* pTransientManager
                                    = acgiGetTransientManager();
      int numOfMarkers = _markers.length();
    if (numOfMarkers > 0)
    {
        for(int index = 0; index < numOfMarkers; index++)
        {
            AcDbEntity *pMarker = _markers.at(index);
            pTransientManager->eraseTransient
                                    (
                                        pMarker,
                                        viewportNumbers
                                    );
            delete pMarker;
        }
        _markers.removeAll();
    }
}
Using AutoCAD .Net API :
using Autodesk.AutoCAD.GraphicsInterface;
  DBObjectCollection _markers = null;
  [CommandMethod("Test")]
public void TestMethod()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      PromptEntityOptions peo
        = new PromptEntityOptions("Select a polyline : ");
    peo.SetRejectMessage("Not a polyline");
    peo.AddAllowedClass
        (
            typeof(Autodesk.AutoCAD.DatabaseServices.Polyline),
            true
        );
    PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status != PromptStatus.OK)
        return;
      ObjectId plOid = per.ObjectId;
      PromptPointResult ppr =
        ed.GetPoint
        (
            new PromptPointOptions("Select an internal point : ")
        );
    if (ppr.Status != PromptStatus.OK)
        return;
    Point3d testPoint = ppr.Value;
      PromptAngleOptions pao
        = new PromptAngleOptions("Specify ray direction");
    pao.BasePoint = testPoint;
    pao.UseBasePoint = true;
    PromptDoubleResult rayAngle = ed.GetAngle(pao);
    if (rayAngle.Status != PromptStatus.OK)
        return;
      Point3d tempPoint = testPoint.Add(Vector3d.XAxis);
    tempPoint
        = tempPoint.RotateBy(
                                rayAngle.Value,
                                Vector3d.ZAxis,
                                testPoint
                            );
    Vector3d rayDir = tempPoint - testPoint;
      ClearTransientGraphics();
    _markers = new DBObjectCollection();
      using (Transaction tr
                = db.TransactionManager.StartTransaction())
    {
        Curve plcurve = tr.GetObject(
                                        plOid,
                                        OpenMode.ForRead
                                    ) as Curve;
          for (int cnt = 0; cnt < 2; cnt++)
        {
            if (cnt == 1)
                rayDir = rayDir.Negate();
              using (Ray ray = new Ray())
            {
                ray.BasePoint = testPoint;
                ray.UnitDir = rayDir;
                  Point3dCollection intersectionPts
                                    = new Point3dCollection();
                plcurve.IntersectWith(
                                        ray,
                                        Intersect.OnBothOperands,
                                        intersectionPts,
                                        IntPtr.Zero,
                                        IntPtr.Zero
                                     );
                  foreach (Point3d pt in intersectionPts)
                {
                    Circle marker
                        = new Circle(pt, Vector3d.ZAxis, 0.2);
                    marker.Color = Color.FromRgb(0, 255, 0);
                    _markers.Add(marker);
                      IntegerCollection intCol
                                    = new IntegerCollection();
                    TransientManager tm
                        = TransientManager.CurrentTransientManager;
                      tm.AddTransient
                        (
                            marker,
                            TransientDrawingMode.Highlight,
                            128,
                            intCol
                        );
                      ed.WriteMessage("\n" + pt.ToString());
                }
            }
        }
        tr.Commit();
    }
}
  void ClearTransientGraphics()
{
    TransientManager tm
            = TransientManager.CurrentTransientManager;
    IntegerCollection intCol = new IntegerCollection();
    if (_markers != null)
    {
        foreach (DBObject marker in _markers)
        {
            tm.EraseTransient(
                                marker,
                                intCol
                             );
            marker.Dispose();
        }
    }
}

## 评论

**内容**: Matthias said...
Hi,
is it possible to control the draw order of a non-persistent transient drawable, relative to database-resident entities in the drawing through .NET or P/Invoking the Object-ARX-API? I know about TransientDrawMode / subDrawMode parameters of the TransientManager.AddTransient method, but it seems this is not enough.
Background is, we're trying to draw a transient image with worldDraw.Geometry.Image(...) which works, but sometimes the image is drawn above and sometimes below database-resident entities. Our goal is to keep it always in the background.
Reply
04/26/2018 at 04:32 AM

---
