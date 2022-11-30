class Menu:
    id = None           # ID主键
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