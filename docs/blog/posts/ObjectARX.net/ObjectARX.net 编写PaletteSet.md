---
title: ObjectARX.net 编写PaletteSet
date: 2024-09-05
categories:
  - CAD开发
  - ObjectARX
  - .NET
tags:
  - ObjectARX
  - PaletteSet
  - AutoCAD
  - 工具面板
description: ObjectARX.net中创建和使用PaletteSet工具面板的详细教程
author: JerryMa
---

# ObjectARX.net 编写PaletteSet

## 创建基础的PaletteSet

```csharp
[Autodesk.AutoCAD.Runtime.CommandMethod("AddMyPaletteSet")]
public void AddMyPaletteSet()
{
    Autodesk.AutoCAD.Windows.PaletteSet myPaletteSet = new Autodesk.AutoCAD.Windows.PaletteSet("我的PallteSet");
    myPaletteSet.Add("我的工具集", new System.Windows.Forms.Control("我的工具集"));   
    myPaletteSet.Add("我的颜色", new System.Windows.Forms.Control("我的颜色")); 
    myPaletteSet.Add("我的控件", new System.Windows.Forms.Control("我的控件"));
    myPaletteSet.Visible = true;
}
```

## 处理每个control

### 新建一个UserControl1

底部用用两个==SplitContainer==将列表分隔成

