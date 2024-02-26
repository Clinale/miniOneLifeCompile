#!/usr/bin/env python3
import requests
import os
from os.path import dirname, realpath
import sys
import pandas as pd

def main():
    # 读取xlsx文件中名为'sheet_name'的sheet
    df = pd.read_excel('THOL Translation.xlsx', sheet_name='使用说明', dtype=str)

    # 访问名为'語言列表'（或者'语言列表'）的列
    langs = df['語言列表 / 语言列表'].dropna()  # 或者 df['语言列表']

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
    main()
