* 简体中文
* [English]()

![Alt text](https://camo.githubusercontent.com/4da62e9d0a03f219020490243608ab79088fa6b2/68747470733a2f2f696d672e626c657373696e672e73747564696f2f696d616765732f323031372f30312f30312f62732d6c6f676f2e706e67)

 

**崩坏广场**是一款专为留言板，个人博客等（BoomSquare）打造的WEB站点，通过精心的设计与耐心的研究，配合Markdown强大的排版功能，带来前所未有的书写体验。


#### **功能丰富** ：

* 支持Markdown语法，支持高亮代码 [√]
* 支持于皮肤站账号系统对接 [×]
* 支持authme插件对接 [×]
* 更多后续完善

#### **崩坏广场的优点**：

* 专注你的文字内容而不是排版样式，安心写作。
* 随时修改你的文章版本，不必像字处理软件生成若干文件版本导致混乱。
* 可读、直观、学习成本低。
* 统一管理authme账号，实现与登陆插件对接等功能

#### **得心应手** ：

* 简洁高效的编辑器，轻松的导出 HTML、PDF 和本身的 .md 文件, 纯文本内容。
* 兼容所有的文本编辑器与字处理软件；
* 优雅的界面，加上Markdown让你写作更完美



## 如何安装崩坏广场？

### 环境要求
BoomSquare 对您的服务器有一定的要求。
* 一台支持 URL 重写的主机，Nginx、Apache 和 uwsgi
* Python > 3.0 （服务器不支持？）
* 安装如下 Python 扩展：

	* pip  >= 8.0
    * Django >= 1.9.0
    * Markdown
    * setuptools
    * uwsgi



### 快速指南
![Alt text](img/log.png)

#### Python 环境安装

*CentOS 7 安装epel YUM源*

    wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    rpm -ivh epel-release-latest-7.noarch.rpm
    yum makecache
   
*或者通过yum直接安装*

    yum install epel-release -y
    # 如果安装失败，请通过上面命令安装，不要忘记清缓存yum makecache

*CentOS 6 安装epel YUM 源*

    wget http://mirrors.ustc.edu.cn/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
    rpm -ivh epel-release-6-8.noarch.rpm
    yum makecache

*安装完事后，开始安装python36或者python34环境[本人使用python36]*

    yum install python36 wget




#### pip工具以及uwsgi 安装 [WEB]
    
*开始下载pip*

    wget https://bootstrap.pypa.io/get-pip.py
    
*然后就是安装pip*

    python3.6 get-pip.py

*用pip安装Django == 1.9.2，和uwsgi*

    pip3.6 install Django==1.9.2
    pip3.6 install uwsgi
 
    
    






















## Markdown简介

> Markdown 是一种轻量级的「标记语言」，它的优点很多，目前也被越来越多的写作爱好者，撰稿者广泛使用。看到这里请不要被「标记」、「语言」所迷惑，Markdown 的语法十分简单。常用的标记符号也不超过十个，这种相对于更为复杂的 HTML 标记语言来说，Markdown 可谓是十分轻量的，学习成本也不需要太多，且一旦熟悉这种语法规则，会有一劳永逸的效果。—— [维基百科](https://zh.wikipedia.org/wiki/Markdown)

正如您在阅读的这份文档，它使用简单的符号标识不同的标题，将某些文字标记为**粗体**或者*斜体*，创建一个[链接](http://www.example.com)。下面列举了几个高级功能，更多语法请百度查看帮助。 

### 标题

	This is an H1
	=============

	This is an H2
	-------------


### 链接
链接文字都是用 [方括号] 来标记。

    This is [an example](http://example.com/ "Title") inline link.


### 图片

    ![Alt text](http://www.baidu.com/img.jpg)

    ![Alt text](http://www.baidu.com/img.jpg "Optional title")


### 反斜杠
Markdown 可以利用反斜杠来插入一些在语法中有其它意义的符号

	\   反斜线
	`   反引号
	*   星号
	_   底线
	{}  花括号
	[]  方括号
	()  括弧
	#   井字号
	\+   加号
	\-   减号
	.   英文句点
	!   惊叹号


### 代码块
标准Markdown基于缩进代码行或者4个空格位:
``` python
def somefunc(param1=None, param2=0):
    if param1 > param2: # interesting
        print 'Greater'
    return (param2 - param1 + 1) or None
class SomeClass:
    pass

... prompt'''
```

### 表格
	| Item      |    Value | Qty  |
	| :-------- | --------:| :--: |
	| Computer  | 1600 USD |  5   |
	| Phone     |   12 USD |  12  |
	| Pipe      |    1 USD | 234  |

### 引用文本
	> That is pulled out like this from the text my post.



# 
# 

 

> **提示：**想了解更多，请查看 **百度百科** [Markdown语法][4]。





## 反馈与建议
- Q群：661890020
- 邮箱：job@6box.net

---------


  [1]: http://maxiang.info/client_zh
  [2]: https://chrome.google.com/webstore/detail/kidnkfckhbdkfgbicccmdggmpgogehop
  [3]: http://adrai.github.io/flowchart.js/
  [4]: http://bramp.github.io/js-sequence-diagrams/
  [5]: https://dev.yinxiang.com/doc/articles/enml.php

