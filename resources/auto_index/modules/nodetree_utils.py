#! /usr/bin/python
#-*- coding: utf-8 -*-

import os

import nodetree


"""
ノードツリーを利用した独立モジュール集
"""

def gen_fileTree(dirName,parentNode=None):
    """ ファイル木構造を検索する。お得意の引数束縛型再起呼び出し形式"""
    dirName = os.path.abspath(dirName)
    # ルートノード初期化
    if not parentNode :
        parentNode = nodetree.Node(dirName)
        parentNode.file_type = "dir"

    # ディレクトリをなめる
    for path in os.listdir(dirName):
        # ノード生成
        path = os.path.join(dirName,path)
        abs_path = os.path.abspath(path)
        node = nodetree.Node(abs_path)
        # 親子関係束縛
        parentNode.add_child(node)
            
        # ディレクトリであれば再帰的になめる
        if os.path.isdir(abs_path) :
            node.file_type = "dir"
            gen_fileTree(abs_path,node)

        elif os.path.isfile(abs_path):
            node.file_type = "file"

        else :
            node.file_type = ""

    return parentNode
    

class App(object):
    def main(self):
        print gen_fileTree(".").format_containerStructure(convertFunc=lambda node : node.file_type +"\n",indent="    ---> ")

if __name__ == '__main__':
    App().main()

