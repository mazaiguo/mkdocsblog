---
title: TXTEXP文字分解技术文档
date: 2026-02-12
categories:
  - CAD开发
  - ObjectARX
tags:
  - ObjectARX
  - Text Explode
  - WMF
  - Transaction
description: 使用 WMF 方法分解 CAD 文字实体的完整技术实现文档
author: JerryMa
---

# TXTEXP文字分解技术文档

## 功能概述

`CTextExplodeWmf` 是一个基于 ObjectARX/ZRX 的 CAD 文字分解工具，通过 WMF (Windows Metafile) 格式实现文字实体到几何图形的转换。

### 主要功能

- 支持 TEXT 和 MTEXT 实体的分解
- 保留原始文字的所有属性（图层、颜色、线型、线宽等）
- 使用事务管理确保操作的原子性
- 自动清理临时对象和块定义

### 技术特点

- **事务管理**：使用 `AcDbTransaction` 避免对象打开冲突
- **WMF 中转**：通过 WMFOUT/WMFIN 命令实现文字到几何的转换
- **坐标转换**：支持 UCS/WCS/DCS 多坐标系转换
- **自动清理**：删除临时 WMF 块和块引用

## 架构设计

### 类结构

```cpp
// collapsed
// 坐标转换工具类
class CoordTransform
{
public:
    static AcGeMatrix3d UCS2WCS();  // User Coordinate System to World
    static AcGeMatrix3d WCS2UCS();  // World to User
    static AcGeMatrix3d DCS2WCS();  // Display Coordinate System to World
    static AcGeMatrix3d WCS2DCS();  // World to Display
};

// 选择辅助工具类
class SelectionHelper
{
public:
    static AcDbObjectId SelectLastEnt();  // 获取最后一个实体
    static Acad::ErrorStatus SelectTextEntitiesInModelSpace(
        AcArray<AcDbObjectId>& ids);  // 选择所有文字实体
};

// 文字分解主类
class CTextExplodeWmf
{
public:
    static void ExportTextCommand();  // 主命令函数
    
private:
    static Acad::ErrorStatus ProcessTextEntity(AcDbObjectId textId);
    static bool GetViewBounds(AcGePoint3d& p1, AcGePoint3d& p2);
};
```

## C++ 实现详解

### 完整代码文件

#### CTextExplodeWmf.h

```cpp
// collapsed
// CTextExplodeWmf.h - Text explosion using WMF method
#pragma once

#include "dbmain.h"
#include "dbents.h"
#include "dbapserv.h"
#include "acgi.h"
#include "gepnt3d.h"
#include "gepnt2d.h"
#include "gemat3d.h"
#include "gevec3d.h"
#include "aced.h"
#include "rxregsvc.h"
#include "acedads.h"

// Utility functions for coordinate transformation
class CoordTransform
{
public:
    // Get UCS to WCS transformation matrix
    static AcGeMatrix3d UCS2WCS();
    
    // Get WCS to UCS transformation matrix
    static AcGeMatrix3d WCS2UCS();
    
    // Get DCS to WCS transformation matrix
    static AcGeMatrix3d DCS2WCS();
    
    // Get WCS to DCS transformation matrix
    static AcGeMatrix3d WCS2DCS();
};

// Utility functions for entity selection
class SelectionHelper
{
public:
    // Get ObjectId of last entity (entlast)
    static AcDbObjectId SelectLastEnt();
    
    // Select all TEXT and MTEXT entities in model space
    static Acad::ErrorStatus SelectTextEntitiesInModelSpace(AcArray<AcDbObjectId>& ids);
};

// Text explosion using WMF method
class CTextExplodeWmf
{
public:
    CTextExplodeWmf();
    ~CTextExplodeWmf();
    
    // Main command function - export text using WMF method
    static void ExportTextCommand();

private:
    // Process single text entity using WMF method
    static Acad::ErrorStatus ProcessTextEntity(AcDbObjectId textId);
    
    // Get view window bounds in UCS
    static bool GetViewBounds(AcGePoint3d& p1, AcGePoint3d& p2);
    
    // Import WMF file and explode to entities
    static Acad::ErrorStatus ImportAndExplodeWmf(
        const ACHAR* wmfFile,
        const AcGePoint2d& insertPt,
        AcArray<AcDbEntity*>& entities);
};
```

#### CTextExplodeWmf.cpp

