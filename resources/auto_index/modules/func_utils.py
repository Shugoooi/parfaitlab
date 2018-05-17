#! /usr/bin/python
#-*- coding: utf-8 -*-


import types


"""
Pythonにおける関数オブジェクトに関するあらゆるユーティリティを提供する
"""

# Globals 
CO_VARIABLE_ARG_FLAG = 4
CO_KEYWORD_ARG_FLAG = 8




# Check Function
def is_function(func):
    """ 引数が関数オブジェクトかどうか """
    if type(func) in ( types.FunctionType,types.MethodType,types.LambdaType ) :
        return func
    else :
        return False

def check_function(func):
    """ 引数が関数オブジェクトかどうかを評価し、さもなくば例外の送出 """
    result = is_function(func)
    if result :
        return result
    else :
        raise TypeError("引数 %s は、関数オブジェクトでありません" % func)

def is_specialFunction(func):
    check_function(func)
    return func.func_name.startswith("_")



# Check Defined Argments
def count_args(func):
    """
    関数オブジェクトfuncを引数に、その関数オブジェクトに通常引数がいくつ定義されているかを算出する
    """
    check_function(func)
    numof_args = func.func_code.co_argcount
    return numof_args

def check_argCount(func,valid_argCount,strict=True):
    """
    関数オブジェクトfuncを引数にとり、その関数オブジェクトに通常引数が、指定された個数だけ定義されているか算出する関数。
    オプション引数strictがTrueの時、可変長引数による条件回避を免れない。
    つまり、厳格性オプションstrictがFalseなら、可変長引数による条件回避を行う。

    ただし、その場合、いかなる通常引数も定義されていてはいけない。
    なぜなら、この関数は、一般に、モジュールAPIなどの形式において、
    そのコード多様性のための「インターフェイス」として関数オブジェクトを受け取るユーティリティにおいて使われることを前提としているためである。
    つまり、元来にして、「外部」から不確実な 「入力」として関数が与えられる状況でもなければ、往々にして、引数の個数チェックなどはおおよそ問題にならない。

    なお、この関数ではキーワード引数に関するいかなるチェックも行わない
    """
    # Arg Check
    check_function(func)
    if type(valid_argCount) is not int or not 0 <= valid_argCount <= 10 :
        raise ValueError("引数が不正です")

    # 引数に関する値の算出
    numof_args = count_args(func)
    has_vArgs = has_variableArgs(func)

    # 可変長引数が定義されているとき
    if has_vArgs:
        # 厳格性オプション内においては可変長引数の定義を認めない
        if strict:
            raise Exception("関数 %s は可変長引数を有しています。: 認められていない条件です" % func)
        # 非厳格チェックにおいては可変長引数による盲目のチェック通過を認めるが、ただし通常引数との併用はエラーとして検出
        else:
            if not numof_args :
                return func
            # 可変長引数と通常引数の両方の定義はエラー
            else :
                raise Exception("関数 %s には可変長引数及び通常引数が定義されています" % func)

    # 可変長引数が定義されていない時、単純に引数個数チェック
    if numof_args == valid_argCount :
        return func
    else :
        raise Exception("関数 %s には %d 個の引数が定義されています : 条件 -- %d 個の引数" % (func,numof_args,valid_argCount))


def has_variableArgs(func):
    """
    関数オブジェクトfuncを引数に取り、その関数オブジェクトに可変長引数が定義されているかどうかを判定する
    """
    check_function(func)
    coFlag = func.func_code.co_flags
    return coFlag & CO_VARIABLE_ARG_FLAG

def has_KeywordArgs(func):
    """
    関数オブジェクトfuncを引数に取り、その関数オブジェクトに可変長引数が定義されているかどうかを判定する
    """
    check_function(func)
    coFlag = func.func_code.co_flags
    return coFlag & CO_KEYWORD_ARG_FLAG

    


