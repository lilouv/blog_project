# 基于Flask实现简单的博客系统
## 介绍
这是用flask写的简单的博客系统。

功能：用户注册、头像上传、资料修改、支持Markdown编辑、博客的删除和修改、评论、点赞、收藏、博客可添加分类及封面、支持上传视频(可发弹幕)、后台管理


## 项目结构
```python
—— blog 
     |—— admin # 蓝图目录
           |—— views # html模板目录
                 |——...
           |—— admin.py # url 视图文件
     |—— article # 蓝图目录 
           |—— views # html模板目录
                 |——...
           |—— admin.py # url 视图文件                
     |—— static # 静态文件目录
     |—— templates # html模板目录
           |——...
     |—— app.py # 主文件
     |—— config.py # 配置文件
     |—— models.py # 数据类
     |—— utils.py # 辅助类
     |—— README.md # 说明
```
## 展示
![图片1](https://img-blog.csdnimg.cn/20210306120155241.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbmtlZXA=,size_16,color_FFFFFF,t_70)

![图片2](https://img-blog.csdnimg.cn/20210306120155450.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbmtlZXA=,size_16,color_FFFFFF,t_70)

