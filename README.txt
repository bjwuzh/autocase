��ʹ��˵����

һ��pip����:
python setup.py sdist bdist_wheel
twine upload dist/*

����axxac���װ:
�״ΰ�װ��pip3 install axxac
���£�pip3 install axxac --upgrade

����ִ��axxac����
axxac -c <case_config_file> -l <login_config_file> -o <output_directory>

-c case�����ļ�·��
-l ��¼�ӿ������ļ�·��
-o
 case�������itest json�ļ����Ŀ¼

���磺axxac -c ./data/case����.xls -l ./data/��¼�ӿ�����.xls -o ./output