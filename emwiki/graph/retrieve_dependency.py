import glob
import os
import re
from collections import defaultdict

from django.conf import settings

DIRECTIVES = ['vocabularies', 'constructors', 'notations', 'registrations',
              'theorems', 'schemes', 'definitions', 'requirements',
              'expansions', 'equalities']


def make_miz_dependency():
    """
    articleが参照しているarticleを取得する．
    参照しているarticle ＝ 環境部に記載されたarticle（ただし，vocabulariesを除く）
    Args:
    Return:
        article2dependency: keyがarticle名，valueがkeyのarticleが参照しているarticle．
                            key: str(), value: set()
    """
    cwd = os.getcwd()
    try:
        article2dependency_articles = dict()
        os.chdir(settings.MML_MML_DIR)
        miz_files = glob.glob("*.miz")  # mmlディレクトリの.mizファイルを取り出す

    finally:
        os.chdir(cwd)

    for miz_file in miz_files:
        with open(os.path.join(settings.MML_MML_DIR, miz_file), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            miz_file_contents = f.read()
        directive2articles = extract_articles(miz_file_contents)
        dependency_articles = merge_values(
            directive2articles, remove_keys=["vocabularies"])
        article2dependency_articles[format_mizfile_name_to_import_style(
            miz_file)] = dependency_articles

    return article2dependency_articles


def extract_articles(contents):
    """
    mizファイルが環境部(environ~begin)で参照しているarticleを
    各ディレクティブごとに取得する。
    Args:
        contents: mizファイルのテキスト(内容)
    Retrun:
        directive2articles: keyがディレクティブ名、valueが参照しているarticleのリスト
    """
    directive2articles = defaultdict(list)
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

    # ディレクティブでどのarticleを参照しているかを得る
    directive_name = str()
    for word in environ_words:
        # 環境部の終了条件
        if re.match(r"begin", word):
            break
        # ディレクティブ名が来たとき
        if word in DIRECTIVES:
            directive_name = word
            continue
        # ;でそのディレクティブでの参照が終わったとき
        if re.match(r";", word):
            directive_name = str()
            continue
        # ディレクティブ名が決まっているとき
        if directive_name:
            directive2articles[directive_name].append(word)

    return directive2articles


def merge_values(key2list, remove_keys=list()):
    """
    valueがlistのdictについて，そのvalueをマージする．
    その後，重複を取り除く．
    Args:
        key2list: valueがlist()の辞書
        remove_keys: マージしたくない項目がある場合は，ここに記述することで取り除くことができる
    Return:
        merge_values_set: key2listのvalueをマージしたもの．set()．
    """
    merge_values = []
    for k, v in key2list.items():
        if k in remove_keys:
            continue
        merge_values.extend(v)
    merge_values_set = set(merge_values)

    return merge_values_set


def format_mizfile_name_to_import_style(mizfile_name):
    """
    (小文字のファイル名).mizを(大文字のファイル名)に変換する．
    例：tarski.miz -> TARSKI
    Args:
        mizfile_name: (小文字のファイル名).miz，str()
    Return:
        new_miz_name: (大文字のファイル名)，str()
    """
    new_miz_name = re.sub(r'\.miz', '', mizfile_name)
    new_miz_name = new_miz_name.upper()

    return new_miz_name