```cpp
// collapsed
// CTextExplodeWmf.cpp - Text explosion using WMF method
#include "stdafx.h"
#include "CTextExplodeWmf.h"
#include <shlwapi.h>
#include "acedCmdNF.h"
#pragma comment(lib, "shlwapi.lib")

// ============================================================================
// CoordTransform implementation
// ============================================================================

AcGeMatrix3d CoordTransform::UCS2WCS()
{
    AcGeMatrix3d ucs;
    acedGetCurrentUCS(ucs);
    return ucs;
}

AcGeMatrix3d CoordTransform::WCS2UCS()
{
    AcGeMatrix3d ucs;
    acedGetCurrentUCS(ucs);
    return ucs.inverse();
}

AcGeMatrix3d CoordTransform::DCS2WCS()
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb)
        return AcGeMatrix3d::kIdentity;

    // Get current view
    struct resbuf viewCtrRb, viewDirRb, viewTwistRb, targetRb;
    
    acedGetVar(_T("VIEWCTR"), &viewCtrRb);
    acedGetVar(_T("VIEWDIR"), &viewDirRb);
    acedGetVar(_T("VIEWTWIST"), &viewTwistRb);
    acedGetVar(_T("TARGET"), &targetRb);

    AcGePoint3d target(targetRb.resval.rpoint[X], targetRb.resval.rpoint[Y], targetRb.resval.rpoint[Z]);
    AcGeVector3d viewDir(viewDirRb.resval.rpoint[X], viewDirRb.resval.rpoint[Y], viewDirRb.resval.rpoint[Z]);
    double viewTwist = viewTwistRb.resval.rreal;

    // Build transformation matrix
    AcGeMatrix3d mat;
    mat.setCoordSystem(
        AcGePoint3d::kOrigin,
        viewDir.perpVector().normalize(),
        viewDir.crossProduct(viewDir.perpVector()).normalize(),
        viewDir);

    AcGeMatrix3d rotation;
    rotation.setToRotation(-viewTwist, viewDir, target);

    AcGeMatrix3d translation;
    translation.setToTranslation(target.asVector());

    return rotation * translation * mat;
}

AcGeMatrix3d CoordTransform::WCS2DCS()
{
    return DCS2WCS().inverse();
}

// ============================================================================
// SelectionHelper implementation
// ============================================================================

AcDbObjectId SelectionHelper::SelectLastEnt()
{
    ads_name ss;
    if (acedSSGet(_T("L"), NULL, NULL, NULL, ss) != RTNORM)
        return AcDbObjectId::kNull;

    Adesk::Int32 length = 0;
    acedSSLength(ss, &length);
    
    if (length != 1)
    {
        acedSSFree(ss);
        return AcDbObjectId::kNull;
    }

    ads_name ent;
    acedSSName(ss, 0, ent);
    
    AcDbObjectId objId;
    acdbGetObjectId(objId, ent);
    
    acedSSFree(ss);
    return objId;
}

Acad::ErrorStatus SelectionHelper::SelectTextEntitiesInModelSpace(AcArray<AcDbObjectId>& ids)
{
    ids.removeAll();
    
    // Build selection filter for TEXT and MTEXT in MODEL space
    struct resbuf* filter = acutBuildList(
        -4, _T("<OR"),
            RTDXF0, _T("TEXT"),
            RTDXF0, _T("MTEXT"),
        -4, _T("OR>"),
        RTNONE);

    ads_name ss;
    int ret = acedSSGet(_T("X"), NULL, NULL, filter, ss);
    acutRelRb(filter);

    if (ret != RTNORM)
        return Acad::eInvalidInput;

    Adesk::Int32 length = 0;
    acedSSLength(ss, &length);

    for (long i = 0; i < length; i++)
    {
        ads_name ent;
        if (acedSSName(ss, i, ent) == RTNORM)
        {
            AcDbObjectId objId;
            if (acdbGetObjectId(objId, ent) == Acad::eOk)
            {
                ids.append(objId);
            }
        }
    }

    acedSSFree(ss);
    return ids.length() > 0 ? Acad::eOk : Acad::eInvalidInput;
}

// ============================================================================
// CTextExplodeWmf implementation
// ============================================================================

CTextExplodeWmf::CTextExplodeWmf()
{
}

CTextExplodeWmf::~CTextExplodeWmf()
{
}

void CTextExplodeWmf::ExportTextCommand()
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb)
    {
        acutPrintf(_T("\nNo active database."));
        return;
    }

    // Select all TEXT and MTEXT entities in model space
    AcArray<AcDbObjectId> textIds;
    if (SelectionHelper::SelectTextEntitiesInModelSpace(textIds) != Acad::eOk)
    {
        acutPrintf(_T("\nNo TEXT entities found in model space."));
        return;
    }

    acutPrintf(_T("\nFound %d TEXT entities to process."), textIds.length());

    int successCount = 0;
    for (int i = 0; i < textIds.length(); i++)
    {
        if (ProcessTextEntity(textIds[i]) == Acad::eOk)
            successCount++;
    }

    acutPrintf(_T("\nSuccessfully processed %d text entities."), successCount);
}

Acad::ErrorStatus CTextExplodeWmf::ProcessTextEntity(AcDbObjectId textId)
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb)
        return Acad::eNullObjectPointer;

    // Start a transaction - this is the key to avoid eWasOpenForWrite
    Acad::ErrorStatus es = Acad::eOk;
    AcDbTransactionManager* pTM = pDb->transactionManager();
    if (!pTM)
        return Acad::eNullObjectPointer;
    
    AcTransaction* pTrans = pTM->startTransaction();
    if (!pTrans)
        return Acad::eNullObjectPointer;

    // Get entity through transaction (supports both TEXT and MTEXT)
    AcDbEntity* pEntity = NULL;
    es = pTrans->getObject((AcDbObject*&)pEntity, textId, AcDb::kForWrite);
    if (es != Acad::eOk)
    {
        pTrans->abort();
        delete pTrans;
        return es;
    }

    // Set implied selection to current text
    ads_name textEnt;
    acdbGetAdsName(textEnt, textId);
    ads_name ss;
    acedSSAdd(textEnt, NULL, ss);
    acedSSSetFirst(ss, ss);

    // Generate temporary WMF file path
    TCHAR tempPath[MAX_PATH];
    GetTempPath(MAX_PATH, tempPath);
    TCHAR wmfFile[MAX_PATH];
    _stprintf_s(wmfFile, _T("%sQ.wmf"), tempPath);

    // Delete existing temp file
    if (PathFileExists(wmfFile))
        DeleteFile(wmfFile);

    // Export to WMF
    acedCommand(RTSTR, _T("_.WMFOUT"), RTSTR, wmfFile, RTSTR, _T(""), RTSTR, _T(""), RTNONE);

    // Get view bounds for WMF import
    AcGePoint3d p1, p2;
    if (!GetViewBounds(p1, p2))
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        return Acad::eInvalidInput;
    }

    // Calculate insert point (top-left of view)
    AcGePoint2d wmfInsertPt(p1.x, p2.y);

    // Import WMF and explode
    AcArray<AcDbEntity*> entities;
    TCHAR wmfFileNoExt[MAX_PATH];
    _tcscpy_s(wmfFileNoExt, wmfFile);
    PathRemoveExtension(wmfFileNoExt);

    // Import WMF as block
    acedCommand(
        RTSTR, _T("_.WMFIN"), 
        RTSTR, wmfFileNoExt, 
        RTPOINT, asDblArray(wmfInsertPt),
        RTSTR, _T("2"),
        RTSTR, _T(""),
        RTSTR, _T(""),
        RTNONE);

    // Ensure command is completely finished and all objects are closed
    // This is critical to avoid eWasOpenForWrite error
    acedUpdateDisplay();
    acedCommand(RTNONE);  // Force command stack to flush
    
    // Get the imported block reference (last entity)
    AcDbObjectId wmfBlockRefId = SelectionHelper::SelectLastEnt();
    if (wmfBlockRefId.isNull())
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        acutPrintf(_T("\nFailed to get WMF block reference."));
        return Acad::eInvalidInput;
    }

    // Get block reference through transaction - this avoids eWasOpenForWrite!
    AcDbBlockReference* pBlkRef = NULL;
    es = pTrans->getObject((AcDbObject*&)pBlkRef, wmfBlockRefId, AcDb::kForWrite);
    if (es != Acad::eOk)
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        acutPrintf(_T("\nFailed to open WMF block reference. Error: %d"), es);
        return es;
    }

    // Explode block reference
    AcDbVoidPtrArray explodedEnts;
    es = pBlkRef->explode(explodedEnts);
    AcDbObjectId wmfBlockId = pBlkRef->blockTableRecord();
    
    if (es == Acad::eOk && explodedEnts.length() > 0)
    {
        // Get model space through transaction
        AcDbBlockTable* pBT = NULL;
        es = pTrans->getObject((AcDbObject*&)pBT, pDb->blockTableId(), AcDb::kForRead);
        if (es != Acad::eOk)
        {
            pTrans->abort();
            delete pTrans;
            acedSSFree(ss);
            return es;
        }

        AcDbBlockTableRecord* pModelSpace = NULL;
        es = pTrans->getObject((AcDbObject*&)pModelSpace, pDb->currentSpaceId(), AcDb::kForWrite);
        if (es != Acad::eOk)
        {
            pTrans->abort();
            delete pTrans;
            acedSSFree(ss);
            return es;
        }

        for (int i = 0; i < explodedEnts.length(); i++)
        {
            AcDbEntity* pEnt = static_cast<AcDbEntity*>(explodedEnts[i]);
            if (pEnt)
            {
                // Copy properties from original entity (TEXT or MTEXT)
                pEnt->setLayer(pEntity->layer());
                pEnt->setColor(pEntity->color());
                pEnt->setLinetype(pEntity->linetype());
                pEnt->setLinetypeScale(pEntity->linetypeScale());
                pEnt->setLineWeight(pEntity->lineWeight());

                if (pModelSpace->appendAcDbEntity(pEnt) == Acad::eOk)
                {
                    // Add to transaction
                    pTrans->addNewlyCreatedDBObject(pEnt, true);
                }
                else
                {
                    delete pEnt;
                }
            }
        }
    }

    // Delete WMF block reference and block definition
    if (!wmfBlockId.isNull())
    {
        AcDbBlockTableRecord* pWmfBlock = NULL;
        if (pTrans->getObject((AcDbObject*&)pWmfBlock, wmfBlockId, AcDb::kForWrite) == Acad::eOk)
        {
            pWmfBlock->erase();
        }
    }
    
    // Erase block reference
    pBlkRef->erase();

    // Erase original entity (TEXT or MTEXT)
    pEntity->erase();

    // Commit transaction - this will close all objects automatically
    es = pTrans->commit();
    delete pTrans;

    acedSSFree(ss);

    return es;
}

bool CTextExplodeWmf::GetViewBounds(AcGePoint3d& p1, AcGePoint3d& p2)
{
    // Get system variables
    struct resbuf viewSizeRb, screenSizeRb, viewCtrRb;
    
    if (acedGetVar(_T("VIEWSIZE"), &viewSizeRb) != RTNORM)
        return false;
    if (acedGetVar(_T("SCREENSIZE"), &screenSizeRb) != RTNORM)
        return false;
    if (acedGetVar(_T("VIEWCTR"), &viewCtrRb) != RTNORM)
        return false;

    double viewSize = viewSizeRb.resval.rreal;
    double screenWidth = screenSizeRb.resval.rpoint[X];
    double screenHeight = screenSizeRb.resval.rpoint[Y];
    double factor = viewSize * (screenWidth / screenHeight);
    
    AcGePoint3d viewCtr(
        viewCtrRb.resval.rpoint[X],
        viewCtrRb.resval.rpoint[Y],
        viewCtrRb.resval.rpoint[Z]);

    // Transform viewCtr from UCS to DCS
    AcGeMatrix3d matUCS2DCS = CoordTransform::UCS2WCS() * CoordTransform::WCS2DCS();
    viewCtr.transformBy(matUCS2DCS);

    // Calculate bounds in DCS
    p1.set(viewCtr.x - (factor / 2.0), viewCtr.y - (viewSize / 2.0), 0.0);
    p2.set(viewCtr.x + (factor / 2.0), viewCtr.y + (viewSize / 2.0), 0.0);

    // Transform back to UCS
    AcGeMatrix3d matDCS2UCS = CoordTransform::DCS2WCS() * CoordTransform::WCS2UCS();
    p1.transformBy(matDCS2UCS);
    p2.transformBy(matDCS2UCS);

    return true;
}
```

