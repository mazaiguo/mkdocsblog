---
title: "Enable click inside selection of entity in 2d Wireframe visual style"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Selection
  - Solid
description: "I have an entity which has a solid filled area. If the user clicks somewhere in this area the entity gets selected in any visual style except 2d Wi..."
author: Autodesk
---
# Enable click inside selection of entity in 2d Wireframe visual style

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/enable-click-inside-selection-of-entity-in-2d-wireframe-visual-style.html

## 文章内容

By Adam Nagy
I have an entity which has a solid filled area. If the user clicks somewhere in this area the entity gets selected in any visual style except 2d Wireframe. How could I enable this sort of selection in 2d Wireframe mode as well?
Solution
By default in 2d Wireframe mode only the entity's frame or edges are selectable in case of 3d solid as well.
To enable click inside selection, so that the user can just click inside the filled area of the entity in order to select it, you can implement an AcEdSubSelectFilter.
Note that the following sample is very crude and is provided only to show the concept. For a more comprehensive sample have a look at [ObjectARX SDK 2009]\samples\reactors\selectionfilter
The best thing is to create a hitTest() function for your entity, which can tell if the cursor is inside the entity's area or not:
bool MyEntity::hitTest(
  const AcGePoint3d& wvpt, const AcGeVector3d& wviewVec,
  double wxaper, double wyaper)
{
  if (wvpt.x > 0 && wvpt.x < 10 &&
      wvpt.y > 0 && wvpt.y < 10)
    return true;
  else
    return false;
}
Then implement the AcEdSubSelectFilter:
class MyEdFilter : public AcEdSubSelectFilter
{
  virtual Acad::ErrorStatus subSelectClassList(AcArray& clsIds)
  {
    clsIds.append(MyEntity::desc());  
      return Acad::eOk;
  }
    virtual bool selectEntity(
    const AcGePoint3d& wvpt,
    const AcGeVector3d& wvwdir,
    const AcGeVector3d& wvwxdir,
    double wxaper,
    double wyaper,
    long flags,
    const AcGiViewport* pCurVp,
    AcDbEntity* pEnt
    ) const
  {
    return (MyEntity::cast(pEnt)->hitTest(
      wvpt, wvwdir, wxaper, wyaper));
  }
    virtual SubSelectStatus subSelectEntity(
    const AcGePoint3d&        wpt1,
    const AcGePoint3d&        wpt2,
    const AcGeVector3d&       wvwdir,
    const AcGeVector3d&       wvwxdir,
    double                    wxaper,
    double                    wyaper,                            
    AcDb::SelectType          seltype,
    bool                      bAugment,
    bool                      bIsInPickfirstSet,
    bool                      bEvery,
    const AcGiViewport*       pCurVP,
    AcDbEntity*               pEnt,
    AcDbFullSubentPathArray&  paths)
  {
    return kSubSelectAll;
  }
};
  MyEdFilter g_myFilter;
Now we just need to use an instance of this filter in the drawings where we want to enable this type of selection:
curDoc()->inputPointManager()->addSubSelectFilter(&g_myFilter);
Also, if you want to let the user pick-select this entity programmatically when using acedSSGet() then you need to use the ":A" option. This is what the ObjectARX Reference says about it:
This mode option causes acedSSGet() to perform single pick selection in space on entities that implement a subselection filter.

