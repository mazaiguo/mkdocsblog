---
title: "AutoCAD command in Managed C++/CLI"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
description: "Here is a very simple example of an AutoCAD command using Managed C++. The buildable project is attached."
author: Autodesk
---
# AutoCAD command in Managed C++/CLI

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/autocad-command-in-managed-ccli.html

## 文章内容

By Balaji Ramamoorthy
Here is a very simple example of an AutoCAD command using Managed C++. The buildable project is attached.
#pragma once
  using namespace System;
using namespace Autodesk::AutoCAD::Runtime;
using namespace Autodesk::AutoCAD::ApplicationServices;
using namespace Autodesk::AutoCAD::EditorInput;
using namespace Autodesk::AutoCAD::DatabaseServices;
  namespace MgdCpp
{
    public ref class MyClass
    {
        public:
          MyClass()
        {
        }
          [CommandMethod("MyCommand")]
        static void MyCommand()
        {
            DocumentCollection ^ docMgr
                    = Application::DocumentManager;
            Document ^ doc
                    = docMgr->MdiActiveDocument;
            Database ^ db
                    = doc->Database;
            Editor ^ ed = doc->Editor;
              PromptEntityResult ^per
                    = ed->GetEntity("Select an entity : ");
            if (per->Status != PromptStatus::OK)
                return;
              ObjectId oid = per->ObjectId;
              Transaction ^tr
                = db->TransactionManager->StartTransaction();
              Entity ^ent
                = (Entity ^)tr->GetObject(oid, OpenMode::ForRead);
              ed->WriteMessage(ent->GetRXClass()->Name);
              tr->Commit();
            tr->~Transaction();
        }
    };
}
  [assembly: CommandClass(MgdCpp::MyClass::typeid)];
Download MgdCpp

