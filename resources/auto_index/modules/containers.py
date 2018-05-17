#! /usr/bin/python
#-*- coding: utf-8 -*-


import copy
import func_utils


"""
包含関係を有するオブジェクト間のデータ構造を記述するための基底モジュール。
このモジュールには「被コンテナクラス」、「コンテナクラス」およびその派生クラスが実装されている。

1:被コンテナクラス
被コンテナクラスは自身を含む「コンテナ」オブジェクトへのアクセス手段及びその設定、取り消しのためのインターフェイスが規定されている。

2:コンテナクラス
コンテナクラスは、「被コンテナ」オブジェクトを自身に「格納」したり「取り出し」たりするためのインターフェイスが規定されている。
また、「コンテナ」には防御的な「制限」のために以下の２つの概念が実装されている

2-1:有効被コンテナ型
    「コンテナ」型には、その被格納アイテムの「型」を制限するための枠組みがあらかじめ実装されている。
    この概念のうちで「格納」の許可されている「型」の集合を「有効被コンテナ型」と呼ぶ。
    この「格納許可型」についての設定は「いつでも」行える。
2-2:有効実装型
    コンテナはその派生クラスとして、格納可能な型やあるいは個数を制限するような別のクラスを拡張できる。
    ところで、ある「コンテナ」オブジェクトはその様な派生クラスのうち、２つ以上のそれを同時に継承していてもよい。
    この時には、その継承されたクラスによって規定される「制限」のうちのかならず「いずれか」が適用されなければならない。
    このような「アクティブ」な「制限」状態にある「コンテナ」の継承型を「有効実装型」と呼ぶ。
    この「アクティブ制限型」についての設定は「初期化状態」のみにおいて行える。

なお、このオブジェクト間の「包含関係」という形式のデータ構造は、しばしば、「ノードツリー」のデータ構造を形成するのに用いられる。
このモジュールにおいてはその「ツリー構造」としてのデータ構造までの面倒は見ない。
これはこのモジュールを拡張する「nodetree」モジュールに拠って提供されるだろう。
"""


# Define Class As ContainerImplementedClass :
def containerImplementedClass(cls):
    """
    コンテナ実装型であることを宣言するクラスデコレータ
    """
    if type(cls) is not type or not issubclass(cls,Base_Container) :
        raise TypeError("このデコレーターの許可する引数はBase_Containerを継承する任意のクラスオブジェクトです")

    last_baseCls = cls.mro()[1]
    if last_baseCls is not Base_Container and not is_containerImplementedClass(last_baseCls) :
        raise TypeError("%s : デコレートされるクラスの直轄の継承もとは、Base_Containerであるかあるいはコンテナ実装型でなければなりません" % (cls))

    # 少なくとも直轄の親クラスはコンテナ実装型の継承クラスであるはずであるから、そのクラス要素を継承するはずである。
    # このクラスのコンテナ実装型継承リストは、直轄の親コンテナ実装型クラスのそれに、自信を追加した、「新しい」リストである。
    cls.CONTAINER_IMPLEMENTED_CLASS_LIST = last_baseCls.CONTAINER_IMPLEMENTED_CLASS_LIST +[cls]
    return cls

def is_containerImplementedClass(cls):
    """ コンテナ実装型かどうかを返す """
    return hasattr(cls,"CONTAINER_IMPLEMENTED_CLASS_LIST") and cls in cls.CONTAINER_IMPLEMENTED_CLASS_LIST




