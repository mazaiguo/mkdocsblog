---
title: "How to convert a resbuf chain to a SAFEARRAY and vice versa?"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - COM
description: "I want to convert a resbuf linked list into a SAFEARRAY so that I can pass it via COM, the receiving application must be able to convert the SAFEAR..."
author: Autodesk
---
# How to convert a resbuf chain to a SAFEARRAY and vice versa?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-convert-a-resbuf-chain-to-a-safearray-and-vice-versa.html

## 文章内容

By Philippe Leefsma
Q:
I want to convert a resbuf linked list into a SAFEARRAY so that I can pass it via COM, the receiving application must be able to convert the SAFEARRAY back to a resbuf... How to convert a resbuf chain to a SAFEARRAY and visa versa?
A:
the code below handles *standard* resbufs, it will need modifying to handle rbinary chunks and other groups codes < 0 which are not –3
//////////////////////////////////////////////////////////////////////////////  
// constructs a resbuf filled from safearray, by Fenton Webb, DevTech
  bool ResbufToSafeArrays (
        struct resbuf *rb,
        COleSafeArray &restypes,
        COleSafeArray &resvals)
{
 USES_CONVERSION;
 struct resbuf *ptr = rb;
   // count how many entries we have
 long count;
   for (count=0; ptr!=NULL; ++count)
 {
  ptr = ptr->rbnext;
 }
   // create the datatypes array
 VARIANT *dataTypes = new VARIANT[count];
   // create the data
 VARIANT *dataVals = new VARIANT[count];
   // set up the datastrings with the resbuf
 for (long i=0; i<count; ++i)
 {
  // setup the datatypes
  dataTypes[i].vt = VT_I2;
  dataVals[i].vt = VT_BSTR;
    // if we are dealing with a string
  if (rb->restype == RTSTR)
  {
   // make the bit minus so that we know it's a string value
   dataTypes[i].iVal = -rb->restype;
     // now create the bstr
   dataVals[i].bstrVal = CComBSTR(rb->resval.rstring);
  }
  else
  {
   dataTypes[i].iVal = rb->restype;
   dataVals[i].bstrVal =
       ::SysAllocStringByteLen ((LPCSTR)(&rb->resval), sizeof (rb->resval));
  }
    // move to the next one
  rb = rb->rbnext;
 }
   // create the safearrays
 restypes.CreateOneDim (VT_VARIANT, count, dataTypes);
 resvals. CreateOneDim (VT_VARIANT, count, dataVals);
   //delete[] dataVals;
 return true;
}
    bool SafeArraysToResbuf (
        COleSafeArray &restypes,
        COleSafeArray &resvals,
struct resbuf **rb)
{
 USES_CONVERSION;
   // get the total number of restypes
 long numberResTypes = restypes.GetOneDimSize();
   // get the total number of resvals
 long numberResVals = resvals.GetOneDimSize();
 struct resbuf *resbufList = NULL, *currentPtr = NULL;
   // now extract the data
 for (long i=0; i<numberResVals; ++i)
 {
  COleVariant dataType;
  COleVariant dataVal;
    // extract the resval from the ith level in the resval safearray
  restypes.GetElement(&i, (void*)dataType);
    // extract the resval from the ith level in the resval safearray
  resvals.GetElement(&i, (void*)dataVal);
    // create a new resbuf using the datatype received
  struct resbuf *rb = acutNewRb (abs(dataType.iVal));
    // if it is a string
  if (dataType.iVal <= 0)
  {
   // extract the string value
   _bstr_t strValue(dataVal.bstrVal);
      // allocate the memory for the string
   rb->resval.rstring = strValue.copy();
  }
  else
  {
   // convert the bstring into the binary chunk known as a resbuf
   memcpy (&rb->resval, dataVal.bstrVal, sizeof (rb->resval));
  }
    // special cases
  switch (dataType.iVal)
  {
   // xdata start
   case -3 :
   {
    rb->restype = dataType.iVal;
   };
  }
    // if this is the first time through
  if (currentPtr == NULL)
  {
   // create a new resbuf, set its restype to a default value
   resbufList = currentPtr = rb;
  }
  else
  {
   // create a new entry at the next pointer
   currentPtr->rbnext = rb;
   // now move to it
   currentPtr = currentPtr->rbnext;
  }
 }
   // return the resbuf
 *rb = resbufList;
 return true;
}
  void TestSafeArrayConversion(void)
{
 struct resbuf rs2;
 rs2.restype = RTSTR;
 rs2.resval.rstring = L"resbuf2";
 rs2.rbnext = NULL;
   struct resbuf rs1;
 rs1.restype = RTSHORT;
 rs1.resval.rint = 2008;
 rs1.rbnext = &rs2;
   COleSafeArray restypes;
 COleSafeArray resvals;
 ResbufToSafeArrays(&rs1, restypes, resvals);
   struct resbuf* rb;
 SafeArraysToResbuf(restypes, resvals, &rb);
}

## 评论

**内容**: Tony Tanzillo said...
If I'm not mistaken (it's been a while since I did this), the resTypes array should be VT_I2, rather than VT_VARIANT.
Reply
09/22/2012 at 01:35 AM

---
