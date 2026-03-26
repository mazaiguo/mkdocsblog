---
title: "AcDbRegion::transformBy"
date: 2014-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "Question:  I have a situation where the use of the method AcDbRegion::transformBy is giving me different results in AutoCAD 2015 as opposed to Auto..."
author: Autodesk
---
# AcDbRegion::transformBy

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/acdbregiontransformby-.html

## 文章内容

By Madhukar Moogala
Question:  I have a situation where the use of the method AcDbRegion::transformBy is giving me different results in AutoCAD 2015 as opposed to AutoCAD 2014. Can you tell me what has changed in the method that would account for the change.
Answer : It worked in Acad 2014 because we used a bigger tolerance before (equalPoint to 1.0e-8 and  equalVector to 1.0e-6). In Acad 2015 the tolerance setting was removed,this change is having impact on few scenarios ,one such scenario is illustrated below and possible workaround is also demonstrated. Thanks to our ADN partner for surfacing this behavior.
To restore legacy behavior in such circumstances we may have to reset system wide tolerance to
/*Resetting sytsem wide tolerance for ACAD 2015*/
AcGeContext::gTol.setEqualPoint(1.0e-8);
AcGeContext::gTol.setEqualVector(1.0e-6);

static void transformTest()
{
/*Resetting sytsem wide tolerance for ACAD 2015*/
AcGeContext::gTol.setEqualPoint(1.0e-8);
AcGeContext::gTol.setEqualVector(1.0e-6);

double epTol = AcGeContext::gTol.equalPoint();
double evTol = AcGeContext::gTol.equalVector();

CString msg;
msg.Format(_T("point tolerance is %e, and vector tolerance is %e\n"), epTol, evTol);
acedPrompt(msg);

// Second, create a transform matrix that maps from one coordinate syste to another

AcGePoint3d startPoint;
AcGeVector3d mStockProfileXDir, mExtrudeDir, mNormalDir;

startPoint.set(12342.705102605765, -14874.057509290647, 25.766600469474248);

mStockProfileXDir.set(0.00000000000000000, 1.0000000000000000, 0.00000000000000000);
mNormalDir.set(-0.048960818631765893, -6.4357153980460105e-012, 0.99880069995915965);
mExtrudeDir.set(-0.99880069995915977, 0.00000000000000000, -0.048960818631764047);

AcGeMatrix3d xform;
xform.setToAlignCoordSys(AcGePoint3d(0, 0, 0),
                            AcGeVector3d::kXAxis,
                            AcGeVector3d::kYAxis,
                            AcGeVector3d::kZAxis,
                            startPoint,
                            mStockProfileXDir,
                            mNormalDir,
                            mExtrudeDir);

// Is the new coordinate system orthogonal?

if (!xform.isUniScaledOrtho())
    acedPrompt(_T("Transform matrix axes are not orthogonal\n"));
else
    acedPrompt(_T("Transform matrix axes are orthogonal\n"));


// Finally, transform a region to the new coordinate system.
AcDbVoidPtrArray curves, regions;
AcDbCircle *pTestCircle = new AcDbCircle(AcGePoint3d::kOrigin, AcGeVector3d::kZAxis, 10.0);

if (pTestCircle != NULL)
{
    curves.append(pTestCircle);

    AcDbRegion::createFromCurves(curves, regions);
    if (regions.length() != 0)
    {
        for (int i = 0; i < regions.length(); i++)
        {
            AcDbRegion* testRegion = static_cast<AcDbRegion*>(regions[i]);
            Acad::ErrorStatus es = testRegion->transformBy(xform);
            delete testRegion;
            msg.Format(_T("The transform operation returned %d\n"), es);
            acedPrompt(msg);
        }
    }

    delete pTestCircle;
}
}
Edit:
Caution:

It should be noted that lowering the existing precision can also have drawbacks and unwanted side-effects.
I recommend to not change the global tolerances as described in that article below, as it impacts not only the app that does this, but it impacts the tolerances globally (across all loaded apps, and also for AutoCAD itself).
The global tolerances should be changed only in a local scope when doing calculations that require them, and should be reset to the previous defaults afterwards.

## 评论

**内容**: Gaston Nunez said...
Hi,
I wonder if this mean that the .NET API has been affected too (the Tolerance class). If so it's not documented.
Reply
08/19/2014 at 09:07 PM

---
**内容**: Madhukar Moogala said in reply to Gaston Nunez...
Hi Gaston,
This blog post is to indicate a workaround and test check if your old algorithms are not working on 2015, how ever this is only a temporary solution.
If there is a change in Tolerance class we would know and let you know.
Reply
08/19/2014 at 09:36 PM

---
**内容**: Gaston Nunez said in reply to Madhukar Moogala...
Thanks
Reply
08/20/2014 at 09:11 PM

---
