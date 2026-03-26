---
title: "Identifying the group name of a command"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - API
  - Layer
  - Plot
description: "You can use “AcEdCommandIterator:: commandGroup” API class to identify the group name of the command. Below code shows the procedure to identify th..."
author: Autodesk
---
# Identifying the group name of a command

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/identifying-the-group-name-of-a-command.html

## 文章内容

By Virupaksha Aithal
You can use “AcEdCommandIterator:: commandGroup” API class to identify the group name of the command. Below code shows the procedure to identify the command group name of the “layer” command
AcEdCommand *pCmd = acedRegCmds->lookupCmd(_T("LAYER"), true);
  if(pCmd == NULL)
{
    acutPrintf(_T("Unable to find the command\n"));
    return;
}
  AcEdCommandIterator *pCmdItr = acedRegCmds->iterator();
  for(;! pCmdItr->done(); pCmdItr->next())
{
    if(pCmdItr->command() == pCmd)
    {
        acutPrintf(_T("layer command belongs to Group : %s\n"),
                                        pCmdItr->commandGroup());
        break;
    }
}
  delete pCmdItr;

