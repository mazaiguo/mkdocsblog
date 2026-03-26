---
title: "Locking an Entity in AutoCAD using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "Here are few ways to lock entities in drawing, so that the user can't move or do any kind of operations to them. It allows some objects to be locke..."
author: Autodesk
---
# Locking an Entity in AutoCAD using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/locking-an-entity-in-autocad-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Here are few ways to lock entities in drawing, so that the user can't move or do any kind of operations to them. It allows some objects to be locked and some not, in same drawing.
The best way to do this is to use overrule. The "AcDbTransformOverrule" can be used to prevent any transformation (Move, Rotate, Scale etc) from affecting the entity. The "AcDbGripOverrule" can be used to remove the default grips that appear on the entity. This will prevent the entity from being grip edited. Here is a sample code snippet to prevent circles in the drawing from getting transformed :
Step 1: Implement a Transform overrule
#include "dbentityoverrule.h"
  class CTransformOverrule: public AcDbTransformOverrule
{
public:
      static CTransformOverrule* _pTheOverrule;
    ACRX_DECLARE_MEMBERS(CTransformOverrule);
      bool isApplicable(const AcRxObject* pOverruledSubject) const
    {
        return true;
    }
      Acad::ErrorStatus transformBy(
                                    AcDbEntity* pSubject,
                                    const AcGeMatrix3d& xform
                                )
    {
        if(pSubject->isA() != AcDbCircle::desc())
            return Acad::eOk;
          AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
        if(pCircle != NULL)
            return Acad::eNotApplicable;
          return AcDbTransformOverrule::transformBy(pSubject, xform);
    }
      // Take care about calling "CTransformOverrule::rxInit();"
    // in "On_kInitAppMsg" of the arx that uses this overrule.
    static void CTransformOverrule::AddOverrule()
    {
        if(_pTheOverrule != NULL)
            return;
          _pTheOverrule = new CTransformOverrule();
          AcRxOverrule::addOverrule(
                                    AcDbCircle::desc(),
                                    _pTheOverrule,
                                    true
                                 );
          CTransformOverrule::setIsOverruling(true);
    }
      static void CTransformOverrule::RemoveOverrule()
    {
        if(_pTheOverrule == NULL)
            return;
          CTransformOverrule::setIsOverruling(false);
          AcRxOverrule::removeOverrule(
                                        AcDbCircle::desc(),
                                        _pTheOverrule
                                    );
        delete _pTheOverrule;
          _pTheOverrule = NULL;
    }
};
  CTransformOverrule* CTransformOverrule::_pTheOverrule = NULL;
  ACRX_NO_CONS_DEFINE_MEMBERS(CTransformOverrule, AcDbTransformOverrule);
Step 2 : Implement a Grip overrule
class CGripOverrule: public AcDbGripOverrule
{
public:
      static CGripOverrule* _pTheOverrule;
    ACRX_DECLARE_MEMBERS(CGripOverrule);
      bool isApplicable(const AcRxObject* pOverruledSubject) const
    {
        return true;
    }
      //Add the overrule.
    //Take care about calling "CGripOverrule::rxInit();"
    // in "On_kInitAppMsg" of the arx that uses this overrule.
    static void CGripOverrule::AddOverrule()
    {
        if(_pTheOverrule != NULL)
            return;
          _pTheOverrule = new CGripOverrule();
          AcRxOverrule::addOverrule(AcDbCircle::desc(), _pTheOverrule, true);
          CViewportDrawOverrule::setIsOverruling(true);
    }
      static void CGripOverrule::RemoveOverrule()
    {
        if(_pTheOverrule == NULL)
            return;
          CGripOverrule::setIsOverruling(false);
          AcRxOverrule::removeOverrule(AcDbCircle::desc(), _pTheOverrule);
          delete _pTheOverrule;
          _pTheOverrule = NULL;
    }
      Acad::ErrorStatus CGripOverrule::getGripPoints(const AcDbEntity* pSubject,
                                AcGePoint3dArray&  gripPoints,
                                AcDbIntArray &     osnapModes,
                                AcDbIntArray &  geomIds)
    {
        AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
        if(pCircle != NULL)
        {// Remove the grip points, for a circle
            gripPoints.removeAll();
            return Acad::eNotApplicable;
        }
          return AcDbGripOverrule::getGripPoints(pSubject, gripPoints, osnapModes, geomIds);
    }
      Acad::ErrorStatus CGripOverrule::getGripPoints
                            (
                                const AcDbEntity* pSubject,
                                AcDbGripDataPtrArray& grips,
                                const double curViewUnitSize,
                                const int gripSize,
                                const AcGeVector3d& curViewDir,
                                const int bitflags
                            )
    {
        AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
        if(pCircle != NULL)
        {// Remove the grip points, for a circle
            grips.removeAll();
            return Acad::eNotApplicable;
        }
          return AcDbGripOverrule::getGripPoints
                                            (
                                                pSubject,
                                                grips,
                                                curViewUnitSize,
                                                gripSize,
                                                curViewDir,
                                                bitflags
                                            );
    }
};
  CGripOverrule* CGripOverrule::_pTheOverrule = NULL;
  ACRX_NO_CONS_DEFINE_MEMBERS(CGripOverrule, AcDbGripOverrule);
