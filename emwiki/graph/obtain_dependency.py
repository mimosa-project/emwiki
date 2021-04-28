import os
import glob
from pathlib import Path
from emwiki.settings import MIZFILE_DIR
import re

CATEGORIES = ['vocabularies', 'constructors', 'notations', 'registrations', 'theorems', 'schemes',
              'definitions', 'requirements', 'expansions', 'equalities']


def make_miz_dependency():
    """
    各カテゴリ内で参照しているファイルを取得する。
    Args:
    Return:
        miz_file_dict: 各カテゴリ(vocabularies, constructors等)において、各ライブラリが
                       どのライブラリを参照しているかを示す辞書。
                       例：lib_aがlib_x, lib_y, ... をvocabulariesで参照している場合、
                        miz_file_dict = {
                            'vocabularies': {
                                'lib_a': {'lib_x', 'lib_y', ...},
                                ...
                            }
                            'constructors': { ... },
                            ...
                        }
    """
    cwd = os.getcwd()
    try:
        article2dependency_articles = dict()
        os.chdir(MIZFILE_DIR)
        miz_files = glob.glob("*.miz")  # mmlディレクトリの.mizファイルを取り出す
        
        for miz_file in miz_files:
            with open(miz_file, 'rt', encoding='utf-8', errors="ignore") as f:
                miz_file_contents = f.read()
            category2articles = extract_articles(miz_file_contents)
            dependency_articles = merge_values(category2articles, remove_keys="vocabularies")
            article2dependency_articles[miz_file] = dependency_articles     

    finally:
        os.chdir(cwd)

    return article2dependency_articles


def extract_articles(contents):
    """
    mizファイルが環境部(environ~begin)で参照しているarticleを
    各カテゴリごとに取得する。
    Args:
        contents: mizファイルのテキスト(内容)
    Retrun:
        category2articles: keyがカテゴリ名、valueが参照しているarticleのリスト
    """
    category2articles = create_key2list(CATEGORIES)
    # 単語、改行、::、;で区切ってファイルの内容を取得
    file_words = re.findall(r"\w+|\n|::|;", contents)
    is_comment = False
    environ_words = list()

    # mizファイルから環境部を抜き出す
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
            continue
        # コメント以外の部分(environ ~ beginまで)
        if not is_comment:
            environ_words.append(word)
            # 本体部に入ったら、ループから抜け出す
            if re.match(r"begin", word):
                break

    # 改行文字の削除
    environ_words = [w for w in environ_words if not re.match(r"\n", w)] 

    # カテゴリでどのarticleを参照しているかを得る
    category_name = str()
    for word in environ_words:
        # 環境部の終了条件
        if re.match(r"begin", word):
            break
        # カテゴリ名が来たとき
        if word in category2articles.keys():
            category_name = word
            continue
        # ;でそのカテゴリでの参照が終わったとき
        if re.match(r";", word):
            category_name = str()
            continue
        # カテゴリ名が決まっているとき
        if category_name:
            category2articles[category_name].append(word)
        
    return category2articles


def create_key2list(keys):
    """
    keyがkeys，valueがlist()の辞書を作成する．
    Args:
        keys: keyに設定したい値(リスト)
    return:
        key2list: keyがkeys，valueがlist()の辞書
    """
    key2list = dict()
    for i in keys:
        key2list[i] = list()
    return key2list


def merge_values(key2list, remove_keys=list()):
    """
    valueがlistのdictについて，そのvalueをマージする．
    その後，重複を取り除く．
    Args: 
        key2list: valueがlistのdict
        remove_keys: マージしたくないkeyがある場合は記述する
    Return:
        
    """
    merge_values = []
    for k, v in key2list.items():
        if k in remove_keys:
            continue
        merge_values.extend(v)
    merge_values_set = set(merge_values)
    return merge_values_set