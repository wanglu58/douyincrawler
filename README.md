# Douyincrawler
抖音批量下载用户所有无水印视频
## Run
安装python3

安装依赖

```
pip3 install requests -i https://pypi.doubanio.com/simple/
pip3 install python-dateutil -i https://pypi.doubanio.com/simple/
```
运行py文件

获取用户主页分享链接

- 打开抖音-进入你要爬取的用户主页
  ![1](https://raw.githubusercontent.com/wanglu58/douyincrawler/master/screenshots/1.png)

- 用户主页右上角点开-分享主页-复制链接
  ![2](https://raw.githubusercontent.com/wanglu58/douyincrawler/master/screenshots/2.png)

粘贴你要爬取的抖音号的链接

输入你要从哪个时间开始爬取（2018年1月：输入2018.01）

它会自动创建文件夹并下载用户所有**无水印视频**。
## Release
下载打包好的exe文件一键运行

-  [douyincrawler.exe](https://github.com/wanglu58/douyincrawler/releases)