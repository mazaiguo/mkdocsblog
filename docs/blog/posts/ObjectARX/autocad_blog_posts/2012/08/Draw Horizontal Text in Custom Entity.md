---
title: "Draw Horizontal Text in Custom Entity"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Plot
  - Unicode
description: "How to draw a text in a custom entity which is always horizontal irrespective of view direction and plot rotation?"
author: Autodesk
---
# Draw Horizontal Text in Custom Entity

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/draw-horizontal-text-in-custom-entity.html

## 文章内容

By Philippe Leefsma
Q:
How to draw a text in a custom entity which is always horizontal irrespective of view direction and plot rotation?
A:
You can use the AcGiViewport::getCameraUpVector() function to get the up vector for the current view direction. Using the up vector one can easily calculate the flow direction for drawing the text horizontal to the current view.
During plot, one needs to take into account the plot rotation. During the plot, the drawing is rotated depending on the drawing orientation(Portrait or Landscape).
Of course, this can be implemented only in the viewportDraw() override of the custom entity, since this is where the viewport-specific graphics are drawn. The following sample shows how to implement this:
void AsdkcusEnt::viewportDraw(AcGiViewportDraw * mode)
{
       //draw the text
       AcGeVector3d vecUp;
       mode->viewport().getCameraUpVector(vecUp);
         AcGeVector3d vecFlow = vecUp.crossProduct(
        mode->viewport().viewDir());
         //check the context
       if (mode->context()->isPlotGeneration())
       {
              //Get the plot configuration of the current layout
              AcApLayoutManager *pLayMan = (AcApLayoutManager *)
                acdbHostApplicationServices()->layoutManager();
                AcDbLayout *pLay = pLayMan->findLayoutNamed(
                pLayMan->findActiveLayout(Adesk::kTrue),Adesk::kTrue);
                // Check if this plot is rotated or not
              double pi = 3.14159265;
                switch(pLay->plotRotation())
              {
              case AcDbPlotSettings::PlotRotation::k90degrees:
                     vecFlow.rotateBy(-pi/2,mode->viewport().viewDir());
                     break;
                case AcDbPlotSettings::PlotRotation::k180degrees:
                     vecFlow.rotateBy(pi,mode->viewport().viewDir());
                     break;
                case AcDbPlotSettings::PlotRotation::k270degrees:
                     vecFlow.rotateBy(pi/2,mode->viewport().viewDir());
                     break;
              }
                pLay->close();
                mode->geometry().text(
                AcGePoint3d(10,10,0),
                mode->viewport().viewDir(),
                vecFlow, 10, 1, 0,
                L"Test");
       }
       else
       {
              mode->geometry().text(
                AcGePoint3d(10,10,0),
                mode->viewport().viewDir(),
                vecFlow, 10, 1, 0,
                L"Test");
       }
         AcDbEntity::viewportDraw(mode);
}

## 评论

**内容**: matlab said...
could you provide an version of c#?
Reply
08/30/2012 at 07:38 PM

---
**内容**: Philippe said...
Hi There,
Well, in .Net custom entities do not exist but you could achieve the same result by using "DrawableOverrule.ViewportDraw" method.
I don't have a sample ready to send you unfortunately. You should be able to find overrule sample on this blog or on Kean's Through The Interface blog.
I hope it helps.
Reply
08/31/2012 at 01:49 AM

---
