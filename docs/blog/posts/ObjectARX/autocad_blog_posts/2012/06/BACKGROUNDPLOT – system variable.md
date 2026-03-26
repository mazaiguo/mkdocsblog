---
title: "BACKGROUNDPLOT – system variable"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Plot
description: "Most common issue developer’s face during plotting/publishing the drawing through API is of back ground plotting/publishing. Developers expect call..."
author: Autodesk
---
# BACKGROUNDPLOT – system variable

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/backgroundplot-system-variable.html

## 文章内容

By Virupaksha Aithal
Most common issue developer’s face during plotting/publishing the drawing through API is of back ground plotting/publishing. Developers expect call to plot/publish API, should finish the plot/publish and return. But the finishing of plotting/publishing in AutoCAD depends on system variable BACKGROUNDPLOT. During background plotting/publish a background process is started to plot/publish the drawing. So, to avoid this starting of background process, Developers need to set the value of BACKGROUNDPLOT  to 0 temporarily before starting the plotting/publishing through API as shown in below.
[CommandMethod("plotTest")]
static public void plotTest()
{
    short bgPlot =
       (short)Application.GetSystemVariable("BACKGROUNDPLOT");
      //set the BACKGROUNDPLOT = 0 temporarily.
    Application.SetSystemVariable("BACKGROUNDPLOT", 0);
      //
    //
    // plotting API calls
    //
    //
      //re-set the original value of BACKGROUNDPLOT.
    Application.SetSystemVariable("BACKGROUNDPLOT",
                                bgPlot);
}

## 评论

**内容**: Yamini said...
Above solution is not working with AutoCAD 2021. It is working with other AutoCAD versions. Please give solution for AutoCAD 2021.
Reply
05/16/2021 at 03:30 AM

---
**内容**: Yamini said...
For AutoCAD 2021 on plot and publish details showing error "Layout not found". For other CAD versions this error not coming. Please give solution on CAD 2021.
Reply
05/16/2021 at 05:08 AM

---
