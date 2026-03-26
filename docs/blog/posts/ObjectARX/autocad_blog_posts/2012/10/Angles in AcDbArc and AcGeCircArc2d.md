---
title: "Angles in AcDbArc and AcGeCircArc2d"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Polyline
description: "I use the AutoCAD RECTANG command to draw an unrotated rectangle with the FILLET option. When prompted for the startAng and endAng of the resulting..."
author: Autodesk
---
# Angles in AcDbArc and AcGeCircArc2d

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/angles-in-acdbarc-and-acgecircarc2d.html

## 文章内容

By Balaji Ramamoorthy
Issue
I use the AutoCAD RECTANG command to draw an unrotated rectangle with the FILLET option. When prompted for the startAng and endAng of the resulting AcDbPolyline's corner arcs, the values are always 0 and 90 degree.
However, if the polyline is selected and LIST is typed, the values for startAng and endAng are displayed correctly with only the upper-right corner sweeping from 90 to 0 degrees. Why ?
Solution
The LIST command and entity definition data for an arc uses AcDbArc class information, whereas a polyline provides AcGeCircArc2d information.
Querying the arcs of a filleted rectangle, which is represented as a polyline entity, pPoly:
Acad::ErrorStatus es;
AcDbDatabase *pDb = acdbHostApplicationServices()->workingDatabase();
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
  AcDbTransactionManager* pTM = pDb->transactionManager();
AcTransaction *pTransaction = pTM->startTransaction();
AcDbObject *pCurveObj = NULL;
  es = pTransaction->getObject(
                                pCurveObj,
                                plOid,
                                AcDb::kForRead
                            );
AcDbPolyline *pPoly = AcDbPolyline::cast(pCurveObj);
if(pPoly != NULL)
{
    int n = pPoly->numVerts();
    AcGeCircArc2d arc; AcGeVector2d dir;
      for (int i=0; i < n; i++)
    {
        if (pPoly->segType(i) != AcDbPolyline::kArc)
            continue;
          if ((es = pPoly->getArcSegAt(i, arc)) == Acad::eOk)
        {
            dir =  arc.refVec();
            acutPrintf(
                ACRX_T("\nVertex %d:\tstartang= %f \t endang= %f \trefvec= {%i %i}"),
                i,
                arc.startAng(),
                arc.endAng(),
                (int)dir[0],
                (int)dir[1]);
        }
    }
}
pTM->endTransaction();
Printed results are:
Vertex 0: startang= 0.000000 endang= 1.570796 refvec= {-1 0}
Vertex 2: startang= 0.000000 endang= 1.570796 refvec= {0 1}
Vertex 4: startang= 0.000000 endang= 1.570796 refvec= {1 0}
Vertex 6: startang= 0.000000 endang= 1.570796 refvec= {0 -1}
This is the expected result because the angles are measured with respect to the arc's reference vector, which in this case is always oriented to contain the startpoint of the arc. Therefore, vertex 0 is the upper left arc (corner) of an unrotated rectangle. Its reference vector of [-1 0] proceeds from the arc's center point along the -x axis in WCS. The startpoint of the arc then lies on this reference vector, and thus the start angle from the reference vector is 0. The arc's endpoint is found 1.57 rads away from the startpoint/reference vector in a + clockwise direction.
The start and end angles for an AcDbArc are invariably measured in respect to the +x axis. Also, the positive direction for rotation is considered to be counter-clockwise. Vertex 0, the upper-left corner will then list a start angle=180 and an end angle=90.

