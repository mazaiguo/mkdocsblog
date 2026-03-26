---
title: "Creating a Mixed Mode RealDWG Application"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - DWG
  - Database
description: "If you are a seasoned RealDWG developer, you will have probably noticed that the .NET version of the RealDWG SDK’s HostApplicationServices object d..."
author: Autodesk
---
# Creating a Mixed Mode RealDWG Application

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/creating-a-mixed-mode-realdwg-application.html

## 文章内容

by Fenton Webb
If you are a seasoned RealDWG developer, you will have probably noticed that the .NET version of the RealDWG SDK’s HostApplicationServices object does not implement all of the virtual functions that are exposed by its unmanaged ObjectDBX counterpart, AcDbHostApplicationServices.
For the most part, this is a good idea because it simplifies your RealDWG application immensely.
The problem is that sometimes, just sometimes, you really need the full power of the SDK. If you do need that power from .NET then you are going to need to implement a Mixed Mode RealDWG app – one that implements both an underlying unmanaged AcDbHostApplicationServices derived class and a managed HostApplicationServices class that feeds off of it.
So in this example, I simply want to override AcDbHostApplicationServices::fatalError() with my own implementation. This is because the default implementation simply calls Exit( 0 ) which in my case is bad because I want to process many DWG files without failure. If I did not override this function, my RealDWG app would simply exit out and not finish.
Here’s the RealDWG .NET code I want to use… Ok, it’s not scanning lots of DWG files but you get the idea… Remember, I want an exception to be thrown when RealDWG encounters a corrupted DWG file rather than calling Exit( 0 )…
Imports Autodesk.AutoCAD.DatabaseServices
Imports System.Windows.Forms
  ' by Fenton Webb, DevTech, Autodesk 30/04/2010
Public Class SimpleSampleDBXEngine
  Shared Sub Main()
    ' init the undelying CLI C++ HostApplication
    Using app As AdskDBXEngine = New AdskDBXEngine
        For i As Integer = 0 To 100
        Try
          ' new the database making sure to dispose it once we are finished, using/end using
          Using db As New Database(False, True)
            ' read some drawing tile
            db.ReadDwgFile("d:\wutemp\fatal.dwg", FileOpenMode.OpenForReadAndAllShare, False, Nothing)
            ' set the working database via our DbxExtender
            DevTech.DbxExtender.Utils.SetWorkingDatabase(db)
            End Using
        Catch ex As Exception
            MessageBox.Show(ex.Message)
          End Try
      Next
      End Using
  End Sub 
End Class
  I’m going to implement my own unmanaged AcDbHostApplicationServices, but I still need to create .NET HostApplicationServices class which my .NET code can use… it’s implemented but not Initialize()’d – basically it’s a dummy HostApplicationServices object…
Imports Autodesk.AutoCAD
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
  ' by Fenton Webb, DevTech, Autodesk 30/04/2010
'this host app should never be called. It will be replaced by DevTech.DbxExtender.Utils.Initialize()
Public Class DummyHost
  Inherits HostApplicationServices
    Public Overrides Function FindFile(ByVal fileName As String, ByVal database As Autodesk.AutoCAD.DatabaseServices.Database, ByVal hint As Autodesk.AutoCAD.DatabaseServices.FindFileHint) As String
    FindFile = Nothing
  End Function
End Class
  Public Class AdskDBXEngine
  Implements IDisposable
    Public Sub New()
      ' create a new database
    Try
      Dim host As New DummyHost
      RuntimeSystem.Initialize(host, 1033)
      GC.KeepAlive(host)
      DevTech.DbxExtender.Utils.Initialize()
      Catch ex As Exception
      Throw New Exception("Error creating new database")
    End Try
  End Sub
    Public Sub Dispose() Implements IDisposable.Dispose
    DevTech.DbxExtender.Utils.Terminate()
  End Sub
End Class
  Now into an unmanaged C++ DBX module… Here’s my C++ implementation of my custom AcDbHostApplicationServices object…
