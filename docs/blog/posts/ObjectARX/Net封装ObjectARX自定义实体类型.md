---
title: Net封装ObjectARX自定义实体类型
date: 2025-04-07
categories:
  - windows程序
tags:
  - ObjectARX
  - CSharp
description: 使用.NET技术封装ObjectARX自定义实体类型的完整实现方法
author: JerryMa
---

# .Net封装ObjectARX自定义实体类型

[参考Github ManagedCircle](https://github.com/MadhukarMoogala/ManagedCircle)

## 使用ARX自带的向导

### 选择.NET mixed managed code support工程

### 选择OExtension DLL using MFC Shared DLL (recommended for MFC support)

## 将props中关于arx的删除

## 配置信息按照如下所示：

![image-20250407193241272](http://image.mazaiguo.xyz/images/image-20250407193241272.png)

![image-20250407193257438](http://image.mazaiguo.xyz/images/image-20250407193257438.png)

![image-20250407193310752](http://image.mazaiguo.xyz/images/image-20250407193310752.png)

![image-20250407193323409](http://image.mazaiguo.xyz/images/image-20250407193323409.png)

![image-20250407193335187](http://image.mazaiguo.xyz/images/image-20250407193335187.png)

## 关于主代码

![image-20250407193517842](http://image.mazaiguo.xyz/images/image-20250407193517842.png)

`acrxEntryPoint.cpp`

```cpp
//-----------------------------------------------------------------------------
//----- acrxEntryPoint.cpp
//-----------------------------------------------------------------------------
#include "StdAfx.h"
#include "resource.h"
#include "ZwSerialNoMgd.h"

//-----------------------------------------------------------------------------
#define szRDS _RXST("")
AC_DECLARE_EXTENSION_MODULE(MgdWrapperDLL) ;
static AcMgObjectFactoryBase** g_PEs = NULL;

//-----------------------------------------------------------------------------
//----- ObjectARX EntryPoint
class CMgdWrapperApp : public AcRxArxApp {

public:
	CMgdWrapperApp() : AcRxArxApp() {}

	virtual AcRx::AppRetCode On_kInitAppMsg(void *pkt) {
		// TODO: Load dependencies here
		// Save critical data pointers before running the constructors (see afxdllx.h for details)
		AFX_MODULE_STATE* pModuleState = AfxGetModuleState();
		pModuleState->m_pClassInit = pModuleState->m_classList;
		pModuleState->m_pFactoryInit = pModuleState->m_factoryList;
		pModuleState->m_classList.m_pHead = NULL;
		pModuleState->m_factoryList.m_pHead = NULL;

		MgdWrapperDLL.AttachInstance (_hdllInstance) ;
		InitAcUiDLL () ;
		
		// You *must* call On_kInitAppMsg here
		AcRx::AppRetCode retCode = AcRxArxApp::On_kInitAppMsg(pkt);

		// TODO: Add your initialization code here
		AcMgObjectFactoryBase* PEs[] =
		{
			new AcMgObjectFactory<ZDN::CustomWrapper::ZwSerialNoMgd, CZwSerialNo>(),
					NULL
		};

		g_PEs = PEs;
		return (retCode);
	}

	virtual AcRx::AppRetCode On_kUnloadAppMsg(void *pkt) {
		// TODO: Add your code here
		int i = 0;
		while (g_PEs[i] != NULL)
			delete g_PEs[i++];
		// You *must* call On_kUnloadAppMsg here
		AcRx::AppRetCode retCode = AcRxArxApp::On_kUnloadAppMsg(pkt);

		// TODO: Unload dependencies here
		MgdWrapperDLL.DetachInstance () ;

		return (retCode);
	}

	virtual void RegisterServerComponents() {
	}
};

//-----------------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CMgdWrapperApp)
```



![image-20250407193555427](http://image.mazaiguo.xyz//images/20250407-image-20250407193555427.png)

`stdafx.h`

```cpp
#pragma once
#define MGDWRAPPER_MODULE

#pragma pack (push, 8)
#pragma warning(disable: 4786 4996)
//#pragma warning(disable: 4098)

//-----------------------------------------------------------------------------
#define STRICT

#include <sdkddkver.h>

//- ObjectARX and OMF headers needs this
#include <map>

//-----------------------------------------------------------------------------
#include <afxwin.h>				//- MFC core and standard components
#include <afxext.h>				//- MFC extensions
#include <afxcmn.h>				//- MFC support for Windows Common Controls

//-----------------------------------------------------------------------------
#using <mscorlib.dll>
#using <System.dll>

//#using <acdbmgd.dll>
//#using <acmgd.dll>
//#using <AcCui.dll>

#include <vcclr.h>
//-----------------------------------------------------------------------------
#include <afxwin.h>				//- MFC core and standard components
#include <afxext.h>				//- MFC extensions

#ifndef _AFX_NO_OLE_SUPPORT
#include <afxole.h>				//- MFC OLE classes
#include <afxodlgs.h>			//- MFC OLE dialog classes
#include <afxdisp.h>			//- MFC Automation classes
#endif // _AFX_NO_OLE_SUPPORT

#ifndef _AFX_NO_DB_SUPPORT
#include <afxdb.h>				//- MFC ODBC database classes
#endif // _AFX_NO_DB_SUPPORT

#ifndef _AFX_NO_DAO_SUPPORT
#include <afxdao.h>				//- MFC DAO database classes
#endif // _AFX_NO_DAO_SUPPORT

#include <afxdtctl.h>			//- MFC support for Internet Explorer 4 Common Controls
#ifndef _AFX_NO_AFXCMN_SUPPORT
#include <afxcmn.h>				//- MFC support for Windows Common Controls
#endif // _AFX_NO_AFXCMN_SUPPORT
//-----------------------------------------------------------------------------
//- Include ObjectDBX/ObjectARX headers
//- Uncomment one of the following lines to bring a given library in your project.
//#define _BREP_SUPPORT_					//- Support for the BRep API
//#define _HLR_SUPPORT_						//- Support for the Hidden Line Removal API
//#define _AMODELER_SUPPORT_				//- Support for the AModeler API
//#define _ASE_SUPPORT_							//- Support for the ASI/ASE API
//#define _RENDER_SUPPORT_					//- Support for the AutoCAD Render API
//#define _ARX_CUSTOM_DRAG_N_DROP_	//- Support for the ObjectARX Drag'n Drop API
//#define _INC_LEAGACY_HEADERS_			//- Include legacy headers in this project
#include "arxHeaders.h"

#include <afxcview.h>
//-----------------------------------------------------------------------------
#include "DocData.h" //- Your document specific data class holder

//- Declare it as an extern here so that it becomes available in all modules
extern AcApDataManager<CDocData> DocVars ;

#pragma pack (pop)
```

![image-20250407193816704](http://image.mazaiguo.xyz//images/20250407-image-20250407193816704.png)

`ZwSerialNoMgd.h`

```cpp
#pragma once
#include <CZwSerialNo.h>
using namespace System ;
using namespace ZwSoft::ZwCAD::Geometry ;
using namespace  ZwSoft::ZwCAD::DatabaseServices ;
namespace ZDN
{
	namespace CustomWrapper
	{
		[ZwSoft::ZwCAD::Runtime::Wrapper("CZwSerialNo")] 
        public ref class ZwSerialNoMgd
            : public ZwSoft::ZwCAD::DatabaseServices::Entity 
		{
         public:
          //- Constructor
          ZwSerialNoMgd();

        internal:

          ZwSerialNoMgd(System::IntPtr unmanagedPointer, bool bAutoDelete);

          //- Returns the unmanaged ARX Object
          inline CZwSerialNo *GetImpObj() {
            return (static_cast<CZwSerialNo *>(UnmanagedObject.ToPointer()));
          }

         public:
          void SetInsertPt(ZwSoft::ZwCAD::Geometry::Point3d center);
          void setScale(ZwSoft::ZwCAD::Geometry::Scale3d newScale);
          void setDescription(String ^ strDescription);
          void setTag(String ^ strDescription);
          void setValue(String ^ strDescription);
          void setGaugename(String ^ strDescription);
          void setGaugecode(String ^ strDescription);

         /* void setRadius(double radius);
          void gc2AcString(System::String ^ s);*/
          void convertFromMgdObjectId(ZwSoft::ZwCAD::DatabaseServices::ObjectId mgdId);
		};
	}
	
} // namespace ZDN
```

![image-20250407193859988](http://image.mazaiguo.xyz/images/image-20250407193859988.png)

`ZwSerialNoMgd.cpp`

```cpp
#include "StdAfx.h"
#include "ZwSerialNoMgd.h"
#include <gcroot.h>
#include "zmgdinterop.h"

ZDN::CustomWrapper::ZwSerialNoMgd::ZwSerialNoMgd() :
	ZwSoft::ZwCAD::DatabaseServices::Entity((System::IntPtr) new CZwSerialNo(), true)
{}
ZDN::CustomWrapper::ZwSerialNoMgd::ZwSerialNoMgd(System::IntPtr unmanagedPointer, bool bAutoDelete) :
	ZwSoft::ZwCAD::DatabaseServices::Entity(unmanagedPointer, bAutoDelete)
{}
void ZDN::CustomWrapper::ZwSerialNoMgd::SetInsertPt(ZwSoft::ZwCAD::Geometry::Point3d center)
{
	AcGePoint3d _center = GETPOINT3D(center);

	GetImpObj()->SetInsertPt(_center);
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setScale(ZwSoft::ZwCAD::Geometry::Scale3d newScale)
{
	AcGeScale3d _center = GETSCALE3D(newScale);

	GetImpObj()->setScale(_center);
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setDescription(String ^ strDescription)
{
	GetImpObj()->setDescription((LPCTSTR)StringToCIF(strDescription));
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setTag(String ^ strDescription)
{
	GetImpObj()->setTag((LPCTSTR)StringToCIF(strDescription));
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setValue(String ^ strDescription)
{
	GetImpObj()->setValue((LPCTSTR)StringToCIF(strDescription));
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setGaugename(String ^ strDescription)
{
	GetImpObj()->setGaugename((LPCTSTR)StringToCIF(strDescription));
}

void ZDN::CustomWrapper::ZwSerialNoMgd::setGaugecode(String ^ strDescription)
{
    GetImpObj()->setGaugecode((LPCTSTR)StringToCIF(strDescription));
}

void ZDN::CustomWrapper::ZwSerialNoMgd::convertFromMgdObjectId(
	ZwSoft::ZwCAD::DatabaseServices::ObjectId mgdId)
{
	System::String ^ hStr = mgdId.Handle.ToString();
	UInt64     hInt = System::Convert::ToInt64(hStr, 16);
	AcDbHandle handle(hInt);

	AcDbObjectId      objId;
	Acad::ErrorStatus es =
		acdbHostApplicationServices()->workingDatabase()->getAcDbObjectId(objId, false, handle);
	if (es == Acad::eOk)
	{
		acutPrintf(ACRX_T("\nObjectClass from Id : %s"), objId.objectClass()->name());
	}
}
```

![image-20250407193924510](http://image.mazaiguo.xyz/images/image-20250407193924510.png)

## .net中调用

```csharp
 [CommandMethod("TestNo")]
 public void TestNo()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;

     PromptEntityOptions peo = new PromptEntityOptions("\nSelect custom object: ");
     peo.SetRejectMessage("\nInvalid selection...");
     peo.AddAllowedClass(typeof(ZwSerialNoMgd), true);

     PromptEntityResult per = ed.GetEntity(peo);

     if (per.Status != PromptStatus.OK)
         return;

     using (Transaction Tx = db.TransactionManager.StartTransaction())
     {
         ZwSerialNoMgd entity = Tx.GetObject(per.ObjectId, OpenMode.ForWrite)
             as ZwSerialNoMgd;

         entity.ColorIndex = 1;

         Tx.Commit();
     }
 }
```