# Contained Class
class Contained(object):
    """
    コンテナオブジェクトの子オブジェクト(=被コンテイン型)となる型のインターフェイス
    """
    # Special
    def __init__(self):
        self._container = None

    # parent setting method
    def _set_container(self,container):
        """
        隠蔽された親コンテナ設定メソッド。
        このメソッドを直接このプログラミングAPI利用者が呼び出すことはない。

        このメソッドは、任意のContainerオブジェクトの有するadd関数によって間接的に自動で呼び出される
        """
        # Check Arg
        if self.get_parent() is not None :
            raise Exception("既に親コンテナを持っています。")
        elif not isinstance(container,Base_Container) :
            raise TypeError("引数がコンテナオブジェクトでありません")
        #Set
        self._container = container

    def _remove_parent(self):
        """
        親Containerオブジェクトのremoveメソッド呼び出しーとその成功ーにバウンドして呼び出される隠蔽されたメソッド。
        このオブジェクトの親をNoneに再設定する。
        """
        self._container = None


    # Access to parent
    def get_parent(self):
        """
        自身の親コンテナオブジェクトを返す
        >>> contained, parent = Contained(), Base_Container()
        >>> parent.add_child(contained)
        >>> contained.get_parent() is parent
        True
        """
        return self._container

    def get_depth(self):
        """
        深さ探索する
        """
        parents = self.get_all_parent()
        return len(list(parents))

    def get_father(self):
        """
        親コンテナを持たない最上位のコンテナオブジェクトを得る
        最上位にたどり着く為に条件分岐の再帰呼び出しを用いる。

        なお、このオブジェクト自身が最上位オブジェクトであり、且つコンテナ実装型がRoot_Containerでないとき、このメソッドは例外を送出する。
        """
        parent = self.get_parent()
        # もしこのオブジェクトがRoot_Containerでない最上位コンテナなら例外の送出
        if parent is None :
            raise Exception("このオブジェクトにいかなる親オブジェクトもありません")

        # 親コンテナが最上位ならそれを返し、さもなくば再帰的に親コンテナを検索する
        return parent if is_topContainer(parent) else parent.get_father()

    def get_all_parent(self,filterFunc=None):
        """
        このオブジェクトのすべての親オブジェクトの順序づけられたリストを返す。
        このオブジェクト自身が最上位オブジェクトであるとき、このメソッドは例外を送出する。
        """
        # Check Optionargments
        if filterFunc is not None :
            func_utils.check_argCount(filterFunc,1)

        # もしこのオブジェクトがRoot_Containerでない最上位コンテナなら例外の送出
        if self.get_parent() is None :
            raise Exception("このオブジェクトにいかなる親オブジェクトもありません")

        # 再帰的に親オブジェクトをyieldするジェネレータ
        def generate_parent(context_container):
            # context_nodeが最上位ノード以外ならyield
            while context_container.get_parent() is not context_container :
                # 親ノードの算出
                context_container = parent = context_container.get_parent()
                # フィルタリングを通ったら
                if filterFunc is None or filterFunc(parent) :
                    yield parent 

        # 驚き最小の、ルートノードをindex=0,最下位ノードをindex=-1の形式のリストに変換
        return reversed(list(generate_parent(self)))



