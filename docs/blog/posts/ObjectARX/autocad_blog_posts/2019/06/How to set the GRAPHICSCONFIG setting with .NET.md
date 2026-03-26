---
title: "How to set the GRAPHICSCONFIG setting with .NET"
date: 2019-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "You need to use GraphicsSystem.Configuration API to set or unset various effects on graphics system."
author: Autodesk
---
# How to set the GRAPHICSCONFIG setting with .NET

发布日期: 2019-06-01

原始链接: https://adndevblog.typepad.com/autocad/2019/06/how-to-set-the-graphicsconfig-setting-with-net.html

## 文章内容

By Madhukar Moogala
You need to use GraphicsSystem.Configuration API to set or unset various effects on graphics system.
For example this will turn on LineSmoothing
public string[] FeatureName = {

           "ACAD_Configlevel",
           "ACAD_2DRetainModeLevel",
           "ACAD_HQGeom",
           "ACAD_PerPixelLighting",
           "ACAD_AdvancedMaterial",
           "ACAD_FullShadows",
           "ACAD_TextureCompression",
           "ACAD_LineSmoothing",
           "ACAD_LineFading",
           "ACAD_GlowHighlighting",
           "ACAD_2DRetainMode",
           "ACAD_GPULineType",
           "ACAD_GPUHatch"
        };

        [CommandMethod("GSTEST")]
        public void GsConfigTest()
        {
            Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
            using (Autodesk.AutoCAD.GraphicsSystem.Configuration config = new Autodesk.AutoCAD.GraphicsSystem.Configuration())
            {
                if (!config.IsHardwareAccelerationAvailable())
                {
                    Application.ShowAlertDialog("Check your Video Card");
                    return;
                }
                //if we Hardware is available, check if it is enabled else turn on.
                if (!config.IsHardwareAccelerationEnabled())
                {
                    config.setHardwareAcceleration(true);
                }
                foreach (EffectStatus effStatus in config.GetEffectList(EffectListType.kEL_Current))
                {
                    var effectName = effStatus.EffectName;
                    var unqString = effStatus.EffectUniqueString;
                    int featureLevel = effStatus.FeatureLevel;
                    var isEnabled = effStatus.Enabled;
                    ed.WriteMessage($"\n{effectName}\t{featureLevel}\t{isEnabled}"); 
                }
                //Turn on LineSmoothing
                UniqueString featureString = UniqueString.Intern("ACAD_LineSmoothing");
                if (config.IsFeatureAvailable(featureString))
                {
                    if (!config.IsFeatureEnabled(featureString))
                        config.SetFeatureEnabled(featureString, true);

                }
            }
        }