Step 3 : Ensure that our overrule classes are part of the class hierarchy.
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
{
    AcRx::AppRetCode retCode = AcRxArxApp::On_kInitAppMsg (pkt) ;
      CGripOverrule::rxInit();
    CTransformOverrule::rxInit();
    acrxBuildClassHierarchy();
      return (retCode) ;
}
Step 4 : Add commands to enable / disable the overruling
// Command to enable overruling
static void asdkOverrule_Start(void)
{
    CTransformOverrule::AddOverrule();
    CGripOverrule::AddOverrule();
}
  // Command to disable overruling
static void asdkOverrule_Stop(void)
{
    CTransformOverrule::RemoveOverrule();
    CGripOverrule::RemoveOverrule();
}

## 评论

**内容**: Alexander Rivilis said...
Hi, Balaji!
I think that after explanation of Art Cooney (http://forums.autodesk.com/t5/Autodesk-ObjectARX/How-to-use-a-reactor-to-prevent-CAD-s-modify-command/m-p/3809644#M30007) was necessary to correct this post.
Reply
03/20/2013 at 12:05 AM

---
**内容**: Balaji said in reply to Alexander Rivilis...
Hi Alexander,
Thanks for pointing that out.
I wanted to provide alternate ways without using the overruling and so had included suggestions from a another Devnote that we have had for quite some time. Sorry, I havent tested those suggestions using a code. Art Cooney has rightly pointed out that such changes from reactors can cause other problems.
I have removed the other suggestions from the blog post and have only retained the overruling method that I had tested.
Reply
03/20/2013 at 01:33 AM

---
**内容**: Alexander Rivilis said...
Hi, Balaji!
This was a very radical solution to removing the other suggestions from the blog post and have only retained the overruling method! :-)
Reply
03/20/2013 at 01:51 AM

---
**内容**: Tony Tanzillo said...
>>>> CGripOverrule::setIsOverruling(false);
Hi Balaji.
Since Overrules have appeared, I have been puzzled at how Autodesk could have provided a 'global' switch that allows any application (managed or native) to completely disable all overruling, application-wide.
Your example in this case, serves to make my point, which is that setIsOverruling() is a massive screw-up.
Your code incorrectly calls it when you remove your overrule, and in doing so, disables all overrules in the application.
Well that certainly is radical, isn't it? :D
Since when, does an API allow one application to corrupt, disable, or interfere with other applications?
Please ask one of your collages who may be more familiar with the design of the Overrule functionality, to please explain how this could have happened.
Reply
05/02/2013 at 01:44 PM

---
**内容**: Balaji said in reply to Tony Tanzillo...
Hi Tony,
You have rightly pointed out the issue with my code snippet. I haven't considered the possibility of other overrules, which a production code must definitely consider.
A "well-behaved" :) plugin can check the state of overruling using the "isOverruling" method even before it adds its own overrules. Based on this information, it should only stop the application wide overruling if no other overrule was initially active.
If any of the plugins do not follow this, then it will be affecting the overrule of other plugins.
I dont think this is the first instance where AutoCAD is expecting certain "right" behavior from plugins to prevent interfering with other plugins.
For example, when working with AcEdInputPointFilter, the plugin needs to look for other point filters and if they do exist then store a pointer to it and forward calls to it.
I am not aware of the reasoning for the design decision behind having an application wide switch for overrules but these are my thoughts on this topic.

Reply
05/03/2013 at 04:06 AM

---