//////////////////////////////////////////////////////////////////////////
// by Fenton Webb, DevTech, Autodesk 30/04/2010
//-----------------------------------------------------------------------------
//----- HostApplicationServices.cpp
//-----------------------------------------------------------------------------
#include "StdAfx.h"
#include "HostApplicationServices.h"
#include "Wininet.h"
#include "Shlwapi.h"
  //////////////////////////////////////////////////////////////////////////
#pragma unmanaged
  //////////////////////////////////////////////////////////////////////////////
HostApplication::HostApplication()   
{
}
//////////////////////////////////////////////////////////////////////////////
HostApplication::~HostApplication()
{
 CString local,url;
 for (POSITION pos = m_localToUrl.GetStartPosition();pos!=NULL;)
{
  m_localToUrl.GetNextAssoc(pos,local,url);
  DeleteUrlCacheEntry(url);
}
}
//////////////////////////////////////////////////////////////////////////////
// Return the Install directory for customizable files
Acad::ErrorStatus HostApplication::getRoamableRootFolder(const ACHAR*& folder)
{
 Acad::ErrorStatus ret = Acad::eOk;
 static ACHAR buf[MAX_PATH] = _T("\0"); //MDI SAFE
 if (buf[0]==0)
  if (GetModuleFileName(NULL, buf, MAX_PATH) != 0)
   ret = Acad::eRegistryAccessError;
 folder = buf;
 return ret;
}
  //////////////////////////////////////////////////////////////////////////////
// Return the Install directory for customizable files
Acad::ErrorStatus HostApplication::getLocalRootFolder(const ACHAR*& folder)
{
 Acad::ErrorStatus ret = Acad::eOk;
 static ACHAR buf[MAX_PATH] = _T("\0"); //MDI SAFE
 if (buf[0]==0)
  if (GetModuleFileName(NULL, buf, MAX_PATH) != 0)
   ret = Acad::eRegistryAccessError;
 folder = buf;
 return ret;
}
  //////////////////////////////////////////////////////////////////////////////
Acad::ErrorStatus HostApplication::findFile(ACHAR* pcFullPathOut, int nBufferLength,
          const ACHAR* pcFilename, AcDbDatabase* pDb,
          AcDbHostApplicationServices::FindFileHint hint)
{
  ACHAR pExtension[5];
  switch (hint)
  {
  case kCompiledShapeFile:
    _tcscpy(pExtension, _T(".shx"));
    break;
  case kTrueTypeFontFile:
    _tcscpy(pExtension, _T(".ttf"));
    break;
  case kPatternFile:
    _tcscpy(pExtension, _T(".pat"));
    break;
  case kARXApplication:
    _tcscpy(pExtension, _T(".dbx"));
    break;
  case kFontMapFile:
    _tcscpy(pExtension, _T(".fmp"));
    break;
  case kXRefDrawing:
    _tcscpy(pExtension, _T(".dwg"));
    break;
  case kFontFile:                // Fall through.  These could have
  case kEmbeddedImageFile:       // various extensions
  default:
    pExtension[0] = _T('\0');
    break;
  }
  ACHAR* filePart;
  DWORD result;
  ACHAR path[MAX_PATH];
  GetModuleFileName(NULL, path, MAX_PATH);
  PathRemoveFileSpec(path);
  _tcscat(path, _T("\\AutoCADImages"));
    result = SearchPath(path,
    pcFilename, pExtension, nBufferLength, pcFullPathOut, &filePart);
    if (result && result < (DWORD)nBufferLength)
    return Acad::eOk;
  else
      return Acad::eFileNotFound;
}
//////////////////////////////////////////////////////////////////////////////
Adesk::Boolean HostApplication::isURL(const ACHAR* pszURL) const
{
 return PathIsURL(pszURL);
}
  //////////////////////////////////////////////////////////////////////////////
Adesk::Boolean HostApplication::isRemoteFile(const ACHAR* pszLocalFile, ACHAR* pszURL) const
{
 CString value;
 if (m_localToUrl.Lookup(pszLocalFile,value))
{
  _tcscpy(pszURL,value);
  return TRUE;
}
 return FALSE;
}
  //////////////////////////////////////////////////////////////////////////////
