---
title: "Determine if point is on line bounded or unbounded"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "We need firstly create the AcGeXXXX classes and their member functions because the abstract class AcGeEntity2d derives all the curves, arcs and lin..."
author: Autodesk
---
# Determine if point is on line bounded or unbounded

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/determine-if-point-is-on-line-bounded-or-unbounded.html

## 文章内容

By Xiaodong Liang
We need firstly create the AcGeXXXX classes and their member functions because the abstract class AcGeEntity2d derives all the curves, arcs and lines. As such, there is an exact member function isOn(...) that can fulfill this task. Following are the codes for demo:
  // Judge point containment in a line which is a
// bounded line segment or an unbounded line
  //
// Name:    pointOnLine;
  // Return value: 1 within, 0 outside, -1 error, int;
  // Parameters ( all are input ):
// pt    -- single point to judge,
//ads_point/AcGePoint2d;
// endpt1    -- one end point of the line,
// ads_point AcGePoint2d;
//  endpt2    -- the other end point of the line,
//  ads_pointAcGePoint2d;
// bounded -- the line is bounded (not zero) or
//unbounded
  int pointOnLine(AcGePoint2d pt,
                AcGePoint2d endpt1,
                AcGePoint2d endpt2,
                int bounded)
{
    int retCode;
      if( bounded )
    {
        AcGeLineSeg2d *line;
        line = new AcGeLineSeg2d(endpt1, endpt2);
          if(line == NULL)
            return -1;
          retCode = (int) line->isOn(pt);
        delete line;
    }
    else
    {
        AcGeLine2d *line;
        line = new AcGeLine2d(endpt1, endpt2);
          if(line == NULL)
            return -1;
          retCode = (int) line->isOn(pt);
        delete line;
    }
      return (retCode == Adesk::kTrue ? 1 : 0);
}
  int pointOnLine( ads_point pt, ads_point endpt1,
                ads_point endpt2, int bounded)
{
    int retCode;
      if( bounded )
    {
        AcGeLineSeg2d *line;
        line = new AcGeLineSeg2d( asPnt2d(endpt1), asPnt2d(endpt2) );
          if(line == NULL)
            return -1;
          retCode = (int) line->isOn( asPnt2d(pt) );
    }
    else
    {
        AcGeLine2d *line;
        line = new AcGeLine2d( asPnt2d(endpt1), asPnt2d(endpt2) );
          if(line == NULL)
            return -1;
          retCode = (int) line->isOn( asPnt2d(pt) );
    }
      return (retCode == Adesk::kTrue ? 1 : 0);
}

