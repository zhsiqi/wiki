%% 补全数据多个csv的拼接 
% 读取当前文件夹里所有.csv的文件，且把文件名按顺序读取在Files中
Files=dir('*.csv'); 
n=length(Files); % n表示Files中有多少个文件
x=Files(1).name; % 把Files中第一个文件的名字放进x里

%设置读取文件的方式
opts = detectImportOptions(x);
opts.PreserveVariableNames = 1; %保留原表头的变量名
% opts = setvartype(opts,opts.VariableNames(1),'char');%设置"原微博内容"字段的格式

%读取第一个csv放进evquan里
evquan=readtable(x,opts); %用更新过的option读取.csv文件

for i=1:n-1 %循环加入新文件的内容
    
    x=Files(i+1).name; %依次读取后面Files的每个名字 
    z=readtable(x,opts); %依次读取文件夹中.csv的文件
    evquan=[evquan;z];% 把新文件的数据接在rawdata下面
    %下面两行代码用于在命令窗口显示代码运行的进度，因为有时候文件太多处理的时间长，这个可以不要
    Dis=strcat('当前进度 ',int2str(i/n*100),'%');
    disp(Dis)
   
end

writetable(evquan,'wiki5个.xlsx');