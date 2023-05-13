*导入csv, utf-8编码
import delimited evadd.csv, encoding(UTF-8)

import excel "/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/evdata.xlsx", sheet("Sheet1") firstrow

*根据分类变量生成虚拟变量
tab disaster, gen(disaster)
tab antici, gen(antici)
tab indisas, gen(indisas)


format cre_range_d %8.00f

*缺失值
drop if event_id==202001

*2023-03-10
tab type, gen(type)

pwcorr type1 type2 type3 year cre_range_d, sig star(0.05)

pwcorr year cite_range, sig star(0.05)

pwcorr type1 type2 type3 cite_range, sig star(0.05)

*collapse，它针对由一个或更多个变量所界定的不同群体汇总出均值、中位数或其他统计量。

*collapse (mean, sd, min p25 median p75 max) cre_range_d, by(disaster)
* 描述统计
tabstat cre_range_d, by(disaster) stat(count mean sd min p25 median p75 max)
tabstat cre_range_d, by(antici) stat(count mean sd min p25 median p75 max)

*上面的只是在stata运行，下面的包括输出文件
logout, save(stat_disas_des) word excel replace: ///
tabstat cre_range_d, by(disaster2) stat(count mean sd min p25 median p75 max)

logout, save(stat_indisas_des) word excel replace: ///
tabstat cre_range_d, by(indisas2) stat(count mean sd min p25 median p75 max)

logout, save(stat_antici_des) word excel replace: ///
tabstat cre_range_d, by(antici2) stat(count mean sd min p25 median p75 max)

*corr
pwcorr disaster2 indisas2 antici2 cre_range_d, sig star(0.05) /* 显示显著性，以及若小于0.05标注* */

logout, save(stat_pwcor) word excel replace: ///
pwcorr disaster2 indisas2 antici2 cre_range_d, sig star(0.05)

*scatter cre_range_d indisas2
*pwcorr antici2 cre_range_d, sig

*scatter cre_range_d disaster2
*pwcorr cre_range_d disaster2, sig
*reg cre_range_d antici2 disaster2

*方差齐性检查
sdtest cre_range_d, by (disaster2) 
sdtest cre_range_d, by (indisas2)
sdtest cre_range_d, by (antici2)
*上面结果都不齐

*分组比较：使用两组方差不齐的 非配对 独立样本的 t-test

ttest cre_range_d, by (type1) unpaired unequal
ttest cre_range_d, by (type2) unpaired unequal
ttest cre_range_d, by (type3) unpaired unequal

*下面三个是输出
logout, save(stat_tt_disas) word excel replace: ///
ttest cre_range_d, by (disaster2) unpaired unequal

logout, save(stat_tt_indisas) word excel replace: ///
ttest cre_range_d, by (indisas2) unpaired unequal

logout, save(stat_tt_antici) word excel replace: ///
ttest cre_range_d, by (antici2) unpaired unequal

*anova

oneway cre_range_d type
*前提不满足，无法anova 
gen type12 =.
replace type12=1 if type1==1
replace type12=2 if type2==1

gen type13 =.
replace type13=1 if type1==1
replace type13=2 if type3==1

gen type23 =.
replace type23=1 if type2==1
replace type23=2 if type3==1

*分组比较：使用两组方差不齐的 非配对 独立样本的 t-test

ttest cre_range_d, by (type12) unpaired unequal
ttest cre_range_d, by (type13) unpaired unequal
ttest cre_range_d, by (type23) unpaired unequal


tabstat cre_range_d if type1==1, stat(count mean sd var min max)
tabstat cre_range_d if type2==1, stat(count mean sd var min max)
tabstat cre_range_d if type3==1, stat(count mean sd var min max)

*正态分布检验
sktest cre_range_d if type1==1
sktest cre_range_d if type2==1
sktest cre_range_d if type3==1


*方差齐性检验*
robvar cre_range_d, by(type)

kwallis cre_range_d, by(type)

kwallis2 

kwallis2 cre_range_d, by(type)



* 编辑者人数 与 事件类型

tab type, gen(type)

robvar author_count_1, by(type) 
*显示方差是齐的

*将type的文字编码改为数字编码
gen typenum =. 
replace typenum=1 if type=="媒介事件"
replace typenum=2 if type=="媒介灾难"
replace typenum=3 if type=="新闻事件"

anova author_count_1 typenum


