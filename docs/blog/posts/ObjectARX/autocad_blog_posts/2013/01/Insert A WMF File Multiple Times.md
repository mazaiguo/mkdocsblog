---
title: "Insert A WMF File Multiple Times"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
description: "Unfortunately the only way to insert a metafile is by using acedCommand( RTSTR,"wmfin" .... )"
author: Autodesk
---
# Insert A WMF File Multiple Times

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/insert-a-wmf-file-multiple-times.html

## 文章内容

By Augusto Goncalves
Unfortunately the only way to insert a metafile is by using acedCommand( RTSTR,"_wmfin" .... )
This means that for the first time you have to create the block definition and the first insert of the metafile using acedCommand() and after this you can insert additional references which point to the previously inserted block definition.
In order to do this after calling acedCommand( RTSTR, "_wmfin" .... ) you have to get the last entity using acdbEntlast(). This will return the AcDbBlockReference which points to the AcDbBlockTableRecord containing the newly inserted WMF file.
You can get the ObjectId of this block table record by calling AcDbBlockReference::blockTableRecord().
Now you can add more AcDbBlockReferences to your drawing and set them to point to the inserted WMF by calling AcDbBlockReferences::setBlockTableRecord.
You can get the size of the inserted metafile using the getGeomExtents() function of the block reference. The sample below demonstrates this.
void InsertWMF()
{
  struct resbuf buf,oldbuf;
  acedGetVar(_T("filedia"), &oldbuf );
  buf.restype = RTSHORT;
  buf.resval.rint = 0;
  buf.rbnext = NULL;
  acedSetVar(_T("filedia"), &buf );
  ACHAR A_WmfFile[] = _T("c:\\temp\\t.wmf");
  ads_point point1 = { 0,0,0 };
  acedCommand(RTSTR,_T("_wmfin"),RTSTR,A_WmfFile,
    RT3DPOINT,point1,RTSTR,"",RTSTR,"", RTREAL, 0,0,RTNONE);
  acedSetVar (_T("filedia"), &oldbuf );
    ads_name name;
  AcDbObjectId objId;
  acdbEntLast( name );
  acdbGetObjectId ( objId, name );
    AcDbBlockReference *pRef;
  AcDbExtents extents;
  acdbOpenObject ( pRef, objId, AcDb::kForRead );
  objId = pRef->blockTableRecord();
  pRef->close();
    //Get the size of the insert 
  pRef->getGeomExtents (extents);
  pRef->close();
  //Use AcDbExtents member functions to get bounding box corners
  AcGePoint3d pt;
  pt = extents.maxPoint();
  pt = extents.minPoint();
    //Create a new insert
  pRef =new AcDbBlockReference ;
  pRef->setBlockTableRecord ( objId );
  pRef->setPosition ( AcGePoint3d ( 1.0, 1.0, 0.0) ) ;
  postToDb ( pRef, objId );
}
NOTE: In the case that the wmf insert is rotated, getGeomExtents() will NOT return an accurate size. Please check also this post which describes a way to make a good approximation of a "tight" bounding box for such cases.
Below is the commonly used postToDb method.
Acad::ErrorStatus postToDb(AcDbEntity* ent, AcDbObjectId& objId)
{
  Acad::ErrorStatus es; 
  AcDbBlockTable* pBlockTable;
  AcDbBlockTableRecord* pSpaceRecord; 
  if (ent==NULL)
    return Acad::eNullObjectPointer; 
    if ((es = acdbHostApplicationServices()->workingDatabase()->
    getBlockTable(pBlockTable, AcDb::kForRead))!=
    Acad::eOk)
    return es;
  if ((es =
    pBlockTable->getAt(ACDB_MODEL_SPACE,pSpaceRecord,
    AcDb::kForWrite)) != Acad::eOk)
  {      
    pBlockTable->close();  
    return es; 
  } 
  pBlockTable->close();
  if ((es = pSpaceRecord->appendAcDbEntity(objId, ent))
    != Acad::eOk) {
    pSpaceRecord->close();
    return es;
  }
  pSpaceRecord->close();
  return ent->close(); 
}

