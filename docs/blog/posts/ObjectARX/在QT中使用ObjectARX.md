---
title: 在QT中使用ObjectARX
date: 2024-05-12
categories:
  - QT
  - ObjectARX
  - CPP
tags:
  - QT
  - ObjectARX
  - CAD开发
  - cpp
description: 在QT应用程序中集成和使用ObjectARX的详细实现方法
author: JerryMa
---
`LoadQtDlls.pro`

```cpp
TARGET = QTARXLoadQtDlls
#the sdk include path
INCLUDEPATH += "D:\ObjectARX 2022\inc"
INCLUDEPATH += "D:\ObjectARX 2022\inc-x64"
 
#rxapi.lib; acdb21.lib; acge21.lib; acad.lib; ac1st21.lib; accore.lib;
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -lrxapi
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -lacdb24
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -lacge24
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -lacad
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -lac1st24
LIBS+= -L"D:\ObjectARX 2022\lib-x64" -laccore
 
#DEF_FILE
DEF_FILE += $$PWD/AcRxDefault.def
 
#use md dll
QMAKE_CXXFLAGS += /MD
 
#change .dll to .arx
TARGET_EXT = .arx
 
#remove _DEBUG
DEFINES -= _DEBUG 
DEFINES += _OBJECT_ARX_VERSION_X64_=2022
 
QT       += core
QT       += gui
QT       += widgets
QT       += qml
 
#Qt project template
TEMPLATE = lib
 
SOURCES += this_main.cpp \
    form.cpp
 
RESOURCES += \
    images.qrc
 
DESTDIR = $$PWD/../../release/Autocad2022
 
FORMS += \
    form.ui
 
HEADERS += \
    form.h
```



`main.cpp`

```cpp
#pragma warning( push)
#pragma warning (disable: 4189 4100 )
//#define _AFXDLL
//#define _AFXDLL
#include <Windows.h>
#include <arxHeaders.h>
#include "Dialog.h"
#pragma warning( pop)
#include<QtWidgets/QApplication>
#include <string_view>
#include <iostream>
#include <string>
#include <fstream>
#include <cstring>
#include <string.h>
#include <QString>
#include <QStringList>
#include <QLabel>
#include <stdio.h>
//#include <rxmfcapi.h>
 
//#include <afx.h>
 
 
 
using namespace std::string_literals;
 
#include <QtWidgets>
#include <QtQml>
#include <QMessageBox>
 
struct resbuf* pBuf;
int flag = 0;
int i = 0;
double dCount[10];
namespace {
namespace _cpp_private {
const std::string qtApplicationPath = "123";/*!!!*/
//#if _OBJECT_ARX_VERSION_X64_ == 2018
//            u8R"(D:\Program Files\AutoCAD 2018\acad.exe)"s;
//#else
//            u8R"(D:\Program Files\AutoCAD 2022\AutoCAD 2022\acad.exe)";
//#endif
inline int & getArgc() {
    static int ans;
    ans = 1;
    return ans;
}
inline char** getArgv() {
    static char acadpath[] =u8R"(E:\AutoDesk CAD\AutoCAD 2020\acad.exe)";
    static char *argv[] = { nullptr };
    std::copy(qtApplicationPath.begin(), qtApplicationPath.end(),
              static_cast<char*>(acadpath));
    argv[0] = static_cast<char *>(acadpath);
    return argv;
}
}
}/*namespace*/
 
inline void ShowQtWindow() {
 
    Dialog *p = new Dialog;
    p->setAttribute(Qt::WA_DeleteOnClose);// 应用控件时自动释放
 
    p->show();
 
}
 
 
extern "C" AcRx::AppRetCode
acrxEntryPoint(AcRx::AppMsgCode msg, void* pkt) {
    switch (msg) {
    case AcRx::kInitAppMsg: {
        acrxDynamicLinker->unlockApplication(pkt);
        acrxRegisterAppMDIAware(pkt);
        /*****************************************/
        {
            if (qApp == nullptr) {
                /*create the qt applicaton and never destory it*/
                auto varQtApplication =
                        new QApplication(_cpp_private::getArgc(), _cpp_private::getArgv());
                (void)varQtApplication;
            }
            {
                /*force to load images plugins*/
                QImage varImage{ QString(":/png/this.png") };
                varImage.width();
                varImage.height();
            }
        }
        /*****************************************/
        acedRegCmds->addCommand(
                    L"SSTD_GLOBAL_CMD_GROUP",
                    L"ShowQtWindow",
                    L"ShowQtWindow",
                    ACRX_CMD_MODAL,
                    &ShowQtWindow);
 
 
    }break;
    case AcRx::kUnloadAppMsg: {}break;
    default:break;
    }
    return AcRx::kRetOK;
}
```

