import excel "/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/entry_cite_di_range.xlsx", sheet("Sheet1") firstrow

*根据分类变量生成虚拟变量
tab type, gen(type)


format cre_range_d %8.00f

pwcorr type1 type2 type3 year time_di_d cite_range_x , sig star(0.05)


gen type12 =.
replace type12=1 if type1==1
replace type12=2 if type2==1

gen type13 =.
replace type13=1 if type1==1
replace type13=2 if type3==1

gen type23 =.
replace type23=1 if type2==1
replace type23=2 if type3==1

*正态分布检验

sktest cite_range_x
sktest cite_range_x if type1==1
sktest cite_range_x if type2==1
sktest cite_range_x if type3==1

swilk cite_range_x if type1==1
swilk cite_range_x if type2==1
swilk cite_range_x if type3==1

qnorm cite_range_x if type1==1
qnorm cite_range_x if type2==1
qnorm cite_range_x if type3==1

*方差齐性检验*
robvar cite_range_x, by(type)


*分组比较：使用两组方差不齐的 非配对 独立样本的 t-test

ttest cre_range_d, by (type12) unpaired unequal
ttest cre_range_d, by (type13) unpaired unequal
ttest cre_range_d, by (type23) unpaired unequal


tabstat cre_range_d if type1==1, stat(count mean sd var min max)
tabstat cre_range_d if type2==1, stat(count mean sd var min max)
tabstat cre_range_d if type3==1, stat(count mean sd var min max)