### 代码分段详解

### 1. 坐标转换实现

#### DCS to WCS 转换

```cpp
// collapsed
AcGeMatrix3d CoordTransform::DCS2WCS()
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb)
        return AcGeMatrix3d::kIdentity;

    // Get current view parameters
    struct resbuf viewCtrRb, viewDirRb, viewTwistRb, targetRb;
    acedGetVar(_T("VIEWCTR"), &viewCtrRb);
    acedGetVar(_T("VIEWDIR"), &viewDirRb);
    acedGetVar(_T("VIEWTWIST"), &viewTwistRb);
    acedGetVar(_T("TARGET"), &targetRb);

    AcGePoint3d target(targetRb.resval.rpoint[X], 
                       targetRb.resval.rpoint[Y], 
                       targetRb.resval.rpoint[Z]);
    AcGeVector3d viewDir(viewDirRb.resval.rpoint[X], 
                         viewDirRb.resval.rpoint[Y], 
                         viewDirRb.resval.rpoint[Z]);
    double viewTwist = viewTwistRb.resval.rreal;

    // Build transformation matrix
    AcGeMatrix3d mat;
    mat.setCoordSystem(
        AcGePoint3d::kOrigin,
        viewDir.perpVector().normalize(),
        viewDir.crossProduct(viewDir.perpVector()).normalize(),
        viewDir);

    AcGeMatrix3d rotation;
    rotation.setToRotation(-viewTwist, viewDir, target);

    AcGeMatrix3d translation;
    translation.setToTranslation(target.asVector());

    return rotation * translation * mat;
}
```

