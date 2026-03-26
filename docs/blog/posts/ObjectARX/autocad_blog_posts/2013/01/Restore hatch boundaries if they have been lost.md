---
title: "Restore hatch boundaries if they have been lost"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - DWG
  - Database
description: "How can I restore hatch boundaries if they have been lost due to some reason?"
author: Autodesk
---
# Restore hatch boundaries if they have been lost

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/restore-hatch-boundaries-if-they-have-been-lost.html

## 文章内容

By Philippe Leefsma
Q:
How can I restore hatch boundaries if they have been lost due to some reason?
A:
AutoCAD doesn't have a command to do that. Fortunately, we can create one with ObjectARX API.
The most complex in the task is to handle splines properly as there are various of splines in AutoCAD, fixed point spline, rational spline, not rational spline, etc. The code works quite well for lines, arcs, circles, ellipses and splines.  Note that error checking is minimal for brevity.  Please bear in mind that it is not possible to restore the original boundary entities exactly, because the underlying geometry objects prefixed with AcGe in AcDbHatch do not match AutoCAD database entities prefixed with AcDb one by one. For example, if there is a closed loop composed of some lines in the original hatch boundary entities, it will become a polyline in the final result restored back.
In the example, the boundaries restored are in red and put on the current layer. You can use selection filter to get them for further modification.  There is a Test.dwg drawing included, for test purposes.
How To Use The Example:
1. Build the attached project with VC2010 or copy the code for “BzhRestoreHatchBoundary” to your own project
2. Startup AutoCAD
3. Load the ARX file
4. Open the drawing that you want to restore hatch boundaries
5. Issue the command with short name RHB or long name RESTOREHATCHBOUNDARY
6. Choose hatch entities that you would like to restore boundaries. You could choose multiple hatches one time
RestoreHatchBoundary.zip

## 评论

**内容**: Andrew Puller said...
Autocad has two methods to restore hatch boundaries.
Method 1. Select a hatch, right click and select generate boundary (which runs the HatchGenerateBoundary command).
Method 2. Select a hatch, on the ribbon, Hatch Editor context tab, Boundaries panel, click Recreate, choose polyline or region, then yes or no to associate the new boundary to the hatch.
Reply
01/24/2013 at 01:42 PM

---
**内容**: incognito said in reply to Andrew Puller...
Mr Andrew, you are the cad Master !
Thanks a lot ! Your advice worked perfectly and saved me a lot of trouble !
Reply
02/26/2016 at 09:19 AM

---
**内容**: Afiqah Ismail said in reply to Andrew Puller...
Thank you so much! :'D You help me.
Reply
02/05/2018 at 09:35 AM

---
**内容**: René Davis Ramirez said...
Is it possible to have the same code posted as managed .Net (VB or C#), not all of us are able to build / understand the ObjectARX API.
Thanks
Reply
02/12/2013 at 01:19 AM

---
**内容**: Philippe Leefsma said in reply to René Davis Ramirez...
Sorry René, we can't convert every arx sample we post into .Net. The .Net API is mainly a wrapper around arx classes, so in most of the cases the member methods are pretty similar. As far as the class names are concerned, they are identical but without prefix in .Net: AcDbHatch -> Hatch, AcGePoint3d -> Point3d.
Reply
02/12/2013 at 01:47 PM

---
**内容**: René Davis Ramirez said in reply to Philippe Leefsma...
I have been trying to convert the sample to managed Net myself, but it seems that I'm missing some header files:
acmemdebug.h
gemetatp.h
gegetmti.h
dbidnln.h
I have also tried asking ADN, CaseNo-08044841, but with no result.
Thanks in any case.
René
Reply
02/12/2013 at 11:58 PM

---
**内容**: Alexander Rivilis said...
Hi, René!
I've tried to help you: http://forums.autodesk.com/t5/NET/Restore-hatch-boundaries-if-they-have-been-lost-with-NET/m-p/3779514#M33429
Reply
02/13/2013 at 08:03 AM

---
