# What's this?

基于drebin开发的简易版安卓APK恶意检测模型

# Environment

python 3.9.0

# How do I use it?

1、将数据集放置文件目录下的dataset文件夹中（可以仅将恶意APK放至malware_train目录下，良性APK放至goodware_train目录下）

2、直接运行main.py文件，等待特征工程与模型训练完毕，在控制台输入模型名称即可

# Function of each file

- main.py：文件的入口，此处进行参数的配置
- get_apk_data.py：利用androguard进行特征提取
- util.py：一些常用工具，利于列出文件夹中所有文件
- classify.py：简单的分类模型
