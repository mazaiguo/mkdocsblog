---
title: "Linking from one off-page connector to the other in Plant3d P&ID"
date: 2013-05-01
categories:
  - Plant 3D
tags:
  - API
  - Plant 3D
description: "If you want to obtain an id or reference to an off-page connector that is linked to a given off-page connector using the API then…"
author: Autodesk
---
# Linking from one off-page connector to the other in Plant3d P&ID

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/linking-from-one-off-page-connector-to-the-other-in-plant3d-pid.html

## 文章内容

by Fenton Webb
If you want to obtain an id or reference to an off-page connector that is linked to a given off-page connector using the API then…
For the 2013 Plant3d SDK
Use the DataLinksManager.GetRelatedAcPpObjectIds(), GetRelatedRowIds() using “ConnectorsRelationship” as the relationship name and “Connector1”, “Connector2” as the role names. Relationships of this nature have to be checked using both roles.
For the 2014 Plant3d SDK
Use the OffpageConnectionManager. If has methods such as: IsConnected(), GetConnectedPpId(), GetConnectedRowId().