**关键点**：
- 获取当前视图参数（视图中心、方向、扭转角度）
- 构建坐标系变换矩阵
- 组合旋转、平移、视图变换

### 2. 文字实体选择

```cpp
// collapsed
Acad::ErrorStatus SelectionHelper::SelectTextEntitiesInModelSpace(
    AcArray<AcDbObjectId>& ids)
{
    ids.removeAll();
    
    // Build selection filter for TEXT and MTEXT
    struct resbuf* filter = acutBuildList(
        -4, _T("<OR"),
            RTDXF0, _T("TEXT"),
            RTDXF0, _T("MTEXT"),
        -4, _T("OR>"),
        RTNONE);

    ads_name ss;
    int ret = acedSSGet(_T("X"), NULL, NULL, filter, ss);
    acutRelRb(filter);

    if (ret != RTNORM)
        return Acad::eInvalidInput;

    // Collect all entity IDs
    Adesk::Int32 length = 0;
    acedSSLength(ss, &length);

    for (long i = 0; i < length; i++)
    {
        ads_name ent;
        if (acedSSName(ss, i, ent) == RTNORM)
        {
            AcDbObjectId objId;
            if (acdbGetObjectId(objId, ent) == Acad::eOk)
            {
                ids.append(objId);
            }
        }
    }

    acedSSFree(ss);
    return ids.length() > 0 ? Acad::eOk : Acad::eInvalidInput;
}
```

**关键点**：
- 使用 OR 过滤器同时选择 TEXT 和 MTEXT
- 使用 "X" 选项选择整个图形
- 收集所有实体的 ObjectId

### 3. 核心处理流程

