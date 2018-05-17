#/usr/bin/python
# -*- coding: utf-8 -*-

"""
自動化されたindex生成機
"""
import setup

import re
import os
import datetime
import time

import file_utils
import md_constructor
import nodetree_utils
import nodetree


# GLOBALS
INDEXINFO_FILE = "__init__.conf"
INDEX_FILE = "index.md"
EXCLUSIVE_MD = [
    "index.md",
    "README.md"
] # 除外MDファイル一覧



class AutoIndexer(object):
    """ 自動インデクシングマシーン """
    def __init__(self):
        # 最近変更されたファイル一覧
        self.recently_files = list()
        # 直下のファイル
        self.files = list()
        # ディレクトリパスと、その情報格納ファイルパス
        self.dir_indexInfoFile = dict()
        self.dir_indexInfo = dict()
        # ディレクトリ階層をノード化
        self.rootNode = None

    def construct_data(self,_from="."):
        """ 情報の構築 """
        self.base_file = _from
        # ファイル情報取得
        self.extract_files(_from)
        # グループ情報構築
        self.load_indexInfo() 
        # 自身のインデックス情報
        self.index_name = self.doLoad_indexInfo(gen_infoPath(_from)).strip()

    def extract_files(self,_from="."):
        """ ファイル情報の検索 """
        # 絶対パス化
        _from = os.path.abspath(_from)
        # 現在時刻
        timestamp = time.time()

        # 直下ファイル検索
        for path in os.listdir(_from) :
            abs_path = os.path.join(_from,path)
            if os.path.isfile(abs_path) and is_targetMD(path) :
                self.files.append(abs_path)

        # ディレクトリウォーキング
        for root, dirs, files in os.walk(_from):
            for f_name in files:
                abs_path = os.path.join(root, f_name)
                # root名 : 情報ファイルパス のセットを取得
                if f_name == INDEXINFO_FILE :
                    self.dir_indexInfoFile[root] = abs_path
                # および近日更新のファイル取得
                elif is_targetMD(f_name) and timestamp -os.path.getmtime(abs_path) < 86400*5:
                    self.recently_files.append(abs_path)

        # ディレクトリ階層をノード化
        self.rootNode = nodetree_utils.gen_fileTree(_from)

        # ソート
        self.files = [ name for mtime,name in sorted( [(os.path.getmtime(name),name) for name in self.files], reverse=True ) ]
        self.recently_files = [ name for mtime,name in sorted( [(os.path.getmtime(name),name) for name in self.recently_files], reverse=True ) ]

    def doLoad_indexInfo(self,filePath):
        """ 実際の情報ファイル読み込み関数 """
        # 本当に読むだけ
        with open(filePath) as f :
            return f.read()

    def load_indexInfo(self):
        """ ディレクトリに定義されたindex情報の取得"""
        # index情報の構築
        self.dir_indexInfo = { dirPath : self.doLoad_indexInfo(infoFile) for dirPath,infoFile in self.dir_indexInfoFile.items() }

    def print_fileStructure(self):
        """ ファイル構造印字 """
        scraper = DocumentScraper()
        def node2Info(node):
            path = node.get_nodeName()
            if node.file_type == "dir" :
                name = self.dir_indexInfo.get(path)
                return name and name.strip()
            elif node.file_type == "file":
                name = scraper.extract_header(path)
                return name and name.strip()

        self.rootNode.print_containerStructure("below",node2Info)

    def construct_md(self):
        """ マークダウンのコンストラクション """
        # コンストラクタ
        md = md_constructor.MarkdownConstructor()
        # ドキュメントスクレイパ
        scraper = DocumentScraper()

        # 題名と署名追加
        md.add_tag("h1","%s一覧" % (self.index_name,))
        md.add_p("> author : auto_indexing.py \n> generated : %s" % datetime.date.today() )

        # 直下ファイル
        if self.files :
            md.add_tag("h2","ドキュメント一覧")
            ls = []
            sub_ls = []
            for f_name in self.files :
                # 見出しの抽出
                header = scraper.extract_header(f_name)
                # 小見出しの抽出
                h2 = " / ".join(list(scraper.gen_h2(f_name)))
                #h2 = list(scraper.gen_h2(f_name))

                if header :
                    # リスト生成
                    link = md.gen_link(header,f_name)
                    ls.append(link)
                    if h2 :
                        sub_ls.append([h2])
                    else :
                        sub_ls.append([])

            md.add_list(ls,sub_ls)

        # index情報名に参照リンクをつけたリストを生成
        if self.rootNode.extract_node(lambda node: node.file_type == "dir") :
            md.add_tag("h2","分類")
            # ディレクトリノードをリンク付きリストに変換
            def dirNode2link(node):
                info = self.dir_indexInfo.get(node.get_nodeName())
                indexpath = gen_indexPath(node.get_nodeName())
                if not info :
                    return 
                return md.gen_link(info,indexpath) + "\n"

            # リスト文字に変換
            node2list = lambda indentLevel : "\t" *(indentLevel-1) +"* "

            ls_str = self.rootNode.format_containerStructure(lambda node : node is not self.rootNode and node.file_type == "dir" and dirNode2link(node), "\t" ,node2list)
            md.add_p(ls_str)
        
        # 最新更新ファイルリストの生成
        md.add_tag("h2","最近更新したドキュメント")
        ls = []
        for f_name in self.recently_files :
            # 見出しの抽出
            header = scraper.extract_header(f_name)
            if header :
                ls.append(md.gen_link(header,f_name))
        md.add_list(ls)
            
        # 出力
        md.write(gen_indexPath(self.base_file))


def is_targetMD(path):
    """ 取得対象MDか単純判定"""
    return path.endswith(".md") and path not in EXCLUSIVE_MD

def gen_infoPath(path):
    """ グループインフォパスを生成 """
    return os.path.join(path,INDEXINFO_FILE)

def gen_indexPath(path):
    """ indexファイルパスを生成 """
    return os.path.join(path,INDEX_FILE)



class DocumentScraper(object):
    """
    ドキュメントスクレイパ
    面倒なので簡単なのはHTML化とかせずMDのまま文字列処理
    """
    def __init__(self):
        pass

    def extract_header(self,fileName):
        """ 題名を読む"""
        with open(fileName) as f :
            for line in f :
                if line.strip().startswith("#"):
                    return line.strip()[1:]

    def gen_h2(self,fileName):
        """ H2をじぇねレート"""
        with open(fileName) as f :
            for line in f :
                if re.match('^##[^#]',line.strip()):
                    line = line.replace(" ","")
                    yield line.strip()[2:]


class App(object):
    def main(self):
        # 自ディレクトリについて処理
        indexer = AutoIndexer()
        indexer.construct_data()
        #indexer.print_fileStructure()
        indexer.construct_md()
        #import sys;sys.exit()

        # 全ディレクトリについて処理
        # ディレクトリウォーキング
        for root, dirs, files in os.walk(os.path.abspath(".")):
            for dir_name in dirs :
                if (not dir_name.startswith(".")) and (".git" not in root):
                    abs_path = os.path.join(root,dir_name)
                    if os.path.isfile(gen_infoPath(abs_path)):
                        indexer.__init__()
                        indexer.construct_data(os.path.join(root,dir_name))
                        indexer.construct_md()


if __name__ == '__main__':
    App().main()



