from urllib.request import urlopen
from os import mkdir,popen,system
from os.path import isdir

def main():
    print('输入"1":安装\n输入"2":更新\n输入其他:退出\n\n程序必须在联网环境下使用!')
    user_input = input('>')
    if user_input == '1':
        if isdir('C:\\Wit'):
            print('文件已安装，无需再次安装.')
            a = input('按回车退出...')
            del a
            return None
        try:
            print('正在连接服务器...')
            github_wit = urlopen('https://raw.githubusercontent.com/Pygriaaf/Wit/master/src/wit.py')
        except:
            print('失败:没有连上服务器!请重启网络再尝试.')
            a = input('按回车退出...')
            del a
            return None
        print('正在从服务器上下载文件...')
        wit_file_content = github_wit.read()
        github_wit.close()
        print('正在复制文件...')
        mkdir('C:\\Wit')
        wit_file = open('C:\\Wit\\wit.py','wb')
        wit_file.write(wit_file_content)
        wit_file.close()
        print('正在设置系统变量...')
        a = popen('wmic ENVIRONMENT where "name=\'path\' and username=\'<system>\'" set VariableValue="%path%;C:\\Wit"')
        del a
        print('完成!')
        a = input('按回车退出...')
        del a
    elif user_input == '2':
        if not isdir('C:\\Wit'):
            print('Wit未安装,请安装.')
            return None
        try:
            print('正在连接服务器...')
            github_wit = urlopen('https://raw.githubusercontent.com/Pygriaaf/Wit/master/src/wit.py')
        except:
            print('没有连上服务器!请重新尝试.')
            a = input('按回车退出...')
            del a
            return None
        print('正在从服务器上下载文件...')
        wit_file_content = github_wit.read()
        github_wit.close()
        print('正在更新文件...')
        wit_file = open('C:\\Wit\\wit.py','wb')
        wit_file.write(wit_file_content)
        wit_file.close()
        print('完成!')
        a = input('按回车退出...')
        del a
    else:
        pass

if __name__ == '__main__':
    main()
