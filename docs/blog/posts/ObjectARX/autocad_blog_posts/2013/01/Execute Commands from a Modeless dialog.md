---
title: "Execute Commands from a Modeless dialog"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
description: "As a modeless dialog in AutoCAD application run on session, we cannot execute commands, so below is a list of alternatives:"
author: Autodesk
---
# Execute Commands from a Modeless dialog

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/execute-commands-from-a-modeless-dialog.html

## 文章内容

By Augusto Goncalves
As a modeless dialog in AutoCAD application run on session, we cannot execute commands, so below is a list of alternatives:
1. Use the function AcApDocManager::sendStringToExecute() (ensure one escape (ASCII 27) characters down first before the real string, this will cancel any previous running commands, if any).
2. Simulate menu selection by sending WM_COMMAND rather than WM_CHAR messages. Once the command is active you can then, of course, send WM_CHAR messages for the parameters. This would then only call commands that exist in the menu structure (though they could hidden/deeply nested).
3. Use the function int acedPostCommand(const ACHAR*) to send characters command-prompt.
4. Use the function int ads_queueexpr(const ACHAR *) to again send characters to the command prompt.

