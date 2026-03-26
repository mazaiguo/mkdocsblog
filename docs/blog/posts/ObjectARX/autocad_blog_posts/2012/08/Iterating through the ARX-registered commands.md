---
title: "Iterating through the ARX-registered commands"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "This can achieved by using AcEdCommandIterator to iterate through all the AcEd-registered commands."
author: Autodesk
---
# Iterating through the ARX-registered commands

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/iterating-through-the-arx-registered-commands.html

## 文章内容

By Balaji Ramamoorthy
This can achieved by using AcEdCommandIterator to iterate through all the AcEd-registered commands.
Here is a sample code fragment :
ACHAR cmdLocalName[133];  
ACHAR cmdGlobalName[133];  
ACHAR cmdGroupName[133];
  AcEdCommandIterator *pCmdItr = acedRegCmds->iterator();
if(NULL == pCmdItr) 
    return;
  for(;! pCmdItr->done(); pCmdItr->next())
{       
    wcscpy(cmdGlobalName, pCmdItr->command()->globalName());
    wcscpy(cmdLocalName, pCmdItr->command()->localName());
    wcscpy(cmdGroupName, pCmdItr->commandGroup()); 
    acutPrintf
    (
        ACRX_T("\n    Group name = %s, Local name = %s, Global name = %s"),
        cmdGroupName,
        cmdLocalName,
        cmdGlobalName
    );
}
delete pCmdItr;

