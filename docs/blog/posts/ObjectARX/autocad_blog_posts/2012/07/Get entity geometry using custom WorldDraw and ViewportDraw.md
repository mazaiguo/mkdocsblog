---
title: "Get entity geometry using custom WorldDraw and ViewportDraw"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Solid
  - Unicode
description: "When AutoCAD draws an entity, it is passing an implementation of WorldDraw and ViewportDraw classes to the entity which then can call the functions..."
author: Autodesk
---
# Get entity geometry using custom WorldDraw and ViewportDraw

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/get-entity-geometry-using-custom-worlddraw-and-viewportdraw.html

## 文章内容

By Adam Nagy
When AutoCAD draws an entity, it is passing an implementation of WorldDraw and ViewportDraw classes to the entity which then can call the functions of those classes to draw itself. First WorldDraw is called, where the entity should draw geometry which is not viewport or view orientation specific. If the entity returns false from that function, then it means that it also wants to draw viewport specific geometry, so we could/should call ViewportDraw as well on the entity to gather the additional geometry.
We can create our own implementation of WorldDraw, ViewportDraw and the additionally needed classes so that we can collect the geometry the entity uses to represent itself.
If we are only interested in non-viewport specific geometry then we only need to implement our own Context, SubEntityTraits, WorldGeometry, and WorldDraw classes. Otherwise we also need Viewport, ViewportGeometry, and ViewportDraw classes.
Some entities draw all their geometry inside ViewportDraw(), but probably most draw it all inside WorldDraw(), while others may use both.
If you are interested in the solid representation of an entity it is a good idea to use an isometric view direction for the Viewport, like (1, 1, 1), that's what the sample uses too, because some entities have a non solid representation in views like Top.
ARX SDK contains the ArxDbg sample application, which among other things implements its own WorldDraw to collect the entity geometry. The attached sample also implements ViewportDraw - it simply lists the calls that the entity makes to draw itself and in case of solid entities which use Shell() to draw themselves creates lines based on the edges of the mesh facets. It draws all edges twice - it's not optimized. It's just a very basic sample. :)
You can use the attached classes like so:
[Autodesk.AutoCAD.Runtime.CommandMethod("GetGeometry")]
public void GetGeometry()
{
  Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.
    DocumentManager.MdiActiveDocument.Editor;
    PromptEntityResult per = ed.GetEntity("Select entity");
    if (per.Status != PromptStatus.OK)
    return;
    Database db = ed.Document.Database;
  using (Transaction tr = db.TransactionManager.StartTransaction())
  {
    Entity ent = (Entity)tr.GetObject(per.ObjectId, OpenMode.ForRead);

    if (!ent.WorldDraw(new MyWorldDraw()))
      ent.ViewportDraw(new MyViewportDraw());
      tr.Commit();
  }
}
Download MyDraw

## 评论

**内容**: Miroslav Vrabec said...
Wow Just what i needed thanks!
Reply
08/06/2014 at 07:50 AM

---
