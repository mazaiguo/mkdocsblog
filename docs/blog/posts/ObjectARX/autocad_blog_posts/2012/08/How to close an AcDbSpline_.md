---
title: "How to close an AcDbSpline?"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "There is no specific isClosed() method defined for AcDbSpline as there is for"
author: Autodesk
---
# How to close an AcDbSpline?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-close-an-acdbspline.html

## 文章内容

By Augusto Goncalves
There is no specific isClosed() method defined for AcDbSpline as there is for
AcDbPolyline. However, in many cases, an AcDbSpline can be closed. Here is a
simple solution to implement a setClosed function for splines. It uses the
getNurbsData() and setNurbsData() AcDbSpline methods. getNurbsData will gather
the information about the spline, including a Boolean closed that indicates if
the spline is closed or not. setNurbsData() takes the same arguments as
getNurbsData(), so only the closed argument will be changed to Adesk::kTrue to
obtain the desired result.
And the same idea can be applied to the .NET Spline.NurbData property.
void setClosed(AcDbSpline *pSpline)
{
    int          degree;
    Adesk::Boolean    rational;
    Adesk::Boolean    closed;
    Adesk::Boolean    periodic;
    AcGePoint3dArray  controlPoints;
    AcGeDoubleArray    knots;
    AcGeDoubleArray    weights;
    double        controlPtTol;
    double        knotTol;
    // get data from the spline
    pSpline->getNurbsData(degree, rational, closed, periodic,
                 controlPoints, knots, weights,
                 controlPtTol, knotTol);
    if(closed == Adesk::kTrue)
        return;
    // set as closed
  closed = Adesk::kTrue;
    // apply data back
    pSpline->setNurbsData(degree, rational, closed, periodic,
                 controlPoints, knots, weights,
                 controlPtTol, knotTol);
}

## 评论

**内容**: Oleg said...
Hello, Augusto!
I have not found setNurbsData method in C#,
do you know how to do it in C#?
Regards,
Oleg
Reply
08/18/2012 at 01:11 AM

---
**内容**: Augusto Goncalves said in reply to Oleg...
Hi Oleg
You have probably noticed Alexander reply below, which is correct. And, in general, many C++ methods of Objects/Entities starting with set/get were implemented as properties in .NET, and this prefix was removed.
Regards,
Augusto Goncalves
Reply
08/22/2012 at 10:00 AM

---
**内容**: Account Deleted said...
Hi, Oleg!
Spline entity has property Spline.NurbsData in .NET
Reply
08/18/2012 at 09:07 AM

---
