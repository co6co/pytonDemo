1. 《python 绝技》
```
pip install requests
python -m pip install --upgrade pip
pip install BeautifulSoup4
pip install loguru
pip install pyyaml
pip install ping3
pip install geoip2
```

# 包导入3.x 中的变化
- 绝对导入 :修改了模块导入搜索路径的定义[跳过包自己的目录]，导入时只检查sys.path 列表中的搜索路径 

- 相对导入 扩展了from语句的语法，允许显示要求导入时只搜索包的目录[以点号开头]

```
from . import spam # 告诉Python把位于语句中给出的文件相同包路径中的名为spam的模块导入
```
```
from __future__import absolute_import # py3.x 仅绝对搜索路径策略
```

