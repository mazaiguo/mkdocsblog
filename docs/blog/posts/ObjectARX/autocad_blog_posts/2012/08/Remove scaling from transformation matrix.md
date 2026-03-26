---
title: "Remove scaling from transformation matrix"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "If you are trying to create a transformation matrix and e.g. because of imprecision it will get a scaling factor, and this scaling factor is non-un..."
author: Autodesk
---
# Remove scaling from transformation matrix

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/remove-scaling-from-transformation-matrix.html

## 文章内容

By Adam Nagy
If you are trying to create a transformation matrix and e.g. because of imprecision it will get a scaling factor, and this scaling factor is non-uniform (i.e. different value along the X, Y or Z axis) then you cannot use it to transform certain entities like a Polyline. If you try it you'll get an eCannotScaleNonUniformly error. If you do not want to scale at all, you can just remove the scaling factor like so:
Public Sub RemoveScaling(ByRef mx As Matrix3d)
  Dim axes As New List(Of Vector3d)
    For i As Integer = 0 To 2
    Dim vec As New Vector3d(mx(i, 0), mx(i, 1), mx(i,2))
      ' This will make the vector have length = 1.0
    vec = vec.GetNormal()
      axes.Add(vec)
  Next
    mx = New Matrix3d(New Double() _
  {
    axes(0).X, axes(0).Y, axes(0).Z, mx(0, 3), 
    axes(1).X, axes(1).Y, axes(1).Z, mx(1, 3), 
    axes(2).X, axes(2).Y, axes(2).Z, mx(2, 3), 
    mx(3, 0), mx(3, 1), mx(3, 2), mx(3,3)
  })
End Sub
The same way you could also make sure that the scaling is uniform by making the length of each axis vector the same. You would need to modify the above code like so:
    vec = vec.GetNormal().MultiplyBy(scalingValue)

## 评论

**内容**: Veli V. said...
Hi Adam,
can I transform (rotate and scale) AcDbArc entity with matrix? Of course I can get AcDbArc points and transform them but I´m looking the right way. =)
-Veli V.
Reply
08/12/2012 at 10:43 PM

---
**内容**: Adam Nagy said...
Hi Veli,
Yes, it should work. Did you give it a try? :)
In the ARX help file, under AcDbEntity::transformBy, you can find information about it.
Cheers,
Adam
Reply
08/13/2012 at 12:10 PM

---
**内容**: Srinivasan said...
Hi Adam
This doen't work if the matrix has rotation as well as transformation
Srini
Reply
10/07/2012 at 07:13 AM

---
**内容**: Veli V. said...
The solution is to transform AcDbArc points and set them back AcDbArc entity.
Example below:
Acad::ErrorStatus BPEntityHelper::TransformEntity(AcDbArc *arc)
{
Acad::ErrorStatus err = Acad::eOk;
if(!arc)
return Acad::eNullEntityPointer;
AcGePoint3d ptStart, ptMid, ptEnd, ptCenter;
double angStart = arc->startAngle(), angEnd = arc->endAngle();
double startParam = 0.0, endParam = 0.0, midParam = 0.0, dist = 0.0;
AcGeMatrix3d arc_mat;
arc_mat.setToIdentity();
AcGeVector3d normal_vec = arc->normal();
arc_mat = arc_mat.planeToWorld(normal_vec);
err=arc->getStartParam(startParam);
err=arc->getEndParam(endParam);
err=arc->getDistAtParam(endParam, dist);
err=arc->getParamAtDist(dist / 2.0, midParam);

// Get arc three points
arc->getStartPoint(ptStart);
arc->getPointAtParam(midParam, ptMid);
arc->getEndPoint(ptEnd);

// Transform points
ptStart = updatePoint3d(ptStart);
ptMid = updatePoint3d(ptMid);
ptEnd = updatePoint3d(ptEnd);
ptStart.transformBy(arc_mat);
ptMid.transformBy(arc_mat);
ptEnd.transformBy(arc_mat);
// Create temporary arc geometry to analyze it
AcGeCircArc2d *geArc = new AcGeCircArc2d(ptStart.convert2d(AcGePlane::kXYPlane),
ptMid.convert2d(AcGePlane::kXYPlane),
ptEnd.convert2d(AcGePlane::kXYPlane));
AcGePoint3d center = AcGePoint3d(geArc->center().x, geArc->center().y, 0.0);
center.transformBy(arc_mat);
double radius = geArc->radius();
angStart = acutAngle(asDblArray(geArc->center()), asDblArray(geArc->startPoint()));
angEnd = acutAngle(asDblArray(geArc->center()), asDblArray(geArc->endPoint()));
if(geArc->isClockWise())
{
double dTmp = angStart;
angStart = angEnd;
angEnd = dTmp;
}
err = arc->setCenter(center);
if(err!=Acad::eOk)
return err;
err = arc->setStartAngle(angStart);
if(err!=Acad::eOk)
return err;
err = arc->setEndAngle(angEnd);
if(err!=Acad::eOk)
return err;
err = arc->setRadius(radius);
if(err!=Acad::eOk)
return err;

delete geArc;
return err;
}
Reply
12/20/2012 at 03:26 AM

---
