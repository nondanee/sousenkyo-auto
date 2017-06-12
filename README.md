# 总选验/投票Python脚本  
随便写的，很简单，也没太多价值。  
筹票才是第一大事，求求你给咱家麻友再投几票吧 orz  
避免惹事，脚本会在总选结束后传上来。  

## 实现  
打开浏览器开发者工具试试就明白了  
除了 google analytics 没有其它 js 了 (真简洁)  
拿到隐藏表单和 cookie，带着一起 post 就好了  
投票验票一个步骤，投票也没有二次确认。根本不用怀疑，这肯定就是给小偶像投票的网站，肥肠煎蛋 (逃  
要伪装得像一点，把 headers 里的东西都设一下 (反正我能设的都设了，也没有验证过存不存在反爬机制)  
*测试还发现请求不带 &parent=...&parentkey=... ，隐藏表单里的 parent,parentkey 是空也可以提交，用手机 ua 得到的 time 是空的，保险起见，该带的都带*  

## 额外  
membercode 和 teamcode 的关系，举个栗子就知道了  
```
渡辺 麻友
membercode: 1307
teamcode: 103

membercode[0] = teamcode[1] = 1 -> AKB48
membercode[1] = teamcode[3] = 3 -> teamB
membercode[2:3] = 07 -> AKB48 teamB 参选的第7位成员 (五十音序吧应该) 
```
membercode 表先提供吧，反正没啥用。  
也是脚本爬的，shift-jis 到 utf-8 好像有点转码问题，就直接 ignore 了。名字缺了字不要怪我，反正我也没几个认识的，出坑出不去系列。  
  
我看别人的脚本里还有"投票过于频繁被封"? 我还没遇到过，不好加啊  