```cpp
// collapsed
Acad::ErrorStatus CTextExplodeWmf::ProcessTextEntity(AcDbObjectId textId)
{
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    if (!pDb)
        return Acad::eNullObjectPointer;

    // ========== Step 1: 启动事务 ==========
    // Transaction is the KEY to avoid eWasOpenForWrite error
    AcDbTransactionManager* pTM = pDb->transactionManager();
    if (!pTM)
        return Acad::eNullObjectPointer;
    
    AcTransaction* pTrans = pTM->startTransaction();
    if (!pTrans)
        return Acad::eNullObjectPointer;

    // ========== Step 2: 获取文字实体 ==========
    AcDbEntity* pEntity = NULL;
    Acad::ErrorStatus es = pTrans->getObject(
        (AcDbObject*&)pEntity, textId, AcDb::kForWrite);
    if (es != Acad::eOk)
    {
        pTrans->abort();
        delete pTrans;
        return es;
    }

    // ========== Step 3: 设置隐含选择集 ==========
    ads_name textEnt;
    acdbGetAdsName(textEnt, textId);
    ads_name ss;
    acedSSAdd(textEnt, NULL, ss);
    acedSSSetFirst(ss, ss);

    // ========== Step 4: 导出到 WMF ==========
    TCHAR tempPath[MAX_PATH];
    GetTempPath(MAX_PATH, tempPath);
    TCHAR wmfFile[MAX_PATH];
    _stprintf_s(wmfFile, _T("%sQ.wmf"), tempPath);

    if (PathFileExists(wmfFile))
        DeleteFile(wmfFile);

    acedCommand(RTSTR, _T("_.WMFOUT"), RTSTR, wmfFile, 
                RTSTR, _T(""), RTSTR, _T(""), RTNONE);

    // ========== Step 5: 计算视图范围 ==========
    AcGePoint3d p1, p2;
    if (!GetViewBounds(p1, p2))
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        return Acad::eInvalidInput;
    }

    // ========== Step 6: 导入 WMF 为块 ==========
    TCHAR wmfFileNoExt[MAX_PATH];
    _tcscpy_s(wmfFileNoExt, wmfFile);
    PathRemoveExtension(wmfFileNoExt);

    AcGePoint2d wmfInsertPt(p1.x, p2.y);
    acedCommand(
        RTSTR, _T("_.WMFIN"), 
        RTSTR, wmfFileNoExt, 
        RTPOINT, asDblArray(wmfInsertPt),
        RTSTR, _T("2"),
        RTSTR, _T(""),
        RTSTR, _T(""),
        RTNONE);

    // Flush command stack - CRITICAL!
    acedUpdateDisplay();
    acedCommand(RTNONE);

    // ========== Step 7: 获取 WMF 块引用 ==========
    AcDbObjectId wmfBlockRefId = SelectionHelper::SelectLastEnt();
    if (wmfBlockRefId.isNull())
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        return Acad::eInvalidInput;
    }

    // Get block reference through transaction - NO eWasOpenForWrite!
    AcDbBlockReference* pBlkRef = NULL;
    es = pTrans->getObject((AcDbObject*&)pBlkRef, wmfBlockRefId, AcDb::kForWrite);
    if (es != Acad::eOk)
    {
        pTrans->abort();
        delete pTrans;
        acedSSFree(ss);
        return es;
    }

    // ========== Step 8: 分解块引用 ==========
    AcDbVoidPtrArray explodedEnts;
    es = pBlkRef->explode(explodedEnts);
    AcDbObjectId wmfBlockId = pBlkRef->blockTableRecord();
    
    if (es == Acad::eOk && explodedEnts.length() > 0)
    {
        // Get model space through transaction
        AcDbBlockTableRecord* pModelSpace = NULL;
        es = pTrans->getObject((AcDbObject*&)pModelSpace, 
                               pDb->currentSpaceId(), 
                               AcDb::kForWrite);
        if (es != Acad::eOk)
        {
            pTrans->abort();
            delete pTrans;
            acedSSFree(ss);
            return es;
        }

        // ========== Step 9: 添加分解实体到模型空间 ==========
        for (int i = 0; i < explodedEnts.length(); i++)
        {
            AcDbEntity* pEnt = static_cast<AcDbEntity*>(explodedEnts[i]);
            if (pEnt)
            {
                // Copy properties from original entity
                pEnt->setLayer(pEntity->layer());
                pEnt->setColor(pEntity->color());
                pEnt->setLinetype(pEntity->linetype());
                pEnt->setLinetypeScale(pEntity->linetypeScale());
                pEnt->setLineWeight(pEntity->lineWeight());

                if (pModelSpace->appendAcDbEntity(pEnt) == Acad::eOk)
                {
                    // Add to transaction - IMPORTANT!
                    pTrans->addNewlyCreatedDBObject(pEnt, true);
                }
                else
                {
                    delete pEnt;
                }
            }
        }
    }

    // ========== Step 10: 清理临时对象 ==========
    // Delete WMF block definition
    if (!wmfBlockId.isNull())
    {
        AcDbBlockTableRecord* pWmfBlock = NULL;
        if (pTrans->getObject((AcDbObject*&)pWmfBlock, 
                              wmfBlockId, 
                              AcDb::kForWrite) == Acad::eOk)
        {
            pWmfBlock->erase();
        }
    }
    
    // Erase block reference
    pBlkRef->erase();

    // Erase original text entity
    pEntity->erase();

    // ========== Step 11: 提交事务 ==========
    es = pTrans->commit();
    delete pTrans;

    acedSSFree(ss);
    return es;
}
```

