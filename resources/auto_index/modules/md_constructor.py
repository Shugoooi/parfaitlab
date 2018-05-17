#/usr/bin/python
# -*- coding: utf-8 -*-

import markdown2

import file_utils
import re_utils

"""
マークダウン文章を構築する
HTMLジャ無いのはMDのほうが楽だから
"""

class MarkdownConstructor(object):
    """
    マークダウン文章構築オブジェクト
    """
    def __init__(self):
        self.mdList = []
        self.buf = [] # バッファ

    def add(self,src):
        """ マークダウンソースの追加 """
        self.mdList.append(src)
        self.buf.append(src) # バッファに保存

    def add_p(self,src):
        """ \nをMD改行に変更して追加 : 段落追加 """
        self.add(src.replace("\n","  \n") +"\n")

    def add_tag(self,tag,src):
        """ タグを追加 """
        # エスケープ
        src = self.escape(src)

        # Hタグ
        if ( tag == "h1" ):
            self.add("# "+src)
        elif ( tag == "h2" ):
            self.add("## "+src)
        elif ( tag == "h3" ):
            self.add("### "+src)
        elif ( tag == "h4" ):
            self.add("#### "+src)

        # コード
        elif ( tag == "code" ) :
            self.add("""
            ```
            %s
            ```
            """ % (src,)
            )
        elif ( tag == "code_inline" ):
            self.add("`%s`" % (src,))

        # イタリック/ボールド/打ち消し
        elif ( tag == "italic" ):
            self.add("*%s*" % (src,))
        elif ( tag == "bold" ):
            self.add("**%s**" % (src,))
        elif ( tag == "s" ):
            self.add("~~%s~~" % (src,))

        # 引用
        elif ( tag == "q" ):
            self.add("> %s" % (src,))

        else :
            raise TypeError("タグ名 %s は未定義です" % tag,)

    def escape(self,src):
        """ マークダウン用にエスケープする"""
        # ユニコードサポート
        if isinstance(src,unicode):
            src = src.encode("utf-8")
        # 文字コードの混在が致命になるので無理くりutf-8化
        else :
            src = re_utils.convert_anyway(src)

        # ストリップ
        src = src.strip()

        # エスケープのエスケープ
        if src.startswith("[") and src.endswith(")") : # リンク
            return src

        # MD文字エスケープ
        if "|" in src : # テーブルエスケープ
            src = src.replace('|','&#124;') 
        if "_" in src :
            src = src.replace('_',r'\_') 
        if "*" in src :
            src = src.replace('*',r'\*') 

        # HTMLエスケープ
        if "<" in src :
            src = src.replace('<','&#60;') 
        if ">" in src :
            src = src.replace('<','&#62;') 
        if "&" in src :
            src = src.replace('<','&#38;') 

        return src
            
    def add_table(self,thList,tdList):
        """
        テーブルを構築して追加
        tdを空のリストにするとテーブルヘッダのみを出力できるハックが利用可能
        thを空リストにするとテーブルボディのみ出力できる
        """
        if not all( isinstance(ls,(list,tuple)) for ls in tdList ) :
            raise TypeError("tdリストはリストのリストで無ければなりません")
        format_str = ""

        # TH行の生成
        thStr = " | ".join( self.escape(src) for src in thList )
        sepStr = " | ".join( "---" for _ in range(len(thList)) )
        # TD行の生成
        tdStr = ""
        for contentList in tdList :
            # エスケープ
            contentList = map(self.escape, contentList)
            tdStr += " | ".join(contentList) +"\n"

        # コンストラクション /TDオンリーハッキング用にif節
        if thStr: 
            format_str += thStr +"\n"
        if sepStr:
            format_str += sepStr +"\n"
        format_str += tdStr

        # 追加
        self.add(format_str.strip())

    def add_list(self,ls,subLists=None):
        """
        リストを構築して追加
        多次元リストもサポート
        """
        if subLists is not None :
            if len(ls) != len(subLists) :
                raise TypeError("the two list length is not equal")
            elif not all( isinstance(sub,list) for sub in subLists ) :
                raise TypeError("sublists include object that is not list")

        format_str = ""
        for index,item in enumerate(ls) :
            format_str += "* %s\n" % (self.escape(item),)
            if subLists :
                for sub in subLists[index] :
                    format_str += "\t* %s\n" % (self.escape(sub),)

        self.add(format_str)

    def gen_link(self,text,href):
        """ リンクタグを生成するユーティリティ"""
        return "[%s](%s)" % (self.escape(text),href)

    def construct_md(self,mdList=None):
        """ マークダウンを構築する"""
        # オプショナル定義があればそれをコンストラクション
        if mdList :
            return "\n".join(mdList)
        else :
            # 1つだけのときは空行入れとく
            if len(self.mdList) == 1:
                return "\n" +self.mdList[0]
            # 改行でつなぐだけ
            return "\n".join(self.mdList)

    def write(self,_file=None,mode="w"):
        """ マークダウンを吐き出す"""
        # マークダウンのコンストラクション
        md_str = self.construct_md()
        # 書き込み
        file_utils.write2(_file,md_str,mode)
        # MDリストを空にする(追記ハック用)
        self.mdList = []

    def write_asHTML(self,_file=None,css_file=None):
        """ HTMLとして吐き出す """
        # マークダウンをコンストラクション
        md_str = "\n".join(self.mdList)
        # HTML二変換
        html = md2html(md_str,css_file)
        # 書き込み
        file_utils.write2(_file,html,"w")


def md2html(md_str,css_file=None):
    """ 
    コンストラクトされたMDからHMLTを起こす。
    CSSファイルが指定されれば、それを埋め込む
    """
    # マークダウンから変換
    html_for_md = markdown2.markdown(md_str,extras=["tables","fenc-code-blocks","code-color"]).encode("utf-8")

    # 埋め込み用CSS
    css_str = ""
    if css_file :
        with open(css_file) as f :
            css_str = f.read() # 読み込み

    # HTMLのコンストラクション
    html = """
    <HTML>
    <HEAD>
        <STYLE type="text/css">
            <!--
                %s
            -->
        </STYLE>
    </HEAD>
    <BODY>
       %s
    </BODY>
    </HTML>
    """ % (css_str,html_for_md)

    return html



class App(object):
    def main(self):
        header_str = """
        然るに遺憾で御座る１
        然るに遺憾で御座る2 
        然るに遺憾で御座る3
        """
        md = MarkdownConstructor()

        md.add_tag("h1","ヘッダ")
        md.add_p(header_str)

        md.add_tag("h2","リスｔo")
        md.add_list( "list"+str(num) for num in range(10) )

        table = [
            [ str(x) for x in range(3) ],
            [ str(x) for x in range(3) ],
            [ str(x) for x in range(3) ],
            [ str(x) for x in range(3) ],
            [ str(x) for x in range(3) ],
            [ str(x) for x in range(3) ]
        ]
        md.add_tag("h2","テーブル")
        md.add_table(["th1","th2","th3"],table)

        md.add_tag("h1","ヘッダ22")
        md.add_p(header_str)

        #md.write_asHTML(css_file="")
        #md.write()
        with open("out") as f :
            string = f.read()
        print md2html(string.decode("utf-8"))




if __name__ == '__main__':
    App().main()



        
