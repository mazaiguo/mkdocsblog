---
title: "Prevent a Mirror operation on a custom Entity"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "To stop a custom entity from being mirrored, inside the subTransformBy() method, simply check to see if the determinant of the matrix passed to it ..."
author: Autodesk
---
# Prevent a Mirror operation on a custom Entity

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/prevent-a-mirror-operation-on-a-custom-entity.html

## 文章内容

By Balaji Ramamoorthy
To stop a custom entity from being mirrored, inside the subTransformBy() method, simply check to see if the determinant of the matrix passed to it is negative - if so, then do nothing and return Acad::eOk.
Here is a sample code snippet :
Acad::ErrorStatus MyCustomLine::subTransformBy
                                    (const AcGeMatrix3d& xform)
{
    assertWriteEnabled( Adesk::kFalse );
      // Prevent mirror of our custom line
    if(xform.det() < 0)
        return Acad::eOk;
      // Provide default implementation for other transformations
    return AcDbLine::subTransformBy(xform);
}

## 评论

**内容**: tyler agent said...
Thanks for sharing, and my wife and I are thinking about getting custom mirrors for our bathrooms in our home. And we're thinking about getting them made from http://www.careflections.com we just still deciding whether or not we want to go.
Reply
11/14/2013 at 07:13 AM

---
**内容**: Jak Manson said...
I have been looking into getting a custom mirror for my house and I was just wondering if the site I found is the best for what I am looking for. They look really promising and really know what they are talking about. www.careflections.com
Reply
11/14/2013 at 07:26 AM

---
**内容**: Alenamauer said...
As in many homes, I have a plain big mirror in my master suite. I am wondering if you were able to add a custom frame to it for me? I want a big chunky frame with detail, if at possible. I think it adds a lot of character to the bathroom.
Alena | http://www.careflections.com
Reply
02/14/2014 at 09:28 AM

---
