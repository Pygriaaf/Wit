#文件名:wit.py
#作者:Pygriaaf
#版权:GPL v3.0 (C) Pygriaaf
#时间:2020-2-24
#邮箱:pygriaaf@163.com

import sys
from os import mkdir,getcwd
from os.path import getsize,isdir
from shutil import copy,move
from hashlib import sha1
from time import localtime

def debug(return_words=None,if_return_words=False,if_exit=False):
    if return_words:
        print(return_words)
    if if_exit:
        exit()


class Command():
    def cmd_init(self,parameter):
        #错误输入处理
        if len(parameter) == 0:
            print("提示: init [项目名] [文件名]")
            exit()
        if len(parameter) > 2:
            print("错误:没有找到选项或参数'%s'." % ('\',\''.join(parameter[2:]),))
            exit()
        if parameter[1].count('.') != 1 or parameter[1].split('.')[1] not in  ['doc','docx']:
            print("错误:'%s' 不是Word文档!请输入带有'.doc' 或 '.docx'后缀的文件名." % (parameter[1],))
            exit()
        if isdir(getcwd() + '\\' + parameter[0]): #判断目录是否已经被创建
            print("错误:该目录下已存在%S目录，无法创建项目." % (parameter[0],))
            exit()
        #创建项目文件 = 执行init命令
        mkdir(getcwd() + ("\\%s" % (parameter[0],)))
        mkdir(getcwd() + ("\\%s\\.wit" % (parameter[0],)))
        mkdir(getcwd() + ("\\%s\\.wit\\storage" % (parameter[0])))
        mkdir(getcwd() + ("\\%s\\.wit\\history" % (parameter[0])))
        init_make_filename = open(getcwd() + ("\\%s\\.wit\\filename" % (parameter[0],)),'x')
        init_make_filename.write(parameter[1])
        init_make_filename.close()
        init_make_pointer = open(getcwd() + ("\\%s\\.wit\\pointer" % (parameter[0],)),'x')
        init_make_pointer.write('master:nohistories')
        init_make_pointer.close()
        init_make_record = open(getcwd() + ("\\%s\\.wit\\history\\master.htrc" % (parameter[0],)),"x")
        init_make_record.close()
        mkdir(getcwd() + ("\\%s\\.wit\\history\\master" % (parameter[0],)))
        make_doc_file = open(getcwd() + ("\\%s\\%s" % (parameter[0],parameter[1])),'x')
        make_doc_file.close()

    def cmd_add(self,parameter):
        #错误输入处理
        if len(parameter) > 2:
            print("错误:没有找到选项或参数'%s'." % ('\',\''.join(parameter[2:])))
            exit()
        if not isdir(getcwd() + '\\.wit'): #判断是否是项目目录
            print("错误:该目录不是wit项目，无法使用add命令.")
            exit()
        #将文件复制到暂存区 = 执行add命令
        open_filename = open("./.wit/filename",'r')
        filename = open_filename.read()
        open_filename.close()
        copy('./%s' % (filename,),'./.wit/storage')
    def cmd_commit(self,parameter):
        #错误输入处理
        if len(parameter) == 0:
            print("提示: commit [说明]")
            exit()
        if len(parameter) > 1:
            print("错误:没有找到选项或参数'%s'." % ('\',\''.join(parameter[1:])))
            exit()
        if not isdir(getcwd() + '\\.wit'): #判断是否是项目目录
            print("错误:该目录不是wit项目，无法使用commit命令.")
            exit()
        #将文件记录到历史 = 执行commit命令
        open_pointer = open('./.wit/pointer','r')
        branch_pointer = open_pointer.read().split(':')[0]
        open_pointer.close()
        open_filename = open("./.wit/filename",'r')
        filename = open_filename.read()
        open_filename.close()
        try: #判断暂存区是否有文件
            open_file = open(('./.wit/storage/' + filename),'rb')
            hashsha1 = sha1((str(open_file.read()) + '%s-%s-%s-%s-%s-%s' % localtime()[:6]).encode('utf-8')).hexdigest()
            open_file.close()
        except:
            print("错误:暂存区里没有文件!请使用add命令将文件移至暂存区.")
            exit()
        if getsize('./.wit/history/%s.htrc' % (branch_pointer,)) == 0: #"空记录"判断
            move('./.wit/storage/' + filename,'./.wit/history/master/%s.%s' % (hashsha1,filename.split('.')[1]))
            open_historyrecord = open('./.wit/history/%s.htrc' % (branch_pointer),'a')
            open_historyrecord.write(
                'ID:'+hashsha1+' '+'Time:'+('%s-%s-%s-%s-%s-%s' % localtime()[:6])+' '+'Message:'+parameter[0]+' '+'Tag:'+' '+'Point:'+'\n'
            )
            open_historyrecord.close()
            open_pointer = open('./.wit/pointer','w')
            open_pointer.write(branch_pointer + ':' + hashsha1)
            open_pointer.close()
        else:
            open_historyrecord = open('./.wit/history/%s.htrc' % (branch_pointer),'r')
            historyrecord_newest_pointer = open_historyrecord.readlines()[-1][:-1].split(' ')[0].split(':')[1]
            open_historyrecord.close()
            open_pointer = open('./.wit/pointer','r')
            hash_pointer = open_pointer.read().split(':')[1]
            open_pointer.close()
            if historyrecord_newest_pointer == hash_pointer: #指针指向判断
                move('./.wit/storage/' + filename,'./.wit/history/master/%s.%s' % (hashsha1,filename.split('.')[1]))
                open_historyrecord = open('./.wit/history/%s.htrc' % (branch_pointer),'a')
                open_historyrecord.write(
                    'ID:'+hashsha1+' '+'Time:'+('%s-%s-%s-%s-%s-%s' % localtime()[:6])+' '+'Message:'+parameter[0]+' '+'Tag:'+' '+'Point:'+'\n'
                )
                open_historyrecord.close()
                open_pointer = open('./.wit/pointer','w')
                open_pointer.write(branch_pointer + ':' + hashsha1)
                open_pointer.close()
            else:
                print("错误:当前文件指针没有指向最新历史记录,无法提交文件.")
                exit()

def main():
    user_input = sys.argv[1:] #获取参数
    #try:
    cmd = getattr(Command,"cmd_" + user_input[0]) #命令入口
    #except:
        #print("没有找到" + user_input[0] + "命令.")
        #exit()
    cmd(cmd,user_input[1:]) #执行命令

if __name__ == '__main__': #程序入口
    main()