Acad::ErrorStatus HostApplication::getRemoteFile(const ACHAR* pszURL, ACHAR* pszLocalFile, Adesk::Boolean bIgnoreCache) const
{
 DWORD err = ERROR_FILE_NOT_FOUND;
 if (!bIgnoreCache)
{
  DWORD size = 0;
  if (GetUrlCacheEntryInfo(pszURL,NULL,&size))
   return Acad::eInetFileGenericError; //this shouldn't succeed
  err = GetLastError();
  if (err == ERROR_INSUFFICIENT_BUFFER)
  {
   INTERNET_CACHE_ENTRY_INFO* pCacheEntry = (INTERNET_CACHE_ENTRY_INFO*)malloc(size);
   if (GetUrlCacheEntryInfo(pszURL,pCacheEntry,&size))
   {
    _tcscpy(pszLocalFile,pCacheEntry->lpszLocalFileName);
    m_localToUrl.SetAt(pszLocalFile,pszURL);
    free(pCacheEntry);
    return Acad::eInetOk;
   }
   err = GetLastError();
  }
}
 if (err == ERROR_FILE_NOT_FOUND)
{
  if (SUCCEEDED(URLDownloadToCacheFile(NULL,pszURL,pszLocalFile,_MAX_PATH,0,NULL)))
  {
   m_localToUrl.SetAt(pszLocalFile,pszURL);
   return Acad::eInetOk;
  }
}
 return Acad::eInetFileGenericError;
}
  //////////////////////////////////////////////////////////////////////////////
ACHAR * HostApplication::getAlternateFontName() const
{
  return _T("txt.shx"); //findFile will be called again with this name
}
  //////////////////////////////////////////////////////////////////////////////
void HostApplication::fatalError(const ACHAR *format, ...)
{
  throw Acad::eFileInternalErr;
} 
// Called when an unhandled exception occurs in an arx command or message.
// The EXCEPTION_POINTERS pointer is obtained from the win32 api:
// GetExceptionInformation().
//
//////////////////////////////////////////////////////////////////////////////
void HostApplication::reportUnhandledArxException(const _EXCEPTION_POINTERS *pExcPtrs,
                                         const ACHAR *pAppName)
{
  // might want to send your minidump file back to your company for processing
}
  // The equivalent of ads_usrbrk()
//////////////////////////////////////////////////////////////////////////////
Adesk::Boolean HostApplication::userBreak(bool updCtrlsWhenEnteringIdle) const
{
  throw Acad::eUserBreak;
}
  //////////////////////////////////////////////////////////////////////////////
Now my Mixed Mode acrxEntryPoint()…
//////////////////////////////////////////////////////////////////////////
// by Fenton Webb, DevTech, Autodesk 30/04/2010
//-----------------------------------------------------------------------------
//----- acrxEntryPoint.cpp
//-----------------------------------------------------------------------------
#include "StdAfx.h"
#include "resource.h"
  //-----------------------------------------------------------------------------
#define szRDS _RXST("asdk")
  //-----------------------------------------------------------------------------
//----- ObjectARX EntryPoint
class CDBXExtensionDotNetWrapperApp : public AcRxDbxApp {
  public:
 CDBXExtensionDotNetWrapperApp () : AcRxDbxApp () {}
   virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt) {
  // TODO: Load dependencies here
    // You *must* call On_kInitAppMsg here
  AcRx::AppRetCode retCode =AcRxDbxApp::On_kInitAppMsg (pkt) ;
    return (retCode) ;
}
   virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt) {
  // TODO: Add your code here
    // You *must* call On_kUnloadAppMsg here
  AcRx::AppRetCode retCode =AcRxDbxApp::On_kUnloadAppMsg (pkt) ;
    return (retCode) ;
}
   virtual void RegisterServerComponents () {
}
  } ;
  #pragma unmanaged
