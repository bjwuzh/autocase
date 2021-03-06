from setuptools import setup, find_packages

setup(name='axxac',
      version='1.2.1',
      description='Generate case list and itest json automatically.',
      # 项目主页
      url='https://github.com/bjwuzh/autocase.git',
      author='bjwuzh',
      author_email='bjwuzh@163.com',
      # 许可证信息
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
        'console_scripts': ['axxac = axxac.main:cmdexe']
      },
      install_requires=['xlwt', 'xlrd'])
