# 总选验/投票Python脚本  
~~随便写的，很简单，也没太多价值。~~  
~~避免惹事，脚本会在总选结束后传上来。~~  
没几天投票就结束了，大家加油吧  
错误得把程序直接给了别人，自己怕永远没得参与了，难过  
虽然不止我一个人写，但还是希望有人能用一用，拜托了  

## 环境  
使用 python 2.7 编写  
使用软件包 xlrd ```pip install xlrd``` , xlwt ```pip install xlwt``` 提示import失败就安装一下  

## 使用  
step1.导入票号  
  
把要验要投的票号做成excel放在xls文件夹里，可以有多个excel表，文件名没有要求，格式参见xls文件夹中的例子 (其实只要有两列是票号就可以了，随便相邻的两列)  
  
step2.运行程序  
```
python humanscript.py #模拟人类操作 
python autoscript.py #无脑跑求效率
windows 直接双击打开.py文件也可以
```  
两个脚本，功能其实是一样的  
如果特别在意的话，还是人工投吧，无力反驳  
  
step3.等待验票结束  
  
程序运行结束自动退出  
生成```output.xls```是全部验票结果  
**中途退出不会生成文件，输出文件为覆盖写，请及时取出**  

## 特性
考虑了每次后退访问带cookie的情况   
考虑了复制填写票号的所需时间    
考虑了后退操作表单未清空可以直接再次提交的情况  
考虑了看到结果到点击回退所需时间  
*这些时间是服从泊松分布吗？有必要的话再改*  

打开链接超时重试最多5次，超过则视为网络崩溃，退出程序  
提交结果超时重试最多3次，超过直接下一票  
代投票后会进行验票操作  

## 原理  
打开浏览器开发者工具试试就明白了  
除了 google analytics 没有其它 js 了 (真简洁)  
拿到隐藏表单和 cookie，带着一起 post 就好了  
投票验票一个步骤，投票也没有二次确认。根本不用怀疑，这肯定就是给小偶像投票的网站，肥肠煎蛋 (逃  
要伪装得像一点，把 headers 里的东西都设一下 (反正我能设的都设了，也没有验证过存不存在反爬机制)  
测试还发现请求不带 ```&parent=...&parentkey=...``` ，隐藏表单里的 parent,parentkey 是空也可以提交，用手机 ua 得到的 time 是空的，保险起见，该带的都带

## 附加
所有参选成员的代码已经在 ```membercode.txt``` 中给出，是用爬虫爬的，解码可能有点问题，如果名字缺了就自己补一下吧。
 
## 多嘴
我看别人的脚本里还有"投票过于频繁被封"? 我都没代投过。。。不知道。。。不要问我 