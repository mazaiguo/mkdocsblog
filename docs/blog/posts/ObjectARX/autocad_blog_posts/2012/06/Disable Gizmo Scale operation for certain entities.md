---
title: "Disable Gizmo Scale operation for certain entities"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Selection
description: "In the 3D Modeling workspace under Home tab > Selection panel there is a tool called Gizmo. I observed that the AcEditorRector::commandWillStart is..."
author: Autodesk
---
# Disable Gizmo Scale operation for certain entities

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/disable-gizmo-scale-operation-for-certain-entities.html

## 文章内容

By Adam Nagy
In the 3D Modeling workspace under Home tab > Selection panel there is a tool called Gizmo. I observed that the AcEditorRector::commandWillStart is called with "GRIPEDIT_TOOL" when the Gizmo is being used, but I cannot tell if it's a Move, Rotate or Scale operation. Ultimately, I would like to prevent the Gizmo Scale operation being used on certain entities.
Solution
Actually, the tooltip of the Gizmo button shows the name of the system variable (DEFAULTGIZMO) that controls which Gizmo is being used. And the help file describes the possible values and their meaning.
When the pick selection changes, then you could check what objects are selected, and if it includes the one that you do not want the gizmo to work for then just set the DEFAULTGIZMO to 3 (= no gizmo)
Here is a code that "disables" the gizmo if 2 objects are selected, otherwise sets it back to its previous value:
class MyEditorReactor : public AcEditorReactor
{
  static int prevGizmovalue;
  virtual void pickfirstModified()
  {
    struct resbuf * ss = NULL;
    int ret = acedSSGetFirst(NULL, &ss);
    if (ret != RTNORM)
      return;
      long len;
    struct resbuf gizmo;
    ret = acedSSLength(ss->resval.rlname, &len);
    if (ret != RTNORM)
    {
      if (prevGizmovalue != -1)
      {
        gizmo.restype = 5003;
        gizmo.resval.rint = prevGizmovalue;
        acedSetVar(L"DEFAULTGIZMO", &gizmo);
        prevGizmovalue = -1;
      }
        acedSSFree(ss->resval.rlname);
      return;
    }
      if (len == 2)
    {
      acedGetVar(L"DEFAULTGIZMO", &gizmo);
      prevGizmovalue = gizmo.resval.rint;
      gizmo.resval.rint = 3; // 3 = no gizmo
      acedSetVar(L"DEFAULTGIZMO", &gizmo);
    }
    else if (prevGizmovalue != -1)
    {
      gizmo.restype = 5003;
      gizmo.resval.rint = prevGizmovalue;
      acedSetVar(L"DEFAULTGIZMO", &gizmo);
      prevGizmovalue = -1;
    }
      acedSSFree(ss->resval.rlname);
  }
};
int MyEditorReactor::prevGizmovalue = -1;
MyEditorReactor g_reactor;

## 评论

**内容**: marcel said...
A normal engineer does not ask for a Gizmo.
How stupid can Autodesk be.
Reply
04/08/2021 at 12:00 AM

---
**内容**: marcel said...
I have turn it off many times, but it turns on by it's self....
wanting to irritate again and again ...
Is Autocad for real ?
Reply
10/19/2021 at 01:24 AM

---
