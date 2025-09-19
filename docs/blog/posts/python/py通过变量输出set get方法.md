---
title: Python通过变量输出setter getter方法
date: 2024-03-15
categories:
  - Python
  - 编程技巧
tags:
  - Python
  - setter
  - getter
  - 代码生成
description: Python脚本实现通过变量名自动生成setter和getter方法的实用工具
author: JerryMa
---

# python通过传入的变量生成setter getter方法

代码如下所示：

```python
import sys
import os
import subprocess
import platform

# 获取当前目录
current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))


def camel_case_split(identifier):
    components = identifier.split("_")
    return "".join(x.title() for x in components)


def create_getter_setter(input_string, class_name):
    lines = input_string.strip().split("\n")
    data = []
    hppFunctionRows = []
    cppContents = []
    variable_names = []
    print("\n")

    type_config = {
        "int": {"prefix": "m_n", "initValue": "0"},
        "double": {"prefix": "m_d", "initValue": "0.0"},
        "CString": {"prefix": "m_str", "initValue": '_T("")'},
        "bool": {"prefix": "m_b", "initValue": "false"},
        "AcGePoint3d": {"prefix": "m_pt", "initValue": "AcGePoint3d::kOrigin"},
        "AcGeMatrix3d": {"prefix": "m_mat", "initValue": "AcGeMatrix3d::kIdentity"},
        "AcGeVector2d": {"prefix": "m_vec", "initValue": "AcGeVector2d::kXAxis"},
        "AcGeVector3d": {"prefix": "m_vec", "initValue": "AcGeVector3d::kXAxis"},
        "AcGePoint2d": {"prefix": "m_pt", "initValue": "AcGePoint2d::kOrigin"},
        # 默认配置cle
        "default": {"prefix": "m_", "initValue": "nullptr"},
    }
    try:
        for line in lines:
            line = line.strip()
            var_comment = "" if "//" not in line else line.split("//")[1].strip()
            var_declaration = line.split("//")[0].strip()

            var_type, var_name = var_declaration.split()[:2]
            var_name = var_name.replace(";", "")

            # 使用配置化处理
            prefix, initValue = type_config.get(
                var_type, type_config["default"]
            ).values()

            method_suffix = camel_case_split(
                var_name.split(prefix)[1] if prefix in var_name else var_name
            )

            init = f"{var_name}({initValue}),//{var_comment}"
            variable_names.append(init)

            getter_method = (
                f"//获取{var_comment}\n"
                f"{var_type} {class_name}::get{method_suffix}() const\n"
                "{\n"
                f"    return {var_name};\n"
                "}\n"
            )
            cppContents.append(getter_method)

            setter_method = (
                f"//设置{var_comment}\n"
                f"void {class_name}::set{method_suffix}({var_type} value)\n"
                "{\n"
                f"    {var_name} = value;\n"
                "}\n"
            )
            cppContents.append(setter_method)

            function_name = (
                f"//获取{var_comment}\n"
                f"{var_type} get{method_suffix}() const;\n"
                f"//设置{var_comment}\n"
                f"void set{method_suffix}({var_type} value);\n"
            )
            hppFunctionRows.append(function_name)

            row = f"{var_name} = other.get{method_suffix}();//获取{var_comment}\n"
            data.append(row)

    except Exception as e:
        print(e)
        return

    # 构造函数
    operate_method = (
        f"//构造函数\n"
        f"{class_name}& {class_name}::operator=(const {class_name}& other)\n"
        "{\n"
        f"  if (this != &other)\n"
        "   {\n"
        f"{''.join(data)}\n"
        "   }\n"
        f"  return *this;\n"
        "}\n"
    )
    cppContents.append(operate_method)

    # 异常处理增强
    try:
        # 检查列表是否不为空并且最后一个元素包含逗号
        variable_names = dealwithListInfo(variable_names)

        with open(f"{current_directory}/{class_name}.md", "w", encoding="utf-8") as f:
            f.write("* 初始化列表信息\n")
            f.write("```cpp\n")
            for i in variable_names:
                f.write(i + "\n")
            f.write("```\n")
            f.write("* 头文件信息\n")
            f.write("```cpp\n")
            f.write("".join(hppFunctionRows))
            # for i in hppFunctionRows:
            #     f.write(i+ "\n")
            f.write(f"{class_name}& operator=(const {class_name}& other);\n")
            f.write("private:\n")
            for line in lines:
                f.write(line + "\n")
            f.write("```\n")
            f.write("* cpp函数信息\n")
            f.write("```cpp\n")
            f.write("".join(cppContents))
            f.write("```\n")

    except IOError as e:
        print(f"文件操作失败: {e}")

    print("生成初始化列表\n")
    for i in variable_names:
        print(i)
    # 打开文件

    # 根据操作系统打开目录
    fileName = current_directory + "\\" + class_name + ".md"
    # 处理windows中的反斜杠
    if platform.system() == "Windows":
        subprocess.run(["explorer", fileName])
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", fileName])
    else:  # Assuming Linux or other Unix-like systems
        subprocess.run(["xdg-open", fileName])


