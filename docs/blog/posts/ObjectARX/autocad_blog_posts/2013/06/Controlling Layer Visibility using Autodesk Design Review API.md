---
title: "Controlling Layer Visibility using Autodesk Design Review API"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - API
  - JavaScript
  - Layer
description: "If you want to control the layer visibility of a DWF file embedded in a Web Page using Autodesk Design Review JavaScript API, you can access the La..."
author: Autodesk
---
# Controlling Layer Visibility using Autodesk Design Review API

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/controlling-layer-visibility-using-autodesk-design-review-api.html

## 文章内容

By Partha Sarkar
If you want to control the layer visibility of a DWF file embedded in a Web Page using Autodesk Design Review JavaScript API, you can access the Layers property from the DWF Viewer control object and for a specific layer in the layer list you can set the Visible property to true or false to show that layer or to switch it off.
Here is a relevant JavaScript code snippet – 
function LayerON(){ 

// Switching a Layer ON
// DWFViewer is DwfViewer Object that represents the DWF Viewer control
DWFViewer.Viewer.Layers.Item(2).Visible = true; 

//
}

function LayerOFF(){ 

// Switching a Layer OFF
// DWFViewer is DwfViewer Object that represents the DWF Viewer control
DWFViewer.Viewer.Layers.Item(2).Visible = false;  

}

