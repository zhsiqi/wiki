*根据分类变量生成虚拟变量
tab type, gen(type0)

pwcorr type01 type02 type03 link_count sci_paper_count relevant, sig star(0.05)

pwcorr year link_count sci_paper_count relevant, sig star(0.05)

list year if relevant==1

sum link_count sci_paper_count relevant, detail
