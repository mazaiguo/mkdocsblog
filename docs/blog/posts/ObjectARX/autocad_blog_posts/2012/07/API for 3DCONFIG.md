---
title: "API for 3DCONFIG"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
description: "I know I can use the command line version of 3DCONFIG to change graphics settings using e.g. SendStringToExecute(). However, I'm wondering if it's ..."
author: Autodesk
---
# API for 3DCONFIG

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/api-for-3dconfig.html

## 文章内容

By Adam Nagy
I know I can use the command line version of 3DCONFIG to change graphics settings using e.g. SendStringToExecute(). However, I'm wondering if it's also possible through some direct API.
Solution
Yes, you can access these settings through the AcGsConfig class.
This ARX sample command toggles the Hardware Acceleration setting:
static void ToggleHWAcceleration(void)
{
  AcGsConfig * gsConf =
    acgsGetGsManager()->getGSClassFactory()->getConfig();
  bool b = gsConf->isFeatureEnabled(AcGsConfig::kHwAcceleration);
  gsConf->setFeatureEnabled(AcGsConfig::kHwAcceleration, !b);
  gsConf->saveSettings();
}
The same in .NET:
[CommandMethod("ToggleHWAcceleration")]
public void ToggleHWAcceleration()
{
  using (Autodesk.AutoCAD.GraphicsSystem.Configuration config =
    new Autodesk.AutoCAD.GraphicsSystem.Configuration())
  {
    bool b = config.IsFeatureEnabled(
      Autodesk.AutoCAD.GraphicsSystem.
      HardwareFeature.HardwareAcceleration);
    config.SetFeatureEnabled(
      Autodesk.AutoCAD.GraphicsSystem.
      HardwareFeature.HardwareAcceleration, !b);
    config.SaveSettings();
  }
}

## 评论

**内容**: BJHuffine said...
In AutoCAD 2015, there's evidently been a graphics change and this construct has changed. To be honest, what is the UniqueString object and how is it typically used? And, how should this look with the new construct?
Reply
03/18/2015 at 04:56 AM

---
**内容**: Balaji said...
Hi Jason,
This should work in AutoCAD 2015 :
AcGsKernelDescriptor descriptor;
descriptor.addRequirement(AcGsKernelDescriptor::k3DDrawing);
AcGsGraphicsKernel *pGraphicsKernel = AcGsManager::acquireGraphicsKernel(descriptor);
AcGsConfig * gsConf = pGraphicsKernel->getConfig();
gsConf->setHardwareAcceleration(false); // or true
About UniqueString, it helps do a quick string comparison as it involves direct pointer comparison rather than a character comparison. It works just like enums and you would need to get the pointer to a AcUniqueString.
For example, here is a code snippet to get the uniquestring :
AcArray *effectLists = gsConf->getEffectList(AcGsConfig::EffectListType::kEL_Current);
for (int i = 0 ; i < effectLists->length(); ++ i)
{
const AcGsConfig::EffectStatus & effectStatus = effectLists->at(i);
acutPrintf(effectStatus.effectName);
const AcUniqueString *pUniqueString = effectStatus.pUniqueString;
}
Regards,
Balaji
Reply
03/18/2015 at 11:16 PM

---
**内容**: Balaji said in reply to Balaji...
Just an update to the above code snippet :
It is also required to release the graphics kernel using
AcGsManager::releaseGraphicsKernel(pGraphicsKernel);
Cheers,
Balaji
Reply
03/24/2015 at 11:24 PM

---
