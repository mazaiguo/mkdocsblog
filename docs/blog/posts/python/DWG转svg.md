---
title: DWG转SVG
date: 2024-05-22
categories:
  - windows程序
tags:
  - DWG
  - SVG
  - ezdxf
  - CAD转换
description: 使用Python和ezdxf库将DWG文件转换为SVG格式的详细实现方法
author: JerryMa
---

# DWG转svg

## 安装软件

ezdxf不支持处理dwg文件，那么就需要使用[oda_file_converter](https://www.opendesign.com/guestfiles/oda_file_converter)

## 安装python插件

```python
pip install pydantic ezdxf
```

## 代码

将dwg转成svg

```python
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing import layout, svg
from ezdxf.addons import odafc
# 通过修改win_exec_path的值为自定义安装路径
odafc.win_exec_path = r'C:\\Program Files\\ODA\\ODAFileConverter 25.5.0\\ODAFileConverter.exe'

def convert_dwg_to_svg(dxf_path, svg_path):
    doc = odafc.readfile(dxf_path)
    msp = doc.modelspace()
    # 1. create the render context
    context = RenderContext(doc)
    # 2. create the backend
    backend = svg.SVGBackend()
    # 3. create the frontend
    frontend = Frontend(context, backend)
    # 4. draw the modelspace
    frontend.draw_layout(msp)
    # 5. create an A4 page layout, not required for all backends
    page = layout.Page(64, 64, layout.Units.mm, margins=layout.Margins.all(20))
    # 6. get the SVG rendering as string - this step is backend dependent
    svg_string = backend.get_string(page)
    with open(svg_path, "wt", encoding="utf8") as fp:
        fp.write(svg_string)

if __name__ == '__main__':
    filePath = 'D:\\Test\\'
    dwg_path = filePath + '5000报废矩形立井.dwg'
    svg_path = filePath + '5000报废矩形立井11.svg'
    convert_dwg_to_svg(dwg_path, svg_path)
```

完整代码如下所示：

```python
from ezdxf.addons.drawing import Frontend, RenderContext, pymupdf, layout, svg, config
from ezdxf.addons import odafc
import configparser
import sys
import os
from PIL import Image

# 通过修改win_exec_path的值为自定义安装路径
odafc.win_exec_path = (
    r"C:\\Program Files\\ODA\\ODAFileConverter 25.5.0\\ODAFileConverter.exe"
)

# 自定义config解析
class myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        """
        初始化ConfigParser类的实例。
        通过调用父类configparser.ConfigParser的构造方法，初始化配置解析器实例。
        该构造方法允许指定默认配置值，这些值将在读取配置文件之前提供基本的配置项。
        参数:
        - defaults: 可选参数，字典类型，提供基本的配置项和值。如果未提供，将使用父类的默认设置。
        """
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr

    def write(self, fp):
        """
        将配置数据写入指定的文件指针。
        参数:
        - fp: 文件指针，用于写入配置数据。
        该方法首先检查是否有默认配置，默认配置是 configparser 模块的特殊部分。
        如果有默认配置，它将写入一个包含默认值的部分。
        然后，它遍历所有部分，为每个部分写入对应的键值对。
        """
        # 检查是否有默认配置，如果有，则写入默认配置部分
        if self._defaults:
            fp.write("[%s]\n" % configparser.DEFAULTSECT)
        # 遍历默认配置，写入每个键值对
        for key, value in self._defaults.items():
            if key.strip():
                fp.write("%s=%s\n" % (key, str(value).replace("\n", "\n\t")))
                # fp.write("\n")
        # 遍历所有部分，写入每个部分及其键值对
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for key, value in self._sections[section].items():
                if key == "__name__":
                    continue
                # 添加一行key为空的代码
                if (value is not None) or (self._optcre == self.OPTCRE):
                    if key.strip():
                        key = "=".join((key, str(value).replace("\n", "\n\t")))
                        fp.write("%s\n" % (key))
            fp.write("\n")


# 获取同一目录下的所有dwg文件的绝对路径
def getFileName(filedir):
    """
    获取指定目录下所有以"dwg"为后缀的文件的绝对路径列表。
    参数:
    filedir: str - 文件目录的路径。
    返回:
    List[str] - 包含所有符合条件的文件的绝对路径的列表，如果没有找到任何文件，则返回空列表。
    """
    # 使用列表推导式和os.walk遍历指定目录及其子目录，查找所有以"dwg"结尾的文件
    # os.path.join用于拼接文件的绝对路径
    file_list = [
        os.path.join(root, filespath)
        for root, dirs, files in os.walk(filedir)
        for filespath in files
        if str(filespath).endswith("dwg")
    ]
    # 如果file_list不为空，则返回file_list，否则返回空列表
    return file_list if file_list else []


# 获取当前脚本目录
def get_current_file_path():
    # 通过命令行参数获取当前脚本的绝对路径
    abs_file = sys.argv[0]
    # 将路径中的斜杠替换为反斜杠，以适应Windows系统
    windows_path = abs_file.replace("/", "\\")
    # 去除路径中的脚本文件名，仅保留目录部分
    windows_path = windows_path[: windows_path.rfind("\\")]
    # 返回脚本所在的目录路径
    return windows_path


# 用于将DXF格式的文件转换为指定格式的图像文件
def convert_dxf_to_image(
    dxf_path, output_file_name, width=64, height=64, backgroundtype=0, file_suffix="pdf"
):
    try:
        doc = odafc.readfile(dxf_path)
    except odafc.DXFStructureError as e:
        print(f"DXF Structure Error in file {dxf_path}: {e}")
        return
    except FileNotFoundError:
        print(f"File not found: {dxf_path}")
        return
    except PermissionError:
        print(f"Permission denied for file: {dxf_path}")
        return
    except Exception as e:
        print(f"Error reading file {dxf_path}: {e}")
        return
    msp = doc.modelspace()
    # 创建渲染上下文
    context = RenderContext(doc)
    # 创建后端
    backend = pymupdf.PyMuPdfBackend()
    # 创建前端
    # 定义一个字典来映射 backgroundtype 到对应的 BackgroundPolicy
    policy_map = {
        0: config.BackgroundPolicy.DEFAULT,
        1: config.BackgroundPolicy.BLACK,
        2: config.BackgroundPolicy.WHITE,
        3: config.BackgroundPolicy.CUSTOM,
        4: config.BackgroundPolicy.PAPERSPACE,
        5: config.BackgroundPolicy.MODELSPACE,
        6: config.BackgroundPolicy.OFF,
    }
    # 使用 try-except 来处理可能出现的 KeyError 异常
    try:
        background_policy = policy_map[backgroundtype]
    except KeyError:
        # 如果 backgroundtype 不在预定义的映射中，则使用默认策略
        background_policy = config.BackgroundPolicy.DEFAULT
        print("Warning: Invalid backgroundtype. Using default policy.")

    # 创建 Configuration 对象
    cfg = config.Configuration(background_policy=background_policy)
    # 初始化 Frontend 实例
    frontend = Frontend(context, backend, config=cfg)
    # 绘制模型空间
    frontend.draw_layout(msp)
    # 创建A4页面布局
    page = layout.Page(width, height, layout.Units.mm, margins=layout.Margins.all(20))
    # 获取PDF或PNG渲染结果作为字节流
    if file_suffix == "pdf":
        pdf_bytes = backend.get_pdf_bytes(page)
        try:
            with open(output_file_name, "wb") as fp:
                fp.write(pdf_bytes)
        except Exception as e:
            print(f"Error writing to file {output_file_name}: {e}")
            return
    else:
        png_bytes = backend.get_pixmap_bytes(page, fmt="png", dpi=96)
        try:
            with open(output_file_name, "wb") as fp:
                fp.write(png_bytes)
        except Exception as e:
            print(f"Error writing to file {output_file_name}: {e}")
            return

        if file_suffix == "bmp":
            img = Image.open(output_file_name)
            img = img.convert("RGB")
            bmp_out_file_name = output_file_name.replace(".png", ".bmp")
            img.save(bmp_out_file_name, "BMP")
            output_file_name = bmp_out_file_name

    print(output_file_name + "文件已经转换")


# 用于将DXF格式的文件转换为SVG格式的文件
def convert_dwg_to_svg(dxf_path, svg_path, width=64, height=64):
    try:
        doc = odafc.readfile(dxf_path)
    except odafc.DXFStructureError as e:
        print(f"DXF Structure Error in file {dxf_path}: {e}")
        return
    except FileNotFoundError:
        print(f"File not found: {dxf_path}")
        return
    except PermissionError:
        print(f"Permission denied for file: {dxf_path}")
        return
    except Exception as e:
        print(f"Error reading file {dxf_path}: {e}")
        return
    msp = doc.modelspace()
    # 1. create the render context
    context = RenderContext(doc)
    # 2. create the backend
    backend = svg.SVGBackend()
    # 3. create the frontend
    # 定义一个字典来映射 backgroundtype 到对应的 BackgroundPolicy
    policy_map = {
        0: config.BackgroundPolicy.DEFAULT,
        1: config.BackgroundPolicy.BLACK,
        2: config.BackgroundPolicy.WHITE,
        3: config.BackgroundPolicy.CUSTOM,
        4: config.BackgroundPolicy.PAPERSPACE,
        5: config.BackgroundPolicy.MODELSPACE,
        6: config.BackgroundPolicy.OFF,
    }

    # 使用 try-except 来处理可能出现的 KeyError 异常
    try:
        background_policy = policy_map[backgroundtype]
    except KeyError:
        # 如果 backgroundtype 不在预定义的映射中，则使用默认策略
        background_policy = config.BackgroundPolicy.DEFAULT
        print("Warning: Invalid backgroundtype. Using default policy.")

    # 创建 Configuration 对象
    cfg = config.Configuration(background_policy=background_policy)

    # 初始化 Frontend 实例
    frontend = Frontend(context, backend, config=cfg)
    # 4. draw the modelspace
    frontend.draw_layout(msp)
    # 5. create an A4 page layout, not required for all backends
    page = layout.Page(width, height, layout.Units.mm, margins=layout.Margins.all(20))
    # 6. get the SVG rendering as string - this step is backend dependent
    svg_string = backend.get_string(page)
    with open(svg_path, "wt", encoding="utf8") as fp:
        fp.write(svg_string)
    print(svg_path + "文件已经转换")


def is_float_zero(num, epsilon=1e-6):
    """
    判断一个浮点数是否接近零。
    由于浮点数的精度问题，直接比较数值与零相等通常是不推荐的。通过指定一个极小的误差范围（epsilon），
    判断数值是否在这个误差范围内，从而确定该数值是否接近零。
    参数:
    num: 待判断的浮点数。
    epsilon: 可接受的误差范围，默认值为1e-6。
    返回值:
    如果 num 的绝对值小于 epsilon，返回 True，表示 num 接近零。
    否则，返回 False，表示 num 不接近零。
    """
    return -epsilon < num < epsilon


def read_config_file(inifile):
    """
    读取配置文件并解析其中的设置。
    该函数尝试读取一个INI格式的配置文件，并从中获取特定的设置值，
    包括输入路径、宽度、高度和文件后缀。如果无法读取或解析配置文件，
    它将返回一组默认的空值。
    参数:
    inifile (str): 配置文件的路径。
    返回:
    tuple: 包含输入路径（str）、宽度（float）、高度（float）和文件后缀（str）的元组。
           如果发生错误，返回("", 0.0, 0.0, "")。
    """
    try:
        # 尝试读取配置文件
        iniconfig.read(inifile, encoding="utf-8")
        # 从配置文件的"settings"部分获取各个配置项的值
        inputpath = iniconfig.get("settings", "path")
        width = iniconfig.getfloat("settings", "width")
        height = iniconfig.getfloat("settings", "height")
        file_suffix = iniconfig.get("settings", "file_suffix")
        backgroundtype = iniconfig.getint("settings", "backgroundtype")
        # 返回解析的配置项值
        return inputpath, width, height, file_suffix, backgroundtype
    except Exception as e:
        # 如果发生异常，打印错误信息并返回一组默认的空值
        print(f"读取配置文件时发生错误: {e}")
        return "", 0.0, 0.0, "", 0


def process_files(width, height, file_suffix, backgroundtype, filelist):
    """
    根据提供的文件列表和参数，将指定的文件转换为指定格式的PDF或图片文件。
    参数:
    - width: 转换后文件的宽度，用于调整输出文件的尺寸。
    - height: 转换后文件的高度，用于调整输出文件的尺寸。
    - file_suffix: 输出文件的格式，如'pdf', 'png', 'svg'等。
    - filelist: 需要转换的文件列表，包含多个文件的路径。
    - backgroundtype: 背景颜色信息。
    返回值:
    无直接返回值，该函数的主要作用是转换文件并保存到指定路径。
    """
    for file in filelist:
        # 打印当前处理的文件名
        print(file)
        # 获取文件名，不包含扩展名
        file_name = os.path.basename(file).split(".")[0]
        # 获取文件的目录路径
        outpath = os.path.dirname(file)
        # 根据文件名和指定的文件格式构建输出文件的完整路径
        pdf_file_name = os.path.join(outpath, f"{file_name}.{file_suffix}")
        # 如果文件格式为bmp，则输出格式为png
        if file_suffix == "bmp":
            pdf_file_name = os.path.join(outpath, f"{file_name}.png")
        # 如果文件格式为svg，则调用特定的转换函数
        if file_suffix == "svg":
            convert_dwg_to_svg(file, pdf_file_name, width, height)
        # 对于其他格式，假设为dwg，调用转换为pdf或其他图片格式的函数
        else:
            convert_dxf_to_image(
                file, pdf_file_name, width, height, backgroundtype, file_suffix
            )

def ensure_non_empty_value(value, default):
    """
    Ensure the given value is non-empty. If the value is empty, return the default value.
    Parameters:
    - value: The value to check and return if it is non-empty.
    - default: The default value to return if the given value is empty.
    Returns:
    - The given value if it is non-empty; otherwise, the default value.
    """
    # Return the given value if it is non-empty, otherwise return the default value
    return value if value else default

if __name__ == "__main__":
    currentPath = get_current_file_path()
    inifile = os.path.join(currentPath, "dwg2svg.ini")
    print(f"开始转换,ini文件为{inifile}")
    print(
        """配置文件格式为
            {
                \033[34m[settings]
                path=
                width=64
                height=64
                file_suffix=svg
                backgroundtype=0\033[0m
            }
            \033[32mfile_suffix\033[0m为pdf、bmp、png、svg
            \033[32mbackgroundtype\033[0m默认为0
            \033[34m{
                0: config.BackgroundPolicy.DEFAULT,
                1: config.BackgroundPolicy.BLACK,
                2: config.BackgroundPolicy.WHITE,
                3: config.BackgroundPolicy.CUSTOM,
                4: config.BackgroundPolicy.PAPERSPACE,
                5: config.BackgroundPolicy.MODELSPACE,
                6: config.BackgroundPolicy.OFF,
            }\033[0m
        """
    )
    iniconfig = myconf()
    inputpath, width, height, file_suffix, backgroundtype = "", 0.0, 0.0, "", 0
    if os.path.exists(inifile):
        inputpath, width, height, file_suffix, backgroundtype = read_config_file(
            inifile
        )
    else:
        print(f"{inifile} 配置文件不存在，请检查配置文件路径是否正确")
    inputpath = ensure_non_empty_value(inputpath, currentPath)
    width = ensure_non_empty_value(width, 64)
    height = ensure_non_empty_value(height, 64)
    file_suffix = ensure_non_empty_value(file_suffix, "pdf")
    backgroundtype = ensure_non_empty_value(backgroundtype, 0)
    print(f"dwg文件夹为:{inputpath}")
    filelist = getFileName(inputpath)
    process_files(width, height, file_suffix, backgroundtype, filelist)
    print("结束转换")
```

==dwg2svg.ini==

```ini
[settings]
path=
width=64
height=64
file_suffix=svg
backgroundtype=0
```

## 其它设置

如果要改成白底

```python
# 3. create the frontend
# 定义一个字典来映射 backgroundtype 到对应的 BackgroundPolicy
policy_map = {
    0: config.BackgroundPolicy.DEFAULT,
    1: config.BackgroundPolicy.BLACK,
    2: config.BackgroundPolicy.WHITE,
    3: config.BackgroundPolicy.CUSTOM,
    4: config.BackgroundPolicy.PAPERSPACE,
    5: config.BackgroundPolicy.MODELSPACE,
    6: config.BackgroundPolicy.OFF,
}

# 使用 try-except 来处理可能出现的 KeyError 异常
try:
    background_policy = policy_map[backgroundtype]
except KeyError:
    # 如果 backgroundtype 不在预定义的映射中，则使用默认策略
    background_policy = config.BackgroundPolicy.DEFAULT
    print("Warning: Invalid backgroundtype. Using default policy.")

    # 创建 Configuration 对象
    cfg = config.Configuration(background_policy=background_policy)

    # 初始化 Frontend 实例
    frontend = Frontend(context, backend, config=cfg)
```

