#! /usr/bin/python
#-*- coding: utf-8 -*-

import os.path
import sys
import imp

"""
このスクリプトはモジュール検索パスの設定を行います。
"""
#pwd = os.path.split(os.path.abspath(__file__))[0]
code_dir = os.path.realpath(__file__)
parent_dir = os.path.split(code_dir)[0]
base_dir = os.path.split(parent_dir)[0]

module_dir = os.path.abspath("/Git/module")
#sys.path.insert(0,module_dir)
sys.path.insert(0,os.path.join(parent_dir,"modules"))


# 基底パスに移動
os.chdir(base_dir)

#imp.load_module("setup",*imp.find_module("setup",[parent_dir]))
