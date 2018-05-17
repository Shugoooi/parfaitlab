#! /usr/bin/python
#-*- coding: utf-8 -*-

import containers
import func_utils

"""
コンテナモジュールのツリー構造拡張。
コンテナモジュールによって提供される「格納」「被格納」クラス群の拡張を行う。
"""

class Node(containers.Container_Of_Container):
    """
    ソースコードの構造を表すノードオブジェクトの基底クラス

    すべてのノードオブジェクトは、そのコードブロックを表現する「名前」、「開始行」、「終端行」に関する情報、
    及びそのソースコードにおけるデータ構造関係を表現する為の(GlobalNodeという特別な例外を除いて)ただ１つ「親のノード」また、0個以上の「子ノード」への参照を有する
    """
    def __init__(self,name="undefined",parentNode=None):
        """ 初期化を行う。このオブジェクトはノード名および親ノードを必ず有する。"""
        # 基底クラスの初期化
        containers.Container_Of_Container.__init__(self)
        # ノード名(関数名/クラス名)とソースコードにおける開始行、終了行
        self.nodeName = name
        # 親ノードの設定 :containersモジュールにより親ノードからの子ノード設定も自動化されている
        # 親ノードは省略可能だが、その場合get_parent()/get_father()は利用不可である。
        if parentNode is not None :
            parentNode.add(self)


    # Analysing Interface
    def extract_node(self,state,nodetype=()):
        """
        ノード名をコンテキストにとりその条件に合致したノードオブジェクトのリストを返すインターフェイスメソッド
        """
        # 条件が文字列として与えられたら同じノード名のノードオブジェクトを抽出
        if isinstance(state,str):
            stateFunc = ( lambda node : node.nodeName == state )
        # 条件として関数オブジェクトもまた取りうる
        elif func_utils.is_function(state) :
            func_utils.check_argCount(state,1,strict=True)
            stateFunc = state
        # 明示的なNone値を認める。この時すべてのノードを抽出する
        elif state is None :
            stateFunc = ( lambda node : True ) # 全ノードの抽出
        else :
            raise TypeError("ノード抽出条件引数が不正です")

        # 自分自身を頂点ノードとして、名前/行数のマッチを判定するノード判定関数をコンテキストに、ノードの再帰的検索関数を呼ぶ
        matched_nodes = find_child_recursively(self,stateFunc) # stateFunc関数がTrueを返すようなノードの再帰的な検索

        # オプションノードタイプが定義されたらそのタイプを抽出
        if nodetype :
            if not (isinstance(nodetype,(list,tuple)) and all( issubclass(nodeCls,Node) for nodeCls in nodetype )) :
                raise TypeError("オプション引数nodetypeは0個以上のノードオブジェクトのタプルでなければなりません")
            is_validNodeType = ( lambda node : type(node) in nodetype )
            return filter(is_validNodeType,matched_nodes)

        return matched_nodes

    def set_nodeName(self,name):
        self.nodeName = name

    def get_nodeName(self):
        return self.nodeName

    def get_all_children(self,filterFunc=None):
        """
        このオブジェクトのすべての子オブジェクトの順序づけられたリストを返す。
        このメソッドは、自身にいかなる子オブジェクトがなくとも、例外を送出しない。つまり、単純に空のリストを返す
        """
        if filterFunc :
            func_utils.check_argCount(filterFunc,1)
            return find_child_recursively(self,filterFunc)
        else :
            return find_child_recursively(self)


    def find_parent(self,_filter=None):
        """
        このノードに近いほうから親ノードを返す。またフィルターを定義できる。
        """
        if _filter is None :
            filterFunc = lambda node: True
        elif type(_filter) == type :
            filterFunc = lambda node: isinstance(node,_filter)
        return filter(filterFunc,reversed(list(self.get_all_parent())))
        
    def format_containerStructure(self,convertFunc=str,indent="",preposition=""):
        """ ノードツリーを文字列へフォーマットする関数 """
        # preposition前処理
        if isinstance(preposition,str):
            preprocess = lambda indentLevel : indent *indentLevel +preposition
        else :
            preprocess = preposition

        self._indentLevel = 0 # 便宜的にインデントレベルの定義
        format_str = ""
        # レベルルートノード
        if convertFunc(self):
            format_str += preposition+ convertFunc(self)

        # 子でくるくる
        for child in self.get_all_children():
            # インデントレベルの更新
            child._indentLevel = child.get_parent()._indentLevel+1
            # 文字列の生成
            node_str = convertFunc(child)
            if not node_str :
                continue    
            indent_str = preprocess(child._indentLevel)
            # 追加
            format_str += indent_str +node_str

        return format_str


    # InterFace For Debugging :
    def print_containerStructure(self,trend="below",convertFunc=str,limit=0):
        """
        このコンテナオブジェクトとの格納関係の在る任意のおぶじぇくとについて、その関係性を表す、ヒューマンリーダブルにフォーマットされた文字列を返す

        デバッグ用の関数でかつ基底モジュールとして極めて高い多様性を要するのためいささかオプション系がわかりづらい感がある。
        trendは
        """
        # Arg Check 
        if trend not in ("upper","below") :
            raise ValueError("方向定義オプションが未定義です")
        if limit < 0 :
            limit = 0
        # 名前取得関数コンテキストに文字列を認める。この場合その名前の属性値を参照する。
        if isinstance(convertFunc,str) :
            attrName = convertFunc
            convertFunc = (lambda node: getattr(node,attrName) )
        
        if trend == "upper" :
            uppers = list(self.get_all_parent())[-limit:]
            print " -> ".join(map(convertFunc,uppers+[self]))

        elif trend == "below" :
            print convertFunc(self)
            self._indentLevel = 0 # 便宜的にインデントレベルの定義
            below = self.get_all_children()

            for child in below :
                child._indentLevel = child.get_parent()._indentLevel+1
                # オプション引数Limitの適用
                if limit and child._indentLevel > limit :
                    continue

                format_str = convertFunc(child)
                if not format_str :
                    continue
                tree_line = "\t|" *child._indentLevel

                print tree_line
                print "%s-> %s" % (tree_line,format_str)



