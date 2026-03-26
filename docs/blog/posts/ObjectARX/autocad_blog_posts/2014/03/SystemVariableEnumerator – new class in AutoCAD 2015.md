---
title: "SystemVariableEnumerator – new class in AutoCAD 2015"
date: 2014-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "SystemVariableEnumerator class provides a way to iterate over all of the public system variables and get their names, data type, range (if applicab..."
author: Autodesk
---
# SystemVariableEnumerator – new class in AutoCAD 2015

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/systemvariableenumerator-new-class-in-autocad-2015.html

## 文章内容

By Virupaksha Aithal
SystemVariableEnumerator class provides a way to iterate over all of the public system variables and get their names, data type, range (if applicable), read-only status, and how they are stored. In ObjectARX this call is represented by “AcEdSysVarIterator”
  [CommandMethod("SysVarListTest")]
public void SysVarListTest() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      using(SystemVariableEnumerator sysVar
                        = new SystemVariableEnumerator())
    {
        string storage = "";
          while (sysVar.MoveNext())
        {
            Variable var = sysVar.Current;
              switch (var.Storage)
            {
                case Variable.StorageType.PerDatabase:
                    storage = "PerDatabase";
                    break;
                  case Variable.StorageType.PerProfile:
                    storage = "PerProfile";
                    break;
                  case Variable.StorageType.PerSession:
                    storage = "PerSession";
                    break;
                  case Variable.StorageType.PerUser:
                    storage = "PerUser";
                    break;
                  case Variable.StorageType.PerViewport:
                    storage = "PerViewport";
                    break;
            }
              ed.WriteMessage(var.Name + "   " + storage + "\n");
          }
    }
    //use Application.GetSystemVariable() to get the value.
}

