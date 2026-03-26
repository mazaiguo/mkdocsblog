---
title: "Cast from .NET to COM using Managed C++?"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - COM
description: "After select an object using .NET (Managed C++), how cast to a COM object? First you need to get the IUnknow pointer from AcadObject property, then..."
author: Autodesk
---
# Cast from .NET to COM using Managed C++?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/cast-from-net-to-com-using-managed-c.html

## 文章内容

By Augusto Goncalves
After select an object using .NET (Managed C++), how cast to a COM object? First you need to get the IUnknow pointer from AcadObject property, then cast it to a COM object. This procedure will ensure you maintain COM reference count.
The following code show how do it, also show how get its type name. Keep in mind that this project should be created in Mixed mode.
//get the collection of documents (MDI)
Autodesk::AutoCAD::ApplicationServices::DocumentCollection ^docMgr =
  Autodesk::AutoCAD::ApplicationServices::
  Application::DocumentManager;
//get the active document
Autodesk::AutoCAD::ApplicationServices::Document ^acadDoc =
  docMgr->MdiActiveDocument;
//get the editor
Autodesk::AutoCAD::EditorInput::Editor ^ed = acadDoc->Editor;
  Autodesk::AutoCAD::DatabaseServices::Transaction ^trans;
try
{
  //start a transaction
  trans = acadDoc->Database->TransactionManager->
    StartTransaction();
    //select an entity using .NET
  Autodesk::AutoCAD::EditorInput::PromptEntityResult
    ^promptEntRes = ed->GetEntity(_T("Select an entity: "));
  if (promptEntRes->Status != Autodesk::AutoCAD::
    EditorInput::PromptStatus::OK)
    return;
    //open the entity for read
  Autodesk::AutoCAD::DatabaseServices::Entity ^mgdEntity =
    (Autodesk::AutoCAD::DatabaseServices::Entity^)
    trans->GetObject(promptEntRes->ObjectId,
    Autodesk::AutoCAD::DatabaseServices::OpenMode::ForRead);
    //get the COM object from the .NET object
  System::Object ^acadObj = mgdEntity->AcadObject;
  System::IntPtr ptr = System::Runtime::
    InteropServices::Marshal::GetIUnknownForObject(acadObj);
  IUnknown* iunk = static_cast(ptr.ToPointer());
  CComQIPtr acadEntity = iunk;
  iunk->Release();
    //get the entity name using the COM object
  //it will return something line AcDbLine, AcDbCircle, etc
  CComBSTR entityName;
  acadEntity->get_EntityName(&entityName);
  //if you made the proper cast, such as for IAcadLine,
  //then you can call any other method of this COM object
    //now get the COM interface name of the object
  //it will return something line IAcadLine, IAcadCircle, etc
  CComPtr typeInfo;
  acadEntity->GetTypeInfo(0,LOCALE_SYSTEM_DEFAULT,&typeInfo);
  CComBSTR interfaceName;
  typeInfo->GetDocumentation(-1,&interfaceName, 0,0,0);
    //and print using .NET
  ed->WriteMessage(_T("\nEntity selected: {0} ({1})"),
    gcnew System::String(entityName),
    gcnew System::String(interfaceName));
}
catch(System::Exception^ e)
{
  //something went wrong
  ed->WriteMessage(e->Message);
}
__finally
{
  //dispose the transaction
  trans->~Transaction();
}

## 评论

**内容**: RANJAN said...
I'm looking for the same code in VB.net or C#. Is it something possible ?
Reply
06/21/2015 at 11:07 PM

---
**内容**: Augusto Goncalves said in reply to RANJAN...
From .NET to COM in C#/VB.NET you just need to
VB.NET
Dim myVar as Object = myNETObj.AcadObject
C#
dynamic myVar = myNETObj.AcadObject
And both approaches are using late-binding, but you can replace the actual object type
Regards,
Augusto Goncalves
Reply
06/22/2015 at 04:34 AM

---
