#!/bin/awk -f

BEGIN{
    f = "test -f "
    cmd1 = f""ARGV[1]
    
    # 如果文件不存在，退出程序
    if(system(cmd1)) {
        print "File",ARGV[1],"not exist!"
        exit
    }
    
    print "IPPOOL = [" > "temp"
}
{
    print "    {'ipaddr': '"$0"'}," >> "temp"    
}
END{
    print "]" >> "temp"
    # 重命名临时文件为源文件
    t1 = "mv temp "
    t2 = " 2>/dev/null"
    cmd = t1""ARGV[1]""t2
    system(cmd)
    print "转换成功!!!"
}
