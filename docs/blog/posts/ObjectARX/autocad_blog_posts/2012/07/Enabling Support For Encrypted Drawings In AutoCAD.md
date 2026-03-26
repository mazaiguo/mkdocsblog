---
title: "Enabling Support For Encrypted Drawings In AutoCAD"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - DWG
  - Database
description: "How can I access drawing encryption feature with the ObjectARX API ?"
author: Autodesk
---
# Enabling Support For Encrypted Drawings In AutoCAD

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/enabling-support-for-encrypted-drawings-in-autocad.html

## 文章内容

By Philippe Leefsma
Q:
  How can I access drawing encryption feature with the ObjectARX API ?
A:
ObjectARX  API support for drawing encryption is provided with optional password arguments to the following functions:
  AcDbDatabase::readDwgFile()
AcDbDatabase::saveAs()
acedSyncFileOpen()
acedXrefAttach()
  For access to drawings that already contain encryption, readDwgFile, acedSyncFileOpen and acedXrefAttach provide an optional password argument, which is passed as a wide character wchar_t. 
  To explicitly create encrypted drawings, AcDbDatabase::saveAs() provides an optional SecurityParams struct argument (defined by ObjectARX) which can be used to define the details of the encryption scheme such as encryption provider, encryption type, key length and the access password.  If this argument is NULL, saveAs() will use any default security settings specified with the AcDbDatabase::setSecurityParams() method (which is also defined with the SecurityParams structure).
  The documentation for SecurityParams has information for each item in the struct, but here is an example showing how it might be filled:
  SecurityParams* SetSecurityParams(wchar_t *wszPassword)
{
            SecurityParams *pSecParams=new SecurityParams;
              pSecParams->cbSize=sizeof(SecurityParams);
            pSecParams->ulFlags=SECURITYPARAMS_ENCRYPT_DATA;
  // Must always be this value.
            pSecParams->ulAlgId=SECURITYPARAMS_ALGID_RC4; 
              pSecParams->wszProvName=
                L"Microsoft Base Cryptographic Provider v1.0";
            pSecParams->ulKeyLength=40;
            pSecParams->ulProvType=PROV_RSA_FULL;// Defined in wincrypt.h
            pSecParams->wszCertIssuer=NULL;
            pSecParams->wszCertSerialNum=NULL;
            pSecParams->wszComment=NULL;
            pSecParams->wszPassword=wszPassword;
                       return pSecParams;
}
  Important Note:
  When passwords are specified from within the AutoCAD user interface, they are always converted to upper case.  For the ObjectARX API methods, this is also the case though there is currently a limitation with saveAs() which does NOT convert to an upper-case password.  Therefore it is VERY IMPORTANTthat you convert all passwords to upper-case when passed into AcDbDatabase::saveAs().  If you do not, drawings can be effectively destroyed since they are unopenable with any software.  While this limitation exists, it is generally a good idea to convert all passwords to upper-case before passing them to any ObjectARX APIs.
  It should also be noted that a blank (zero length) password can be passed into AcDbDatabase::saveAs(), however AutoCAD password dialogs and all decryption APIs (readDwgFile,acedSyncFileOpen and acedXrefAttach) will fail when passed a blank password.  This is primarily to allow scripts or batch processes to fail silently when encountering a drawing which is encrypted (see Drawing Security Considerations in the ObjectARX Developers Guide for details).
  Two other basic APIs support password protection.  acedSyncFileOpen() and acedXrefAttach().  These two APIs simply take a wide password string, and return an error status reflecting their success. acedSyncFileOpen() is used to synchronously open a document in AutoCAD, but only works in SDI mode.  The MDI equivalent appContextOpenDocument() method doesnt take a password parameter, so another approach must be taken.  Normally opening any encrypted drawing with this API would invoke the password prompt in AutoCAD.  We can avoid this by caching our password first with a call to readDwgFile().  Example:
  // cache szPassword within ObjectDBX to avoid the automatic password
// dialog after the call to appContextOpenDocument().
  AcDbDatabase *pDb=new AcDbDatabase(false,true);
Acad::ErrorStatus es=pDb->readDwgFile(
res.resval.rstring,
_SH_DENYWR,
false,
convertToWide(szPassword)
);
delete pDb;
  if(Acad::eOk!=acDocManager->appContextOpenDocument(res.resval.rstring))
AfxMessageBox(L"MDI Open Failed");
  For all the encryption enabled APIs an error status is returned which represents the success of the call. For encryption support, there are a few error status values that have been added.  They are defined starting at 1001 in the Acad::ErrorStatus enum defined in acadstrc.h, and all begin with eSec 
  For APIs used to access files that already contain encryption, an eSecErrorDecryptingData error status is returned for a blank or incorrect password.  For the saveAs(), errors within the SecurityParams structure passed will cause an eSecErrorEncryptingData return value.
  The attached cpp file contains some ARX code which demonstrates many of the encryption topics.  It defines three commands; READDWG, SAVEDWG and OPENDWG.  READDWG will use the AcDbDatabase::readDwgFile() to read an encrypted file. SAVEDWG shows how to populate a SecurityParams structure to create an encrypted drawing file. OPENDWG uses either acedSyncFileOpen or appContextOpenDocument() depending on the SDI setting to open a drawing in the AutoCAD editor.  Each of these commands use the custom function acedGetPassword() which prompts the user for a password on the commandline, blanking the password characters with '*' for privacy.   
  DwgSecurityApi.cpp