`dialog.cpp`

```cpp
#include "dialog.h"
#include "ui_dialog.h"
#include<tchar.h>
 
 
Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    ui->setupUi(this);
    th1 = new xiancheng();
 
    connect(th1,SIGNAL(sendData(int)),this,SLOT(recvData(int)));
    connect(this,SIGNAL(sendAllData(std::string)), th1,SLOT(recvAllData(std::string)));
}
 
Dialog::~Dialog()
{
    delete ui;
}
 
int nCount = 0;
 
 
 
 
std::string g_sAllData = "";
/*获得实体数据 实际为非扩展数据*/
void Dialog::on_pushButton_4_clicked(){
 
    dataSize_T data;
    data.str = "56789";
    data.nSize = data.str.length();
 
 
         ads_name ename;
         if(acedSSGet(NULL,NULL,NULL,NULL,ename) ==RTNORM ){
 
         int nLenth;
         acedSSLength(ename,&nLenth);
         acutPrintf(TEXT("\n select sets count is :%d"),nLenth);
 
         ui->textEdit_3->setText("\n aha The Following Content is Total Data:");
         for(int y=0; y<nLenth; y++){
             ads_name entres;
             acedSSName(ename,y,entres);    //将获取的名字放入entres.
             AcDbObjectId entid;
             acdbGetObjectId(entid,entres);
 
             ads_name entName;
             acdbGetAdsName(entName,entid);
 
             int rt, i;
             ads_point pt;
             struct resbuf *rbEnt; // 保存实体数据的结果缓冲区
             struct resbuf* pBuf;
 
//                 if(acedEntSel(TEXT("\n请选择实体："),entName,pt)){
//                 }
                 rbEnt =acdbEntGet(entName);
                 pBuf = rbEnt;
                 TCHAR buf[133];
 
                 for (i = 0; pBuf != NULL; i++, pBuf = pBuf->rbnext) {
                     if (pBuf->restype < 0)
                         rt = pBuf->restype;
                     else if (pBuf->restype < 10)
                         rt = RTSTR;
                     else if (pBuf->restype < 38)
                         rt = RT3DPOINT;
                     else if (pBuf->restype < 60)
                         rt = RTREAL;
                     else if (pBuf->restype < 80)
                         rt = RTSHORT;
                     else if (pBuf->restype < 100)
                         rt = RTLONG;
                     else if (pBuf->restype < 106)
                         rt = RTSTR;
                     else if (pBuf->restype < 148)
                         rt = RTREAL;
                     else if (pBuf->restype < 290)
                         rt = RTSHORT;
                     else if (pBuf->restype < 330)
                         rt = RTSTR;
                     else if (pBuf->restype < 370)
                         rt = RTENAME;
                     else if (pBuf->restype < 999)
                         rt = RT3DPOINT;
                     else
                         rt = pBuf->restype;
 
                     switch (rt) {
                     case RTSHORT:
                         if (pBuf->restype == RTSHORT){
                             acutPrintf(TEXT("RTSHORT : %d\n"),
                                            pBuf->resval.rint);
                             ui->textEdit_3->append(QStringLiteral("\n RTSHORT:")+ ',' +(QString::number(pBuf->resval.rint)));
                             g_sAllData += QString::number(pBuf->resval.rint).toStdString() + '\n';
                         }
                         else{
                             acutPrintf(TEXT("(%d . %d)\n"), pBuf->restype,
                                            pBuf->resval.rint);
                             ui->textEdit_3->append(QStringLiteral("\n RTSHORT:") + ',' + (QString::number(pBuf->restype)) + ',' + (QString::number(pBuf->resval.rint)));
                             g_sAllData += QString::number(pBuf->restype).toStdString() + '\n';
                             g_sAllData += QString::number(pBuf->resval.rint).toStdString() + '\n';
                         }
                         break;
                     case RTREAL:
                         if (pBuf->restype == RTREAL){
                             acutPrintf(TEXT("RTREAL : %0.3f\n"),
                                            pBuf->resval.rreal);
                             ui->textEdit_3->append(QStringLiteral("\n RTREAL:") + ',' + QString::number(pBuf->resval.rreal,'f',2));
                             g_sAllData += QString::number(pBuf->resval.rreal).toStdString() + '\n';
                         }
                         else{
                             acutPrintf(TEXT("(%d . %0.3f)\n"), pBuf->restype,
                                               pBuf->resval.rreal);
                              ui->textEdit_3->append(QStringLiteral("\n RTREAL:") + ',' + QString::number(pBuf->restype) + ',' + QString::number(pBuf->resval.rreal,'f',2));
                              g_sAllData += QString::number(pBuf->restype).toStdString()  + '\n';
                              g_sAllData += QString::number(pBuf->resval.rreal).toStdString() + '\n';
                         }
                         break;
                     case RTSTR:
                         if (pBuf->restype == RTSTR){
                             acutPrintf(TEXT("RTSTR : %s\n"),
                                        pBuf->resval.rstring);
                              ui->textEdit_3->append(QStringLiteral("\n RTSTR:") + ',' + QString::fromWCharArray(pBuf->resval.rstring));
                              g_sAllData +=  QString::fromWCharArray(pBuf->resval.rstring).toStdString() + '\n';
                         }
                         else{
                             acutPrintf(TEXT("(%d . \"%s\")\n"), pBuf->restype,
                                             pBuf->resval.rstring);
                             ui->textEdit_3->append(QStringLiteral("\n RTREAL:") + ',' + QString::number(pBuf->restype) + ',' + QString::fromWCharArray(pBuf->resval.rstring));
                             g_sAllData += QString::number(pBuf->restype).toStdString() + '\n';
                             g_sAllData += QString::fromWCharArray(pBuf->resval.rstring).toStdString() + '\n';
                         }
                         break;
                     case RT3DPOINT:
                         if (pBuf->restype == RT3DPOINT){
                             acutPrintf(
                                 TEXT("RT3DPOINT : %0.3f, %0.3f, %0.3f\n"),
                                 pBuf->resval.rpoint[X],
                                 pBuf->resval.rpoint[Y],
                                 pBuf->resval.rpoint[Z]);
                             QString pop = QString::number( pBuf->resval.rpoint[X],'f',2);
 
                            ui->textEdit_3->append(QStringLiteral("\n RT3DPOINT:") + ',' + QString::number(pBuf->resval.rpoint[X],'f',2) + ',' + QString::number(pBuf->resval.rpoint[Y],'f',2) + ',' + QString::number(pBuf->resval.rpoint[Z],'f',2));
                            g_sAllData += QString::number(pBuf->resval.rpoint[X]).toStdString() + '\n';
                            g_sAllData += QString::number(pBuf->resval.rpoint[Y]).toStdString() + '\n';
                            g_sAllData += QString::number(pBuf->resval.rpoint[Z]).toStdString() + '\n';
                         }
                         else{
                             acutPrintf(
                                 TEXT("(%d %0.3f %0.3f %0.3f)\n"),
                                 pBuf->restype,
                                 pBuf->resval.rpoint[X],
                                 pBuf->resval.rpoint[Y],
                                 pBuf->resval.rpoint[Z]);
                             ui->textEdit_3->append(QStringLiteral("\n RT3DPOINTTwo:") + ',' + QString::number(pBuf->restype,'f',2) + ',' + QString::number(pBuf->resval.rpoint[X],'f',2) + ',' + QString::number(pBuf->resval.rpoint[Y],'f',2) + ',' + QString::number(pBuf->resval.rpoint[Z],'f',2));
                             g_sAllData += QString::number(pBuf->restype).toStdString() + '\n';
                             g_sAllData += QString::number(pBuf->resval.rpoint[X]).toStdString() + '\n';
                             g_sAllData += QString::number(pBuf->resval.rpoint[Y]).toStdString() + '\n';
                             g_sAllData += QString::number(pBuf->resval.rpoint[Z]).toStdString() + '\n';
                         }
                         break;
                     case RTLONG:
                         acutPrintf(TEXT("RTLONG : %d\n"),
                                        pBuf->resval.rlong);
                         ui->textEdit_3->append(QStringLiteral("\n RTLONG:") + QString::number(pBuf->resval.rlong));
                         g_sAllData += QString::number(pBuf->resval.rlong).toStdString() + '\n';
                         break;
                     case -1:
                     case RTENAME:
                         acutPrintf(TEXT("(%d<Entity name:>)\n"),
                                     pBuf->restype, pBuf->resval.rlname[0]);
                         ui->textEdit_3->append(QStringLiteral("\n <Entity name: %x>:") + ',' + QString::number(pBuf->resval.rlname[0],16));
                         g_sAllData +=  QString::number(pBuf->resval.rlname[0]).toStdString() + '\n';
                         break;
                     case -3:
                         acutPrintf(TEXT("(-3)\n"));
                         ui->textEdit_3->append("(-3)");
                         g_sAllData += "(-3)" + '\n';
                     }
 
                     if ((i == 23) && (pBuf->rbnext != NULL)) {
                         i = 0;
                         acedGetString(0,
                             TEXT("Press <ENTER> to continue..."), buf);
                     }
                 }
 
         }
    }
    emit sendAllData(g_sAllData);
    g_sAllData = "";
    return;
 
}
/*连接服务器*/
void Dialog::on_pushButton_clicked(){
 
 
    th1->start();
    acutPrintf(TEXT("i am Client"));
}
 
void Dialog::recvData(int data){
 
    nCount = data;
 
}
void Dialog::on_pushButton_2_clicked(){
 
    acutPrintf(TEXT("\n nCount:%d"),nCount);
}
void Dialog::on_pushButton_3_clicked(){
 
    //emit sendAllData(g_sAllData);
}
```

