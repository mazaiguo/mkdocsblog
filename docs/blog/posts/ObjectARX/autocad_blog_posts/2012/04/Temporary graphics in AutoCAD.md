---
title: "Temporary graphics in AutoCAD"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "It usually helps to visually see the results of our geometric computations. ObjectARX and the AutoCAD .Net API provide a few temporary graphics met..."
author: Autodesk
---
# Temporary graphics in AutoCAD

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/temporary-graphics-in-autocad.html

## 文章内容

By Balaji Ramamoorthy
It usually helps to visually see the results of our geometric computations. ObjectARX and the AutoCAD .Net API provide a few temporary graphics methods that come very handy in such scenario.
One way to do this is to use the transient graphics API, but in this post I will introduce you to yet another way - the usage of the low level graphics methods such as "acedGrVecs" and its .Net equivalent "DrawVectors".
Here is a sample code that draws a vector and its mirror about the X axis. A "zoom" or "regen" will erase the temporary graphics. As mentioned in the ObjectARX documentation, since these methods rely on the graphics system, there can be some change in its behavior between AutoCAD releases. Please ensure that you test your application with all the AutoCAD releases that you expect your application to work with.
Here is the ObjectARX version :
ads_point fromPt;
int rc = acedGetPoint(NULL, _T("\nPick first point"), fromPt);
if(rc != RTNORM)
    return;
  ads_point toPt;
rc = acedGetPoint(NULL, _T("\nPick second point"), toPt);
if(rc != RTNORM)
    return;
  int colorIndex = 2;
  // Compute the mirror vector
ads_point fromPtMirror;
ads_point_set(fromPt, fromPtMirror);
fromPtMirror[1] *= -1.0;
  ads_point toPtMirror;
ads_point_set(toPt, toPtMirror);
toPtMirror[1] *= -1.0;
  struct resbuf  *vlist;
  // Build ResBuf
vlist = acutBuildList(   
                    RTSHORT, colorIndex,   // Color
                      RTPOINT, fromPt,       // Actual vector
                    RTPOINT, toPt,
                      RTPOINT, fromPtMirror, // Mirror vector
                    RTPOINT, toPtMirror,
                      RTNONE);
  // Using aced method to create temporary graphics.
// NULL for identity transformation matrix
rc = acedGrVecs(vlist, NULL);
  // Cleanup
acutRelRb(vlist);
Here is the equivalent of the above code using the AutoCAD .Net API :
private const int RTPOINT = 5002;
private const int RTSHORT = 5003;
Document activeDoc =
            Application.DocumentManager.MdiActiveDocument;
Editor ed = activeDoc.Editor;
  PromptPointResult ppr1 = ed.GetPoint("\nPick first point");
if (ppr1.Status != PromptStatus.OK)
    return;
  PromptPointResult ppr2 = ed.GetPoint("\nPick second point");
if (ppr2.Status != PromptStatus.OK)
    return;
  Point3d sp = ppr1.Value;
Point3d ep = ppr2.Value;
  int colorIndex = 1;
  using (ResultBuffer resBuf = new ResultBuffer())
{
    resBuf.Add(new TypedValue(RTSHORT, colorIndex));
      // The actual vector
    resBuf.Add(new TypedValue(
                                RTPOINT,
                                new Point2d(sp.X, sp.Y)
                             )
               );
      resBuf.Add(new TypedValue(
                                RTPOINT,
                                new Point2d(ep.X, ep.Y)
                             )
               );
      // and its mirror about x axis
    resBuf.Add (new TypedValue(
                                RTPOINT,
                                new Point2d(sp.X, -sp.Y)
                              )
               );
      resBuf.Add(new TypedValue(
                                RTPOINT,
                                new Point2d(ep.X, -ep.Y)
                              )
               );
      ed.DrawVectors(resBuf, Matrix3d.Identity);
}

## 评论

**内容**: Tom DiVittis said...
Am I crazy, or did you switch from VB to C in the middle of this sample?
More importantly, how would one clear such temporary graphics?
Reply
09/10/2012 at 06:48 AM

---
**内容**: Balaji said...
Tom,
I dont understand what you mean by "switching from VB to C in the middle".The post has sample code demonstrated using ObjectARX and in C#. The choice is all yours.
Regarding clearing the graphics, a regen or zoom should do - as explained in the post.
Reply
09/10/2012 at 08:00 AM

---
**内容**: Alexander Rivilis said in reply to Balaji...
Hi Balaji!
I think that Tom DiVittis means that RTSHORT and RTPOINT is not defined in AutoCAD .NET API
But AutoCAD .NET API has Autodesk.AutoCAD.Runtime.LispDataType type. RTSHORT is equivalent of (int)Autodesk.AutoCAD.Runtime.LispDataType.Int16 and RTPOINT is is equivalent of (int)Autodesk.AutoCAD.Runtime.LispDataType.Point2d
Reply
04/05/2013 at 12:51 PM

---
**内容**: Balaji said in reply to Alexander Rivilis...
Thanks Alex :)
I now understand Tom's point.
I have updated the sample code to include the const values for RTSHORT and RTPOINT.
Sorry for missing it out in my original post.
Reply
04/09/2013 at 12:38 AM

---
**内容**: Tom DiVittis said...
Balaji,
It turns out I was crazy. ;) Sorry for the stupid questions. I really have to stop trying to write code in 5 minute increments.
Please excuse my lack of C abilities. I'm trying to do some (very) simple temporary graphics, very similar to this example, in VB and I'm stuck with the RT types (RTSHORT, RTPOINT, etc.).
Thank you.
Reply
04/05/2013 at 05:10 AM

---
**内容**: Balaji said in reply to Tom DiVittis...
Hi Tom,
Sorry for missing a part of the code snippet in my original post.
I have updated the post now.
Please let me know if you have any issues. I would suggest trying the transient graphics API instead of this low level approach.
Have you looked at the other post ?
http://adndevblog.typepad.com/autocad/2012/04/using-transient-graphics.html
Regards,
Balaji
Reply
04/09/2013 at 12:41 AM

---
**内容**: Hemant Carpenter said...
hi
I want to assign LineWeight also for temp line.
like RTSHORT, RTPOINT
Reply
03/18/2015 at 01:49 AM

---
**内容**: Alexander Rivilis said in reply to Hemant Carpenter...
It is impossible to assign LineWeight to temp line drawn with acedGrDraw / acedGrVecs, but you can offset temp line left and right with value from 0 to Width with appropriate step.
Reply
03/19/2015 at 11:58 AM

---
**内容**: HarryKane said...
Too bad this example doesn't show how to render the lines dynamically after Point 1 is placed and Point 2 still on your mouse cursor.
I would like an interactive preview, showing the lines already before Point 2 is placed.
After all points (or other Editor inputs) are done, there is little reason to show any preview as i could then also create the final intended object anyway.
Reply
08/29/2016 at 08:29 AM

---
**内容**: James Maeding said...
I'd like to draw temp vecs at an elevation. Can I do with the RB, or is its the matrix?
Reply
05/08/2018 at 01:31 PM

---
