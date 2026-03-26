---
title: "Getting the state of certain modeless windows"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "To know if certain modeless windows such as the Properties Window, DesignCenter, and DbConnect windows are currently displayed in an AutoCAD sessio..."
author: Autodesk
---
# Getting the state of certain modeless windows

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/getting-the-state-of-certain-modeless-windows.html

## 文章内容

By Balaji Ramamoorthy
To know if certain modeless windows such as the Properties Window, DesignCenter, and DbConnect windows are currently displayed in an AutoCAD session, there are binary system variable that contain this information.
OPMSTATE - Properties Window
ADCSTATE - AutoCAD Design Center
DBCSTATE - Database Connectivity
All three system variables are set to 1 when the corresponding window is visible, and are set to 0 when not visible. To programmatically control the visibility of these modeless windows, you can send the AutoCAD commands such as "PROPERTIES", "PROPERTIESCLOSE", "ADC", "ADCCLOSE", DBC" and "DBCCLOSE" commands.

