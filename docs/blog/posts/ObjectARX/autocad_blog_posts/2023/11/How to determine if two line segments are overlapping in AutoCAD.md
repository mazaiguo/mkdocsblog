---
title: "How to determine if two line segments are overlapping in AutoCAD"
date: 2023-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "To check if two line segments are overlapping, we shall use the AcGeLinearEnt3d::overlap() method. It returns the line that coincides with their re..."
author: Autodesk
---
# How to determine if two line segments are overlapping in AutoCAD

发布日期: 2023-11-01

原始链接: https://adndevblog.typepad.com/autocad/2023/11/how-to-determine-if-two-line-segments-are-overlapping-in-autocad.html

## 文章内容

By Sreeparna Mandal
To check if two line segments are overlapping, we shall use the AcGeLinearEnt3d::overlap() method. It returns the line that coincides with their region of overlap. The declaration of the method goes as mentioned:
GE_DLLEXPIMPORT Adesk::Boolean overlap(
    const AcGeLinearEnt3d& line, 
    AcGeLinearEnt3d*& overlap, 
    const AcGeTol& tol = AcGeContext::gTol
) const;
Here, the overlap parameter is null if this function returns a value of Adesk::kFalse, else the overlap line may be an object of any derived class of AcGeLinearEnt3d, depending on the types of the two lines. The overlap() method can also be used for an input line which is 2D linear entity.
Below is the code snippet for its usage:
static void ADSKMyGroupCheckOverlap()
{

 AcGeLineSeg3d line1(AcGePoint3d(0, 0, 0), AcGePoint3d(5, 0, 0));
 AcGeLineSeg3d line2(AcGePoint3d(2, 2, 0), AcGePoint3d(2, -5, 0)); //intersecting with line1
 AcGeLineSeg3d line3(AcGePoint3d(0, 0, 0), AcGePoint3d(10, 0, 0)); // overlapping with line1

 bool isOverlapped = Adesk::kFalse;

 AcGeLinearEnt3d* overlappingEnt;

 isOverlapped = line1.overlap(line3, overlappingEnt);

 if (isOverlapped)
 {
  AcGePoint3d startPt, endPoint;
  if (!overlappingEnt->hasEndPoint(endPoint))
   return;
  if (!overlappingEnt->hasStartPoint(startPt))
   return;
  acutPrintf(_T("\nBoth lines are overlapping. Start and end points of the overlapping segment are:\n"));
  acutPrintf(_T("\nStart point: %f, %f, %f"), startPt.x, startPt.y, startPt.z);
  acutPrintf(_T("\nEnd point: %f, %f, %f"), endPoint.x, endPoint.y, endPoint.z);
 }
 else
 {
  acutPrintf(_T("\nLines are not overlapping."));
 }
}

## 评论

**内容**: octordle said...
Octordle compared to Wordle and Quordle is somewhat different. With 13 guesses with eight different vertical lines, the player needs to solve all eight horizontal words at the same time.
Reply
11/28/2023 at 01:07 AM

---
**内容**: slope said...
Your writings stick out to me since the content is interesting and simple to understand. Even though I've read a lot of websites, I still like yours more. Your essay was interesting to read. I can understand the essay better now that I've read it carefully. In the future, I'd like to read more of your writing.
Reply
12/19/2023 at 01:04 AM

---
**内容**: heardle 80s said...
The writing is amazing. Looking forward to reading it more.
Reply
01/18/2024 at 07:46 PM

---
**内容**: Sreeparna said...
Thanks!!
Reply
01/18/2024 at 11:42 PM

---
**内容**: slope said...

I am very happy to visit your blog, It tells me a lot of useful information. I will regularly visit the blog to support you.
Reply
02/05/2024 at 08:33 PM

---
**内容**: connections said...
The article in this forum is very good, this article is very helpful for me. Nice to read your post. If you can, take a moment to play game a and b one of the most exciting games
Reply
03/04/2024 at 01:47 AM

---
