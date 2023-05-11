dfci['maindo']= None


dfci.loc[(dfci['domain'].str.contains('www.dahebao.cn')) & (dfci['maindo'].isna()),'maindo'] = '大河报网'
dfci.loc[(dfci['domain'].str.contains('www.gzdaily.cn')) & (dfci['maindo'].isna()),'maindo'] = '广州日报(网站)'
dfci.loc[(dfci['domain'].str.contains('paper.nandu.com')) & (dfci['maindo'].isna()),'maindo'] = '南方都市报(网站)'
dfci.loc[(dfci['domain'].str.contains('kuaixun.stcn.com')) & (dfci['maindo'].isna()),'maindo'] = '证券时报网'
dfci.loc[(dfci['domain'].str.contains('epaper.jinghua.cn')) & (dfci['maindo'].isna()),'maindo'] = '京华时报(网站)'
dfci.loc[(dfci['domain'].str.contains('politics.scdaily.cn')) & (dfci['maindo'].isna()),'maindo'] = '四川日报网'
dfci.loc[(dfci['domain'].str.contains('sjb.qlwb.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '齐鲁晚报（电子报）'
dfci.loc[(dfci['domain'].str.contains('szb.hkwb.net')) & (dfci['maindo'].isna()),'maindo'] = '海口晚报（电子报）'
dfci.loc[(dfci['domain'].str.contains('v5share.cdrb.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '锦观新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('www.21jingji.com')) & (dfci['maindo'].isna()),'maindo'] = '21世纪经济网'
dfci.loc[(dfci['domain'].str.contains('www.bbtnews.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '北京商报网'
dfci.loc[(dfci['domain'].str.contains('www.dailyqd.com')) & (dfci['maindo'].isna()),'maindo'] = '青报网'
dfci.loc[(dfci['domain'].str.contains('www.changjiangtimes.com')) & (dfci['maindo'].isna()),'maindo'] = '长江商报（网站）'
dfci.loc[(dfci['domain'].str.contains('www.jinbw.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '今报网'
dfci.loc[(dfci['domain'].str.contains('www.njdaily.cn')) & (dfci['maindo'].isna()),'maindo'] = '南报'
dfci.loc[(dfci['domain'].str.contains('www.qlwb.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '齐鲁晚报（网站）'
dfci.loc[(dfci['domain'].str.contains('www.wccdaily.com.cn')) & (dfci['maindo'].isna()),'maindo'] = 'huaxidushibao'
dfci.loc[(dfci['domain'].str.contains('www.xtrb.cn')) & (dfci['maindo'].isna()),'maindo'] = '牛城晚报(电子报)'



dfci.loc[(dfci['domain'].str.contains('www.ithome.com')) & (dfci['maindo'].isna()),'maindo'] = 'IT之家(网站)'
dfci.loc[(dfci['domain'].str.contains('ishare.ifeng')) & (dfci['maindo'].isna()),'maindo'] = '凤凰新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('ifeng.')) & (dfci['maindo'].isna()),'maindo'] = '凤凰网'
dfci.loc[(dfci['domain'].str.contains('c.m.163.')) & (dfci['maindo'].isna()),'maindo'] = '网易网（应用程序）'
dfci.loc[(dfci['domain'].str.contains('3g.163.com')) & (dfci['maindo'].isna()),'maindo'] = '网易网（应用程序）'
dfci.loc[(dfci['domain'].str.contains('m.163.')) & (dfci['maindo'].isna()),'maindo'] = '网易网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('163.')) & (dfci['maindo'].isna()),'maindo'] = '网易网'


dfci.loc[(dfci['origin_url_x'].str.contains('sinawap')) & (dfci['maindo'].isna()),'maindo'] = '新浪新闻（应用程序）'
dfci.loc[(dfci['domain']==('m.weibo.cn')) & (dfci['maindo'].isna()),'maindo'] = '新浪微博（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('weibo.com')) & (dfci['maindo'].isna()),'maindo'] = '新浪微博-网站'
dfci.loc[(dfci['domain'].str.contains('.sina.cn')) & (dfci['maindo'].isna()),'maindo'] = '新浪网(应用程序)'
dfci.loc[(dfci['domain'].str.contains('sina.com')) & (dfci['maindo'].isna()),'maindo'] = '新浪网'

dfci.loc[(dfci['domain'].str.contains('weixin.')) & (dfci['maindo'].isna()),'maindo'] = '腾讯微信公众平台（应用程序）'
dfci.loc[(dfci['domain'].str.contains('view.inews.qq')) & (dfci['maindo'].isna()),'maindo'] = '腾讯新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('qq.')) & (dfci['maindo'].isna()),'maindo'] = '腾讯网'

dfci.loc[(dfci['domain'].str.startswith('3g.k.sohu.com')) & (dfci['maindo'].isna()),'maindo'] = '搜狐网（应用程序）'
dfci.loc[(dfci['domain'].str.startswith('m.sohu.')) & (dfci['maindo'].isna()),'maindo'] = '搜狐网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('sohu.')) & (dfci['maindo'].isna()),'maindo'] = '搜狐网'
dfci.loc[(dfci['domain'].str.contains('baike.baidu')) & (dfci['maindo'].isna()),'maindo'] = '百度百科-网站'
dfci.loc[(dfci['domain'].str.contains('baijiahao.baidu')) & (dfci['maindo'].isna()),'maindo'] = '百度百家号'
dfci.loc[(dfci['domain'].str.contains('mbd.baidu.')) & (dfci['maindo'].isna()),'maindo'] = '百度百家号（应用程序）'#也是应用程序，这个mbd本身覆盖不止百家号码
dfci.loc[(dfci['domain'].str.contains('www.baidu.com')) & (dfci['maindo'].isna()),'maindo'] = '百度搜索引擎'

dfci.loc[(dfci['domain'].str.contains('jiemian.')) & (dfci['maindo'].isna()),'maindo'] = '界面新闻-网站'
dfci.loc[(dfci['domain'].str.startswith('m.thepaper.')) & (dfci['maindo'].isna()),'maindo'] = '澎湃新闻（移动端网页版/应用程序）'#也是APP
dfci.loc[(dfci['domain'].str.contains('thepaper.')) & (dfci['maindo'].isna()),'maindo'] = '澎湃新闻-网站'


dfci.loc[(dfci['domain']=='jjckb.xinhuanet.com') & (dfci['maindo'].isna()),'maindo'] = '经济参考报'
dfci.loc[(dfci['domain'].str.contains('api3.cls.cn')) & (dfci['maindo'].isna()),'maindo'] = '财联社（应用程序）'
dfci.loc[(dfci['domain'].str.contains('xhpfmapi')) & (dfci['maindo'].isna()),'maindo'] = '新华社（应用程序）'
dfci.loc[(dfci['domain'].str.contains('h.xinhuaxmt')) & (dfci['maindo'].isna()),'maindo'] = '新华社（应用程序）'
dfci.loc[(dfci['domain']=='m.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网（移动端网页版）'
dfci.loc[(dfci['domain']=='m.xinhuanet.com') & (dfci['maindo'].isna()),'maindo'] = '新华网（移动端网页版）'
dfci.loc[(dfci['domain']=='sports.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网'
dfci.loc[(dfci['domain']=='english.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网'
dfci.loc[(dfci['domain']=='bj.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网'
dfci.loc[(dfci['domain'].str.contains('.xinhuanet.')) & (dfci['maindo'].isna()),'maindo'] = '新华网'
dfci.loc[(dfci['domain']=='www.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网'
dfci.loc[(dfci['domain']=='education.news.cn') & (dfci['maindo'].isna()),'maindo'] = '新华网'

dfci.loc[(dfci['domain'].str.contains('content-static.cctvnews')) & (dfci['maindo'].isna()),'maindo'] = '央视新闻（应用程序）'
dfci.loc[(dfci['domain']=='app.cctv.com') & (dfci['maindo'].isna()),'maindo'] = '央视新闻（应用程序）'
dfci.loc[(dfci['domain'].str.startswith('m.news.cctv')) & (dfci['maindo'].isna()),'maindo'] = '央视网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('cntv.c')) & (dfci['maindo'].isna()),'maindo'] = '央视网'
dfci.loc[(dfci['domain'].str.contains('cctv.com')) & (dfci['maindo'].isna()),'maindo'] = '央视网'
dfci.loc[(dfci['domain'].str.contains('.cnr.cn')) & (dfci['maindo'].isna()),'maindo'] = '央广网'

dfci.loc[(dfci['domain']=='bj.bjd.com.cn') & (dfci['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
dfci.loc[(dfci['domain']=='ie.bjd.com.cn') & (dfci['maindo'].isna()),'maindo'] = '北京日报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('bjd.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '北京日报网'
dfci.loc[(dfci['domain'].str.startswith('m.haiwainet')) & (dfci['maindo'].isna()),'maindo'] = '海外网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('haiwainet.cn')) & (dfci['maindo'].isna()),'maindo'] = '海外网'

dfci.loc[(dfci['domain'].str.startswith('m.chinanews')) & (dfci['maindo'].isna()),'maindo'] = '中国新闻网（应用程序）'
dfci.loc[(dfci['domain'].str.contains('chinanews.')) & (dfci['maindo'].isna()),'maindo'] = '中国新闻网'
dfci.loc[(dfci['domain'].str.startswith('m.gmw.')) & (dfci['maindo'].isna()),'maindo'] = '光明网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('.gmw.')) & (dfci['maindo'].isna()),'maindo'] = '光明网'

dfci.loc[(dfci['domain'].str.contains('.peopleapp.')) & (dfci['maindo'].isna()),'maindo'] = '人民日报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('paper.people.')) & (dfci['maindo'].isna()),'maindo'] = '人民日报（电子报）'
dfci.loc[(dfci['domain'].str.startswith('m.people.cn')) & (dfci['maindo'].isna()),'maindo'] = '人民网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('app.people.cn')) & (dfci['maindo'].isna()),'maindo'] = '人民网（应用程序）'
dfci.loc[(dfci['domain'].str.contains('.people.cn')) & (dfci['maindo'].isna()),'maindo'] = '人民网'
dfci.loc[(dfci['domain'].str.contains('.people.com')) & (dfci['maindo'].isna()),'maindo'] = '人民网'

dfci.loc[(dfci['domain'].str.startswith('m.huanqiu')) & (dfci['maindo'].isna()),'maindo'] = '环球网（移动端网页版）'
dfci.loc[(dfci['domain'].str.contains('hqtime.')) & (dfci['maindo'].isna()),'maindo'] = '环球时报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('huanqiu')) & (dfci['maindo'].isna()),'maindo'] = '环球网'
dfci.loc[(dfci['domain'].str.contains('m.bjnews.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '新京报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('epaper.bjnews.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '新京报（电子报）'
dfci.loc[(dfci['domain'].str.contains('bjnews.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '新京报网'
#3w.huanqiu 是个啥 https://3w.huanqiu.com/a/24d596/48NJJN9tgG4

dfci.loc[(dfci['domain'].str.contains('china.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国网'
dfci.loc[(dfci['domain'].str.endswith('3g.china.com')) & (dfci['maindo'].isna()),'maindo'] = '中华网（移动端网页版）'
dfci.loc[(dfci['domain'].str.endswith('.china.com')) & (dfci['maindo'].isna()),'maindo'] = '中华网'
dfci.loc[(dfci['domain'].str.contains('rmzxb.com')) & (dfci['maindo'].isna()),'maindo'] = '人民政协网'
dfci.loc[(dfci['domain'].str.contains('.youth.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国青年网'
dfci.loc[(dfci['domain'].str.contains('zqb.cyol.com')) & (dfci['maindo'].isna()),'maindo'] = '中国青年报（电子报）'
dfci.loc[(dfci['domain'].str.contains('news.cyol.com')) & (dfci['maindo'].isna()),'maindo'] = '中青在线'
dfci.loc[(dfci['domain'].str.contains('.cankaoxiaoxi.')) & (dfci['maindo'].isna()),'maindo'] = '参考消息网'
dfci.loc[(dfci['domain'].str.contains('m.ckxx.net')) & (dfci['maindo'].isna()),'maindo'] = '参考消息（应用程序）'
dfci.loc[(dfci['domain'].str.contains('js7tv.')) & (dfci['maindo'].isna()),'maindo'] = '中国军视网'
dfci.loc[(dfci['domain'].str.contains('.81.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国军网'
dfci.loc[(dfci['domain'].str.contains('.ce.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国经济网'
dfci.loc[(dfci['domain'].str.contains('.chinadaily.com')) & (dfci['maindo'].isna()),'maindo'] = '中国日报网'
dfci.loc[(dfci['domain'].str.contains('.cri.cn')) & (dfci['maindo'].isna()),'maindo'] = '国际在线-网站'

dfci.loc[(dfci['domain'].str.contains('m.nbd.com')) & (dfci['maindo'].isna()),'maindo'] = '每日经济新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('.nbd.com')) & (dfci['maindo'].isna()),'maindo'] = '每经网'
dfci.loc[(dfci['domain'].str.contains('.mrjjxw.')) & (dfci['maindo'].isna()),'maindo'] = '每经网'
dfci.loc[(dfci['domain'].str.contains('m.guancha.cn')) & (dfci['maindo'].isna()),'maindo'] = '观察者网（移动端网页版）'

dfci.loc[(dfci['domain'].str.contains('.guancha.cn')) & (dfci['maindo'].isna()),'maindo'] = '观察者网'
dfci.loc[(dfci['domain'].str.contains('.caixin.com')) & (dfci['maindo'].isna()),'maindo'] = '财新网'
dfci.loc[(dfci['domain'].str.contains('.caijing.com')) & (dfci['maindo'].isna()),'maindo'] = '财经网'
dfci.loc[(dfci['domain'].str.contains('.hexun.com')) & (dfci['maindo'].isna()),'maindo'] = '和讯网'
dfci.loc[(dfci['domain'].str.contains('m.voc.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '湖南日报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('zjrb.zjol.com')) & (dfci['maindo'].isna()),'maindo'] = '浙江日报（电子报）'
dfci.loc[(dfci['domain'].str.contains('zjnews.zjol.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '浙江在线-网站'

dfci.loc[(dfci['domain'].str.contains('hznews.')) & (dfci['maindo'].isna()),'maindo'] = '杭州网'
dfci.loc[(dfci['domain'].str.contains('.xhby.')) & (dfci['maindo'].isna()),'maindo'] = '新华报业网'
dfci.loc[(dfci['domain'].str.contains('sichuan.scol.')) & (dfci['maindo'].isna()),'maindo'] = '四川在线-网站'
dfci.loc[(dfci['domain'].str.contains('.dzwww.')) & (dfci['maindo'].isna()),'maindo'] = '大众网'
dfci.loc[(dfci['domain'].str.contains('epaper.ynet')) & (dfci['maindo'].isna()),'maindo'] = '北京青年报（电子报）'
dfci.loc[(dfci['domain'].str.contains('ynet.')) & (dfci['maindo'].isna()),'maindo'] = '北青网'
#dfci.loc[(dfci['domain'].str.startswith('t.ynet')) & (dfci['maindo'].isna()),'maindo'] = '北青网（移动端网页版）' 不好判断

dfci.loc[(dfci['domain'].str.contains('takefoto.')) & (dfci['maindo'].isna()),'maindo'] = '北晚在线-网站'
dfci.loc[(dfci['domain'].str.contains('export.shobserver')) & (dfci['maindo'].isna()),'maindo'] = '上观新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('web.shobserver')) & (dfci['maindo'].isna()),'maindo'] = '上观新闻-网站'
dfci.loc[(dfci['domain'].str.contains('jfdaily.')) & (dfci['maindo'].isna()),'maindo'] = '上观新闻网'
dfci.loc[(dfci['domain'].str.contains('n.cztv')) & (dfci['maindo'].isna()),'maindo'] = '新蓝网'
dfci.loc[(dfci['domain'].str.contains('ynet')) & (dfci['maindo'].isna()),'maindo'] = '北青网'
dfci.loc[(dfci['domain'].str.contains('kankanews')) & (dfci['maindo'].isna()),'maindo'] = '看看新闻-网站'
dfci.loc[(dfci['domain']=='www.thecover.cn') & (dfci['maindo'].isna()),'maindo'] = '封面新闻'
dfci.loc[(dfci['domain'].str.contains('m.thecover.cn')) & (dfci['maindo'].isna()),'maindo'] = '封面新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('static.cdsb.com')) & (dfci['maindo'].isna()),'maindo'] = '红星新闻（应用程序）'
dfci.loc[(dfci['domain'].str.contains('static.dingxinwen.com')) & (dfci['maindo'].isna()),'maindo'] = '河南日报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('static.nfapp.southcn.com')) & (dfci['maindo'].isna()),'maindo'] = '南方日报（应用程序）'
dfci.loc[(dfci['original_url'].str.contains('wap.cqcb.com/shangyou_news/')) & (dfci['maindo'].isna()),'maindo'] = '上游新闻网（应用程序）'
dfci.loc[(dfci['original_url'].str.contains('http://qz.fjsen.com/')) & (dfci['maindo'].isna()),'maindo'] = '东南网'
dfci.loc[(dfci['domain'].str.contains('kscgc.sctv-tf.com')) & (dfci['maindo'].isna()),'maindo'] = '四川广播电视台（应用程序）'
dfci.loc[(dfci['domain'].str.contains('cbgc.scol.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '四川日报（应用程序）'
dfci.loc[(dfci['domain'].str.contains('ccwb.1news.cc')) & (dfci['maindo'].isna()),'maindo'] = '长春晚报'
dfci.loc[(dfci['domain'].str.contains('cqcbepaper.cqnews.net')) & (dfci['maindo'].isna()),'maindo'] = '重庆晨报'
dfci.loc[(dfci['domain'].str.contains('daily.cnnb.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '宁波日报（电子报）'
dfci.loc[(dfci['domain'].str.contains('epaper.scjjrb.com')) & (dfci['maindo'].isna()),'maindo'] = '四川经济日报（电子报）'
dfci.loc[(dfci['domain'].str.contains('epaper.tibet3.com')) & (dfci['maindo'].isna()),'maindo'] = '青海法制报（电子报）'
dfci.loc[(dfci['domain'].str.contains('gzdaily.dayoo.com')) & (dfci['maindo'].isna()),'maindo'] = '广州日报（电子报）'
dfci.loc[(dfci['domain'].str.contains('.takungpao.com')) & (dfci['maindo'].isna()),'maindo'] = '大公网'
dfci.loc[(dfci['domain'].str.contains('newpaper.dahe.cn')) & (dfci['maindo'].isna()),'maindo'] = '大河报（电子报）'
dfci.loc[(dfci['domain'].str.contains('news.cnhubei.com')) & (dfci['maindo'].isna()),'maindo'] = '荆楚网'
dfci.loc[(dfci['domain'].str.contains('news.hbtv.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '湖北网络广播电视台-网站'
dfci.loc[(dfci['domain'].str.contains('news.southcn.com')) & (dfci['maindo'].isna()),'maindo'] = '南方网'
dfci.loc[(dfci['domain'].str.contains('news.wenweipo.com')) & (dfci['maindo'].isna()),'maindo'] = '香港文汇网'
dfci.loc[(dfci['domain'].str.contains('photo.wenweipo.com')) & (dfci['maindo'].isna()),'maindo'] = '香港文汇网'
dfci.loc[(dfci['domain'].str.contains('newspaper.jcrb.com')) & (dfci['maindo'].isna()),'maindo'] = '检察日报-电子报'
dfci.loc[(dfci['domain'].str.contains('qjwb.thehour.cn')) & (dfci['maindo'].isna()),'maindo'] = '钱江晚报-电子报'
dfci.loc[(dfci['domain'].str.contains('rmfyb.chinacourt.org')) & (dfci['maindo'].isna()),'maindo'] = '人民法院报-电子报'
dfci.loc[(dfci['domain'].str.contains('shanghai.xinmin.cn')) & (dfci['maindo'].isna()),'maindo'] = '新民网'
dfci.loc[(dfci['domain'].str.contains('www.brtn.cn')) & (dfci['maindo'].isna()),'maindo'] = '北京网络广播电视台'
dfci.loc[(dfci['domain'].str.contains('www.cet.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国经济新闻网'
dfci.loc[(dfci['domain'].str.contains('www.ycwb.com')) & (dfci['maindo'].isna()),'maindo'] = '金羊网'
dfci.loc[(dfci['domain'].str.contains('www.yangtse.com')) & (dfci['maindo'].isna()),'maindo'] = '扬子晚报网'
dfci.loc[(dfci['domain'].str.contains('www.mnw.cn')) & (dfci['maindo'].isna()),'maindo'] = '闽南网'
dfci.loc[(dfci['domain'].str.contains('www.ettoday.net')) & (dfci['maindo'].isna()),'maindo'] = '东森新闻云'
dfci.loc[(dfci['domain'].str.contains('news.qingdaonews.com')) & (dfci['maindo'].isna()),'maindo'] = '青岛新闻网'
dfci.loc[(dfci['domain'].str.contains('www.sznews.com')) & (dfci['maindo'].isna()),'maindo'] = '深圳新闻网'
dfci.loc[(dfci['domain'].str.contains('www.toutiao.com')) & (dfci['maindo'].isna()),'maindo'] = '今日头条'
dfci.loc[(dfci['domain'].str.contains('www.dfcidaily.com')) & (dfci['maindo'].isna()),'maindo'] = '东方早报'
dfci.loc[(dfci['domain'].str.contains('www.henandaily.cn')) & (dfci['maindo'].isna()),'maindo'] = '河南日报网'
dfci.loc[(dfci['domain'].str.contains('www.hxnews.com')) & (dfci['maindo'].isna()),'maindo'] = '海峡网'

dfci.loc[(dfci['domain'].str.contains('www.legaldaily.com.cn')) & (dfci['maindo'].isna()),'maindo'] = '法制网'
dfci.loc[(dfci['domain'].str.contains('www.stdaily.com')) & (dfci['maindo'].isna()),'maindo'] = '中国科技网'
dfci.loc[(dfci['domain'].str.contains('www.chinacourt.org')) & (dfci['maindo'].isna()),'maindo'] = '中国法院网'
dfci.loc[(dfci['domain'].str.contains('www.gongyishibao.com')) & (dfci['maindo'].isna()),'maindo'] = '公益时报网'
dfci.loc[(dfci['domain'].str.contains('news.sciencenet.cn')) & (dfci['maindo'].isna()),'maindo'] = '科学网'
dfci.loc[(dfci['domain'].str.contains('www.apdnews.com')) & (dfci['maindo'].isna()),'maindo'] = '亚太日报'

dfci.loc[(dfci['domain'].str.contains('sputniknews.cn')) & (dfci['maindo'].isna()),'maindo'] = '俄罗斯卫星通讯社'
dfci.loc[(dfci['domain'].str.contains('www.asahi.com')) & (dfci['maindo'].isna()),'maindo'] = '朝日新闻'
dfci.loc[(dfci['domain'].str.contains('www.bbc.com')) & (dfci['maindo'].isna()),'maindo'] = '英国广播公司'

dfci.loc[(dfci['domain'].str.contains('www.g20chn')) & (dfci['maindo'].isna()),'maindo'] = 'G20官网'
dfci.loc[(dfci['domain'].str.contains('olympics')) & (dfci['maindo'].isna()),'maindo'] = '国际奥委会官网'
dfci.loc[(dfci['domain'].str.contains('.fifa.')) & (dfci['maindo'].isna()),'maindo'] = '国际足联官网'
dfci.loc[(dfci['domain'].str.contains('www.yidaiyilu.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国一带一路网'
dfci.loc[(dfci['domain'].str.contains('focacsummit')) & (dfci['maindo'].isna()),'maindo'] = '2018年中非合作论坛北京峰会官网'#由外交部所有
dfci.loc[(dfci['domain'].str.contains('www.beijing2022.cn')) & (dfci['maindo'].isna()),'maindo'] = '北京2022年冬奥委会官网'
dfci.loc[(dfci['domain'].str.contains('results.beijing2022.cn')) & (dfci['maindo'].isna()),'maindo'] = '北京2022年冬奥委会官网'
dfci.loc[(dfci['domain'].str.contains('www.who.int')) & (dfci['maindo'].isna()),'maindo'] = '世界卫生组织官网'
dfci.loc[(dfci['domain'].str.contains('2017.beltandroadfciorum.org')) & (dfci['maindo'].isna()),'maindo'] = ''''“一带一路”国际合作高峰论坛官网'''
dfci.loc[(dfci['domain'].str.contains('www.olympic.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国奥委会官网'

#政府
dfci.loc[(dfci['domain'].str.contains('.cssn.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国社会科学网'
dfci.loc[(dfci['domain'].str.contains('.moh.gov')) & (dfci['maindo'].isna()),'maindo'] = '国家卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('.nhc.gov')) & (dfci['maindo'].isna()),'maindo'] = '国家卫生健康委网站'#部门有更新
dfci.loc[(dfci['domain'].str.contains('.mofcom.gov')) & (dfci['maindo'].isna()),'maindo'] = '商务部网站'
dfci.loc[(dfci['domain'].str.contains('www.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国政府网'
dfci.loc[(dfci['domain'].str.contains('cdc.cn')) & (dfci['maindo'].isna()),'maindo'] = '疾病预防控制中心网站'
dfci.loc[(dfci['domain'].str.contains('ccdi.gov')) & (dfci['maindo'].isna()),'maindo'] = '中央纪委国家监委网站'
dfci.loc[(dfci['domain'].str.contains('www.xichang.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站' #'西昌市人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.beijing.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站' #'北京市人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.fujian.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.fuzhou.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.hunan.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.hubei.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.quanzhou.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('.hebei.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.jiangsu.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.zjc.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.anshun.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.ak.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.haishu.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.sc.gov')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('sc.isd.gov.hk')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站' #香港
dfci.loc[(dfci['domain'].str.contains('www.gov.mo')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站' #澳门
dfci.loc[(dfci['domain'].str.contains('www.gcs.gov.mo')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站' #澳门
dfci.loc[(dfci['domain'].str.contains('www.sansha.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.zjkcl.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('www.yn.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '地方人民政府网站'
dfci.loc[(dfci['domain'].str.contains('appweb.scpublic.cn')) & (dfci['maindo'].isna()),'maindo'] = '四川发布（应用程序）'


dfci.loc[(dfci['domain'].str.contains('wjw.fujian.gov')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'#'福建省卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wsjk.')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('mfa.gov')) & (dfci['maindo'].isna()),'maindo'] = '外交部网站'
dfci.loc[(dfci['domain'].str.contains('.cppcc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国政协网'
dfci.loc[(dfci['domain'].str.contains('.mem.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '应急管理部网站'
dfci.loc[(dfci['domain'].str.contains('.cppcc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国政协网'
dfci.loc[(dfci['domain'].str.contains('www.npc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国人大网'
dfci.loc[(dfci['domain'].str.contains('chinapeace.')) & (dfci['maindo'].isna()),'maindo'] = '中国长安网'
dfci.loc[(dfci['domain'].str.contains('www.spp.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '最高人民检察院网站'
dfci.loc[(dfci['domain'].str.contains('www.court.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '最高人民法院网站'
dfci.loc[(dfci['domain'].str.contains('www.moe.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '教育部网站'
dfci.loc[(dfci['domain'].str.contains('cnda.cfda.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '国家药监局网站'
dfci.loc[(dfci['domain'].str.contains('www.mof.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '财政部网站'
dfci.loc[(dfci['domain'].str.contains('www.moc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '交通运输部网站' #部门有更新
dfci.loc[(dfci['domain'].str.contains('www.forestry.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '国家林草局网站'
dfci.loc[(dfci['domain'].str.contains('cea.gov.')) & (dfci['maindo'].isna()),'maindo'] = '中国地震局网站'
#dfci.loc[(dfci['domain'].str.contains('s.scio.gov.')) & (dfci['maindo'].isna()),'maindo'] = '国务院新闻办公室网站'
dfci.loc[(dfci['domain'].str.contains('www.scio.gov.')) & (dfci['maindo'].isna()),'maindo'] = '国务院新闻办公室网站'
dfci.loc[(dfci['domain'].str.contains('www.mlr.gov.')) & (dfci['maindo'].isna()),'maindo'] = '自然资源部网站' #部门有更新
dfci.loc[(dfci['domain'].str.contains('www.cma.gov.')) & (dfci['maindo'].isna()),'maindo'] = '中国气象局网站'
dfci.loc[(dfci['domain'].str.contains('www.spb.gov.')) & (dfci['maindo'].isna()),'maindo'] = '国家邮政局网站'
dfci.loc[(dfci['domain'].str.contains('www.mod.gov.')) & (dfci['maindo'].isna()),'maindo'] = '国防部网'
dfci.loc[(dfci['domain'].str.contains('www.chinatax.gov.')) & (dfci['maindo'].isna()),'maindo'] = '税务总局网站'
dfci.loc[(dfci['domain'].str.contains('hc.jiangxi.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('sxwjw.shaanxi.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.ah.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.beijing.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'

dfci.loc[(dfci['domain'].str.contains('www.gzhfpc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('www.hebwst.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['origin_url_x'].str.contains('www.jl.gov.cn/szfzt/jlzxd/yqtb')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('www.xjhfpc.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('www.zjwjw.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'

dfci.loc[(dfci['domain'].str.contains('wjw.hubei.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.hunan.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.jiangsu.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.nmg.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wjw.shanxi.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('wst.hainan.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'
dfci.loc[(dfci['domain'].str.contains('www.hnwsjsw.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '各地卫生健康委网站'


dfci.loc[(dfci['domain'].str.contains('www.diaoyudao.org.cn')) & (dfci['maindo'].isna()),'maindo'] = '钓鱼岛官网'
dfci.loc[(dfci['domain'].str.contains('www.cusdn.org.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国城市低碳经济网'
dfci.loc[(dfci['domain'].str.contains('news.ceic.ac.cn')) & (dfci['maindo'].isna()),'maindo'] = '中国地震台网'



dfci.loc[(dfci['domain'].str.contains('.gov.cn')) & (dfci['maindo'].isna()),'maindo'] = '其他网站（政府机构）'
dfci.loc[(dfci['domain'].str.contains('.gov.hk')) & (dfci['maindo'].isna()),'maindo'] = '其他网站（政府机构）'
dfci.loc[(dfci['domain'].str.contains('.edu.cn')) & (dfci['maindo'].isna()),'maindo'] = '高校等教育机构网站'



dfci.loc[dfci['maindo'].isna(),'maindo'] = '其他网站（待确定）'






























