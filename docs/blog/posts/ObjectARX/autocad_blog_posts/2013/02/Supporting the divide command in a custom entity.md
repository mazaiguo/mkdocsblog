---
title: "Supporting the divide command in a custom entity"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How can I have a custom entity support the AutoCAD DIVIDE command?"
author: Autodesk
---
# Supporting the divide command in a custom entity

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/supporting-the-divide-command-in-a-custom-entity.html

## 文章内容

By Xiaodong Liang
Issue
How can I have a custom entity support the AutoCAD DIVIDE command?
Solution
To have a custom entity support the DIVIDE command , you must first must derive from AcDbCurve or one of its derived classes. Then override the following as a minimum implementation to support the DIVIDE command, e.g.
Acad::ErrorStatus getStartParam(double& startParam) const;
Acad::ErrorStatus getEndParam(double& endParam) const;
Acad::ErrorStatus getDistAtParam (double param, double& dist)  const;
Acad::ErrorStatus getPointAtDist(double dist, AcGePoint3d& point) const;
Acad::ErrorStatus getPointAtParam(double param, AcGePoint3d& point) const
For a code sample on how to override these methods and to implement them in a custom entity, refer to polysamp sample in the ObjectARX SDK. This customer entity is a closed poly line e.g.
The relevant overridden methods are:
virtual Acad::ErrorStatus
        getStartParam  (double& startParam)     const
{
    assertReadEnabled();
    startParam = 0.0;
    return Acad::eOk;
}
  virtual Acad::ErrorStatus
        getEndParam  (double& endParam)    const
{
    assertReadEnabled();
    //closed poly. So the end param is 2* PI
      endParam = 6.28318530717958647692;
    return Acad::eOk;
}
  Acad::ErrorStatus AsdkPoly::getDistAtParam(
                                double param,
                                double& dist)  const
{
    assertReadEnabled();
      rx_fixangle(param);
      double circumRadius =
        (startPoint() - center()).length();
    double alpha        =
        3.14159265358979323846 * 0.5 -
        3.14159265358979323846 / mNumSides;
    double sideLength   =
        2.0 * circumRadius * cos(alpha);
      double includedAngle     =
        6.28318530717958647692 / mNumSides;
    int    numIncludedAngles =
        int(param / includedAngle);
    double theta             =
        param - numIncludedAngles * includedAngle;
      if (theta > 1.0e-10) {
        dist = sideLength * numIncludedAngles +
               circumRadius * sin(theta) /
          sin(3.14159265358979323846 - theta - alpha);
    } else {
        dist = sideLength * numIncludedAngles;
    }
      return Acad::eOk;
}
  Acad::ErrorStatus
AsdkPoly::getPointAtParam(
              double param,
              AcGePoint3d& point) const
{
    assertReadEnabled();
      Acad::ErrorStatus es = Acad::eOk;
  // Find out how many included angles "param" contains.
// Find that vertex, and the direction of the line defined
// by that vertex and the following vertex. Add the appropriate
// distance along that line direction to get the new point.
      rx_fixangle(param);
      double circumRadius =
              (startPoint() - center()).length();
    double includedAngle=
              6.28318530717958647692 / mNumSides;
    int    numIncludedAngles =
             int(param / includedAngle);
    double theta =
            param - numIncludedAngles * includedAngle;
      double gamma =
         3.14159265358979323846 * 0.5 +
          3.14159265358979323846 / mNumSides - theta;
      double distToGo =
        circumRadius * sin(theta) / sin(gamma);
      AcGeVector3d lineDir  =
           sideVector(numIncludedAngles);
      AcGePoint3dArray vertexArray;
    if ((es =
          getVertices3d(vertexArray)) != Acad::eOk) {
        return es;
    }
      if (theta > 1.0e-10) {
        point = vertexArray[numIncludedAngles] + (distToGo * lineDir);
    } else {
        point = vertexArray[numIncludedAngles];
    }
      return es;
}
By these method, when DIVID command is executed, users input the segment number of division such as 10. AutoCAD will divide the poly along the sides and create the segment points.

