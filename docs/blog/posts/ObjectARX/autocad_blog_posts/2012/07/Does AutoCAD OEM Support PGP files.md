---
title: "Does AutoCAD OEM Support PGP files"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "Does AutoCAD OEM support shortcut key aliases defined in a PGP file?"
author: Autodesk
---
# Does AutoCAD OEM Support PGP files

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/does-autocad-oem-support-pgp-files.html

## 文章内容

by Fenton Webb
Issue
Does AutoCAD OEM support shortcut key aliases defined in a PGP file?
Solution
The PGP command alias definition file is supported by AutoCAD OEM.
You just have to make sure that the PGP file is the same name as the generated OEM master exe. For example a PGP file used with the OEM tutorial would be named poly.pgp and located in the support directory. It would need to have aliases defined that run commands that have been enabled.

If you try to run commands defined by shortcuts defined in the PGP, the alias is used to run the command, however if the command has not been enabled for the OEM product, the "Unknown command" message will be displayed on the command line.

