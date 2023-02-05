
 
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
