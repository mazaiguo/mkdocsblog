---
title: CAD.net 处理菜单相关功能
date: 2025-08-18
categories:
  - AutoCAD
  - .NET开发
tags:
  - ObjectARX.net
  - AutoCAD
  - C#
  - CUI
  - 菜单开发
  - 工具栏
description: AutoCAD.net中CUI菜单、工具栏和右键菜单的完整开发指南，包含完整源码示例
authors:
  - JerryMa
---

# CAD.net 处理菜单相关功能

![PixPin_2024-10-24_15-37-38](http://image.mazaiguo.xyz//images/20241024-PixPin_2024-10-24_15-37-38.bmp)

![PixPin_2024-10-24_15-37-56](http://image.mazaiguo.xyz//images/20241024-PixPin_2024-10-24_15-37-56.bmp)

## 增加menu

```csharp
[CommandMethod("AddMenu")]
public void AddMenu()
{
    string currentPath = GetProgramDir();//当前运行目录
    //装载局部CUI文件，若不存在，则创建
    CustomizationSection cs = activeDoc.AddCui(cuiFile, menuGroupName);
    //添加表示绘制直线、多段线、矩形和圆的命令宏            
    cs.AddMacro("直线", "^C^C_Line ", "ID_MyLine", "创建直线段:   LINE", currentPath + "\\Image\\Line.BMP");
    cs.AddMacro("多段线", "^C^C_Pline ", "ID_MyPLine", "创建二维多段线:  PLINE", currentPath + "\\Image\\Polyline.BMP");
    cs.AddMacro("矩形", "^C^C_Rectang ", "ID_MyRectang", "创建矩形多段线:  RECTANG", currentPath + "\\Image\\Rectangle.BMP");
    cs.AddMacro("圆", "^C^C_circle ", "ID_MyCircle", "用指定半径创建圆:   CIRCLE", currentPath + "\\Image\\Circle.BMP");
    //添加表示复制、删除、移动及旋转操作的命令宏
    cs.AddMacro("复制", "^C^CCopy ", "ID_MyCopy", "复制对象:   COPY", currentPath + "\\Image\\Copy.BMP");
    cs.AddMacro("删除", "^C^CErase ", "ID_MyErase", "从图形删除对象:   ERASE", currentPath + "\\Image\\Erase.BMP");
    cs.AddMacro("移动", "^C^CMove ", "ID_MyMove", "将对象在指定方向上平移指定的距离:  MOVE", currentPath + "\\Image\\Move.BMP");
    cs.AddMacro("旋转", "^C^CRotate ", "ID_MyRotate", "绕基点旋转对象:  ROTATE", currentPath + "\\Image\\Rotate.BMP");
    //设置用于下拉菜单别名的字符串集合
    StringCollection sc = new StringCollection();
    sc.Add("MyPop1");
    //添加名为“我的菜单”的下拉菜单，如果已经存在，则返回null
    PopMenu myMenu = cs.MenuGroup.AddPopMenu("我的菜单", sc, "ID_MyMenu");
    if (myMenu != null)//如果“我的菜单”还没有被添加，则添加菜单项
    {
        //从上到下为“我的菜单”添加绘制直线、多段线、矩形和圆的菜单项
        myMenu.AddMenuItem(-1, "直线", "ID_MyLine");
        myMenu.AddMenuItem(-1, "多段线", "ID_MyPLine");
        myMenu.AddMenuItem(-1, "矩形", "ID_MyRectang");
        myMenu.AddMenuItem(-1, "圆", "ID_MyCircle");
        myMenu.AddSeparator(-1);//为菜单添加一分隔条
        //添加一个名为“修改”的子菜单
        PopMenu menuModify = myMenu.AddSubMenu(-1, "修改", "ID_MyModify");
        //从上到下为“修改”子菜单添加复制、删除、移动及旋转操作的菜单项
        menuModify.AddMenuItem(-1, "复制", "ID_MyCopy");
        menuModify.AddMenuItem(-1, "删除", "ID_MyErase");
        menuModify.AddMenuItem(-1, "移动", "ID_MyMove");
        menuModify.AddMenuItem(-1, "旋转", "ID_MyRotate");
    }
    cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
}
```

## 增加toolbar

```cs
[CommandMethod("AddToolbar")]
public void AddToolbar()
{
    //装载局部CUI文件，若不存在，则创建
    CustomizationSection cs = activeDoc.AddCui(cuiFile, menuGroupName);
    //添加名为“我的工具栏”的工具栏
    Toolbar barDraw = cs.MenuGroup.AddToolbar("我的工具栏");
    if (barDraw == null)
        return;
    //为“我的工具栏”添加绘制直线、多段线、矩形和圆的按钮
    barDraw.AddToolbarButton(-1, "直线", "ID_MyLine");
    barDraw.AddToolbarButton(-1, "多段线", "ID_MyPLine");
    barDraw.AddToolbarButton(-1, "矩形", "ID_MyRectang");
    barDraw.AddToolbarButton(-1, "圆", "ID_MyCircle");
    //添加名为“修改工具栏”的工具栏，用于弹出式工具栏
    Toolbar barModify = cs.MenuGroup.AddToolbar("修改工具栏");
    if (barDraw == null)
	{
    	cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
    	return;
	}
    //为“修改工具栏”添加复制、删除、移动及旋转操作的按钮
    ToolbarButton buttonCopy = barModify.AddToolbarButton(-1, "复制", "ID_MyCopy");
    ToolbarButton buttonErase = barModify.AddToolbarButton(-1, "删除", "ID_MyErase");
    ToolbarButton buttonMove = barModify.AddToolbarButton(-1, "移动", "ID_MyMove");
    ToolbarButton buttonRotate = barModify.AddToolbarButton(-1, "旋转", "ID_MyRotate");
    //将“修改工具栏”附着到“我的工具栏”的最后
    barDraw.AttachToolbarToFlyout(-1, barModify);
    //barDraw.ToolbarVisible = ToolbarVisible.show;
    cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
}
```

## 增加右键菜单

```csharp
[CommandMethod("AddDefaultContextMenu")]
public void AddDefaultContextMenu()
{
    //定义一个ContextMenuExtension对象，用于表示快捷菜单
    ContextMenuExtension contextMenu = new ContextMenuExtension();
    contextMenu.Title = "我的快捷菜单";//设置快捷菜单的标题
    MenuItem mi = new MenuItem("复制");//添加名为"复制"的菜单项
    //为"复制"菜单项添加单击事件
    mi.Click += new EventHandler(mi_Click);
    contextMenu.MenuItems.Add(mi);//将"复制"菜单项添加到快捷菜单中
    mi = new MenuItem("删除");//添加名为"删除"的菜单项
    //mi.Icon = new Icon(GetProgramDir() + "\\Image\\copy.ico");
    //为"删除"菜单项添加单击事件
    mi.Click += new EventHandler(mi_Click);
    contextMenu.MenuItems.Add(mi);//将"删除"菜单项添加到快捷菜单中
    //为应用程序添加定义的快捷菜单
    Application.AddDefaultContextMenuExtension(contextMenu);
}
void mi_Click(object sender, EventArgs e)
{
    MenuItem mi = sender as MenuItem;//获取发出命令的快捷菜单项
    //根据快捷菜单项的名字，分别调用对应的命令
    if (mi.Text == "复制")
        activeDoc.SendStringToExecute("_Copy ", true, false, true);
    else if (mi.Text == "删除")
        activeDoc.SendStringToExecute("_Erase ", true, false, true);
}
```

## 完整代码如下所示：

![image-20241024163522376](http://image.mazaiguo.xyz//images/20241024-image-20241024163522376.png)



`Class1.cs`

```csharp
using System;
using System.Collections.Specialized;
using System.IO;
using System.Reflection;
using ZwSoft.ZwCAD.ApplicationServices;
using ZwSoft.ZwCAD.Customization;
using ZwSoft.ZwCAD.DatabaseServices;
using ZwSoft.ZwCAD.EditorInput;
using ZwSoft.ZwCAD.Runtime;
using ZwSoft.ZwCAD.Windows;

namespace CuiDemo
{
    public class Class1
    {
        //设置CUI文件的名字，将其路径设置为当前运行目录
        string cuiFile = GetProgramDir() + "\\MyCustom.cuix";
        string menuGroupName = "MyCustom";//菜单组名
        //获得活动文档
        Document activeDoc = ZwSoft.ZwCAD.ApplicationServices.Core.Application.DocumentManager.MdiActiveDocument;
        public static string GetProgramDir()
        {
            string directory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            return directory;
        }
        public Class1()
        {
            //添加程序退出时事件处理
            Application.QuitWillStart += new EventHandler(Application_QuitWillStart);
        }
        void Application_QuitWillStart(object sender, EventArgs e)
        {
            //由于触发此事件前文档已关闭，所以需通过模板重建，以便命令能够执行
            Document doc = Application.DocumentManager.Add("acadiso.dwt");
            //获取FILEDIA系统变量的值
            object oldFileDia = Application.GetSystemVariable("FILEDIA");
            //设置FILEDIA = 0，禁止显示文件对话框，这样可以通过程序输入文件名
            Application.SetSystemVariable("FILEDIA", 0);
            //获取主CUI
            CustomizationSection mainCs = doc.GetMainCustomizationSection();
            //如果存在指定的局部CUI文件，则进行卸载
            if (mainCs.PartialCuiFiles.Contains(cuiFile))
                doc.Editor.Command("cuiunload " + menuGroupName + " ");
            //doc.SendStringToExecute("cuiunload " + menuGroupName + " ", false, false, false);
            //恢复FILEDIA系统变量的值
            Application.SetSystemVariable("FILEDIA", oldFileDia);
        }
        [CommandMethod("AddMenu")]
        public void AddMenu()
        {
            string currentPath = GetProgramDir();//当前运行目录
            //装载局部CUI文件，若不存在，则创建
            CustomizationSection cs = activeDoc.AddCui(cuiFile, menuGroupName);
            //添加表示绘制直线、多段线、矩形和圆的命令宏            
            cs.AddMacro("直线", "^C^C_Line ", "ID_MyLine", "创建直线段:   LINE", currentPath + "\\Image\\Line.BMP");
            cs.AddMacro("多段线", "^C^C_Pline ", "ID_MyPLine", "创建二维多段线:  PLINE", currentPath + "\\Image\\Polyline.BMP");
            cs.AddMacro("矩形", "^C^C_Rectang ", "ID_MyRectang", "创建矩形多段线:  RECTANG", currentPath + "\\Image\\Rectangle.BMP");
            cs.AddMacro("圆", "^C^C_circle ", "ID_MyCircle", "用指定半径创建圆:   CIRCLE", currentPath + "\\Image\\Circle.BMP");
            //添加表示复制、删除、移动及旋转操作的命令宏
            cs.AddMacro("复制", "^C^CCopy ", "ID_MyCopy", "复制对象:   COPY", currentPath + "\\Image\\Copy.BMP");
            cs.AddMacro("删除", "^C^CErase ", "ID_MyErase", "从图形删除对象:   ERASE", currentPath + "\\Image\\Erase.BMP");
            cs.AddMacro("移动", "^C^CMove ", "ID_MyMove", "将对象在指定方向上平移指定的距离:  MOVE", currentPath + "\\Image\\Move.BMP");
            cs.AddMacro("旋转", "^C^CRotate ", "ID_MyRotate", "绕基点旋转对象:  ROTATE", currentPath + "\\Image\\Rotate.BMP");
            //设置用于下拉菜单别名的字符串集合
            StringCollection sc = new StringCollection();
            sc.Add("MyPop1");
            //添加名为“我的菜单”的下拉菜单，如果已经存在，则返回null
            PopMenu myMenu = cs.MenuGroup.AddPopMenu("我的菜单", sc, "ID_MyMenu");
            if (myMenu != null)//如果“我的菜单”还没有被添加，则添加菜单项
            {
                //从上到下为“我的菜单”添加绘制直线、多段线、矩形和圆的菜单项
                myMenu.AddMenuItem(-1, "直线", "ID_MyLine");
                myMenu.AddMenuItem(-1, "多段线", "ID_MyPLine");
                myMenu.AddMenuItem(-1, "矩形", "ID_MyRectang");
                myMenu.AddMenuItem(-1, "圆", "ID_MyCircle");
                myMenu.AddSeparator(-1);//为菜单添加一分隔条
                //添加一个名为“修改”的子菜单
                PopMenu menuModify = myMenu.AddSubMenu(-1, "修改", "ID_MyModify");
                //从上到下为“修改”子菜单添加复制、删除、移动及旋转操作的菜单项
                menuModify.AddMenuItem(-1, "复制", "ID_MyCopy");
                menuModify.AddMenuItem(-1, "删除", "ID_MyErase");
                menuModify.AddMenuItem(-1, "移动", "ID_MyMove");
                menuModify.AddMenuItem(-1, "旋转", "ID_MyRotate");
            }
            cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
        }
        [CommandMethod("AddToolbar")]
        public void AddToolbar()
        {
            //装载局部CUI文件，若不存在，则创建
            CustomizationSection cs = activeDoc.AddCui(cuiFile, menuGroupName);
            //添加名为“我的工具栏”的工具栏
            Toolbar barDraw = cs.MenuGroup.AddToolbar("我的工具栏");
            if (barDraw == null)
                return;
            //为“我的工具栏”添加绘制直线、多段线、矩形和圆的按钮
            barDraw.AddToolbarButton(-1, "直线", "ID_MyLine");
            barDraw.AddToolbarButton(-1, "多段线", "ID_MyPLine");
            barDraw.AddToolbarButton(-1, "矩形", "ID_MyRectang");
            barDraw.AddToolbarButton(-1, "圆", "ID_MyCircle");
            //添加名为“修改工具栏”的工具栏，用于弹出式工具栏
            Toolbar barModify = cs.MenuGroup.AddToolbar("修改工具栏");
            if (barModify == null)
                return;
            //为“修改工具栏”添加复制、删除、移动及旋转操作的按钮
            ToolbarButton buttonCopy = barModify.AddToolbarButton(-1, "复制", "ID_MyCopy");
            ToolbarButton buttonErase = barModify.AddToolbarButton(-1, "删除", "ID_MyErase");
            ToolbarButton buttonMove = barModify.AddToolbarButton(-1, "移动", "ID_MyMove");
            ToolbarButton buttonRotate = barModify.AddToolbarButton(-1, "旋转", "ID_MyRotate");
            //将“修改工具栏”附着到“我的工具栏”的最后
            barDraw.AttachToolbarToFlyout(-1, barModify);
            //barDraw.ToolbarVisible = ToolbarVisible.show;
            cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
        }
        [CommandMethod("AddDoubleClick")]
        public void AddDoubleClick()
        {
            //装载局部CUI文件，若不存在，则创建
            CustomizationSection cs = activeDoc.AddCui(cuiFile, menuGroupName);
            //添加表示双击多段线动作的命令宏  
            MenuMacro macro = cs.AddMacro("多段线 - 双击", "^C^C_DoubleClickPline ", "ID_PlineDoubleClick", "调用自定义命令", null);
            //创建双击动作
            DoubleClickAction action = new DoubleClickAction(cs.MenuGroup, "优化多段线", -1);
            action.ElementID = "EID_mydblclick";//双击动作的标识号
            //设置双击动作的对象为多段线
            action.DxfName = RXClass.GetClass(typeof(Polyline)).DxfName;
            //创建一个双击命令对象，指定双击对象时执行的命令宏
            DoubleClickCmd cmd = new DoubleClickCmd(action, macro);
            action.DoubleClickCmd = cmd;//指定双击动作的命令对象
            cs.LoadCui();//必须装载CUI文件，才能看到添加的菜单
        }
        [CommandMethod("DoubleClickPline")]
        public void DoubleClickPline()
        {
            Application.ShowAlertDialog("你双击了多段线！");
        }
        [CommandMethod("AddDefaultContextMenu")]
        public void AddDefaultContextMenu()
        {
            //定义一个ContextMenuExtension对象，用于表示快捷菜单
            ContextMenuExtension contextMenu = new ContextMenuExtension();
            contextMenu.Title = "我的快捷菜单";//设置快捷菜单的标题
            MenuItem mi = new MenuItem("复制");//添加名为"复制"的菜单项
            //为"复制"菜单项添加单击事件
            mi.Click += new EventHandler(mi_Click);
            contextMenu.MenuItems.Add(mi);//将"复制"菜单项添加到快捷菜单中
            mi = new MenuItem("删除");//添加名为"删除"的菜单项
            //mi.Icon = new Icon(GetProgramDir() + "\\Image\\copy.ico");
            //为"删除"菜单项添加单击事件
            mi.Click += new EventHandler(mi_Click);
            contextMenu.MenuItems.Add(mi);//将"删除"菜单项添加到快捷菜单中
            //为应用程序添加定义的快捷菜单
            Application.AddDefaultContextMenuExtension(contextMenu);
        }
        void mi_Click(object sender, EventArgs e)
        {
            MenuItem mi = sender as MenuItem;//获取发出命令的快捷菜单项
            //根据快捷菜单项的名字，分别调用对应的命令
            if (mi.Text == "复制")
                activeDoc.SendStringToExecute("_Copy ", true, false, true);
            else if (mi.Text == "删除")
                activeDoc.SendStringToExecute("_Erase ", true, false, true);
        }
        [CommandMethod("AddObjectContextMenu")]
        public void AddObjectContextMenu()
        {
            //定义一个ContextMenuExtension对象，用于表示快捷菜单
            ContextMenuExtension contextMenu = new ContextMenuExtension();
            //添加一个名为"统计个数"的菜单项，用于在AutoCAD命令行上显示所选择实体的个数
            MenuItem miCircle = new MenuItem("统计个数");
            //为"统计个数"菜单项添加单击事件，事件处理函数为调用自定义的Count命令
            miCircle.Click += delegate (object sender, EventArgs e)
            {
                activeDoc.SendStringToExecute("_Count ", true, false, false);
            };
            contextMenu.MenuItems.Add(miCircle);//将"统计个数"菜单项添加到快捷菜单中
            //获得实体所属的RXClass类型
            RXClass rx = RXClass.GetClass(typeof(Entity));
            //为实体对象添加定义的快捷菜单
            Application.AddObjectContextMenuExtension(rx, contextMenu);
        }
        [CommandMethod("Count", CommandFlags.UsePickSet)]
        public void CountEnts()
        {
            Editor ed = activeDoc.Editor;
            PromptSelectionResult result = ed.SelectImplied();
            if (result.Status == PromptStatus.OK)
                ed.WriteMessage("共选择了" + result.Value.Count + "个实体\n");
        }
    }
}
```

`CUITools.cs`

```csharp
using System.Collections.Specialized;
using System.IO;
using ZwSoft.ZwCAD.ApplicationServices;
using ZwSoft.ZwCAD.Customization;

namespace CuiDemo
{
    /// <summary>
    /// 操作CUI的类
    /// </summary>
    public static class CUITools
    {
        [DllImport("zwcad.exe", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Cdecl, EntryPoint = "zcedPostCommand")]
        extern static private int zcedPostCommand(string strExpr);
        /// <summary>
        /// 调用C++的acedPostCommand函数
        /// </summary>
        /// <param name="ed">无意义，只是为了定义扩展函数</param>
        /// <param name="expression">要执行的命令字符串</param>
        public static void PostCommand(this Editor ed, string expression)
        {
            zcedPostCommand(expression);
        }
        /// <summary>
        /// 获取并打开主CUI文件
        /// </summary>
        /// <param name="doc">AutoCAD文档对象</param>
        /// <returns>返回主CUI文件</returns>
        public static CustomizationSection GetMainCustomizationSection(this Document doc)
        {
            //获得主CUI文件所在的位置
            string mainCuiFile=Application.GetSystemVariable("MENUNAME") + ".cuix";
            //打开主CUI文件
            return new CustomizationSection(mainCuiFile);
        }

        /// <summary>
        /// 创建局部CUI文件
        /// </summary>
        /// <param name="doc">AutoCAD文档对象</param>
        /// <param name="cuiFile">CUI文件名</param>
        /// <param name="menuGroupName">菜单组的名称</param>
        /// <returns>返回创建的CUI文件</returns>
        public static CustomizationSection AddCui(this Document doc, string cuiFile, string menuGroupName)
        {
            CustomizationSection cs;//声明CUI文件对象
            if (!File.Exists(cuiFile))//如果要创建的文件不存在
            {
                cs = new CustomizationSection();//创建CUI文件对象
                cs.MenuGroupName = menuGroupName;//指定菜单组名称
                cs.SaveAs(cuiFile);//保存CUI文件
            }
            //如果已经存在指定的CUI文件，则打开该文件
            else cs = new CustomizationSection(cuiFile);
            return cs;//返回CUI文件对象
        }

        /// <summary>
        /// 装载指定的局部CUI文件
        /// </summary>
        /// <param name="cs">CUI文件</param>
        public static void LoadCui(this CustomizationSection cs)
        {
            if (cs.IsModified)
                cs.Save();//如果CUI文件被修改，则保存
            //保存CMDECHO及FILEDIA系统变量
            object oldCmdEcho = Application.GetSystemVariable("CMDECHO");
            object oldFileDia = Application.GetSystemVariable("FILEDIA");
            //设置CMDECHO=0，控制不在命令行上回显提示和输入信息
            Application.SetSystemVariable("CMDECHO", 0);
            //设置FILEDIA=0，禁止显示文件对话框，这样可以通过程序输入文件名
            Application.SetSystemVariable("FILEDIA", 0);
            //获取当前活动文档
            Document doc=Application.DocumentManager.MdiActiveDocument;
            //获取主CUI文件
            CustomizationSection mainCs=doc.GetMainCustomizationSection();

            //如果已存在局部CUI文件，则先卸载
            if (mainCs.PartialCuiFiles.Contains(cs.CUIFileName))
                doc.SendStringToExecute("_.cuiunload " + cs.CUIFileBaseName + " ", false, false, false);
            //装载CUI文件，注意文件名必须是带路径的
            doc.SendStringToExecute("_.cuiload " + cs.CUIFileName + " ", false, false, false);
            //恢复CMDECHO及FILEDIA系统变量的初始值
            doc.SendStringToExecute("(setvar \"FILEDIA\" " + oldFileDia.ToString() + ")(princ) ", false, false, false);
            doc.SendStringToExecute("(setvar \"CMDECHO\" " + oldCmdEcho.ToString() + ")(princ) ", false, false, false);
        }

        /// <summary>
        /// 添加菜单项所要执行的宏
        /// </summary>
        /// <param name="source">CUI文件</param>
        /// <param name="name">宏的显示名称</param>
        /// <param name="command">宏的具体命令</param>
        /// <param name="tag">宏的标识符</param>
        /// <param name="helpString">宏的状态栏提示信息</param>
        /// <param name="imagePath">宏的图标</param>
        /// <returns>返回创建的宏</returns>
        public static MenuMacro AddMacro(this CustomizationSection source, string name, string command, string tag, string helpString, string imagePath)
        {
            MenuGroup menuGroup=source.MenuGroup;//获取CUI文件中的菜单组
            //判断菜单组中是否已经定义与菜单组名相同的宏集合
            MacroGroup mg=menuGroup.FindMacroGroup(menuGroup.Name);
            if (mg == null)//如果宏集合没有定义，则创建一个与菜单组名相同的宏集合
                mg = new MacroGroup(menuGroup.Name, menuGroup);
            //如果已经宏已经被定义，则返回
            foreach (MenuMacro macro in mg.MenuMacros)
            {
                if (macro.ElementID == tag)
                    return null;
            }

            //在宏集合中创建一个命令宏
            MenuMacro MenuMacro=new MenuMacro(mg, name, command, tag);
            //指定命令宏的说明信息，在状态栏中显示
            MenuMacro.macro.HelpString = helpString;
            //指定命令宏的大小图像的路径
            MenuMacro.macro.LargeImage = MenuMacro.macro.SmallImage = imagePath;
            return MenuMacro;//返回命令宏
        }

        /// <summary>
        /// 添加下拉菜单
        /// </summary>
        /// <param name="menuGroup">包含菜单的菜单组</param>
        /// <param name="name">菜单名</param>
        /// <param name="aliasList">菜单的别名</param>
        /// <param name="tag">菜单的标识字符串</param>
        /// <returns>返回下拉菜单对象</returns>
        public static PopMenu AddPopMenu(this MenuGroup menuGroup, string name, StringCollection aliasList, string tag)
        {
            PopMenu pm=null;//声明下拉菜单对象
            //如果菜单组中没有名称为name的下拉菜单
            if (menuGroup.PopMenus.IsNameFree(name))
            {
                //为下拉菜单指定显示名称、别名、标识符和所属的菜单组
                pm = new PopMenu(name, aliasList, tag, menuGroup);
            }
            return pm;//返回下拉菜单对象
        }

        /// <summary>
        /// 为菜单添加菜单项
        /// </summary>
        /// <param name="parentMenu">菜单项所属的菜单</param>
        /// <param name="index">菜单项的位置</param>
        /// <param name="name">菜单项的显示名称</param>
        /// <param name="macroId">菜单项的命令宏的Id</param>
        /// <returns>返回添加的菜单项</returns>
        public static PopMenuItem AddMenuItem(this PopMenu parentMenu, int index, string name, string macroId)
        {
            PopMenuItem newPmi=null;
            //如果存在名为name的菜单项，则返回
            foreach (PopMenuItem pmi in parentMenu.PopMenuItems)
                if (pmi.Name == name) return newPmi;
            //定义一个菜单项对象，指定所属的菜单及位置
            newPmi = new PopMenuItem(parentMenu, index);
            ////如果name不为空，则指定菜单项的显示名为name，否则会使用命令宏的名称
            if (name != null) newPmi.Name = name;
            newPmi.MacroID = macroId;//菜单项的命令宏的ID
            return newPmi;//返回菜单项对象
        }

        /// <summary>
        /// 为下拉菜单添加子菜单
        /// </summary>
        /// <param name="parentMenu">下拉菜单</param>
        /// <param name="index">子菜单的位置</param>
        /// <param name="name">子菜单的显示名称</param>
        /// <param name="tag">子菜单的标识字符串</param>
        /// <returns>返回添加的子菜单</returns>
        public static PopMenu AddSubMenu(this PopMenu parentMenu, int index, string name, string tag)
        {
            PopMenu pm=null;//声明子菜单对象（属于下拉菜单类）
            //如果菜单组中没有名称为name的下拉菜单
            if (parentMenu.CustomizationSection.MenuGroup.PopMenus.IsNameFree(name))
            {
                //为子菜单指定显示名称、标识符和所属的菜单组，别名设为null
                pm = new PopMenu(name, null, tag, parentMenu.CustomizationSection.MenuGroup);
                //为子菜单指定其所属的菜单
                PopMenuRef menuRef=new PopMenuRef(pm, parentMenu, index);
            }
            return pm;//返回子菜单对象
        }

        /// <summary>
        /// 为菜单添加分隔条
        /// </summary>
        /// <param name="parentMenu">下拉菜单</param>
        /// <param name="index">分隔条的位置</param>
        /// <returns>返回添加的分隔条</returns>
        public static PopMenuItem AddSeparator(this PopMenu parentMenu, int index)
        {
            //定义一个分隔条并返回
            return new PopMenuItem(parentMenu, index);
        }

        /// <summary>
        /// 添加工具栏
        /// </summary>
        /// <param name="menuGroup">工具栏所属的菜单组</param>
        /// <param name="name">工具栏的显示名称</param>
        /// <returns>返回添加的工具栏</returns>
        public static Toolbar AddToolbar(this MenuGroup menuGroup, string name)
        {
            Toolbar tb=null;//声明一个工具栏对象
            //如果菜单组中没有名称为name的工具栏
            if (menuGroup.Toolbars.IsNameFree(name))
            {
                //为工具栏指定显示名称和所属的菜单组
                tb = new Toolbar(name, menuGroup);
                //设置工具栏为浮动工具栏
                tb.ToolbarOrient = ToolbarOrient.floating;
                //设置工具栏可见
                tb.ToolbarVisible = ToolbarVisible.show;
            }
            return tb;//返回工具栏对象
        }

        /// <summary>
        /// 向工具栏添加按钮
        /// </summary>
        /// <param name="parent">按钮所属的工具栏</param>
        /// <param name="index">按钮在工具栏上的位置</param>
        /// <param name="name">按钮的显示名称</param>
        /// <param name="macroId">按钮的命令宏的Id</param>
        /// <returns>返回工具栏按钮对象</returns>
        public static ToolbarButton AddToolbarButton(this Toolbar parent, int index, string name, string macroId)
        {
            //创建一个工具栏按钮对象，指定其命令宏Id、显示名称、所属的工具栏和位置
            ToolbarButton button=new ToolbarButton(macroId, name, parent, index);
            return button;//返回工具栏按钮对象
        }

        /// <summary>
        /// 向工具栏添加弹出式工具栏
        /// </summary>
        /// <param name="parent">工具栏所属的父工具栏</param>
        /// <param name="index">弹出式工具栏在父工具栏上的位置</param>
        /// <param name="toolbarRef">弹出式工具栏所引用的工具栏</param>
        public static void AttachToolbarToFlyout(this Toolbar parent, int index, Toolbar toolbarRef)
        {
            //创建一个弹出式工具栏，指定其所属的工具栏和位置
            ToolbarFlyout flyout=new ToolbarFlyout(parent, index);
            //指定弹出式工具栏所引用的工具栏 
            flyout.ToolbarReference = toolbarRef.Name;
            //引用的工具栏初始状态不可见
            toolbarRef.ToolbarVisible = ToolbarVisible.show;
        }
    }
}
```

## 找到PostCommand

### 打开命令行

![image-20241119092752464](http://image.mazaiguo.xyz//images/20241119-image-20241119092752464.png)

### 将目录切换到CAD安装目录

### 运行命令

```bash
dumpbin.exe /exports zwcad.exe >D:\zwcad.txt
```

对照txt中zcedPostCommand的函数，写出如下代码：

```csharp
[DllImport("zwcad.exe", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Cdecl, EntryPoint = "zcedPostCommand")]
extern static private int zcedPostCommand(string strExpr);
/// <summary>
/// 调用C++的acedPostCommand函数
/// </summary>
/// <param name="ed">无意义，只是为了定义扩展函数</param>
/// <param name="expression">要执行的命令字符串</param>
public static void PostCommand(this Editor ed, string expression)
{
    zcedPostCommand(expression);
}
```