#include "HostApplicationServices.h"
//////////////////////////////////////////////////////////////////////////
// native C++ unmanaged set working database handler
Acad::ErrorStatus native_setWorkingDatabase(AcDbDatabase* dwg)
{
 Acad::ErrorStatus es = Acad::eOk;
   // if ok
 if (dwg)
{
     acdbHostApplicationServices()->setWorkingDatabase(dwg);
}
   return es;
}
  //////////////////////////////////////////////////////////////////////////
// native C++ setdhost app
Acad::ErrorStatus native_acdbSetHostApplicationServices(AcDbHostApplicationServices* pHost)
{
    return acdbSetHostApplicationServices(pHost);
}
//-----------------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CDBXExtensionDotNetWrapperApp)
  Almost there… Now for my Mixed Mode Utils header…
    //////////////////////////////////////////////////////////////////////////
// mgDbx.h - by Fenton Webb, DevTech, Autodesk 14/01/2005
//////////////////////////////////////////////////////////////////////////
  #pragma once
  using namespace System;
using namespace Autodesk::AutoCAD::DatabaseServices;
  namespace DevTech
{
 namespace DbxExtender
{
  public ref class Utils
  {
  public:
      static void Initialize();
      static void Terminate();
   static long SetWorkingDatabase(Database ^dwg);
  };
}
}
  Finally, my Mixed Mode utils implementation code…
  // This is the main DLL file.
#include "stdafx.h"
  #include "mgDbx.h"
  //////////////////////////////////////////////////////////////////////////
// by Fenton Webb, DevTech, Autodesk 30/04/2010
//////////////////////////////////////////////////////////////////////////
// switch to using the unmanaged ODBX SDK, we must link with rcexelib.obj to avoid security problems
#pragma unmanaged
#include "HostApplicationServices.h"
//////////////////////////////////////////////////////////////////////////
// native C++ unmanaged hatch handler
extern Acad::ErrorStatus native_setWorkingDatabase(AcDbDatabase* pDb);
// native C++ unmanaged set host app
Acad::ErrorStatus native_acdbSetHostApplicationServices(AcDbHostApplicationServices* pHost);
  // switch back, no need really
#pragma managed
//////////////////////////////////////////////////////////////////////////
  #pragma managed
using namespace Autodesk::AutoCAD::DatabaseServices;
using namespace Autodesk::AutoCAD::Runtime;
  //////////////////////////////////////////////////////////////////////////
// initialise the host application
AcDbHostApplicationServices* gpHostApp = NULL;
void DevTech::DbxExtender::Utils::Initialize()
{
    ASSERT(gpHostApp == NULL);
    ASSERT(acdbHostApplicationServices()!=NULL);
    //replace the host app with our own
    gpHostApp = new HostApplication();
    native_acdbSetHostApplicationServices(gpHostApp);
}
//////////////////////////////////////////////////////////////////////////
void DevTech::DbxExtender::Utils::Terminate()
{
    ASSERT(gpHostApp != NULL);
    delete gpHostApp;
}
//////////////////////////////////////////////////////////////////////////
// set Workingdatabase Util
long DevTech::DbxExtender::Utils::SetWorkingDatabase(Database ^managedDwg)
{
 Acad::ErrorStatus es = Acad::eNullPtr;
   // get the unmanaged pointer
 AcDbDatabase *dwg = static_cast<AcDbDatabase*>(managedDwg->UnmanagedObject.ToPointer());
 // if ok
 if (dwg)
{
  // call the native unmanaged DxfOut
  es = native_setWorkingDatabase(dwg);
}
 return (long)es;
}
  You should know that at the time of writing, this all needs o be done, but we should have this updated in the next few releases.

## 评论

**内容**: Vasant PADHIYAR said...
Where do I find "HostApplicationServices.h" in ObjectARX-2011?
Reply
04/15/2013 at 10:38 PM

---
**内容**: Fenton Webb said...
it's in the inc folder of the ObjectARX SDK.
Reply
04/16/2013 at 09:05 AM

---
