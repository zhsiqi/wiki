*导入csv, utf-8编码
import delimited year_edirange.csv, encoding(UTF-8)

import excel "/Users/zhangsiqi/Documents/毕业论文数据/专门输出数据表/0322/year_edirange.xlsx", sheet("Sheet1") firstrow


*年份和编辑历史跨度的相关与回归

logout, save(stat_edi_pwcor) word excel replace: ///
pwcorr year edi_range_y, sig star(0.05)

tab type, gen(type)
pwcorr year type1 type2 type3 edi_range_y, sig star(0.05) 

reg edi_range_y type1 type2 type3 i.year
reg edi_range_y type1 type2 type3 year
reg edi_range_y year

 
scatter edi_range_y year
reg edi_range_y type1 type2 type3 i.year
predict yhat, xb
predict resid, r
sum resid
sum edi_range_y yhat
gen sres = res/1.4829
twoway (scatter sres year), yline(0)


*-------
 
 
recode editcount(-99=.)
recode viewcount(-99=.)

format topeditor_count %18.0f
format reference_count editcount viewcount link_count %8.0f

logout, save(logout-basic1) word excel replace: ///
sum reference_count editcount topeditor_count viewcount link_count, format



*tabout reference_count editcount topeditor_count viewcount link_count using table12.docx, replace style(tex) font(bold) c(mean reference_count) sum
 
///sysuse auto, cleartabout rep78 foreign using table10.tex, replace 
///style(tex) font(italic) c(mean weight) f(0c) sum 
///twidth(9) h1(Car type (mean weight in lbs.)) h3(nil) 
///title(Table 10: Simple twoway summary table of means) 
///fn(auto.dta)