`dialog.h`

```cpp
#ifndef DIALOG_H
#define DIALOG_H
 
#include <QDialog>
#include <Windows.h>
#include <arxHeaders.h>
#include <acedCmdNF.h>
 
#include "xiancheng.h"
 
 
namespace Ui {
class Dialog;
}
 
class Dialog : public QDialog
{
    Q_OBJECT
 
public:
 
    explicit Dialog(QWidget *parent = nullptr);
    ~Dialog();
 
signals:
 
    void sendAllData(std::string data);
 
 
private slots:
 
    void recvData(int data);
 
    void on_pushButton_4_clicked();
 
    void on_pushButton_clicked();
 
    void on_pushButton_2_clicked();
 
    void on_pushButton_3_clicked();
 
private:
    Ui::Dialog *ui;
 
    xiancheng* th1;
 
 
 
};
 
#endif // DIALOG_H
```

`xiancheng.h`

```cpp
#ifndef XIANCHENG_H
#define XIANCHENG_H
 
#include <QThread>
#include <QDebug>
 
#include <string>
#include <Windows.h>
#include <winsock.h>
#include <arxHeaders.h>
#include <acedCmdNF.h>
#include <tchar.h>
 
typedef struct data_T{
 
   int nSize;
   std::string str;
}dataSize_T;
 
class xiancheng:public QThread
{
    Q_OBJECT
public:
    xiancheng();
 
    void run();
signals:
    void sendData(int data);
 
private slots:
 
    void recvAllData(std::string data);
};
 
#endif // XIANCHENG_H
```

