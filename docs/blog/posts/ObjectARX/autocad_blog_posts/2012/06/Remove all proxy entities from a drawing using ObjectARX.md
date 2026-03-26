---
title: "Remove all proxy entities from a drawing using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - ObjectARX
description: "I want to be able to work with a drawing which contains custom entities, for which I do not have the relevant application.  I would like to be able..."
author: Autodesk
---
# Remove all proxy entities from a drawing using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/remove-all-proxy-entities-from-a-drawing-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Issue
I want to be able to work with a drawing which contains custom entities, for which I do not have the relevant application.  I would like to be able to use the data in the drawing, for example for constructing new geometry.  Some entities I can explode, but others I cannot, as they are are marked as being not-erasable, I get the AutoCAD entity(ies) equivalent but the custom entity is still there.  What can I do?
Solution
It is possible to use ObjectARX to change all proxy entities for something else. The sample code does the following: Iterate through the entire drawing, and swaps all proxy entities for anonymous blocks. The blocks contain the equivalent geometry of the proxy entities. Note that this will not allow the creating entity to recover the information stored in the original entities.
AcDbObjectIdArray proxies;  
  // Iterate through the records  
// Make a list of all the proxies, and then process them afterwards. 
AcDbBlockTable* pTable; 
acdbHostApplicationServices()->workingDatabase()->getBlockTable
                                                    (
                                                        pTable,
                                                        AcDb::kForRead
                                                    );
if(pTable == NULL)
    return; 
  AcDbBlockTableIterator* pTableIter;
for( pTable->newIterator(pTableIter); !pTableIter->done(); pTableIter->step())
{     
    AcDbBlockTableRecord* pRecord;     
    pTableIter->getRecord(pRecord,AcDb::kForRead);  
    if(pRecord == NULL)
    {   
        acutPrintf(_T("\nCannot open a BTR"));  
        continue;   
    } 
      AcDbBlockTableRecordIterator* pRecordIter;
    for (    pRecord->newIterator(pRecordIter);
            ! pRecordIter->done();
            pRecordIter->step()
        )
    {
        AcDbEntity*pEnt;    
        pRecordIter->getEntity(pEnt, AcDb::kForRead);
        if(pEnt != NULL )
        {
            if( pEnt->isKindOf(AcDbProxyEntity::desc()))
            {        
                proxies.append(pEnt->objectId() );   
            }          
            pEnt->close();    
        }    
    }   
    delete pRecordIter;   
    pRecord->close(); 
}  
  delete pTableIter;
if( Acad::eOk != pTable->upgradeOpen())
{   
    acutPrintf(_T("\nCannot open table for Write"));
    pTable->close();
    return;
}
int nProxies = proxies.length(); 
for( int i=0;i<nProxies; i++ )
{ 
    AcDbProxyEntity* pProxy;  
    AcDbObject* pObj;   
    acdbOpenAcDbObject(pObj, proxies[i], AcDb::kForRead);
    pProxy = AcDbProxyEntity::cast(pObj); 
    if( NULL == pProxy )
    {   
        pObj->close () ;  
        continue; 
    }    
    AcDbVoidPtrArray explodedEnts; 
    pProxy->explode(explodedEnts);
    int nExplodedEnts = explodedEnts.length();
    if( nExplodedEnts > 0 )
    {       
        AcDbBlockTableRecord*pRecord = new AcDbBlockTableRecord();
        pRecord->setName(_T("*B")); 
        AcDbObjectId blockId;   
        pTable->add(blockId, pRecord ); 
        for( int j=0; j<nExplodedEnts; j++)
        {        
            AcDbEntity*pEnt =(AcDbEntity*)(explodedEnts[j]);
            pRecord->appendAcDbEntity(pEnt);
            pEnt->setColorIndex(0);     
            pEnt->close();       
        }      
        pRecord->close(); 
        AcDbBlockTableRecord* pOwningRecord; 
        acdbOpenObject    (   
                            pOwningRecord,
                            pProxy->ownerId(),
                            AcDb::kForWrite
                        ); 
        if( NULL != pOwningRecord)
        {   
            AcDbBlockReference* pRef = new AcDbBlockReference; 
            pRef->setBlockTableRecord(blockId);      
            pOwningRecord->close();       
            pProxy->upgradeOpen();         
            pProxy->handOverTo(pRef); 
            pRef->setColor(pProxy->color()); 
            pRef->setLayer(pProxy->layerId()); 
            pRef->setVisibility(pProxy->visibility());
            delete pProxy;      
            pRef->close();       
        }     
    }     
    else
    { 
        pProxy->close();
    }  
}
pTable->close();

## 评论

**内容**: Henrik said...
Hi Balaji,
I hae such kind of Proxy Entity but I don't know how I have to use this Program.
Could you please give me an advice?
Thanks in advance !
Henrik
Reply
02/10/2016 at 03:39 AM

---
**内容**: Dale Bartlett said...
I know this is old, but is it possible to do the same in .NET?
Reply
02/11/2016 at 01:15 AM

---
**内容**: petcon said...
int nProxies = proxies.length();

for( int i=0;i {
AcDbEntity *pEnt;
AcDbProxyEntity *pProxy;
if (Acad::eOk == acdbOpenObject(pEnt,proxies[i],AcDb::kForWrite))
{
if (pEnt->isKindOf(AcDbProxyEntity::desc()))
{
pProxy = AcDbProxyEntity::cast(pEnt);
AcGePoint3d ptmp;
ptmp.x = 0;
ptmp.y = 0;
ptmp.z = 0;
AcDbPoint *pp = new AcDbPoint(ptmp);
Acad::ErrorStatus es = pProxy->handOverTo(pp);
if (es == Acad::eObjectToBeDeleted)
{
delete pProxy;
pEnt = (AcDbEntity *)pp;
}
pp->erase();
if (i%100 == 0 )
{
acutPrintf(_T("\r共删除PROXY对象%d个\r"),i);
}

pp->close();
}
pEnt->close();
}
}
acutPrintf(_T("\r共删除PROXY对象%d个\r"),nProxies);
pTable->close();
Reply
02/15/2016 at 06:25 PM

---
