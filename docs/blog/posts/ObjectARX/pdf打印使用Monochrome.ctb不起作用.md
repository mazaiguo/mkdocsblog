---
title: PDF打印使用Monochrome.ctb不起作用
date: 2024-05-18
categories:
  - windows程序
tags:
  - ObjectArx
  - AcDbPlotSettings

description: 解决CAD中PDF打印使用Monochrome.ctb打印样式表不起作用的问题
author: JerryMa
---

# pdf打印使用Monochrome.ctb不起作用

## 设置的plotstyle没起作用，手动打印没有问题

## 

```cpp
//get the active layout
AcDbLayout* pLayout = pLayMan->findLayoutNamed(pLayMan->findActiveLayout(TRUE), TRUE);//获得当前布局
AcDbObjectId  m_layoutId = pLayout->objectId();//获得布局的Id
AcPlPlotInfo plotInfo;
AcDbPlotSettingsValidator* pPSV = acdbHostApplicationServices()->plotSettingsValidator();

plotInfo.setLayout(pLayout->objectId());//必须设置

AcDbPlotSettings* m_pSetting = new AcDbPlotSettings(pLayout->modelType());

m_pSetting->copyFrom(pLayout);
pPSV->refreshLists(m_pSetting);

m_pSetting->setShadePlot(AcDbPlotSettings::kAsDisplayed);
m_pSetting->setShadePlotResLevel(AcDbPlotSettings::kNormal);
m_pSetting->setScaleLineweights(false);
m_pSetting->setPrintLineweights(true);
m_pSetting->setPlotTransparency(false);
m_pSetting->setPlotPlotStyles(true);
m_pSetting->setDrawViewportsFirst(true);

```

缺少`m_pSetting->setPlotPlotStyles(true);`

某些图纸的layout里有数据，没有设置plotstyle信息，需要手动设置

