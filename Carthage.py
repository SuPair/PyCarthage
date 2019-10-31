#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    @File    :   carthage.py
    @Contact :   sp106168@gmail.com
    @License :   (C)Copyright 2014-2019
    
    @Modify Time      @Author    @Version    @Description
    ------------      -------    --------    -----------
    2019/8/17 4:13 PM   moore      1.0         None
    """

# import lib
import os
# 文件所在目录需要存放在项目根目录
carthage_file_dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
cart_file_path = carthage_file_dir_path + '/Cartfile'
carthage_dir_path = carthage_file_dir_path + '/Carthage'


def get_frameworks(path, input_path=None, output_path=None):
    f_list = os.listdir(path)
    f_name_list = []
    # print f_list
    for index in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(index)[1] == '.framework':
            f_name_list.append(index)
    rewrite_file(input_path, f_name_list)
    rewrite_file(output_path, f_name_list, 1)


def rewrite_file(file_path, framework_names, file_type=0):
    with open(file_path, "w+") as f:
        f.seek(0)
        f.truncate()  # 清空文件
        write_type = 'input.xcfilelist'
        if file_type == 0:
            root_path = '$(SRCROOT)/Carthage/Build/iOS/'
        else:
            write_type = 'output.xcfilelist'
            root_path = '$(BUILT_PRODUCTS_DIR)/$(FRAMEWORKS_FOLDER_PATH)/'
        print(write_type + ' 开始写入！')
        for framework_name in framework_names:
            framework_path = root_path + framework_name + '\n'
            f.write(framework_path)
        f.close()
        print(write_type + ' 写入完成！')


def check_path_run():
    support_dir_path = carthage_file_dir_path + '/Support'
    if not os.path.exists(support_dir_path):
        os.makedirs(support_dir_path)

    ios_dir_path = carthage_file_dir_path + '/Carthage/Build/iOS'
    input_path = support_dir_path + '/input.xcfilelist'
    output_path = support_dir_path + '/output.xcfilelist'
    get_frameworks(ios_dir_path, input_path, output_path)


def install_carthage(name=None):
    # state = os.system('command -v carthage')
    state = os.system(
        "if ! command -v carthage > /dev/null; then printf 'Carthage is not installed.\n'; printf 'See "
        "https://github.com/Carthage/Carthage for install instructions.\n'; exit 1; fi")
    if state != 0:
        exit(1)
    cmd_str = 'carthage update --platform iOS --use-submodules --no-use-binaries'
    if name is not None:
        cmd_str = cmd_str + ' ' + name
        pass
    os.chdir(carthage_file_dir_path)
    state = os.system(cmd_str)
    if state != 0:
        exit(1)


def install_update_framework():
    """
    安装框架或者更新框架
    :return:
    """
    cmd_str = None
    if len(os.sys.argv) > 1:
        print('框架更新中。。。')
        cmd_str = ''
        for index, input_value in enumerate(os.sys.argv):
            if index > 0:
                if index == 1:
                    cmd_str = input_value
                else:
                    cmd_str = cmd_str + ' ' + input_value
    else:
        print('框架安装中。。。')
    install_carthage(cmd_str)
    if cmd_str is None:
        print('安装完毕！')
    else:
        print('更新完毕！')
    print('环境更新中。。。')
    check_path_run()
    print('更新完毕！')


def check_cart_file(show_info=True):
    """
    检查是否存在Cartfile
    :return:
    """

    if os.path.exists(cart_file_path):
        if show_info:
            print('Cartfile 存在！')
    else:
        print('Cartfile 不存在！')
        if check_false_input('是否需要创建Cartfile？'):
            return False
        print('Cartfile 创建中。。。')

        while True:
            input_str = input('请输入需要的框架(只支持单个框架添加!):')
            if len(str(input_str)) > 0:
                input_values = [str(input_str)]
                touch_cart_file(write_data=input_values)
                print('Cartfile 创建完毕')
                if check_false_input('是否需要安装？'):
                    return False
            else:
                print('框架名输入有误，请重新输入！')
    return True


def touch_cart_file(file_name='Cartfile', write_data=None):
    """
    创建file_name
    :param write_data: 写入数据
    :param file_name: file_name
    :return:
    """
    fd = open(file_name, 'a+')
    if write_data is not None:
        if len(write_data) > 0:
            for data in write_data:
                fd.writelines(data + '\n')
    fd.close()


def check_false_input(prompt_value) -> bool:
    """
    检查输入是否是N
    :param prompt_value: 提示信息
    :return:
    """
    input_value = input(prompt_value + '(Y/n):')
    if str(input_value) == 'n' or str(input_value) == 'N':
        return True
    return False


def add_framework():
    """
    添加框架
    :return:
    """
    if check_cart_file(show_info=False) is False:
        return
    while True:
        input_str = input('请输入需要的框架(只支持单个框架添加!):')
        if len(str(input_str)) > 0:
            input_values = [str(input_str)]
            touch_cart_file(write_data=input_values)
            if check_false_input('是否继续添加？'):
                """
                不继续添加
                """
                if check_false_input('是否安装或者更新框架？'):
                    return
                install_update_framework()
                return
        else:
            print('框架名输入有误，请重新输入！')


def clear_file():
    os.remove(cart_file_path)
    shutil.rmtree(carthage_dir_path)


def check_cmd():
    while True:
        input_str = input('请输入对应命令：')
        if input_str == 'help' or input_str == 'h':
            cmd_help()
        elif input_str == 'add' or input_str == 'a':
            add_framework()
        elif input_str == 'quite' or input_str == 'q':
            print('退出工具！')
        elif input_str == 'clear' or input_str == 'c':
            print('清除文件中。。。')
            clear_file()
            print('清除文件完毕！')


def cmd_help():
    print('Carthage 帮助脚本！')
    print('help     or h show help info')
    print('add      or a add framework')
#    print('delete   or d delete framework')
    print('update   or u update framework')
    print('clear    or c delete Cartfile')
    print('quite    or q quite cmd')


if __name__ == '__main__':
    cmd_help()
    check_cmd()

