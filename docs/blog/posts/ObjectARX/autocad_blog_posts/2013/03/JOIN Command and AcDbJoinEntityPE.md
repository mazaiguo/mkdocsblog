---
title: "JOIN Command and AcDbJoinEntityPE"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
description: "Is is possible to implement AcDbJoinEntityPE extension protocol in my custom entities, so I can handle custom behavior when JOIN command is used on..."
author: Autodesk
---
# JOIN Command and AcDbJoinEntityPE

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/join-command-and-acdbjoinentitype.html

## 文章内容

By Philippe Leefsma
Q:
Is is possible to implement AcDbJoinEntityPE extension protocol in my custom entities, so I can handle custom behavior when JOIN command is used on them?
A:
Unfortunately at the moment the JOIN command will not invoke the AcDbJoinEntityPE protocol on the involved entities. We have a change request logged against the behavior of the JOIN command, but it has not been addressed yet, sorry for the bad news.
Looking at the source code of the JOIN command, it treats each entity type in a different way and performs a static check on the entity type, hence your custom entity won’t be able to be processed by the JOIN command unless you replace it by your own redefined command.
I gave a quick try at a custom entity using my custom AcDbJoinEntityPE and it worked fine on the API side: calling the “AcDbJoinEntityPE::joinEntity” method using the PE returned by my entity is actually calling the custom “joinEntity” method of my defined PE.
The test sample is attached below.
ArxJoinEntityPE.zip

