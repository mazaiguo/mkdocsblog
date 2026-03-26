---
title: "Zoom & Center to a Lat / Lon location using Autodesk Design Review API"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - API
  - Dimension
  - Unicode
description: "In Autodesk Design Review using the “Center to Coordinates” UI tool we can set the center for a Map to a specific coordinate value entered through ..."
author: Autodesk
---
# Zoom & Center to a Lat / Lon location using Autodesk Design Review API

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/zoom-center-to-a-lat-lon-location-using-autodesk-design-review-api.html

## 文章内容

By Partha Sarkar
  In Autodesk Design Review using the “Center to Coordinates” UI tool we can set the center for a Map to a specific coordinate value entered through the User Interface as seen in the screenshot below –
    Using ECompositeViewer.centerToCoordinates(coordType, x, y) we can replicate the above mentioned UI tool command. You need to pass on the correct Lat & Lon values in context to the page you are trying to view, e.g.
dwfView.centerToCoordinates(2, -12.562387, 131.073166) // Lat & Lon values should be correct to view and zoom to your dataset
Note that, to use this API, sections in the DWF must contain Georeferenced properties.
This API can be used in a URL to open a DWF with a Map section and Center the view to the coordinates provided. However, when used as part of a URL the coordinates must be within the section that is being viewed.

