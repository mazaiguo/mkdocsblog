---
title: "Retrieving entity properties using AccoreConsole"
date: 2015-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Plugin
description: "The "dumpallproperties" is an easy way to list all the properties of an entity using Lisp. Unfortunately, this does not work when used in the scrip..."
author: Autodesk
---
# Retrieving entity properties using AccoreConsole

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/retrieving-entity-properties-using-accoreconsole.html

## 文章内容

By Balaji Ramamoorthy
The "dumpallproperties" is an easy way to list all the properties of an entity using Lisp. Unfortunately, this does not work when used in the script file along with AccoreConsole. A simple way to workaround this and display the entity properties in AccoreConsole, is to create a CRX plugin that uses the Non-COM property system to display the entity properties. 
If you are new to the Non-COM property system, please refer to this blog post : DevTV : Non-COM Property System
The code in this blog post uses portions of the code from that DevTV in a CRX application. Here is the relevant code and the complete sample project can be downloaded here :
Download EntProps_CRX
 static  void  ListEntityProperties(void )
 {
  TCHAR entityHandle[133];
  if  (acedGetString(
   Adesk::kFalse, 
   _T("\\nEnter entity handle : " ), 
   entityHandle) != RTNORM)
  {
   acutPrintf(ACRX_T("\\nInvalid entity handle." ));
   return ;
  }
  CUtils::DisplayProperties(entityHandle);
 }
   void  initApp() 
 { 
     acedRegCmds->addCommand(ACRX_T("MY_COMMANDS" ), 
                             ACRX_T("EntProps" ), 
                             ACRX_T("EntProps" ), 
                             ACRX_CMD_TRANSPARENT, 
                             ListEntityProperties); 
 } 
   #include  "rxmember.h" 
 #include  "rxvaluetype.h" 
 #include  "rxattrib.h" 
 #include  "rxprop.h" 
 #include  "dbobjptr.h" 
   // Utils.cpp 
 void  CUtils::DisplayProperties(LPCTSTR handleStr)
 {
  Acad::ErrorStatus es;
  AcApDocument *pActiveDoc 
   = acDocManager->mdiActiveDocument();
  AcDbDatabase *pDB = pActiveDoc->database();
    AcDbObjectId id = AcDbObjectId::kNull;
  AcDbHandle objHandle(handleStr);
     es = pDB->getAcDbObjectId(id, false , objHandle);
     if  (es != Acad::eOk) 
  {
         acutPrintf(
   _T("\\nCould not translate handle to objectId" ));
     }
    AcDbObjectPointer<AcDbEntity> entity(id, AcDb::kForRead);
    AcRxMemberIterator * iter = 
   AcRxMemberQueryEngine::theEngine()->newMemberIterator
   (entity);   
    for  (; !iter->done(); iter->next())
  {
   printValues(entity, iter->current());
  }
 }
   void  CUtils::getAttInfo(
  const  AcRxAttribute * att, 
  const  AcRxObject * member, 
  AcString & attInfo)
 {
  if  (att->isA() == AcRxCOMAttribute::desc())
  {
   AcRxCOMAttribute * a = AcRxCOMAttribute::cast(att);
   attInfo.format(_T("\\n%s - %s" ), 
    att->isA()->name(), a->name()); 
  }
  else  if  (att->isA() == AcRxUiPlacementAttribute::desc())
  {
   AcRxUiPlacementAttribute * a 
    = AcRxUiPlacementAttribute::cast(att);
   attInfo.format(
   _T("\\n%s - %s - %f" ), 
   att->isA()->name(), 
   a->getCategory(member),
   a->getWeight(member)); 
  }
  else 
  {
   attInfo.format(_T("\\n%s" ), att->isA()->name()); 
  }
 }
   void  CUtils::printValues(
  AcRxObject * entity, 
  const  AcRxMember * member)
 {
  Acad::ErrorStatus err = Acad::eOk;
    AcString strValue;
  AcRxProperty * prop = AcRxProperty::cast(member);
  if  (prop != NULL)
  {
   AcRxValue value;
     if  ((err = prop->getValue(entity, value)) 
    == Acad::eOk) 
   {
    ACHAR * szValue = NULL;
      int  buffSize = value.toString(NULL, 0);
    if  (buffSize > 0)
    {
     buffSize++;
     szValue = new  ACHAR[buffSize];
     value.toString(szValue, buffSize);
    }
      strValue.format(
     _T("%s = %s" ), 
     value.type().name(), 
     (szValue == NULL) ? _T("none" ) : szValue);  
      if  (szValue)
     delete  szValue;
   }
   else 
   {
    strValue.format(_T("Error Code = %d" ), err);
   }
  }
    AcString str;
  str.format(_T("\\n%s - %s [%s]" ), member->isA()->name(), 
   member->name(), strValue.kACharPtr());
  acutPrintf(str);
    const  AcRxAttributeCollection & atts 
   = member->attributes();
      for  (int  i = 0; i < atts.count(); i++)
  {
   const  AcRxAttribute * att = atts.getAt(i); 
     AcString attInfo;
   getAttInfo(att, member, attInfo);
     acutPrintf(attInfo);
  }
    if  (member->children() != NULL)
  {
   for  (int  i = 0; 
    i < member->children()->length(); i++)
   {
    const  AcRxMember * subMember 
     = member->children()->at(i);
    printValues(entity, subMember);  
   }
  }
 }
  The CRX plugin exposes the "EntProps" command which requires handle of the entity for which the properties are to be retrieved as its input.
Here is a sample script file to load the crx and invoke "EntProps" command.
(arxload "D:\\Temp\\CrxTest1.crx")
EntProps
4C4   ;; Handle of the entity for which properties are to be displayed

