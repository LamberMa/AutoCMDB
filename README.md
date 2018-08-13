CMDB解决了你们的什么问题

> - 解决了资产的自动采集问题，终结了以excel表格维护资产的形式
> - 为各种各样的系统提供数据支持。比如监控，堡垒机，等等。

你的CMDB架构是怎么样的？（总共三部分）
- 资产采集（agent，saltstack，ssh(paramiko)）
- 采集到给api，api入库（验证，参考的toronado加密cookie，数据入库使用反射来完成）
- 后台执行管理

后台管理
- 开发增删改查的组件


有没有遇到什么坑：
- 唯一标识
- 难题：错误堆栈信息

有关cmdb的部分参考资料吧
http://www.linuxde.net/2018/08/18494.html
https://www.cnblogs.com/nulige/p/6703160.html
https://www.cnblogs.com/laowenBlog/p/6825420.html
http://www.cnblogs.com/wupeiqi/articles/6415436.html
百度搜索 cmdb 开源
更改国内pip源
https://www.cnblogs.com/walk1314/p/7076853.html



cmdb中subprocess的时候如何让sudo的时候自动输入密码呢，百度解决问题

# 查一下这种用法
server_list = models.Asset.objects
for row in server_list:
    row.get_device_type_id_display()
    
attrs的作用：当修改的时候可以和原值进行比对，这样就知道到底有没有变化了，没有变化的就可以不提交了。
    
    
1.现在配置文件中加一列选择列
2.其实编辑的实质就是点击的时候触发事件，然后将td的内容换成一个input标签。

添加可变化的情况太多因此不封装进插件。这个是可以高度自定制的，比如少了单个添加，用模态框
多了的话用一个单独的页面也是ok的。


为了简化操作可以将table_config迁移到一个单独的文件夹内然后import导入

django进阶
http://www.cnblogs.com/wupeiqi/articles/5246483.html

使用

1-两个url，一个展示页面，一个获取数据。
2-两个公用模板，一个common_tpl，一个，js插件
注意html规则，在引用的时候要调用一个api的地址。
3-配置规则。