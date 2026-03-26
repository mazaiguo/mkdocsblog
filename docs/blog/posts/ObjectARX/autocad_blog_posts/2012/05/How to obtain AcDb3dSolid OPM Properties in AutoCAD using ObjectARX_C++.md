---
title: "How to obtain AcDb3dSolid OPM Properties in AutoCAD using ObjectARX/C++"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Solid
description: "Someone just asked me how to obtain the Position, Height, Length, etc. from a 3D Box in AutoCAD. Actually, from a programming point of view, it’s k..."
author: Autodesk
---
# How to obtain AcDb3dSolid OPM Properties in AutoCAD using ObjectARX/C++

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-obtain-acdb3dsolid-opm-properties-in-autocad-using-objectarxc.html

## 文章内容

by Fenton Webb
Someone just asked me how to obtain the Position, Height, Length, etc. from a 3D Box in AutoCAD. Actually, from a programming point of view, it’s kind of involved. The reason is because what we know as a Box, under the hood, is actually a generalized AcDb3dSolid object, generalized meaning that an AcDb3dSolid can also represent a Torus, Sphere, Cone etc., and, because an AcDb3dSolid can be all of these object types (and more, because you can Push, Pull, Union, Boolean and also Subtract these objects into whatever you want) the object properties that are displayed in the Property window of AutoCAD can vary a lot. We achieve this varying property set by means of an AutoCAD COM API known as Dynamic properties. We also have a slightly different version known as Static properties.
Dynamic Properties can be created on the fly, whereby Static properties are “hard coded” (easiest way to describe) into the object. I should also mention that we have two types of Dynamic properties, Per-Class registered and Per-Instance registered – AcDb3dSolid uses Per-Instance because it is the instance (in the drawing) defines the types of properties that it needs to expose… If you want to see these in action, along with some Static properties, you should check out my QuickProperties ObjectARX sample in the 2009 version of the SDK.
One point to note in the code is, you’ll see me obtaining the Length, Width, Height etc. properties one way, then the Position property in another - that’s because the Length, Width, Height are all Dynamic properties, and the Position is a Static property.
Now for the code…
// by Fenton Webb, DevTech, Autodesk 28/May/2010
ads_point pnt;
ads_name ename;
// pick a solid
int res = acedEntSel(_T("\nPick a Solid : "), ename, pnt);
// if ok
if (res == RTNORM)
{
  AcDbObjectId id;
  // convert from an ADS ename to ObjectARX ObjectId
  acdbGetObjectId(id, ename);
  // get the IUknown of the entity, we’ll need it to get the properties for the instance and also so we can set them
  CComPtr<IUnknown> entIUnknown = NULL;
  HRESULT hr = AcAxGetIUnknownOfObject(&entIUnknown, id, acedGetAcadWinApp()->GetIDispatch(TRUE));
  double length=0.001, height=0.001, width=0.001;
    // get the dynamic properties to obtain Box info
  AcRxClass* pAcrxClass = AcDb3dSolid::desc();
  // Per-instance dynamic property managers
  OPMPerInstancePropertyExtension* pPerInstanceExtension = GET_OPM_PERINSTANCE_EXTENSION_PROTOCOL(pAcrxClass);
  if (NULL != pPerInstanceExtension)
  {
    COleSafeArray sourceNames;
    CComBSTR sourceName;
    // get the property source names stored on the extension object
    pPerInstanceExtension->GetObjectPropertySourceNames((LPVARIANT)sourceNames);
    // find out how many we have
    long start = 0;
    long end = 0;
    sourceNames.GetLBound(1, &start);
    sourceNames.GetUBound(1, &end);
    // loop the property sources
    for (long i=start; i<=end; ++i)
    {
      // extract each one of the property sources out
      CComPtr<IPropertySource> propertySource;
      sourceNames.GetElement(&i, (void*)&sourceName);
      // GetPropertySourceAt does AddRef, so we directly assign pointer here.
      propertySource.p = GET_OPM_PERINSTANCE_PROPERTY_SOURCES()->GetPropertySourceAt(&sourceName);
      // if we have one
      if (propertySource.p)
      {
        // if ok
        if (SUCCEEDED(hr))
        {
          // extract the Dynamic properties from it
          COleSafeArray props;
          hr = propertySource->GetProperties(entIUnknown, props);
          // if ok
          if (SUCCEEDED(hr))
          {
            // loop all the dynamic properties that we have
            long start = 0;
            long end = 0;
            props.GetLBound(1, &start);
            props.GetUBound(1, &end);
            for (long i=start; i<=end; ++i)
            {
              // first get the iUknown to make sure we have something
              CComPtr<IUnknown> unknown = NULL;
              props.GetElement(&i, (void*)&unknown);
              // if we have
              if (unknown.p)
              {
                // try and cast it to an updated IDynamicProperty2
                CComQIPtr<IDynamicProperty2> dynProp = unknown;
                // if ok
                if (dynProp.p)
                {
                  CComBSTR propName;
                  // extract out the property name
                  dynProp->GetDisplayName(&(propName.m_str));
                  // get the value
                  COleVariant getter;
                  dynProp->GetCurrentValueData(entIUnknown, getter);
                  // find out which property we are looking at
                  // extend as you see fit
                  if (CString(propName) == _T("Length"))
                    length = ((*(tagVARIANT*)(&getter))).dblVal;
                  if (CString(propName) == _T("Width"))
                    width = ((*(tagVARIANT*)(&getter))).dblVal;
                  if (CString(propName) == _T("Height"))
                    height = ((*(tagVARIANT*)(&getter))).dblVal;;
                }
              }
            }
          }
        }
      }
    }
      // now get the position from the solid
    CComQIPtr<IAcad3DSolid> solidCom(entIUnknown);
    if(solidCom != NULL)
    {
      COleVariant olePosition;
      hr = solidCom->get_Position(&olePosition);
      AcAxPoint3d position = olePosition;
        minPnt.x = position.x - length/2.0;
      minPnt.y = position.y - width/2.0;
      minPnt.z = position.z - height/2.0;
    }
  }

## 评论

**内容**: rayan said...
How can I read dwg file using arx? I want to extract the coordinates of a revolved object using object arx. how can I do that?
Reply
04/27/2015 at 03:03 AM

---
