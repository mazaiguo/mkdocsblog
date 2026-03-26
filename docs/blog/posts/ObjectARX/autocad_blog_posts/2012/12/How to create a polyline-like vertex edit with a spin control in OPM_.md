---
title: "How to create a polyline-like vertex edit with a spin control in OPM?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "The following snippets of code can be used to implement a polyline-like vertex edit in OPM (Object Property Manager) using IOPMPropertyExpander int..."
author: Autodesk
---
# How to create a polyline-like vertex edit with a spin control in OPM?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-create-a-polyline-like-vertex-edit-with-a-spin-control-in-opm.html

## 文章内容

By Gopinath Taget
The following snippets of code can be used to implement a polyline-like vertex edit in OPM (Object Property Manager) using IOPMPropertyExpander interface for a custom entity.
Lets assume the custom object (called AsDkRings) has two new variables to reflect an array of vertices:
AcGePoint3d m_polyline[5]; 
int m_numbervertices;
For simplicity, lets say the custom entity has a maximum of five vertices.
The custom class also has two corresponding access functions. (Note the vertex number parameter):
Acad::ErrorStatus AsDkRings::polyline(AcGePoint3d& vertex,
 int vertexNumber)
Acad::ErrorStatus AsDkRings::setPolyline(AcGePoint3d vertex,
int vertexNumber)
In AsDkRings:: subWoldDraw(), we draw a polyline connecting the five vertices.
The key to getting a spin control in OPM is to return a grouping number. This number will determine the number of elements to group together.
//IOPMPropertyExpander
STDMETHODIMP CRings::GetElementGrouping(
 /* [in] */ DISPID dispID,
 /* [out] */ short *groupingNumber)
{
.............
  .............
} else if (dispID == 5)
{
  *groupingNumber = 4;
  return S_OK;
}
 return E_NOTIMPL;
}
A grouping number of 4 means there is one entry (called "Vertex") plus 3 entries (Vertex X, Y and Z) to group together into one property. What this would do is put a spin control into the first item (vertex in this case), so that this could be used to traverse an array of 3 remaining grouped items (which is Vertex X, Y and Z).
Next, we should specify the number of items that the property is going to display. Here this would be the number of vertices  = 5. This would mean that the spin contol can go up to a maximum of 5 steps, for five vertices.
//IOPMPropertyExpander
STDMETHODIMP CRings::GetGroupCount(
 /* [in] */ DISPID dispID,
 /* [out] */ long *nGroupCnt)
{
................
  ...............
} else if (dispID == 5)
{
  *nGroupCnt = m_numbervertices; // Number of vertices
  return S_OK;
}
 return E_NOTIMPL;
}
Next, we set the string to display in the OPM.
//IOPMPropertyExpander
STDMETHODIMP CRings::GetElementStrings(
 /* [in] */ DISPID dispID,
 /* [out] */ OPMLPOLESTR __RPC_FAR *pCaStringsOut,
 /* [out] */ OPMDWORD __RPC_FAR *pCaCookiesOut)
{
................................
  ................................
} else if (dispID == 5)
{
  // For the Vertices
  pCaStringsOut->cElems = 4;
  pCaStringsOut->pElems = (LPOLESTR*)CoTaskMemAlloc(sizeof(LPOLESTR)*4);
  pCaStringsOut->pElems[0] = SysAllocString(L"Vertex");
  pCaStringsOut->pElems[1] = SysAllocString(L"Vertex X");
  pCaStringsOut->pElems[2] = SysAllocString(L"Vertex Y");
  pCaStringsOut->pElems[3] = SysAllocString(L"Vertex Z");
  pCaCookiesOut->cElems = 4;
  pCaCookiesOut->pElems = (DWORD*)CoTaskMemAlloc(sizeof(DWORD)*4);
    pCaCookiesOut->pElems[0] = 10;
  pCaCookiesOut->pElems[1] = 1;
  pCaCookiesOut->pElems[2] = 2;
  pCaCookiesOut->pElems[3] = 3;
  return S_OK;
}
 return E_NOTIMPL;
}
The cookies count is the unique identifier for each property item that will be used to get and set values. The table below will give you an idea of cookie value for each vertex value. Please remember that vertex entry has a spin control that goes like 1, 2, 3, 4.........and so on.
Property String  Cookie Value       
                 Vertex = 1    Vertex = 2   Vertex = 3   Vertex = 4  ....and so on        
Vertex              0             4            8           12        ....and so on        
Vertex X            1             5            9           13        ....and so on        
Vertex Y            2             6           10           14        ....and so on        
Vertex Z            3             7           11           15        ....and so on
So just by using the cookie values, you must get the vertex number and find out if it is an x, y, or z coordinate. The following code does that.
// Get the coordinate index (x=0, y= 1, z=2) from dwCookie
for (int i = 1; i < 4; i++) {
vertex = (double(dwCookie) - i) / 4;
 if( vertex == (double(dwCookie) - i) / 4) {
  index = i -1;
  break;
}
}
  index will return 0 for vertex X, 1 for vertex Y and 2 for vertex Z for the corrosponding cookie values.
So this is all that is needed to implement a poly-line vertex edit.

## 评论

**内容**: R.A.Diwas said...
The outcome of this code is wonderful but many of us aren't a big fan of COM. We prefer to customize AutoCAD in plain C++ without COM. If one of you could show how to arrive at the same outcome using the non-COM property system, then it would be great.
I think it would be very helpful if Autodesk should provide relevant sample codes aside from the cryptic documentation of the new AcRx classes like AcRxCollectionProperty, AcRxIndexedProperty, AcRxDictionaryProperty, etc.
Reply
08/02/2015 at 08:40 PM

---
**内容**: Jayaprakash said...
Can you upload sample project to add spin control in ACAD property pallet?
I tried with given code snippet. But "GetElementStrings" function not call by system.
Please provide your input to add spin control in property pallet.
Reply
01/22/2019 at 04:27 AM

---