`xiancheng.cpp`

```cpp
#include "xiancheng.h"
xiancheng::xiancheng()
{
 
}
int nRnt = 99;
std::string g_sDxfData = "";
 
 
char cBuff[50];
 
 
void xiancheng::run(){
 
    char cPop[100];
 
    char sBuff[20]={'0','1','2','3','4','5','6','7','8','9'};
    std::string str = "123456789";
    char sBuffLenth[5];
    std::string sSum = "";
 
    int nClientSock = socket(AF_INET, SOCK_STREAM, 0);
 
    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof (serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(写端口);
    serverAddr.sin_addr.s_addr = inet_addr("写IP地址");
 
    int nRet = ::connect(nClientSock, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    if(nRet < 0){
 
    }
         itoa(g_sDxfData.length(),cPop,10);
         int nLenths = send(nClientSock, cPop, sizeof(cPop), 0);
         if(nLenths > 0){
 
         }
         nRnt = send(nClientSock, g_sDxfData.c_str(), g_sDxfData.length(), 0);
         acutPrintf(TEXT("Socket send data to Service"));
         emit sendData( g_sDxfData.length());
         g_sDxfData = "";
         if(nRnt < 0){
         }
         else{
 
         }
 
}
 
void xiancheng::recvAllData(std::string data){
 
        g_sDxfData = data;
        acutPrintf(TEXT("CAD recv all DXF data"));
        //memcpy(cBuff,&data,sizeof(data));
}
```

