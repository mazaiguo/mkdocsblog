---
title: "Obtaining Plant3d Catalog information using an external EXE"
date: 2012-12-01
categories:
  - Plant 3D
tags:
  - .NET
  - API
  - Plant 3D
  - SQL
description: "The Plant3d API is actually accessible from your own exe. If you create a simple .NET exe, reference these DLL references…"
author: Autodesk
---
# Obtaining Plant3d Catalog information using an external EXE

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/obtaining-plant3d-catalog-information-using-an-external-exe.html

## 文章内容

by Fenton Webb
The Plant3d API is actually accessible from your own exe. If you create a simple .NET exe, reference these DLL references…
PnIDMgd.dll
PnP3dPartsRepository.dll
PnPCommonMgd.dll
PnPDataObjects.dll
PnPSQLiteEngine.dll
And add this code to your Main()
class Program
{
  static void Main(string[] args)
  {
    // open the catalog
    PipePartCatalog repository = PipePartCatalog.OpenCatalog(
      "C:\\AutoCAD Plant 3D 2013 Content\\CPak ASME\\ASME Pipes and Fittings Catalog.pcat");
      // return all parts that meet this search criteria condition
    // "EndType='PL' AND CompatibleStandard = 'ASME B36.19'"
    PartQueryResults result = repository.SelectParts("PIPE",
        "EndType='PL' AND CompatibleStandard = 'ASME B36.19'");
    Part part = null;
    // now list them out
    while ((part = result.NextPart()) != null)
    {
      Console.WriteLine("Diameter = " + part.NominalDiameter);
    }
      // wait for acceptance from user
    Console.ReadKey();
  }
}
Then if you run the program from DOS, you get…
  Diameter = 0.125in
Diameter = 0.25in
Diameter = 0.375in
Diameter = 0.5in
Diameter = 0.75in
Diameter = 1in
Diameter = 1.25in
Diameter = 1.5in
Diameter = 2in
Diameter = 2.5in
Diameter = 3in
Diameter = 3.5in
Diameter = 4in
Diameter = 5in
Diameter = 6in
Diameter = 8in
Diameter = 10in
Diameter = 12in
Diameter = 14in
Diameter = 16in
Diameter = 18in
Diameter = 20in
Diameter = 22in
Diameter = 24in
Diameter = 26in
Diameter = 28in
Diameter = 30in
Diameter = 32in
Diameter = 34in
Diameter = 36in
Diameter = 38in
Diameter = 40in
Diameter = 42in
Diameter = 44in
Diameter = 46in
Diameter = 48in
Diameter = 50in
Diameter = 52in
Diameter = 54in
Diameter = 56in
Diameter = 58in
Diameter = 60in

## 评论

**内容**: Khoa Ho said...
This is interesting. The equivalent SQLite query is:
SELECT NominalDiameter, NominalUnit FROM Pipe_PNP
WHERE EndType='PL' AND CompatibleStandard = 'ASME B36.19'
Reply
12/17/2012 at 11:23 AM

---
**内容**: Le Yu said...
I am trying to use this with 2016 version. But I get an Exception: PnPCompletionStatus.FailedToOpenDatabase and can not open the database. If I put the same code in an addin DLL, I do not get this exception. Any idea what's wrong?
Reply
01/31/2017 at 06:59 AM

---