# Base-Container
class Base_Container(Contained):
    """
    コンテナオブジェクトの最小抽象基底クラス。
    すべてのコンテナオブジェクトは、被コンテナでもある。つまり、この最小基底クラスはContainedを継承する。
    """
    # ClassGlobal
    CONTAINER_IMPLEMENTED_CLASS_LIST = list()


    # Initialize
    def __init__(self):
        """
        すべてのコンテナ実装型がこの初期化ルーチンを呼ばなくてはならない。
        この初期化ルーチンでは、コンテナの多様性に関する初期化処理を行う。
        """
        #コンテナinコンテナのサポートのためContainedの初期化処理の呼び出し
        Contained.__init__(self)

        # その他属性値の初期化
        self.init_attr()
        #initial subroutine
        self.set_valid_container_type()    #有効実装型の初期設定。２つ以上の実装型が継承されているときには未定義にしておく
        
    def init_attr(self):
        #格納を許可するオブジェクトの型のリスト。要素がないならテストを無視。多様性のために有効実装型ごとに格納
        self.valid_child_types = list()
        self.valid_container_type = None    #コンテナの多様性をもたせる為の枠組み。現在有効な(ただ１つの)コンテナ型の情報。

        # 子オブジェクトの格納リスト
        self.childList = list()


    # Protocols
    def __iter__(self):
        """
        イテラブルにします。
        コンテナ多様性のために隠蔽されたクラスのメソッドを呼び出します。
        """
        if self.get_valid_container_type() is Single_Container :
            raise TypeError("Single_Containerはイテレーション不能です.")
        self.test_valid_container_type()    #有効コンテナ型が定義済か確認
        return iter(self.get_children())

    def __contains__(self,item):
        """ inに対応 """
        return item in self.get_children()


    # Utils
    def has_child(self):
        return len(self.childList)

    
    # Get Children
    def get_children(self,filterFunc=None):
        """
        オーバーライド禁止。連鎖的に然るべきオブジェクトの隠蔽された_get_children()を呼ぶ。
        """
        # Check Optionargments
        if filterFunc is not None :
            func_utils.check_argCount(filterFunc,1)

        # フィルタ関数が定義されていればフィルターをかけた新しいリストを返しさもなくば単に子要素オブジェクトのリストのコピーを返す
        return copy.copy(self.childList) if filterFunc is None else filter(filterFunc,self.childList)


    # Add/Remove Childen
    def add(self,child):
        """
        オーバーライド禁止。連鎖的に然るべきオブジェクトの隠蔽された_add()を呼ぶ。
        後の処理はすべて呼び出し先のメソッドに完全に移譲する。

        このメソッドは、コンテナ実装型の区別された名前を持つadd関数のショートカットである。
        コードの意味的透明性をいささか損なうが統一的な名前ですべてのコンテナ実装型のadd関数にアクセスできる。
        """
        self.test_valid_container_type()
        return self.get_valid_container_type()._add(self,child)

    def _add(self):
        """
        addショートカットメソッドのための、基底メソッド。オーバーライド必須。
        多様性のための冗長な隠蔽メソッド。
        """
        raise Exception("オーバーライド必須です")

    def remove(self,child):
        """
        オーバーライド禁止。
        定義された格納済みContainedオブジェクトーchildをこの格納オブジェクトから取り除く。
        この多様性を隠蔽した、統一的メソッドは、現在有効なコンテナ型に対応する隠蔽されたメソッド_remove()を内部で呼び出す。
        なお、引数Childに対するエラーチェックはその末端のメソッドで行う。
        """
        self.test_valid_container_type()
        if child not in self.childList :
            raise Exception("Single_Container: 引数Childはこのオブジェクトの子Containedオブジェクトでありません.")
        self.childList.remove(child)
        child._remove_parent()


    # Check TypeOf Children
    def test_child(self,child):
        """
        与えられた引数childがこのContainerに適合する型であるかを判別し、そうでないならエラーを送出します。
        """
        if not isinstance(child,Contained) :
            raise TypeError("引数がContainedオブジェクトでありません")
        # 子オブジェクト有効型が定義されているとき、型チェック
        elif self.valid_child_types and not any( isinstance(child,validType) for validType in self.valid_child_types ) :
            raise TypeError("引数が許可された型のオブジェクトではありません")

        # エラーフィルタリングをぬけたら真を返す
        return True


    # Check self-implementType
    def test_valid_container_type(self):
        """
        ちゃんと有効コンテナ型が定義されているか確認するユーティリティ
        """
        if self.valid_container_type is None :
            raise Exception("有効コンテナ型が未定義です。")

    def is_valid_container_type(self,container_type,strict=False):
        """
        有効コンテナ型(あるいはその基底クラス)かどうか。
        この基底オブジェクトの外部から呼ばれるユーティリティ関数。
        オプションstrictが定義されたらサブクラスを許可しない厳密なチェックを行う
        """
        # 前提チェック
        self.test_valid_container_type()    #そもそも、ちゃんと定義済かどうかのチェック
        if not is_containerImplementedClass(container_type) :
            raise TypeError("このクラスはコンテナ実装型として定義されていません。")

        # チェック
        if not strict and issubclass(self.valid_container_type,container_type) :
            return True
        elif strict and container_type is self.valid_container_type :
            return True
        else :
            raise TypeError("%sは有効コンテナ型ではありません。" % container_type)


    # Setting of Valid Child Types
    VALIDTYPE_OPARETEMETHODS =\
        VALIDTYPE_OPARETE_ADD ,VALIDTYPE_OPARETE_REMOVE ,VALIDTYPE_OPARETE_RESET = (object() ,object() ,object())
    def operate_valid_type(self,operate_method,valid_type):
        """
        被格納有効型の設定に関する共通ロジック
        操作Operationを引数にとり、実際の操作を定義する
        """
        #引数チェック
        assert ( operate_method in self.VALIDTYPE_OPARETEMETHODS )
        # valid_typeのチェック
        #引数がタプルなら要素ごとの再起呼び出しを行い、あるいは型オブジェクトでなければ例外を送出
        recall = ( lambda val : self.operate_valid_type(operate_method=operate_method,valid_type=val) )
        if isinstance(valid_type,tuple) :
            return map(recall,valid_type)
        elif type(valid_type) is not type :
            raise TypeError("被格納有効型定義のためのコンテキスト %s は('新型'の)型オブジェクトでありません" % (valid_type))

        # Do Operation
        # ADD Valid-Type
        if operate_method is self.VALIDTYPE_OPARETE_ADD :
            if valid_type in self.valid_child_types :
                raise Exception("定義された型 %s はすでに被コンテナ型有効型として定義されています" % valid_type )
            else :
                self.valid_child_types.append(valid_type)

        # REMOVE Valid-Type
        elif operate_method is self.VALIDTYPE_OPARETE_REMOVE :
            if valid_type not in self.valid_child_types :
                raise TypeError("定義された型 %s はこのコンテナオブジェクトの被格納有効型でありません" % valid_type)
            elif any( isinstance(child,valid_type) for child in self.childList ):
                raise Exception("取り消し定義された型 %s を有するオブジェクトが、このコンテナの子オブジェクトとして格納されています" % valid_type)
            else :
                self.valid_child_types.remove(valid_type)

    def add_valid_type(self,valid_type):
        """
        子オブジェクトの型指定を行う。
        引数には型オブジェクトかあるいは、そのタプルをとる。
        """
        self.operate_valid_type(self.VALIDTYPE_OPARETE_ADD,valid_type)

    def set_type_invalid(self,valid_type):
        """ 現在定義されている有効型のセットから、定義された型を取り除く """
        self.operate_valid_type(self.VALIDTYPE_OPARETE_REMOVE,valid_type)



    # Setting of Valid-Container-implement-Type
    def set_valid_container_type(self,valid_type=None):
        """
        現在有効なコンテナ型を設定する。
        デフォルトの初期化処理では明示的な型指定はなしで呼ばれ、
        もし、ただ唯一のコンテナ実装型のみがこのメソッドの呼び出し元に継承されていれば、それをデフォルトで設定する。
        """
        # 有効コンテナ型が明示されていないときデフォルトの設定
        if valid_type is None :
            return self.set_valid_container_type_default()

        # 型チェック
        if not issubclass(valid_type,Base_Container) :
            raise TypeError("型 %s はコンテナオブジェクトでありません" % valid_type)
        elif not isinstance(self,valid_type) :
            raise TypeError("継承していない型 %s を有効型にはできません" % valid_type)

        # 子要素がすでにあればエラー
        if self.get_children() :
            raise Exception("このコンテナオブジェクトには子要素が定義されています。子要素があるときの有効型変更は許されません")

        self.valid_container_type = valid_type

    def set_valid_container_type_default(self):
        """
        有効型コンテナ実装型のデフォルト設定を行う。
        このメソッドは単純に単体で呼び出すこともできるし、
        より一般的な有効被コンテナ型定義メソッドself.set_valid_container_type()にNoneを渡しても自動でこの自動設定メソッドが呼び出される。

        このメソッドは、このオブジェクトの基底クラスをみて、その定義された有効実装型の個数によって動作を分岐する
        """
        #継承している実装型を真偽値で表すリスト
        inherited_contaierTypes = filter(is_containerImplementedClass,self.__class__.mro())

        #いかなる実装型も継承されていなければ例外を送出
        if not inherited_contaierTypes :
            raise Exception("いかなるコンテナ実装型も継承されていません")

        #継承されているコンテナ実装型が唯一ならば、それを有効コンテナ型に設定
        elif len(inherited_contaierTypes) == 1 :
            valid_type = inherited_contaierTypes[0]
            self.set_valid_container_type(valid_type)

        #複数継承時。有効型は未定義で返す
        else :
            return    


    # Get Options
    def get_valid_container_type(self):
        """
        有効コンテナ実装型を得る
        """
        return self.valid_container_type

    def get_valid_child_types(self):
        """ 被格納有効型のリストの取得 """
        return self.valid_child_types



