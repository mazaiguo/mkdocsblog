---
title: "Aligning of Mtext entities one above the other"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "The following code asks the user to select two MText entities and a new alignment point, and then modifies both to be aligned as you describe. The ..."
author: Autodesk
---
# Aligning of Mtext entities one above the other

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/aligning-of-mtext-entities-one-above-the-other.html

## 文章内容

By Gopinath Taget
The following code asks the user to select two MText entities and a new alignment point, and then modifies both to be aligned as you describe. The functions you need to be aware of are:
Acad::ErrorStatus AcDbMText::setLocation (const AcGePoint3d& loc) ;
Acad::ErrorStatus AcDbMText::setAttachment (AttachmentPoint type) ;
  Here is the code:
  int alignmtexts ()
{
 // TODO: Implement the command
resbuf *pArg =acedGetArgs ();
ads_name ent1, ent2;ads_point pt;
 if ( RTNORM != acedEntSel(L"\nSelect first MText entity: ", ent1, pt))
{
  return RTNORM;
}
 if (RTNORM != acedEntSel(L"\nSelect second MText entity: ", ent2, pt))
{
  return RTNORM;
}
AcGePoint3d newPt;
 if ( RTNORM != acedGetPoint(NULL, _T("\nSelect new alignment point:"),asDblArray (newPt)));
{
  return RTNORM;
}
AcDbObjectId objId1, objId2;
 if ( Acad::eOk != acdbGetObjectId( objId1, ent1 ))
{
  acutPrintf(L"\nCannot get object ID for first entity!" );
  return RTNORM;
}
 if ( Acad::eOk != acdbGetObjectId( objId2, ent2 ))
{
  acutPrintf( L"\nCannot get object ID for second entity!" );
  return RTNORM;
}
AcDbObject *pObj1 = NULL, *pObj2 = NULL;
 if ( Acad::eOk != acdbOpenAcDbObject( pObj1, objId1, AcDb::kForRead ))
{
  acutPrintf(L"\nCannot open first entity!" );
  return RTNORM;
}
 if ( Acad::eOk != acdbOpenAcDbObject( pObj2, objId2, AcDb::kForRead ))
{
  acutPrintf (L"\nCannot open second entity!" );
  pObj1->close();
  return RTNORM;
}
AcDbMText *pMText1 = NULL, *pMText2 = NULL;
 if ( NULL == ( pMText1 = AcDbMText::cast( pObj1 )))
{
  acutPrintf(L"\nFirst entity is not an MText object!" );
  pObj1->close(); pObj2->close();
  return RTNORM;
}
 if ( NULL == ( pMText2 = AcDbMText::cast( pObj2 )))
{
  acutPrintf( L"\nSecond entity is not an MText object!" );
  pMText1->close(); pObj2->close();
  return RTNORM;
}
 if ( Acad::eOk != pMText1->upgradeOpen())
{
  acutPrintf(L"\nCannot upgrade open status of first entity!" );
  pMText1->close(); pMText2->close();
  return RTNORM;
}
 if ( Acad::eOk != pMText1->setLocation( newPt ))
{
  acutPrintf( L"\nCannot change location of first entity!" );
  pMText1->close(); pMText2->close();
  return RTNORM;
}
 if ( Acad::eOk != pMText1->setAttachment( AcDbMText::kBottomLeft ))
{
  acutPrintf( L"\nCannot change attachment point of first entity!");
  pMText1->close(); pMText2->close();
  return RTNORM;
}
pMText1->close();
 if ( Acad::eOk != pMText2->upgradeOpen())
{
  acutPrintf(L"\nCannot upgrade open status of second entity!" );
  pMText2->close();
  return RTNORM;
}
 if ( Acad::eOk != pMText2->setLocation( newPt ))
{
  acutPrintf( L"\nCannot change location of first entity!" );
  pMText2->close();
  return RTNORM;
}
 if ( Acad::eOk != pMText2->setAttachment( AcDbMText::kTopLeft ))
{
  acutPrintf( L"\nCannot change attachment point of first entity!");
  pMText2->close();
  return RTNORM;
}
pMText2->close();
 return RTNORM;
}

