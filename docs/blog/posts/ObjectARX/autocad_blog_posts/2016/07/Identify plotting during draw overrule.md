---
title: "Identify plotting during draw overrule"
date: 2016-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
  - Unicode
description: "Recently, I received questions from couple of developers on identifying the plotting state during overrule. Though the context of questions were di..."
author: Autodesk
---
# Identify plotting during draw overrule

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/identify-plotting-during-draw-overrule.html

## 文章内容

By Virupaksha Aithal
Recently, I received questions from couple of developers on identifying the plotting state during overrule. Though the context of questions were different (like one developer wanted to avoid doing draw overrule during plot and other wanted kind of applying plot stamp) I felt I need to make the solution as blog. To identify the plotting state, use “Context.IsPlotGeneration” as shown in below code
public override bool WorldDraw(Autodesk.AutoCAD.GraphicsInterface.Drawable drawable, 
            Autodesk.AutoCAD.GraphicsInterface.WorldDraw wd)
{
    if (wd.Context.IsPlotGeneration)
    {
        //code while ploting 
    }
    else
    {
        //code while not ploting 
    }

    return base.WorldDraw(drawable, wd);
}

## 评论

**内容**: John said...
The above is not quite complete: The IsPlotGeneration state is NOT set when using the Autodesk PDF driver (PDF ePlot by Autodesk).
Note: Based on testing with AutoCAD 2014 and legacy hidden viewports.
Reply
07/19/2016 at 01:08 AM

---
**内容**: TH said...
Thanks for the code. I'm getting a problem when publish drawing in background. Is there any API to detect drawing is publishing in background?
Thanks!
Reply
07/20/2016 at 10:38 PM

---
**内容**: viru said in reply to TH...
Hi,
Please make sure you load the overrule plug-in in the back ground acad process also. Back ground plotting starts a background acad instance. so you need make sure the overrule dll is also loaded in the back ground process. Once method is to use autoloader mechanism (make sure the autoloader bundle) is in trusted location.
Thanks
Viru
Reply
07/20/2016 at 11:13 PM

---
**内容**: TH said in reply to viru...
Thank you very much for very helpful information!
Reply
07/22/2016 at 09:02 AM

---
