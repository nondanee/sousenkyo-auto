# 2017总选验/投票Python脚本(封存)  
~~随便写的，很简单，也没太多价值。~~  
~~避免惹事，脚本会在总选结束后传上来。~~  
~~没几天投票就结束了，大家加油吧~~  
投票结束了，帮忙验了好多，脚本也改版无数次  
感谢所有一起工作的小伙伴，还有一直应援着的饭们，大家辛苦了！  
那么就明年见?(不见，推都毕业了，明年这个时候我也毕业了...)  
**该脚本默认是投给麻友的**  


## 环境  
使用 python 2.7 编写  
使用软件包 xlrd , xlwt 提示import失败就安装一下  
```
pip install xlrd
pip install xlwt
```

## 使用  
### step1.导入票号  
  
把要验要投的票号做成excel放在xls文件夹里，可以有多个excel表，文件名没有要求，只要有两列是票号就可以了(随便相邻的两列)  
  
### step2.运行程序  
```
python humanscript.py #(旧版)模拟人类操作
python autoscript.py #(旧版)无脑跑求效率
python formatscript.py #(改版)无脑跑求效率，调整输出形式
```  
  
### step3.等待验票结束  

*humanscript.py/autoscript.py*  
程序运行结束自动退出  
生成```output.xls```是全部验票结果  
**中途退出不会生成文件，输出文件为覆盖写，请及时取出**  
  
*formatscript.py*  
程序运行结束自动退出  
生成结果在 output 文件夹中, 文件名为```对应原文件名-checked.xls```  
**验/投票过程逐文件进行并输出结果，输出文件仍为覆盖写**
  
  
## 特性

### 所有版本
+ 考虑了每次后退访问带cookie的情况 
+ 打开链接超时重试最多5次，超过则视为网络崩溃，退出程序  
+ 提交结果超时重试最多3次，超过直接下一票   
+ 代投后会进行验票操作  

### humanscript.py   
+ 考虑了复制填写票号的所需时间    
+ 考虑了后退操作表单未清空可以直接再次提交的情况  
+ 考虑了看到结果到点击回退所需时间   
+ 投票时间转换成北京时间  
+ xls文件夹内文件合成输出一个结果

### autoscript.py    
+ 投票时间转换成北京时间  
+ xls文件夹内文件合成输出一个结果

### formatscript.py     
+ 输出结果为网页显示日语提示原文
+ 分文件验/投票并生成结果  
+ 非验票成功行标红(不完美)  

  
  
## 原理  
打开浏览器开发者工具试试就明白了  
除了 google analytics 没有其它 js 了 (真简洁)  
拿到隐藏表单和 cookie，带着一起 post 就好了  
投票验票一个步骤，投票也没有二次确认。根本不用怀疑，这肯定就是给小偶像投票的网站，肥肠煎蛋 (逃  
要伪装得像一点，把 headers 里的东西都设一下 (反正我能设的都设了，也没有验证过存不存在反爬机制)  
测试还发现请求不带 ```&parent=...&parentkey=...``` ，隐藏表单里的 parent,parentkey 是空也可以提交，用手机 ua 得到的 time 是空的，保险起见，该带的都带

## 缺陷  

*那啥，感觉再修也没啥意义了=.=*  

1. humanscript.py autoscript.py 存在无法检查所有空白符的问题，未修复  
2. formatscript.py 存在无法黑红行共存的问题，未修复(只能全红/全黑，应该是因为style全局，全部是指针操作)  


## 附加  

所有参选成员的代码已经在 ```membercode.txt``` 中给出，是用爬虫爬的，解码可能有点问题，如果名字缺了就自己补一下吧。  
 
## 多嘴  

~~我看别人的脚本里还有"投票过于频繁被封"? 我都没代投过。。。不知道。。。不要问我~~  
一直没被封=.=  