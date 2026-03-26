---
title: "Commands defined in an ARX module don't show up in my OEM product"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - OEM
description: "I've defined several commands in an ARX module, but when I load it into my OEM product none of them appear as callable commands. What's going wrong?"
author: Autodesk
---
# Commands defined in an ARX module don't show up in my OEM product

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/commands-defined-in-an-arx-module-dont-show-up-in-my-oem-product.html

## 文章内容

by Fenton Webb
Issue
I've defined several commands in an ARX module, but when I load it into my OEM product none of them appear as callable commands. What's going wrong?
Solution
This most likely caused by not specifying the commands on the "Your Commands" tab in the OEM Make Wizard. If the command doesn't appear in the list, OEM will not allow it to be registered, and you will not be able to use it in your product.
To fix this, add the command name to the list on the "Your Commands" tab in the OEM Make Wizard, or make sure the command is spelled properly, then rebuild your product's resources to incorporate the new command list. You should now see the commands.
Be sure to check how the commands should be defined, this is documented in the OEM Developers Guide (oemdev.chm) under the section Your Module Settings Page