# Check Methods
def has_method(cls,methodName):
    """ """
    if type(cls) is not type or not isinstance(methodName,str):
        raise TypeError("第一引数clsにはクラスオブジェクトを、第二引数methodNameにはメソッド名文字列を、とりえます")
    return hasattr(cls,methodname) and is_function(getattr(cls,methodName))

def check_method(cls,methodName):
    if has_method(cls.methodName) :
        return True
    else :
        raise Exception("クラス %s はメソッド %s を持ちません" % (cls.methodName))

    


# Method Loader
class MethodLoader(object):
    """
    クラスオブジェクトないし任意のインスタンスオブジェクトからその条件づけられたメソッド(名)を検索、抽出するクラス
    """
    def __init__(self,cls_obj=None):
        """
        バグの抑止のために、冗長なクラス事前定義を行う。
        なお、クラスメソッド的汎用使用を許可するために、事前定義を行わないことも可能
        """
        if cls_obj is not None :
            #if type(cls_obj) is not type :
                #raise TypeError("初期化時定義引数がクラスオブジェクトでありません。")
            self.target_cls = cls_obj

    def extract_methods(self,condition):
        """ メソッドを取得する"""
        method_names = self.load_methodnames(condition=condition)
        return self.name2method(method_names)

        
    # MethodName Loader
    def extract_methodnames(self,names,ins=None,condition=None):
        """
        引数namesからメソッド名を抽出する
        """
        #引数チェック
        if not isinstance(names,(list,tuple)) :
            raise TypeError("名前リストの定義はリスト形式でなければなりません")

        # オプション関数conditionのチェック
        if condition is None :
            condition = ( lambda name : True )
        else :
            self.check_conditional_func(condition)
        # insのチェック
        ins = self.check_instance(ins)

        # メソッド名の抽出
        is_valid_name = ( lambda name : self.has_method(name,ins=ins) and condition(name) )
        method_names = filter(is_valid_name,names)

        return method_names

    def load_methodnames(self,ins=None,condition=None,include_specials=False,exclusionCls=None):
        """
        名前条件関数conditionがTrueを返す任意のーしかもその参照先が呼び出し可能オブジェクトであるーすべての名前を(文字列のリストとして)返す。
        """
        # insのチェック
        ins = self.check_instance(ins)
        # メソッド名の抽出
        method_names = self.extract_methodnames(dir(ins),ins,condition)

        # 特殊メソッド名の除外
        if not include_specials :
            isnot_special = ( lambda name : not name.startswith("_") )
            method_names = filter(isnot_special,method_names)

        return method_names

    def load_specialmethodnames(self, ins=None, condition=None):
        """
        特殊メソッド名"のみ"を抽出する。
        load_methodnamesのサブセット。
        """
        # 特殊メソッド名抽出のためのconditionの定義
        is_specialneme = ( lambda name : name.startswith("_") )
        # オプショナルコンディショナルが定義されたら特殊名抽出条件関数と一緒にラップ
        if condition is not None :
            self.check_conditional_func(condition)
            condition = self.link_conditional_func(is_specialneme,condition)
        else :
            condition = is_specialneme

        # 全メソッド名の抽出
        methodnames = self.load_methodnames(ins,condition=condition,include_specials=True)
        return methodnames


    # Method Extracter - Convert name to methodObj
    def name2method(self,*names,**kwargs):
        """
        引数に与えられた名前で参照される値のリストを返す
        load_methodnamesの名前抽出実装部分。
        外部から単品のメソッドとしても呼び出し可能
        """
        # 引数チェック
        if not names :
            raise Exception("メソッド名nameを定義してください。")
        elif not all( isinstance(name,str) for name in names ) :
            raise TypeError("取得メソッド名定義引数 %s は、すべて文字列でなければなりません" % (names,))
        # insのチェック
        if any( key != "ins" for key in kwargs ) :
            raise Exception("このメソッドのとりうるキーワード引数は、'ins'のみです")
        ins = self.check_instance(kwargs.get("ins"))

        # メソッドの抽出
        methods = [ getattr(ins,name) for name in names ]
        if not all( callable(method) and hasattr(method,"func_name") for method in methods) :
            raise Exception("引数namesにメソッド以外への参照を表す名前 %s が入っています"
                % ( filter((lambda obj:not callable(obj)),methods) )
                )
        return methods


    # Filtering Methods
    def filter_methodnames(self,methodnames,exclusionClasses):
        """
        load_methodnames()の返り値である関数名のリストをそのまま取り、定義された例外クラスに定義された任意のメソッド名との差分をとる
        """
        exclusion_methodnames = set()

        # 例外クラスについて、その全名メソッドの抽出を行う
        for exclusionCls in exclusionClasses :
                assert issubclass(self.target_cls,exclusionCls) or issubclass(exclusionCls,self.target_cls)
                exclusive_methodnames = MethodLoader(exclusionCls).load_methodnames()
            # 例外クラスのメソッドの集合
                exclusion_methodnames.update( exclusive_methodnames )

        # フィルタリング
        notin_exclusionCls = ( lambda methodname : methodname not in exclusion_methodnames )
        filtered_methodnames = filter(notin_exclusionCls,methodnames)

        return filtered_methodnames

    def filter_methods(self,methods,exclusionClasses):
        """
        name2method()の返り値である関数のリストをそのまま取り、定義された例外クラスに定義された任意のメソッドオブジェクトとの差分を抽出する
        """
        exclusion_methods =set()

        # 例外クラスについて、その全メソッドの抽出を行う
        for exclusionCls in exclusionClasses :
                assert issubclass(self.target_cls,exclusionCls) or issubclass(exclusionCls,self.target_cls)
                methodnames = MethodLoader(exclusionCls).load_methodnames()
            # 例外クラスのメソッドの集合
                exclusion_methods.update( self.name2method(*methodnames) )

        # フィルタリング
        notin_exclusionCls = ( lambda method : method not in exclusion_methods )
        filtered_methods = filter(notin_exclusionCls,methods)

        return filtered_methods


    # Utils
    def check_instance(self,ins):
        """
        引数チェック共通ロジック
        """
        # 既定の対象クラスが定義されていないとき
        if not hasattr(self,"target_cls") :
            if ins is None :
                raise Exception("抽出対象オブジェクトが未定義です。")
        # オプション引数が定義されていないとき
        elif ins is None :
            ins = self.target_cls
        # オプション引数の型チェック
        elif ins is self.target_cls :
            pass
        elif isinstance(ins,self.target_cls) :
            pass
        elif issubclass(self.target_cls,ins) :
            pass
        # オプション引数insがいかなる許可型にも合致しないとき例外
        else :
            raise TypeError("引数insは定義されたクラスオブジェクトかあるいはそのインスタンスでなければなりません")

        return ins

    def has_method(self,methodname,ins=None) :
        """ 定義されたクラスオブジェクトないしそのインスタンスがメソッド名methodnameを有しているか否か """
        # 引数チェック
        assert isinstance(methodname,str)
        ins = self.check_instance(ins)

        # 名前の参照
        method = hasattr(ins,methodname) and getattr(ins,methodname)
        return ( method and hasattr(method,"func_name") )



    # Utils for MethodLoader
    def check_conditional_func(self,condition):
        """ 引数の数のチェックを行う """
        if not callable(condition):
            raise TypeError("条件Conditionは呼び出し可能でなければなりません")
        if not hasattr(condition,"func_code"):
            raise TypeError("呼び出し可能オブジェクト %s はconditionalとして認められる単純関数オブジェクトでありません。" % (condition,))
        if condition.func_code.co_argcount != 1 :
            raise Exception("関数オブジェクト %s はconditionalとしての要件「名前を受け取る１つの引数」を満たしていません" % (condition,))
        

    def link_conditional_func(self,*functions):
        """ 名前条件判定関数を連結して返却する """
        if not all( callable(func) for func in functions ) :
            raise TypeError("引数はすべて呼び出し可能でなければなりません")

        linked_condition = ( lambda name : all( func(name) for func in functions ) )
        return linked_condition
    