```cpp
// 自定义的PaletteSet类
class QtPaletteSet : public QWidget {
public:
    QtPaletteSet(QWidget* parent = nullptr) : QWidget(parent) {
        setupUi();
    }

private:
    void setupUi() {
        // 创建调色板集（使用QTabWidget模拟）
        QTabWidget* paletteSet = new QTabWidget(this);

        // 创建第一个调色板
        QWidget* palette1 = new QWidget(paletteSet);
        QVBoxLayout* layout1 = new QVBoxLayout(palette1);
        // 这里可以添加更多的Qt控件到调色板1中
        paletteSet->addTab(palette1, "Palette 1");

        // 创建第二个调色板
        QWidget* palette2 = new QWidget(paletteSet);
        QVBoxLayout* layout2 = new QVBoxLayout(palette2);
        // 这里可以添加更多的Qt控件到调色板2中
        paletteSet->addTab(palette2, "Palette 2");

        // 将调色板集添加到主布局中
        QVBoxLayout* mainLayout = new QVBoxLayout(this);
        mainLayout->addWidget(paletteSet);
    }
};

// ObjectARX命令函数
void ShowQtPaletteSet() {
    if (!qtApp) {
        int argc = 0;
        char** argv = nullptr;
        qtApp = new QApplication(argc, argv);
    }

    // 创建PaletteSet窗口
    QtPaletteSet* paletteSetWidget = new QtPaletteSet();
    paletteSetWidget->setWindowTitle("Qt PaletteSet in AutoCAD");
    paletteSetWidget->resize(300, 400);

    // 显示窗口
    paletteSetWidget->show();

    // 处理Qt事件
    qtApp->processEvents();
}
```

```cpp
// 显示Qt DockBar的函数
void ShowQtDockBar() {
    if (!qtApp) {
        int argc = 0;
        char** argv = nullptr;
        qtApp = new QApplication(argc, argv);
    }

    // 获取AutoCAD主窗口句柄
    HWND acadMainWindow = ::GetForegroundWindow();
    if (!acadMainWindow) {
        acutPrintf(L"\nFailed to get AutoCAD main window handle.");
        return;
    }

    // 将HWND转换为QWidget
    QWidget* acadMainWidget = QWidget::createWindowContainer(QWindow::fromWinId((WId)acadMainWindow));

    // 创建DockWidget
    QDockWidget* dockWidget = new QDockWidget("My DockBar", acadMainWidget);
    dockWidget->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);

    // 创建DockWidget的内容
    QWidget* dockContent = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(dockContent);
    QLabel* label = new QLabel("This is a Qt DockBar", dockContent);
    layout->addWidget(label);
    dockWidget->setWidget(dockContent);

    // 将DockWidget添加到主窗口
    acadMainWidget->layout()->addWidget(dockWidget);

    // 显示DockWidget
    dockWidget->show();

    // 处理Qt事件
    qtApp->processEvents();
}
```

