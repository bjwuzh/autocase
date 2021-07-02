【使用说明】

〇、生成发布文件：
python setup.py sdist bdist_wheel

本地安装测试 pip3 install dist/axxac-1.1.0-py3-none-any.whl

一、pip发布:
twine upload dist/*

二、axxac命令安装:
首次安装：pip3 install axxac
更新：pip3 install axxac --upgrade

三、执行axxac命令
axxac -i <input_directory> -o <output_directory>

-i case配置及依赖配置文件目录（该目录下必须包含cases和requires目录，目录下为对应配置文件）
-o case用例表格及itest json文件输出目录


例如：axxac -i ./data -o ./output

目录结构：
---data
---------case.xls
