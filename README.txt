【使用说明】

一、pip发布:
python setup.py sdist bdist_wheel
twine upload dist/*

二、axxac命令安装:
pip3 install axxac

三、执行axxac命令
axxac -c <case_config_file> -l <login_config_file> -o <output_directory>

-c case配置文件路径
-l 登录接口配置文件路径
-o
 case用例表格及itest json文件输出目录

例如：axxac -c ./data/case配置.xls -l ./data/登录接口配置.xls -o ./output