---
title: "Understanding tolerances and limits for dimensions using ObjectARX"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Dimension
  - ObjectARX
description: "When working with AutoCAD dimensions, the user can apply these styles to a dimension entity: NONE, DEVIATION, SYMMETRICAL, LIMITS and BASIC. It may..."
author: Autodesk
---
# Understanding tolerances and limits for dimensions using ObjectARX

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/understanding-tolerances-and-limits-for-dimensions-using-objectarx.html

## 文章内容

By Xiaodong Liang
When working with AutoCAD dimensions, the user can apply these styles to a dimension entity: NONE, DEVIATION, SYMMETRICAL, LIMITS and BASIC. It may not be readily apparent what dimension system variables apply to these style overrides. Although a 'dimlim' dimension variable exists, 'dimnone', 'dimdev', 'dimsym' or 'dimbas' dimension variables do not exist.
In explaining tolerances and limits for dimensions, the background for tolerances and limits is first explained. There are four dimension variables that are involved in this process:
DIMTOL
DIMLIM
DIMTM
DIMTP
DIMTOL = Dimension Tolerance can be On or Off. The dimension will display a value followed by tolerance with a '+', '-' sign and a number if DIMTP = DIMTM, or a dimension value followed by two values stacked on top of each other one with a '+' sign (DIMTP - Dimension Tolerance Plus value) and the other value with a '-' sign (DIMTM - Dimension Tolerance Minus value).
DIMLIM = Dimension Limits can be ON/OFF, the dimension will display stacked values representing the value of the dimension in terms of an upper limit (top) and a lower limit (bottom). If DIMTP = DIMTM the displayed values will be equal to each other.
Dimension are complex entities and are represented by AcDbDimension and reside in Model Space block table or one of the many Paper Space layout block tables. Each dimension is related to an anonymous block which is an instance of AcDbBlockTableRecord which and like any other block contains the entities that represent the dimension block. The dimension entity also references an AcDbDimStyleTableRecord which controls the overall look and feel (dimension style) of the dimension entity.
A dimension may contain overrides (see the DIMOVERRIDE command). When an override is applied to a dimension, the override information is stored as Extended Entity Data (Xdata). Refer to the ObjectARX documentation for a discussion of the  override information: 'Dimension Style Overrides'.
In ObjectARX, you can manipulate this Xdata directly or just simply override the appropriate dimension variable.
There appears to be a paradox when it comes to displaying dimensions with a 'deviation' style (see AutoCAD's Modify Dimension Style dialog). If the dimension variables DIMTP and DIMTM both have a value of 0.00 and the 'deviation' option is applied to a dimension, the dimension will display a value for the dimension and a set of stacked tolerances, one with '+0.000' and one with '-0.000'. This seems to be a contradiction, because mentioned earlier if DIMTP = DIMTM and DIMTOL = ON, the dimension will display as symmetrical. In order for AutoCAD to display a dimension in the 'deviation' manner, AutoCAD changes the value of DIMTM to 1x10-9 , a very small value indeed. With that said it is still true that if 'DIMTP' is not equal 'DIMTM' (regardless of size) and 'DIMTOL' set to 'ON' the dimension will display as 'deviation' style.
Here is an example of a function that manipulates a selected dimension in terms of its Xdata result buffer:
static void selectDim(AcDbDimension *&pDim)
{
    ads_name ent;    
    ads_point pt;
    if (RTNORM != acedEntSel(L"\nSelect a Dimension",ent,pt))
    {
      acutPrintf(L"\nFailed to select an entity");
      return;
     }
       AcDbObjectId objId = NULL;              
     Acad::ErrorStatus es;
     acdbGetObjectId (objId , ent);
       AcDbObject *oObj = NULL;
      es = acdbOpenObject (oObj,
                            objId,
                            AcDb::kForRead);
        if(Acad::eOk == es)
      {
          if(oObj->isKindOf(AcDbDimension::desc()))
          {
            pDim = (AcDbDimension*)oObj;
          }
          else
          {
              acutPrintf(_T("\nSorry that is \
                  not a dimension entity."));
              oObj->close();
          }
      }
}
  static void dimTest()
{   
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
    struct resbuf* pRb;
    pDim->upgradeOpen();
      //Refer to the ObjectARX  help -
    // 'Dimension Style Overrides'
    // for the appropriate DXF group code values.
    pRb = acutBuildList(
        AcDb::kDxfRegAppName,   
        _T("ACAD"),
        AcDb::kDxfXdAsciiString,
        _T("DSTYLE"),
        AcDb::kDxfXdControlString,
        _T("{"),
        AcDb::kDxfXdInteger16,
        48,
        AcDb::kDxfXdReal,
        0.0000000000000001,
        AcDb::kDxfXdInteger16,
        71,
        AcDb::kDxfXdInteger16,
        1,
        AcDb::kDxfXdControlString,
        _T("}"),
        RTNONE);
      pDim->setXData(pRb);
    acutRelRb(pRb);
    pDim->close();
    }
Here is an example of a function that manipulates a selected dimension in terms of it's dimension variables, please note that the dimension variable method is a wrapper for manipulating the underlying Xdata:
static void dimLimVar()
{
      AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;   
      pDim->upgradeOpen();
    pDim->setDimlim(Adesk::kTrue);
    pDim->setDimtol(Adesk::kFalse);
    pDim->close();
}
Here are more examples:
static void dimNone()
{
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      struct resbuf* pRb;
    pDim->upgradeOpen();
    pRb = acutBuildList(
        AcDb::kDxfRegAppName,  
        _T("ACAD"),
        AcDb::kDxfXdAsciiString,
        _T("DSTYLE"),
        AcDb::kDxfXdControlString,
        _T("{"),
        AcDb::kDxfXdInteger16,
        48,
        AcDb::kDxfXdReal,
        0.0,
        AcDb::kDxfXdControlString,
        _T("}"),
        RTNONE);
      pDim->setXData(pRb);
    acutRelRb(pRb);
    pDim->close();
}
    // This is command 'DIMSYM'
static void dimSym()
{
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      struct resbuf* pRb;
    pDim->upgradeOpen();
    pRb = acutBuildList(
        AcDb::kDxfRegAppName,  
        _T("ACAD"),
        AcDb::kDxfXdAsciiString,
        _T("DSTYLE"),
        AcDb::kDxfXdControlString,
        _T("{"),
        AcDb::kDxfXdInteger16,
        71,
        AcDb::kDxfXdInteger16,
        1,
        AcDb::kDxfXdControlString,
        _T("}"),
        RTNONE);
      pDim->setXData(pRb);
    acutRelRb(pRb);
    pDim->close();
}
    // This is command 'DIMLIMIT'
static void dimLimit()
{
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      struct resbuf* pRb;
    pDim->upgradeOpen();
      pRb = acutBuildList(
        AcDb::kDxfRegAppName,  
        _T("ACAD"),
        AcDb::kDxfXdAsciiString,
        _T("DSTYLE"),
        AcDb::kDxfXdControlString,
        _T("{"),
        AcDb::kDxfXdInteger16,
        72,
        AcDb::kDxfXdInteger16, 1,
        AcDb::kDxfXdControlString
        , _T("}"),
        RTNONE);
      pDim->setXData(pRb);
    acutRelRb(pRb);
    pDim->close();
}
    // This is command 'DIMBAS'
static void dimBas()
{
     AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      struct resbuf* pRb;
    pDim->upgradeOpen();
      pRb = acutBuildList(
        AcDb::kDxfRegAppName,   
        _T("ACAD"),
        AcDb::kDxfXdAsciiString, 
        _T("DSTYLE"),
        AcDb::kDxfXdControlString,
        _T("{"),
        AcDb::kDxfXdInteger16,
        147,
        AcDb::kDxfXdReal,
        -0.09,
        AcDb::kDxfXdControlString,
        _T("}"),
        RTNONE);
      pDim->setXData(pRb);
    acutRelRb(pRb);
    pDim->close();
}
    // This is command 'DIMTOLVAR'
static void dimTolVar()
{
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      pDim->upgradeOpen();
      pDim->setDimtol(Adesk::kTrue);
    pDim->setDimlim(Adesk::kFalse);
      pDim->close();
}
    // This is command 'DIMTPVAR'
static void dimTPVar()
{
    AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      double curval = 0.0;
    ads_real newval;
      curval = pDim->dimtp();
      acutPrintf(_T("\nCurrent value of DIMTP = %lf"),
        curval);
    acedInitGet(RSG_NONULL + RSG_NONEG, NULL);
    acedGetReal(_T("\nNew value for DIMTP: "),
        &newval);
      pDim->upgradeOpen();
    pDim->setDimtp((double)newval);
      pDim->close();
}
    // This is command 'DIMTMVAR'
static void dimTMVar()
{
     AcDbDimension* pDim = NULL;
    selectDim(pDim);
    if(!pDim)  return;
      double curval = 0.0;
    ads_real newval;
    curval = pDim->dimtm();
      acutPrintf(_T("\nCurrent value of DIMTM = %lf"), curval);
    acedInitGet(RSG_NONULL + RSG_NONEG, NULL);
    acedGetReal(_T("\nNew value for DIMTM: "), &newval);
      pDim->upgradeOpen();
    pDim->setDimtm((double)newval);
    pDim->close();
}