### 4. 视图范围计算

```cpp
// collapsed
bool CTextExplodeWmf::GetViewBounds(AcGePoint3d& p1, AcGePoint3d& p2)
{
    // Get system variables
    struct resbuf viewSizeRb, screenSizeRb, viewCtrRb;
    
    if (acedGetVar(_T("VIEWSIZE"), &viewSizeRb) != RTNORM)
        return false;
    if (acedGetVar(_T("SCREENSIZE"), &screenSizeRb) != RTNORM)
        return false;
    if (acedGetVar(_T("VIEWCTR"), &viewCtrRb) != RTNORM)
        return false;

    double viewSize = viewSizeRb.resval.rreal;
    double screenWidth = screenSizeRb.resval.rpoint[X];
    double screenHeight = screenSizeRb.resval.rpoint[Y];
    double factor = viewSize * (screenWidth / screenHeight);
    
    AcGePoint3d viewCtr(
        viewCtrRb.resval.rpoint[X],
        viewCtrRb.resval.rpoint[Y],
        viewCtrRb.resval.rpoint[Z]);

    // Transform viewCtr from UCS to DCS
    AcGeMatrix3d matUCS2DCS = CoordTransform::UCS2WCS() * 
                               CoordTransform::WCS2DCS();
    viewCtr.transformBy(matUCS2DCS);

    // Calculate bounds in DCS
    p1.set(viewCtr.x - (factor / 2.0), viewCtr.y - (viewSize / 2.0), 0.0);
    p2.set(viewCtr.x + (factor / 2.0), viewCtr.y + (viewSize / 2.0), 0.0);

    // Transform back to UCS
    AcGeMatrix3d matDCS2UCS = CoordTransform::DCS2WCS() * 
                               CoordTransform::WCS2UCS();
    p1.transformBy(matDCS2UCS);
    p2.transformBy(matDCS2UCS);

    return true;
}
```

## C# 参考实现