class RootNode(Node):
    """
    """
    def __init__(self,nodeName="Root"):
        containers.Container_Of_Container.__init__(self)
        self.nodeName = nodeName

    def get_parent(self):
        """ 自身を返す """
        return self

    def get_father(self):
        """ 自身を返す """
        return self

    def _set_container(self):
        """ Containedクラスに実装されている親コンテナ設定インターフェース。呼び出しを禁止にする。"""
        message = """ このメソッドは呼び出しが禁止されています。
             -> Root定義されたコンテナオブジェクトは、いかなる親コンテナも持ちえません。
             """
        raise Exception(message)
    

# Utils
def find_child_recursively(container,filterFunc=None,childList=None):
    """
    再帰的に子オブジェクトを検索してリストに集積する関数
    Base_Container.get_all_children()のロジック実装
    """
    # check Arg
    if filterFunc is not None :
        func_utils.check_argCount(filterFunc,1)
    else :
        filterFunc = lambda container : True
    if childList is None :
        childList = list()

    # 子オブジェクトの検索
    for child in container.get_children() :
        # フィルタリングをパスしたら対象子オブジェクト
        if filterFunc(child) :
            childList.append(child)
        # 子オブジェクトを有するなら再帰的に検索
        if child.get_children() :
            find_child_recursively(child,filterFunc,childList)
    return childList



def list2tree(ls,nameRule=(lambda item:"NodeName"),parentNode=None):
    """
    リスト系コンテナオブジェクトをノードツリー化する。
    """
    # Check Arguments
    if not hasattr(ls,"__iter__") :
        raise TypeError("引数は組み込みコンテナでなければなりません。")
    # 関数チェック
    func_utils.check_function(nameRule)
    func_utils.check_argCount(nameRule,1)
    # 親ノードが指定されてないならルートノードの生成
    if parentNode is None :
        parentNode = RootNode()

    for item in ls :
        node = Node(nameRule(item),parentNode)
        # コンテナなら再帰呼び出し
        if hasattr(item,"__iter__"):
            list2tree(item,nameRule,node)

    return parentNode # Rootを返す
        
        

if __name__ == "__main__" :
    ls = range(10)
    tree = list2tree(ls,lambda item:str(item))
    print tree.format_containerStructure(convertFunc=lambda node : str(node) +"\n",indent="    |---> ")



