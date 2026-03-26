---
title: "Changing the Entity Type name that appears in the OPM window"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DXF
  - Palette
  - Polyline
description: "Consider this: If you derive a custom entity from AcDbPolyline, and select an instance of your entity in AutoCAD, OPM displays "Polyline"."
author: Autodesk
---
# Changing the Entity Type name that appears in the OPM window

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/changing-the-entity-type-name-that-appears-in-the-opm-window.html

## 文章内容

By Gopinath Taget
Consider this: If you derive a custom entity from AcDbPolyline, and select an instance of your entity in AutoCAD, OPM displays "Polyline".
So, how can you change the type name that appears in the object properties palette window?
In essence, to change the "Entity Type" title in the OPM Dialog you *have* to use Static Properties. It is Static Properties which define the IOPMPropertyExtension::GetDisplayName(DISPID, BSTR*) function and it's in this function that (when receiving a DISPID of 0x401) you can change the title.
Also, if you were to derive your custom entity from AcDbEntity rather than AcDbPolyline then the OPM "Entity Type" would actually appear as the DXF_NAME in your ACRX_DXF_DEFINE_MEMBERS macro. This is because AcDbPolyline defines it's own Static Properties, and, it's own IOPMPropertyExtension::GetDisplayName which updates the DXF_NAME to "Polyline". You need to override this behavior. Here are some sample snippets:
// define callback for IOPMPropertyExtension so
// that we can display some different headings
STDMETHOD(GetDisplayName) (DISPID dispId, BSTR *propName);
And then in the implementation file do something like this:
STDMETHODIMP CCustomEntProps::GetDisplayName (DISPID dispId,
                                          BSTR *propName)
{
 switch (dispId)
{
  // this is the property name title string
 case (0x01):
  *propName  = ::SysAllocString(L"my Text String");
  break;
  // this changes the title of the entity
 case (0x401):
  *propName  = ::SysAllocString(L"My Heading");
  break;
}
 return S_OK;
}

## 评论

**内容**: Jesse said...
Can you explain this further?
Reply
01/06/2016 at 01:16 PM

---
