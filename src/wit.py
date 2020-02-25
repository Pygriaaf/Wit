import sys
from getpass import getuser
from os import mkdir

class Command():
    def cmd_init(self,parameter):
        #错误输入处理
        if len(parameter) == 0:
            print("提示: init [项目名] [文件名]")
            exit()
        if len(parameter) > 2:
            print("错误:没有找到选项或参数'%s'!" % ('\',\''.join(parameter[2:])))
            exit()
        if parameter[1].count('.') != 1 or parameter[1].split('.')[1] not in  ['doc','docx']:
            print("错误:'%s' 不是Word文档!请输入带有'.doc' 或 '.docx'后缀的文件名." % (parameter[1],))
            exit()
        #创建项目文件
        mkdir("C:/Users/%s/%s" % (getuser(),parameter[0]))
        mkdir("C:/Users/%s/%s/.wit" % (getuser(),parameter[0]))
        mkdir("C:/Users/%s/%s/.wit/storage" % (getuser(),parameter[0]))
        mkdir("C:/Users/%s/%s/.wit/history" % (getuser(),parameter[0]))
        init_make_filename = open("C:/Users/%s/%s/.wit/filename" % (getuser(),parameter[0]),'x')
        init_make_filename.write(parameter[1])
        init_make_filename.close()
        init_make_pointer = open("C:/Users/%s/%s/.wit/pointer" % (getuser(),parameter[0]),'x')
        init_make_pointer.write('master:nohistories')
        init_make_pointer.close()
        init_make_record = open("C:/Users/%s/%s/.wit/history/master.htrc" % (getuser(),parameter[0]),"x")
        init_make_record.close()
        mkdir("C:/Users/%s/%s/.wit/history/master" % (getuser(),parameter[0]))
        make_doc_file = open("C:/Users/%s/%s/%s" % (getuser(),parameter[0],parameter[1]),'x')
        make_doc_file.close()

    def cmd_add(self,parameter):
        pass
    def cmd_commit(self,parameter):
        pass

def main():
    USER_INPUT = sys.argv[1:] #获取参数
    #try:
    cmd = getattr(Command,"cmd_" + USER_INPUT[0]) #命令入口
    #except:
        #print("没有找到" + USER_INPUT[0] + "命令！")
        #exit()
    cmd(cmd,USER_INPUT[1:]) #执行命令

if __name__ == '__main__': #程序入口
    main()
