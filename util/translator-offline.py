#!/usr/bin/env python3
import requests
import os
from os.path import dirname, realpath
import sys
import pandas as pd
# 引用 tkinter
from tkinter import *
from tkinter.ttk import *

def tk_win():
    # 新建 tk 窗口
    tran = Tk()
    tran.title('translator')
    screen_width,screen_height = tran.maxsize() #获取屏幕最大长宽
    win_w = int((screen_width-240)/2)
    win_h = int((screen_height-480)/2)
    tran.geometry(f'250x140+{win_w}+{win_h}')
    
    # 文本
    text_1 = Label(tran, text='Choose your language')
    text_1.pack()
    # language 选项框
    language = ['English', '正體中文', '简体中文', 'Українська', 'Deutsch']
    lc = Combobox(tran, values=language)
    lc['state'] = 'readonly'
    lc.current(0)
    lc.pack()
    
    # 调试选项
    '''
    def on_select(event):
        print(f"language is {lc.get()}")
    lc.bind("<<ComboboxSelected>>", on_select)
    '''
    
    # 文本
    text_2 = Label(tran, text='Append English after translated objects?')
    text_2.pack()
    # is_append 选项框
    is_append_list = ["No", "Yes"]
    is_append_choose = Combobox(tran, values=is_append_list)
    is_append_choose['state'] = 'readonly'
    is_append_choose.current(0)
    is_append_choose.pack()

    # 调试选项
    '''
    def on_select_2(event):
        print(f"is_append is {is_append_choose.get()}")
    is_append_choose.bind("<<ComboboxSelected>>", on_select_2)
    '''
    
    def done(window):
        # 处理数据
        global lang
        global is_append
        lang = language.index(str(lc.get()))
        is_append = is_append_list.index(is_append_choose.get())
        
        # 打印选项(用于核对)
        print('--- Your Choose ---')
        print('Language:', lc.get())
        print('is_append:', is_append_choose.get())
        print('Language-Num:', lang)
        #print(type(lang))
        print('is_append-Num:', is_append)
        #print(type(is_append))
        print('--- The End ---')
        window.destroy()
        #ok = input('true?[ENTER to confirm or type N to try again]: ')
        main()
    Bu = Button(tran, text ="Done", command=lambda: done(tran))
    Bu.pack()
    
    tran.mainloop()
def main():
    # 读取xlsx文件中名为'sheet_name'的sheet
    df = pd.read_excel('THOL Translation.xlsx', sheet_name='使用说明', dtype=str)

    # 访问名为'語言列表'（或者'语言列表'）的列
    langs = df['語言列表 / 语言列表'].dropna()  # 或者 df['语言列表']
    
    '''
    for i in range(len(langs)):
        print(f'{i}: {langs[i]}')
    print(f'Please input 0~{len(langs)-1}: ')
    while 1:
        try:
            lang = int(input())
            if lang < 0 or lang > len(langs) - 1:
                raise ValueError
            break
        except ValueError:
            print(f'Please input 0~{len(langs)-1}: ')
    '''
    
    '''
    print('\nAppend English after translated objects?')
    print('0: No')
    print('1: Yes')
    print('Please input 0~1: ')
    while 1:
        try:
            is_append = int(input())
            if is_append < 0 or is_append > 1:
                raise ValueError
            break
        except ValueError:
            print('Please input 0~1: ')
    '''

    print("Translating Objects...")

    if os.path.isfile('objects/cache.fcz'):
        os.remove('objects/cache.fcz')

    df = pd.read_excel('THOL Translation.xlsx', sheet_name='Object', dtype=str)
    keys = df['key'].dropna()
    data1 = df.iloc[:, 3*lang]
    if is_append:
        data2 = df['English']

    for i in range(len(keys)):
        translated = data1[i]
        if not pd.isna(translated):
            try:
                with open(f'objects/{keys[i]}', encoding='utf-8') as f:
                    content = f.readlines()
            except FileNotFoundError as e:
                print(e)
                continue

            if is_append and data2[i] != '':
                content[1] = translated.split('#')[0].split(
                    ' $')[0] + data2[i] + '\n'
            else:
                content[1] = translated + '\n'

            with open(f'objects/{keys[i]}', 'w', encoding='utf-8') as f:
                f.writelines(content)

    menuItems = {}
    try:
        with open('languages/English.txt', encoding='utf-8') as f:
            datas = f.readlines()
            for data in datas:
                if data == '\n':
                    continue
                name = data.split(' ')[0]
                value = data[data.index('"') + 1:-2]
                menuItems[name] = value

    except FileNotFoundError as e:
        print(e)

    print("Translating Menu...")

    df = pd.read_excel('THOL Translation.xlsx', sheet_name='Menu', dtype=str)
    keys = df['Key'].dropna()
    data = df.iloc[:, 3*lang]
    for i in range(len(keys)):
        if not pd.isna(data[i]):
            menuItems[keys[i]] = data[i]

    with open('languages/English.txt', 'w', encoding='utf-8') as f:
        for key in menuItems:
            f.write(f'{key} "{menuItems[key]}"\n')

    print("Translating Images...")

    df = pd.read_excel('THOL Translation.xlsx', sheet_name='Image', dtype=str)
    keys = df['Key'].dropna()
    data = df.iloc[:, 3*lang]
    for i in range(len(keys)):
        link = data[i]
        if not pd.isna(link):
            r = requests.get(link)
            if r.status_code != 200:
                print(f'File can\'t be found: {link}')
                continue
            with open(f'graphics/{keys[i]}', 'wb') as f:
                f.write(r.content)

    print("Apply settings...")

    df = pd.read_excel('THOL Translation.xlsx', sheet_name='Setting', dtype=str)
    keys = df['Key'].dropna()
    data = df.iloc[:, 3*lang]
    for i in range(len(keys)):
        value = data[i]
        if not pd.isna(value):
            with open(f'settings/{keys[i]}', 'w') as f:
                f.write(str(value))

    print("Translating done!")


if __name__ == '__main__':
    tk_win()