@containerImplementedClass
class Single_Container(Base_Container):
    """
    １つの何らかのオブジェクトを「内包」するための枠組みを提供する抽象規定クラス
    「１つ以上」のオブジェクトを格納するには、このクラスの継承クラスplural_containerを用いる
    """
    # Operation of Childrens
    def set_child(self,content):
        """子containedオブジェクトを定義、格納する。"""
        # 有効コンテナ型および有効被コンテナ型のテスト
        self.is_valid_container_type(Single_Container)
        self.test_child(content)

        # 要素のアップデート
        if self.get_children() :
            self.remove(self.get_child())    #子を破棄
        self.childList = [content]
        content._set_container(self)
    _add = set_child    #隠蔽されたエイリアス。


    # Hidden InterFacese for Polymorphism
    def get_child(self):
        """
        このクラスは子オブジェクトを直接返す
        """
        self.is_valid_container_type(Single_Container)
        if self.childList :
            return self.childList[0]
        else :
            return None



@containerImplementedClass
class Plural_Container(Base_Container):
    """
    １つ以上の任意の個数のオブジェクトを格納するするためのコンテナオブジェクトに関する枠組みを規定する抽象規定クラス
    """
    # Operation of Childrens
    def add_child(self,*contents):
        """子containedオブジェクトを新たに格納する"""
        for content in contents :
            self.is_valid_container_type(Plural_Container)
            self.test_child(content)
            self.childList.append(content)
            content._set_container(self)
    _add = add_child    #隠蔽されたエイリアス。

    def insert_child(self,index,content):
        """ 子オブジェクトをインサートする """
        self.is_valid_container_type(Plural_Container)
        self.test_child(content)
        self.childList.insert(index,content)
        content._set_container(self)
        



@containerImplementedClass
class Container_Of_Container(
    Plural_Container,
    object,
    ):
    """
    Plural_Containerのサブセット。あらかじめ有効被格納型としてコンテナ型が設定されている
    つまり、このクラスの継承型はコンテナオブジェクト以外を格納しえない
    """
    # Special
    def __init__(self,from_base=False):
        Base_Container.__init__(self)
        self.set_valid_container_type(Container_Of_Container)
        self.add_valid_type(Base_Container)



# Globals
# Utils For Implementations :
def extract_containerImplementedClass(cls):
    """
    在るクラスに対する直轄のコンテナ実装型クラスオブジェクトを返す
    このクラスにコンテナ実装型が定義されていなければ例外を送出する
    """
    if type(cls) is not type :
        raise TypeError("引数はクラスオブジェクトです")

    # コンテナ実装型の抽出
    for baseCls in cls.mro() :
        if is_containerImplementedClass(baseCls) :
            return baseCls
    # いかなるコンテナ実装型も継承していなければ例外
    else :
        raise TypeError("クラスオブジェクト %s はいかなるコンテナ実装型も継承していません" % cls)

def is_topContainer(container):
    return not bool(container._container)



if __name__ == '__main__' :
    pass