![image-20240828183841663](http://image.jerryma.xyz//images/20240828-image-20240828183841663.png)

![image-20240828183906696](http://image.jerryma.xyz//images/20240828-image-20240828183906696.png)



`FolderTreeView.cs`

```csharp
 class FolderTreeView
    {
        public static void AddFolderToTree(string folderPath, TreeNode treeNode)
        {
            DirectoryInfo directoryInfo = new DirectoryInfo(folderPath);
            TreeNode[] subTreeNodes = new TreeNode[directoryInfo.GetFiles().Length + directoryInfo.GetDirectories().Length];

            // Add files
            int fileIndex = 0;
            // Add directories
            int directoryIndex = 0;
            foreach (DirectoryInfo subDirectoryInfo in directoryInfo.GetDirectories())
            {
                TreeNode directoryNode = new TreeNode(subDirectoryInfo.Name);
                subTreeNodes[fileIndex + directoryIndex++] = directoryNode;
                AddFolderToTree(subDirectoryInfo.FullName, directoryNode);
            }

            // Add nodes to the tree
            foreach (TreeNode subTreeNode in subTreeNodes)
            {
                if (subTreeNode != null)
                {
                    treeNode.Nodes.Add(subTreeNode);
                }
            }
        }

        public static void DisplayFolderTree(TreeView treeView, string folderPath)
        {
            TreeNode rootNode = treeView.Nodes.Add(Path.GetFileName(folderPath));
            AddFolderToTree(folderPath, rootNode);
        }
    }
```

`UserControl1.cs`

```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace ZwForCdMonolithicPower.Net
{
    public partial class UserControl1 : UserControl
    {
        private string strPath;
        private string strRoot;

        private List<string> imagePathList = new List<string>(); //获取列表图片路径
        public UserControl1(string v)
        {
            InitializeComponent();
            strRoot = "E:\\ShGit\\zwcadgitlab\\digitalminedrawing\\标准对象库\\神东矿图标准对象库\\";
        }

        private void UserControl1_Load(object sender, EventArgs e)
        {
            // 使用方法：
            // treeView1，并且你想显示"C:\MyFolder"目录的内容。
            FolderTreeView.DisplayFolderTree(treeView1, strRoot + "整理后的对象库");
        }

        public static void AddFolderToTree(string folderPath, TreeNode treeNode)
        {
            DirectoryInfo directoryInfo = new DirectoryInfo(folderPath);
            TreeNode[] subTreeNodes = new TreeNode[directoryInfo.GetFiles().Length + directoryInfo.GetDirectories().Length];

            // Add files
            int fileIndex = 0;
            foreach (FileInfo fileInfo in directoryInfo.GetFiles())
            {
                TreeNode fileNode = new TreeNode(fileInfo.Name);
                subTreeNodes[fileIndex++] = fileNode;
            }

            // Add directories
            int directoryIndex = 0;
            foreach (DirectoryInfo subDirectoryInfo in directoryInfo.GetDirectories())
            {
                TreeNode directoryNode = new TreeNode(subDirectoryInfo.Name);
                subTreeNodes[fileIndex + directoryIndex++] = directoryNode;
                AddFolderToTree(subDirectoryInfo.FullName, directoryNode);
            }

            // Add nodes to the tree
            foreach (TreeNode subTreeNode in subTreeNodes)
            {
                if (subTreeNode != null)
                {
                    treeNode.Nodes.Add(subTreeNode);
                }
            }
        }
        public static void DisplayFolderTree(TreeView treeView, string folderPath)
        {
            TreeNode rootNode = treeView.Nodes.Add(Path.GetFileName(folderPath));
            AddFolderToTree(folderPath, rootNode);
        }
        //2.加载数据项：遍历文件和目录，按照不同类型添加数据项Item及其子项
        private void LoadDir(DirectoryInfo dir)
        {
            listView2.BeginUpdate();

            //获取当前目录JPG文件列表 GetFiles获取指定目录中文件的名称(包括其路径)
            FileInfo[] fileInfo = dir.GetFiles("*.png");
            //this.imageList1.ColorDepth = ColorDepth.Depth32Bit;
            this.imageList1.ColorDepth = ColorDepth.Depth32Bit;
            for (int i = 0; i < fileInfo.Length; i++)
            {
                //获取文件完整目录
                string picDirPath = fileInfo[i].FullName;
                //记录图片源路径 双击显示图片时使用
                imagePathList.Add(picDirPath);
                //图片加载到ImageList控件和imageList图片列表
                this.imageList1.Images.Add(Image.FromFile(picDirPath));
            }
            //显示文件列表
            this.listView2.Items.Clear();
            this.listView2.LargeImageList = this.imageList1;
            this.listView2.View = View.LargeIcon;        //大图标显示
            //imageList1.ImageSize = new Size(40, 40);   //不能设置ImageList的图像大小 属性处更改

            //增加图片至ListView控件中
            for (int i = 0; i < imageList1.Images.Count; i++)
            {
                ListViewItem lvi = new ListViewItem();
                lvi.ImageIndex = i;
                lvi.Text = fileInfo[i].Name.Split('.')[0];
                this.listView2.Items.Add(lvi);
            }

            listView2.EndUpdate();
        }

        private void treeView1_AfterSelect(object sender, TreeViewEventArgs e)
        {
            // 获取选中的节点
            TreeNode selectedNode = treeView1.SelectedNode;
            //strNodeName = selectedNode.Text;
            strPath = selectedNode.FullPath;
            listView2.Clear();
            imageList1.Images.Clear();
            LoadDir(new DirectoryInfo(strRoot + strPath));
        }
    }
}

```

`Class1.cs`

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ZwSoft.ZwCAD.Runtime;

namespace ZwForCdMonolithicPower.Net
{
    public class Class1
    {
        [CommandMethod("AddMyPaletteSet")]
        public void AddMyPaletteSet()
        {
            ZwSoft.ZwCAD.Windows.PaletteSet myPaletteSet = new ZwSoft.ZwCAD.Windows.PaletteSet("我的PallteSet");
            myPaletteSet.Add("我的工具集", new UserControl1("我的工具集"));
            myPaletteSet.Add("我的颜色", new System.Windows.Forms.Control("我的颜色"));
            myPaletteSet.Add("我的控件", new System.Windows.Forms.Control("我的控件"));
            myPaletteSet.Visible = true;
        }
    }
}
```



## Cad.Net开发问题：可停靠面板无法使用下拉列表

**问题描述**

在 [AutoCAD](https://so.csdn.net/so/search?q=AutoCAD&spm=1001.2101.3001.7020).Net 开发过程中，可停靠面板（PaletteSet）如果包含下拉列表控件（ComboBox），则下拉列表可能无法正常使用。具体表现为：当 PaletteSet的Dock 属性不为 DockSides.None 时，下拉框会在移动鼠标时自动收回，无法选中。

**解决方案**

该问题可以通过设置 PaletteSet.KeepFocus=True 得到解决。但这样会产生另一个问题：鼠标从面板范围移动到绘图工作区时，工作区无法自动获得焦点，需要单击鼠标才行。这点实际体验很不舒服，每次切换都要点一下绘图区，但当时没有更好的解决方案，只能将就。

**最终解决方案**

后来在翻资料时无意找到解决方案：在ComboBox的下拉事件加入判断就行，示例代码如下：

```csharp
ComboBox _comboBox = new ComboBox();
private void _comboBox_DropDown(object sender, EventArgs e)
{
    if (_set.Dock != DockSides.None)
        _set.KeepFocus = true;
}
private void _comboBox_DropDownClosed(object sender, EventArgs e)
{
    if (_set.Dock != DockSides.None)
        _set.KeepFocus = false;
}
```

其实很简单，捕捉 ComboBox 下拉事件，在下拉时候保持 PaletteSet 的焦点，下拉收回的时候取消焦点。只是当时没想到而已，在这里记录下，以飨来者。

原文部分截图如下：
![http://www.doc88.com/p-9925263869083.html](http://image.jerryma.xyz//images/20240828-a6677c6721b409f078c1c894e1226d0e.png)

* 2020.10.20更新：

  好吧，还有问题，PaletteSet在停靠状态时候，使用Win10系统输入法，快速输入中文时，大概率引发致命错误。取消停靠，或者输入英文，或者使用第三方输入中文，或者慢慢输入法输入中文，都不会引发该问题，奇葩！

  困扰了很久也没找到原因，只能当是未处理的Bug作罢

  后来发现设置==PaletteSet.KeepFocus== 对这个Bug 同样有效，好吧，就是这样