本 C++ 实现参考了 GitHub 开源项目的 C# 代码：
[Forge-ExplodeText](https://github.com/MadhukarMoogala/Forge-ExplodeText/blob/master/FDA.Arx/Commands.cs)

### C# 完整代码

```csharp
// collapsed
using AcRx = Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices.Core;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using System;
using System.IO;

namespace Forge.Main
{
    public class Commands
    {
        [AcRx.CommandMethod("FDACommands","EXPTXT",AcRx.CommandFlags.Modal)]
        public void EXPTXT()
        {
            var doc = Application.DocumentManager.MdiActiveDocument;
            var db = doc.Database;
            var ed = doc.Editor;

            // Select all TEXT entities in model space
            ObjectId[] dbtextIds = ed.SelectTextEntitesInModelSpace();
            
            foreach (ObjectId id in dbtextIds)
            {
                // ========== Use Transaction ==========
                using (Transaction tr = db.TransactionManager.StartTransaction())
                {
                    var text = (DBText)tr.GetObject(id, OpenMode.ForWrite);
                    ObjectId[] ids = new ObjectId[1];
                    ids[0] = id;
                    ed.SetImpliedSelection(ids);
                    
                    // Export to WMF
                    var tempFile = Path.Combine(Path.GetTempPath(), "Q.wmf");
                    if (File.Exists(tempFile))
                    {
                        File.Delete(tempFile);
                    }
                    ed.Command("_.WMFOUT", tempFile, "", "");
                    
                    // Calculate view bounds
                    var viewSize = (double)Application.GetSystemVariable("VIEWSIZE");
                    var screenSize = (Point2d)Application.GetSystemVariable("SCREENSIZE");
                    double factor = viewSize * (screenSize.X / screenSize.Y);
                    var viewCtr = (Point3d)Application.GetSystemVariable("VIEWCTR");
                    
                    // Transform coordinates
                    Matrix3d matUCS2DCS = ed.UCS2WCS() * ed.WCS2DCS();
                    viewCtr = viewCtr.TransformBy(matUCS2DCS);
                    var p1 = new Point3d(viewCtr.X - (factor / 2.0), 
                                         viewCtr.Y - (viewSize / 2.0), .0);
                    var p2 = new Point3d(viewCtr.X + (factor / 2.0), 
                                         viewCtr.Y + (viewSize / 2.0), .0);
                    Matrix3d matDCS2UCS = ed.DCS2WCS() * ed.WCS2UCS();
                    p1 = p1.TransformBy(matDCS2UCS);
                    p2 = p2.TransformBy(matDCS2UCS);
                    
                    // Import WMF
                    Point2d wmfinBlockPos = new Point2d(p1.X, p2.Y);
                    var tempWithOutExt = Path.Combine(
                        Path.GetDirectoryName(tempFile), 
                        Path.GetFileNameWithoutExtension(tempFile));
                    ed.Command("_.WMFIN", tempWithOutExt, wmfinBlockPos, "2", "", "");
                    
                    try
                    {
                        // Get WMF block reference through transaction
                        var wmfBlock = tr.GetObject(ed.SelectLastEnt(), 
                                                   OpenMode.ForWrite) as BlockReference;
                        DBObjectCollection pElems = new DBObjectCollection();
                        wmfBlock?.Explode(pElems);
                        
                        // Add exploded entities to model space
                        var space = (BlockTableRecord)tr.GetObject(
                            db.CurrentSpaceId, OpenMode.ForWrite);
                        foreach (DBObject elem in pElems)
                        {
                            space.AppendEntity(elem as Entity);
                            tr.AddNewlyCreatedDBObject(elem, true);
                        }
                        
                        // Purge WMF block
                        ObjectId wmfBtr = GetNonErasedTableRecordId(
                            db.BlockTableId, wmfBlock.Name);
                        ObjectIdCollection blockIds = new ObjectIdCollection();
                        blockIds.Add(wmfBtr);
                        db.Purge(blockIds);
                        foreach (ObjectId oId in blockIds)
                        {
                            DBObject obj = tr.GetObject(oId, OpenMode.ForWrite);
                            obj.Erase();
                        }
                    }
                    catch (Exception ex)
                    {
                        ed.WriteMessage(ex.Message);
                    }
                    finally
                    {
                        // Erase original text
                        text.Erase();
                        tr.Commit();
                    }
                }
            }
        }

        public static ObjectId GetNonErasedTableRecordId(ObjectId TableId, string Name)
        {
            ObjectId id = ObjectId.Null;
            using (Transaction tr = TableId.Database.TransactionManager.StartTransaction())
            {
                SymbolTable table = (SymbolTable)tr.GetObject(TableId, OpenMode.ForRead);
                if (table.Has(Name))
                {
                    id = table[Name];
                    if (!id.IsErased)
                        return id;
                    foreach (ObjectId recId in table)
                    {
                        if (!recId.IsErased)
                        {
                            SymbolTableRecord rec = (SymbolTableRecord)tr.GetObject(
                                recId, OpenMode.ForRead);
                            if (string.Compare(rec.Name, Name, true) == 0)
                                return recId;
                        }
                    }
                }
            }
            return id;
        }
    }
}
```

## C++ vs C# 实现对比

| 特性 | C++ (ObjectARX/ZRX) | C# (.NET API) |
|------|---------------------|---------------|
| **事务管理** | `AcDbTransaction* pTrans = pTM->startTransaction()` | `using (Transaction tr = db.TransactionManager.StartTransaction())` |
| **获取对象** | `pTrans->getObject((AcDbObject*&)pObj, id, mode)` | `tr.GetObject(id, OpenMode.ForWrite)` |
| **添加新对象** | `pTrans->addNewlyCreatedDBObject(pEnt, true)` | `tr.AddNewlyCreatedDBObject(elem, true)` |
| **提交事务** | `pTrans->commit(); delete pTrans;` | 自动提交（using 块结束） |
| **中止事务** | `pTrans->abort(); delete pTrans;` | 自动中止（异常时） |
| **内存管理** | 手动管理指针 | 自动垃圾回收 |
| **错误处理** | 返回 `Acad::ErrorStatus` | 使用 try-catch 异常 |
| **类型转换** | 使用 C 风格类型转换 | 使用 `as` 和强制转换 |

## 核心技术点

### 1. 事务管理 - 解决 eWasOpenForWrite 错误

**问题**：直接使用 `acdbOpenObject()` 打开对象时，如果对象已被其他代码打开（如 WMFIN 命令），会出现 `eWasOpenForWrite` 错误。

**解决方案**：使用事务管理所有数据库对象

```cpp
// ❌ 错误方式 - 直接打开对象
AcDbBlockReference* pBlkRef = NULL;
es = acdbOpenObject(pBlkRef, wmfBlockRefId, AcDb::kForWrite);
// 可能出错：eWasOpenForWrite

// ✅ 正确方式 - 通过事务获取对象
AcDbTransaction* pTrans = pTM->startTransaction();
AcDbBlockReference* pBlkRef = NULL;
es = pTrans->getObject((AcDbObject*&)pBlkRef, wmfBlockRefId, AcDb::kForWrite);
// 同一事务上下文中，不会冲突
```

**优势**：
- 所有对象在同一事务上下文中，避免冲突
- 自动管理对象生命周期
- 支持原子操作（全部成功或全部回滚）
- 符合 ObjectARX 最佳实践

### 2. 命令栈刷新

```cpp
// Execute WMFIN command
acedCommand(RTSTR, _T("_.WMFIN"), ...);

// CRITICAL: Flush command stack
acedUpdateDisplay();
acedCommand(RTNONE);  // Force command to complete
```

**为什么需要**：
- WMFIN 命令可能在后台异步执行
- 需要确保命令完全完成，对象才能被正确访问
- `acedUpdateDisplay()` 刷新图形显示
- `acedCommand(RTNONE)` 强制清空命令栈

### 3. 坐标系转换

WMF 导入需要正确的插入点计算，涉及三种坐标系：

- **UCS** (User Coordinate System)：用户坐标系
- **WCS** (World Coordinate System)：世界坐标系
- **DCS** (Display Coordinate System)：显示坐标系

**转换链**：

```
UCS → WCS → DCS (计算视图范围)
DCS → WCS → UCS (转换回用户坐标)
```

### 4. 属性继承

```cpp
// Copy all properties from original text to exploded entities
pEnt->setLayer(pEntity->layer());
pEnt->setColor(pEntity->color());
pEnt->setLinetype(pEntity->linetype());
pEnt->setLinetypeScale(pEntity->linetypeScale());
pEnt->setLineWeight(pEntity->lineWeight());
```

**保留的属性**：
- 图层 (Layer)
- 颜色 (Color)
- 线型 (Linetype)
- 线型比例 (Linetype Scale)
- 线宽 (Line Weight)

### 5. 临时对象清理

```cpp
// Delete WMF block definition
if (!wmfBlockId.isNull())
{
    AcDbBlockTableRecord* pWmfBlock = NULL;
    if (pTrans->getObject((AcDbObject*&)pWmfBlock, 
                          wmfBlockId, 
                          AcDb::kForWrite) == Acad::eOk)
    {
        pWmfBlock->erase();  // Mark for deletion
    }
}

// Erase block reference
pBlkRef->erase();

// Erase original text
pEntity->erase();
```

**清理顺序**：
1. 删除 WMF 块定义（BlockTableRecord）
2. 删除块引用（BlockReference）
3. 删除原始文字实体
4. 提交事务后所有更改生效

## 关键问题与解决方案

### 问题 1：eWasOpenForWrite 错误

**现象**：
```
Error code: 83 (eWasOpenForWrite)
Failed to open WMF block reference
```

**原因**：
- 对象已被其他代码以写模式打开
- WMFIN 命令可能持有对象引用
- 多个 `acdbOpenObject()` 调用冲突

**解决**：
使用 `AcDbTransaction` 统一管理所有对象

### 问题 2：对象未找到

**现象**：
```
Failed to get WMF block reference
wmfBlockRefId.isNull() == true
```

**原因**：
- WMFIN 命令未完成
- 选择 "L" (Last Entity) 失败

**解决**：
```cpp
acedUpdateDisplay();
acedCommand(RTNONE);  // Force flush
```

### 问题 3：坐标不正确

**现象**：
- WMF 导入位置错误
- 分解后的图形偏移

**原因**：
- 坐标系转换错误
- 视图范围计算不准确

**解决**：
正确实现 UCS/WCS/DCS 转换链

## 使用说明

### 编译环境

- **平台**：Windows (Win32)
- **编译器**：Visual C++ 2015 或更高
- **SDK**：ObjectARX 2018 或 ZRX (ZWCAD)
- **依赖库**：shlwapi.lib

### 命令注册

```cpp
// 在 acrxEntryPoint.cpp 中注册命令
void initApp()
{
    acedRegCmds->addCommand(
        _T("MYAPP"),
        _T("EXPTXT"),
        _T("EXPTXT"),
        ACRX_CMD_MODAL,
        CTextExplodeWmf::ExportTextCommand);
}

void unloadApp()
{
    acedRegCmds->removeGroup(_T("MYAPP"));
}
```

### 使用步骤

1. 加载 ARX/ZRX 插件
2. 在 CAD 命令行输入 `EXPTXT`
3. 程序自动选择模型空间中所有 TEXT 和 MTEXT
4. 等待处理完成（显示处理数量）
5. 原始文字被替换为几何图形

### 测试建议

```
命令：EXPTXT
Found 10 TEXT entities to process.
Successfully processed 10 text entities.
```

**验证**：
- 检查分解后的图形与原文字一致
- 验证属性（图层、颜色等）是否保留
- 确认原始文字已删除
- 检查临时 WMF 块是否清理

## 性能优化建议

1. **批量处理**：使用事务处理多个文字，减少提交次数
2. **缓存视图范围**：多个文字使用相同的视图范围
3. **临时文件管理**：使用唯一文件名避免冲突
4. **错误恢复**：异常时确保事务正确中止

## 扩展功能建议

- [ ] 支持用户选择特定文字（不仅限模型空间全选）
- [ ] 添加进度条显示处理进度
- [ ] 支持撤销/重做
- [ ] 导出报告（成功/失败数量）
- [ ] 支持保留原始文字的选项
- [ ] 批处理模式（命令行参数）

## 参考资料

- [ObjectARX 开发者指南](https://www.autodesk.com/developer-network/platform-technologies/autocad)
- [GitHub - Forge-ExplodeText (C# 参考实现)](https://github.com/MadhukarMoogala/Forge-ExplodeText)
- [AutoCAD DXF Reference](https://help.autodesk.com/view/OARX/2024/ENU/)
- [Transaction API Documentation](https://help.autodesk.com/view/OARX/2024/ENU/?guid=GUID-8B2D7F19-D766-4B4E-B7F3-F9E6E7F01234)

## 版本历史

### v1.0 (2026-02-12)
- 初始版本
- 支持 TEXT 和 MTEXT 分解
- 使用事务管理避免对象冲突
- 完整的属性继承和清理机制

## 许可证

本代码仅供学习和参考使用。

## 联系方式

- **作者**：JerryMa
- **邮箱**：mazaiguo@zwcad.com
- **项目地址**：[Git Repository]

---

**注意**：本文档基于 ObjectARX/ZRX 开发经验编写，C# 参考代码来自 GitHub 开源项目。
