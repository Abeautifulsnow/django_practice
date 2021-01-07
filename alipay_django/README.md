# 说明

## 使用

* 克隆该项目到本地：```git clone https://github.com/Abeautifulsnow/alipay_django225.git```
* 未上传密钥文件，相关私钥、公钥、以及支付宝密钥请自行生成【[密钥生成教程](https://docs.open.alipay.com/291/105971)】，并保存到demo/keys路径下，名称务必和我的一样：
  
    ```plain/text
    demo/keys/alipay_key_2048.txt   // 支付宝密钥
    demo/keys/private_2048.txt      // 自己的私钥
    demo/keys/pub_2048.txt          // 自己的公钥
    ```

* 安装Python环境，Python3.x。并安装项目环境：```pip install -r requirements.txt```
* 然后运行：```python manage.py runserver```
