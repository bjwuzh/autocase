��ʹ��˵����

�������ɷ����ļ���
python setup.py sdist bdist_wheel

���ذ�װ���� pip3 install dist/axxac-1.1.0-py3-none-any.whl

һ��pip����:
twine upload dist/*

����axxac���װ:
�״ΰ�װ��pip3 install axxac
���£�pip3 install axxac --upgrade

����ִ��axxac����
axxac -i <input_directory> -o <output_directory>

-i case���ü����������ļ�Ŀ¼����Ŀ¼�±������cases��requiresĿ¼��Ŀ¼��Ϊ��Ӧ�����ļ���
-o case�������itest json�ļ����Ŀ¼


���磺axxac -i ./data -o ./output

Ŀ¼�ṹ��
---data
------cases
---------case.xls
------requires
---------1-login.xls
---------2-login.xls
---------3-login.xls

��ע��requiresĿ¼���ļ�Ϊ���������ļ������¼�ӿڣ����ļ������밴����˳����С���������������淶Ϊ������-xxx.xls��