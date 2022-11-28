# DirectoryUtil

## 前言

致力于目录批量操作，节省生产过程中批量操作的时间

## 目录结构说明

|—commons #公共组件

|—model #模块实体类

|—logs #记录程序运行日志

|—service #功能业务类

|—utils #工具类

|—main.py #程序入口

|—logo,ini #系统LOGO

## 运行

1. 前提需要在宿主机安装python3
2. 将程序下载到宿主机
3. 进入程序目录下，执行start.bat或start.sh

## 二次开发

### 如何自定义系统菜单选项

只需要配置service程序目录的system_service.py中，初始化方法即可

```python
def __init__(self) -> None:
        '''
        初始化菜单信息
        '''
        self.menus.append(MenuModel(1, 0, "目录工具类", "描述", None))
        self.menus.append(MenuModel(2, 1, "提取目录", "描述", None))
        self.menus.append(MenuModel(3, 2, "提取目录子菜单", "描述", DirService.print))
        self.menus.append(MenuModel(0, 0, "退出", "描述", sys.exit))
```

MenuModel结构信息如下：

```python
class MenuModel:
    id = None           # ID主键(不可重复，顶级菜单ID为0)
    parentId = None     # 父ID主键
    name = None         # 功能菜单名称
    description = None  # 功能菜单描述
    method = None       # 功能菜单调用对应的方法

    def __init__(self, id, parentId, name, description, method) -> None:
        self.id = id
        self.parentId = parentId
        self.name = name
        self.description = description
        self.method = method
```