# 示例输入
input_string1 = """int m_nShaft_diameter_row;            //轴径行
int m_nShaft_diameter_col;            //轴径列
double m_dShaft_diameter;                  //轴径 d1
double m_dCavity_diameter;                 //腔体直径 D
double m_dHole_depth;                      //高度 b
CString m_strInfo;//信息相关
"""


def dealwithListInfo(my_list):
    # 检查列表是否不为空并且最后一个元素包含逗号
    if my_list and "," in my_list[-1]:
        # 将最后一个元素转化为字符串（保证它是字符串格式）
        last_element = str(my_list[-1])
        # 查找最后一个逗号的位置
        last_comma_index = last_element.rfind(",")
        # 当找到最后一个逗号时
        if last_comma_index != -1:
            # 仅删除这个逗号：创造一个没有最后一个逗号的新字符串
            my_list[-1] = (
                last_element[:last_comma_index] + last_element[last_comma_index + 1 :]
            )
        return my_list


if __name__ == "__main__":
    print(
        "请输入变量定义的字符串,每行一个变量定义,结束后请按Ctrl+Z(Windows)或Ctrl+D(Linux/macOS)并回车:"
    )
    input_string = ""
    try:
        while True:
            line = input()
            input_string += line + "\n"
    except EOFError:  # 当用户结束输入时（Ctrl+D/Linux/macOS, Ctrl+Z/Windows）
        pass

    class_name = input("请输入类名：")
    if class_name == "":
        class_name = "CTableParameterInfo"
    create_getter_setter(input_string, class_name)
```

结果如下所示：

```cpp
生成初始化列表

m_nShaft_diameter_row(0),//轴径行   
m_nShaft_diameter_col(0),//轴径列   
m_dShaft_diameter(0.0),//轴径 d1    
m_dCavity_diameter(0.0),//腔体直径 D
m_dHole_depth(0.0),//高度 b
m_strInfo(_T("")),//信息相关    

//CTableParameterInfo.h
//获取轴径行
int CTableParameterInfo::getShaftDiameterRow() const;
//设置轴径行
void setShaftDiameterRow(int value);
//获取轴径列
int CTableParameterInfo::getShaftDiameterCol() const;
//设置轴径列
void setShaftDiameterCol(int value);
//获取轴径 d1
double CTableParameterInfo::getShaftDiameter() const;
//设置轴径 d1
void setShaftDiameter(double value);
//获取腔体直径 D
double CTableParameterInfo::getCavityDiameter() const;
//设置腔体直径 D
void setCavityDiameter(double value);
//获取高度 b
double CTableParameterInfo::getHoleDepth() const;
//设置高度 b
void setHoleDepth(double value);
//获取信息相关
CString CTableParameterInfo::getInfo() const;
//设置信息相关
void setInfo(CString value);
CTableParameterInfo& operator=(const CTableParameterInfo& other);
private:
int m_nShaft_diameter_row;            //轴径行
	int m_nShaft_diameter_col;            //轴径列
	double m_dShaft_diameter;                  //轴径 d1
	double m_dCavity_diameter;                 //腔体直径 D
	double m_dHole_depth;                      //高度 b
    CString m_strInfo;//信息相关

//CTableParameterInfo.cpp
//获取轴径行
int CTableParameterInfo::getShaftDiameterRow() const
{
    return m_nShaft_diameter_row;
}
//设置轴径行
void CTableParameterInfo::setShaftDiameterRow(int value)
{
    m_nShaft_diameter_row = value;
}
//获取轴径列
int CTableParameterInfo::getShaftDiameterCol() const
{
    return m_nShaft_diameter_col;
}
//设置轴径列
void CTableParameterInfo::setShaftDiameterCol(int value)
{
    m_nShaft_diameter_col = value;
}
//获取轴径 d1
double CTableParameterInfo::getShaftDiameter() const
{
    return m_dShaft_diameter;
}
//设置轴径 d1
void CTableParameterInfo::setShaftDiameter(double value)
{
    m_dShaft_diameter = value;
}
//获取腔体直径 D
double CTableParameterInfo::getCavityDiameter() const
{
    return m_dCavity_diameter;
}
//设置腔体直径 D
void CTableParameterInfo::setCavityDiameter(double value)
{
    m_dCavity_diameter = value;
}
//获取高度 b
double CTableParameterInfo::getHoleDepth() const
{
    return m_dHole_depth;
}
//设置高度 b
void CTableParameterInfo::setHoleDepth(double value)
{
    m_dHole_depth = value;
}
//获取信息相关
CString CTableParameterInfo::getInfo() const
{
    return m_strInfo;
}
//设置信息相关
void CTableParameterInfo::setInfo(CString value)
{
    m_strInfo = value;
}
//构造函数
CTableParameterInfo& CTableParameterInfo::operator=(const CTableParameterInfo& other)
{
  if (this != &other)
   {
m_nShaft_diameter_row = other.getShaftDiameterRow();//获取轴径行
m_nShaft_diameter_col = other.getShaftDiameterCol();//获取轴径列
m_dShaft_diameter = other.getShaftDiameter();//获取轴径 d1
m_dCavity_diameter = other.getCavityDiameter();//获取腔体直径 D
m_dHole_depth = other.getHoleDepth();//获取高度 b
m_strInfo = other.getInfo();//获取信息相关

   }
  return *this;
}

```

