---
title: "Create a hatch object and set its scale"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - Hatch
  - Layer
description: "How do I create a hatch object and set its scale? I had a function in my ARX application that was used to create HATCH pattern. However, I found th..."
author: Autodesk
---
# Create a hatch object and set its scale

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-a-hatch-object-and-set-its-scale.html

## 文章内容

By Xiaodong Liang
Issue
How do I create a hatch object and set its scale? I had a function in my ARX application that was used to create HATCH pattern. However, I found that it was useless to set scale in my application because I had to set the scale manually
once again in AutoCAD. Why did this happen?
Solution
This might be caused by the wrong placement of setPatternScale() function. Note that you have to set hatch pattern properties, such as, pattern angle, pattern scale, associativity, and pattern name just after AcDbHatch has been created. After appending loops to the hatch object, you can set its other properties, such as layer name, color index, hatch style and so on. Then evaluateHatch() method must be used to evaluate if it can be properly displayed on the screen. And lastly it should be appended to AutoCAD database and closed. The following code shows how to do this exactly. For detailed information, refer to AcDbHatch class explanation in ObjectARX documentation.
  #define AOK(es) if(es != Acad::eOk) throw es;
void createHatch(void)
{    
    AcDbObjectId objId;
      AcDbEntity* pEnt; 
      ads_name ent;
      ads_point point; 
      if (RTNORM !=
          acedEntSel(_T("SELECT AN ENTITY TO BE HATCHED: "),
          ent,
          point))  
           return;  
      assert(objId.setFromOldId(ent[0]));  
      AOK( acdbOpenObject(pEnt,objId,AcDb::kForRead) );
      AcDbHatch *pHatch = new AcDbHatch;  
      assert(pHatch); 
      try 
      {   
           AcDbBlockTableRecordPointer pBtr(
               ACDB_MODEL_SPACE,
               curDoc()->database(),
               AcDb::kForWrite);   
           AOK(pBtr.openStatus());    
           AOK(pHatch->setPatternAngle(0));  
           AOK(pHatch->setPatternScale(10)); 
           AOK(pHatch->setAssociative(Adesk::kFalse));
           AOK(pHatch->setPattern(AcDbHatch::kPreDefined,
               _T("ANSI32")));
           // append loop to hatch   
           AcDbObjectIdArray dbObjIds; 
           int objNum =
               dbObjIds.append(pEnt->objectId());
           acutPrintf(_T("\nOBJ number is %d."), objNum);   
           AOK(pHatch->appendLoop(AcDbHatch::kExternal,
               dbObjIds));    
           AOK(pHatch->setLayer(pEnt->layer()));     
           AOK(pHatch->setColorIndex(256));  
           //bylayer      
           AOK(pHatch->setHatchStyle(AcDbHatch::kNormal));   
           AOK(pHatch->evaluateHatch()); 
           AOK(pBtr->appendAcDbEntity(pHatch));  
           AOK(pHatch->close());  
      } 
      catch (const Acad::ErrorStatus es) 
      {     
           acutPrintf(_T("Error: %s"),
               acadErrorStatusText(es)); 
           delete pHatch; 
      }

