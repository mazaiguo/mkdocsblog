---
title: "Accessing hatches as individual lines with LISP"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - Hatch
  - ObjectARX
description: "I am working with an AutoLISP routine and I am running into a problem. The routine uses a hatch pattern to fill an object and then uses the individ..."
author: Autodesk
---
# Accessing hatches as individual lines with LISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/accessing-hatches-as-individual-lines-with-lisp.html

## 文章内容

By Balaji Ramamoorthy
Issue :
I am working with an AutoLISP routine and I am running into a problem. The routine uses a hatch pattern to fill an object and then uses the individual line information that makes up the hatch to do some calculations on the object. Is there a way to get this information with LISP ?
Solution
To get the start and end points of hatch lines, the alternative to exploding the hatch is to use ObjectARX.  The function AcDbHatch::getHatchLinesData() can be used to obtain the start and endpoints of the hatch lines. So a way to access this from Lisp is to create a Lisp callable function from ObjectARX.
The attached zip file contains a buildable project which demonstrates this technique.  The arx file defines the lisp function (hatchlines) and needs an ename as parameter. The function returns a list with the start points of the hatch lines.
Here is the Lisp callable function implemented using ObjectARX. Please have a look at the attached source code for the complete project.
int hatchlines()
{
    int res;
    resbuf *argRb;
    ads_name ename;
    AcDbObjectId objId;
    AcDbEntity *pEnt;
    AcDbHatch *pHatch;
      argRb = acedGetArgs();
      if (!argRb) {
        //
        // Get parameters
        //
        ads_point pt;
          if (RTNORM != (res = acedEntSel(
                                        _T("\nSelect hatch: "),
                                        ename,
                                        pt
                                        )))
        {
            acedRetNil();
            return res;
        }
      } else {
        //
        // Analyze parameters
        //
        if (argRb->restype != RTENAME) {
            acutPrintf(_T("\nFirst argument must be an ename."));
            acedRetNil();
            return RTERROR;
        }
        if (argRb->rbnext != NULL) {
            acutPrintf(_T("\nOnly one parameter accepted."));
            acedRetNil();
            return RTERROR;
        }
        acdbNameSet(argRb->resval.rlname, ename);
    }
      // Is the specified entity a hatch?
    acdbGetObjectId(objId, ename);
    if (Acad::eOk != acdbOpenAcDbEntity(   
                                            pEnt,
                                            objId,
                                            AcDb::kForRead
                                        ))
    {
        acedRetNil();
        return RTERROR;
    }
      if (!pEnt->isKindOf(AcDbHatch::desc())) {
        acutPrintf(_T("\nNot a hatch specified."));
        pEnt->close();
        acedRetNil();
        return RTERROR;
    }
      pHatch = (AcDbHatch*) pEnt;
      //
    // Get the hatch lines
    //
    AcGePoint2dArray startPoints,
        endPoints;
      if (Acad::eOk != pHatch->getHatchLinesData
                                            (
                                                startPoints,
                                                endPoints
                                            ))
    {
        acutPrintf(_T("\nError extracting hatch lines."));
        pHatch->close();
        acedRetNil();
        return RTERROR;
    }
      pHatch->close();
      //
    // Build a resbuf containing the coordinates
    //
      resbuf *retList = NULL,
        *retIter = NULL,
        *onePoint;
    int length = startPoints.length();
      for (int i = 0; i < length; ++i) {
        onePoint = acutNewRb(RTPOINT);
        onePoint->resval.rpoint[X] = startPoints[i].x;
        onePoint->resval.rpoint[Y] = startPoints[i].y;
        if (!retList) {
            retList = onePoint;
            retIter = retList;
        } else {
            retIter->rbnext = onePoint;
            retIter = retIter->rbnext;
        }
    }
      acedRetList(retList);
      // end of function
    return RTNORM;
}
Download HatchesFromLisp

## 评论

**内容**: Juergen.Becker@CAD-Becker.de said...
Hi,
is there any way to do that in C#?
I just want to get the start and endpoint of hatchlines without using ARX.
Regards Jürgen
Reply
12/03/2012 at 10:36 AM

---
**内容**: Balaji said...
Hi Juergen,
I see a method called "GetHatchLinesData" in the Hatch class that returns a "Line2dCollection" in the managed API documentation. So I think it is possible to get that info without using ObjectARX.
I havent used it but please do let me know if you have any issues in getting that method to work.
Reply
12/03/2012 at 09:59 PM

---
**内容**: Subir Kumar Dutta said...
Hi , During converting some old Lisp code to .Net , I faced a situation. After analysing the Lisp code we understand its calling some ARX functions (not commands , originally ads function - the whole ObjectARX project does not have a single executable commands but all are functions called by AutoLisp ).
For example as below,
int ReturnListToAutoLisp(void)
{
struct resbuf *LIST;
//...
//... = acedGetArgs
//...

acedRetList(LIST);
return RTNORM;
}
The function itself does not return the list but the list is returned by the acedRetList.
Now the below AutoLisp code that calls this functions and store the return value in a list.
(setq returnedList (ReturnListToAutoLisp 5))
Through it looks that the ReturnListToAutoLisp takes an integer ( like 5 here ) but actually in the ObjectARX code its parameter list is void ) . However the parameter value passed are collected by calling acedGetArgs.
Also the return value is not a single integer but a list of strings which are collected in the AutoLisp variable named ‘returnedList’ and which is used to populated DropDown list in DCL UI.
So far its okey.
I have ported the old ObjectARX 2005 code to ObjectARX 2014 version and its working fine when called from AutoLisp.
But while converting the Lisp code to VB.Net , I can’t find a way to collect the return value in a .Net variable of type string List (List(Of String)).
I found samples to call ObjectARX functions from .Net using P/Invoke which focus on passing arguments by creating a ResultBuffer. But I did not find a single sample that demonstrate how to collect the list of values retuned from ObjectARX functions through acedRetList.
I am counting that there must be a way but can’t figure it out.
Please help.

Reply
03/25/2014 at 04:41 AM

---
**内容**: Balaji said...
Hi Subir,
From what I understand, your ObjectARX function is implemented to provide its output to Lisp. Trying to make it work with .Net could be more work that simply rewriting the ObjectARX implementation to work with your new .Net code. You can have the ObjectARX method return an array of values that can be easily accessed by your .Net code.
Regards,
Balaji
Reply
03/26/2014 at 10:57 PM

---
