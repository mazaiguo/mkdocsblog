---
title: "Resetting current color when a different layer is set as current"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
description: "Setting the current color using the CECOLOR system variable helps create entities with a certain color irrespective of the color of the current lay..."
author: Autodesk
---
# Resetting current color when a different layer is set as current

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/resetting-current-color-when-a-different-layer-is-set-as-current.html

## 文章内容

By Balaji Ramamoorthy
Setting the current color using the CECOLOR system variable helps create entities with a certain color irrespective of the color of the current layer. But when you set a different layer as current, you may want to the layer color to take effect.
So, How do I automatically change the current color to BYLAYER if the user changes the layer?
The current color can be set by AcDbDatabase::setCecolor(). You will be notified of system variable changes if you plant your own AcEditorReactor and override the member function sysVarChanged(). The system variable for the current layer is CLAYER.
class MyEditorReactor : public AcEditorReactor
{
    public:
       void sysVarChanged(const ACHAR* varName, Adesk::Boolean success);
};
  MyEditorReactor *pReactor = NULL;
  /*
* Set the current color
*/
void setCurColor(int index)
{
   AcCmColor color;
   color.setColorIndex(index);
   acdbHostApplicationServices()->workingDatabase()->setCecolor(color);
}
  /*
* System variable changed
*/
void MyEditorReactor::sysVarChanged(const ACHAR* varName, Adesk::Boolean
success)
{
   if(success)
   {
    // change the current color to "ByLayer" if the layer
    // was changed
    if(!_tcscmp(L"CLAYER",varName))
        setCurColor(256);
   }
}
  void initApp()
{
    pReactor  = new MyEditorReactor;
    if(pReactor)
        acedEditor->addReactor(pReactor);
}
  void unloadApp()
{
    if(pReactor)
        acedEditor->removeReactor(pReactor);
}

## 评论

**内容**: sean said...
what about changing objects colors when printing so cadd users can use their internal habitual colors but print using another companies ctb file. In other words, every object that is green (bylayer or byentity) upon print command changes to red (for instance) then changes back to green. This way a user can map their colors to an outside companies colors for plotting due to ctb file differences. Application could compare ctb files or just have a manual lookup table saved in a txt format. Maybe the option to convert colors permanently for digital dwg delivery.
Time for me to learn arx maybe?
Reply
01/13/2015 at 05:37 PM

---
