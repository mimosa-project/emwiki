import codecs
from collections import defaultdict
import glob
import os
from pathlib import Path
import pickle
import re

from emparser.preprocess import Lexer

from emwiki.settings import ABSTR_DIR, VCT_DIR, DATA_FOR_SEARCH_DIR

lexer = Lexer()
lexer.load_symbol_dict(os.path.join(VCT_DIR, 'mml.vct'))
lexer.build_len2symbol()
RESERVED_WORDS = set(["according", "aggregate", "all", "and", "antonym", "are", "as", "associativity", "assume", "asymmetry", "attr",
                  "be", "begin", "being", "by", "canceled", "case", "cases", "cluster", "coherence", "commutativity", "compatibility", 
                  "connectedness", "consider", "consistency", "constructors", "contradiction", "correctness", "def", "deffunc", "define",
                  "definition", "definitions", "defpred", "do", "does", "end", "environ", "equals", "ex", "exactly", "existence", "for",
                  "from", "func", "given", "hence", "hereby", "holds", "idempotence", "identify", "if", "iff", "implies", "involutiveness",
                  "irreflexivity", "is", "it", "let", "means", "mode", "non", "not", "notation", "notations", "now", "of", "or", "otherwise",
                  "over", "per", "pred", "prefix", "projectivity", "proof", "provided", "qua", "reconsider", "reduce", "reducibility",
                  "redefine", "reflexivity", "registration", "registrations", "requirements", "reserve", "sch", "scheme", "schemes",
                  "section", "selector", "set", "sethood", "st", "struct", "such", "suppose", "symmetry", "synonym", "take", "that", "the", 
                  "then", "theorem", "theorems", "thesis", "thus", "to", "transitivity", "uniqueness", "vocabularies", "when", "where",
                  "with", "wrt", ",", ";", ":", "(", ")", "[", "]", "{", "}", "=", "&", "->", ".=", "...", "$1", "$2", "$3", "$4", "$5",
                  "$6", "&7", "$8", "$9", "$10", "(#", "#)"])

def is_symbol(word):
    if "__" in word and "_" in word.replace("__", ""):
        return True

    else:
        return False

def is_variable(word):
    # 変数ならTrueを返し、そうでないならFalseを返す関数
    if word in RESERVED_WORDS or word.isdecimal() or is_symbol(word):
        return False
    else:
        return True

def create_abs_dictionary():
    # (definition or theorem)  (行数)  (ファイル名)  (ラベル名)       (テキスト)
    # definition               51      abcmiz_0.abs  BCMIZ_0:def 1   let T be RelStr;   attr T is Noetherian means   the InternalRel of T is co-well_founded; 

    cwd = os.getcwd()
    try:
        path = ABSTR_DIR
        os.chdir(path)
        abs_files = sorted(glob.glob("*.abs"))
    finally:
        os.chdir(cwd)

    with open (os.path.join(DATA_FOR_SEARCH_DIR, 'abs_dictionary.txt'), "w") as abs_dictionary_file:
        for file in abs_files:
            with codecs.open(os.path.join(ABSTR_DIR, file), "r", "utf-8", "ignore") as f:
                save_abs_dictionary_by_theorem_or_definition(abs_dictionary_file, file, f)

def save_abs_dictionary_by_theorem_or_definition(abs_dictionary_file, file, f):
    lines = f.readlines()

    state = {
        "is_definition_block": False, # definitionのブロック内にあるかどうか  definition ~~ end; までの部分

        "is_theorem": False, # theoremの中にあるかどうか　theorem ~~ ; までの部分

        "is_definition": False # definitionのラベル内かどうか
    }

    common_definition_statement = [] # 変数定義などのdefinitionの共通部分の要素

    indivisual_definition_statement = [] # definitionのラベルごとの要素
    
    # abs_dictionaryに保存する情報
    item = {
        "title": "",
        "line_no": "",
        "filename": file,
        "label": "",
        "text": ""
    }

    for line_no, line in enumerate(lines):
                    
        line = line.strip() # 改行文字を除くため
        words = line.split()

        for word_no, word in enumerate(words): 
            if word == "::" and word_no == 0 and state["is_definition_block"] == False and state["is_theorem"] == False:
                break

            elif word == "theorem" and word_no == 0:
                state["is_theorem"] = True
                item["title"] = "theorem"
                item["line_no"] = line_no
                if bool(re.search(r"\w+:\w+", line.split('::')[1])):
                    item["label"] = line.split('::')[1]
                break

            elif state["is_theorem"] == True:
                # コメントの場合は無視
                if word == "::":
                    break
                on_theorem(item, state, file, word, line, line_no, abs_dictionary_file)
    
            elif word == "definition" and word_no == 0:
                state["is_definition_block"] = True
                item["title"] = "definition"

            elif state["is_definition_block"] == True:
                on_definition_block(item, state, file, word, line, line_no, common_definition_statement, indivisual_definition_statement, abs_dictionary_file)
                break
                

def clear_item(item, file):
    item["title"] = ""
    item["line_no"] = ""
    item["filename"] = file
    item["label"] = ""
    item["text"] = ""

def on_theorem(item, state, file, word, line, line_no, abs_dictionary_file):
    item["text"] += " " + word

    # ";"はtheoremの最後の文字なため、改行しtheoremに関する変数を初期化している
    if word[-1] == ";":
        if item["label"] != "":
            abs_dictionary_file.write(f"{item['title']} {item['line_no']} {item['filename']} {item['label']} {item['text']}\n")
        clear_item(item, file)
        state["is_theorem"] = False

def on_definition_block(item, state, file, word, line, line_no, common_definition_statement, indivisual_definition_statement, abs_dictionary_file):
    if "end" in line and ";" in line:
        state["is_definition_block"] = False
        state["is_definition"] = False
        common_definition_statement = []
        indivisual_definition_statement = []
                                                 
    elif word == ":::":
        pass

    elif state["is_definition"] == False and word != "::":
        # definition let ~
        # 等の場合があるためdefinitionが含まれていたら除く
        common_definition_statement.append(line.replace("definition", ""))

    # definition内かつ最終行でない場合のとき
    elif state["is_definition"] and ";" not in line:
        indivisual_definition_statement.append(line)

    # definitionのラベルがある場合
    elif word == "::" and state["is_definition"] == False:
        state["is_definition"] = True
        on_definition_label(item, line, line_no, common_definition_statement, indivisual_definition_statement)
                                                    
    # definitionのラベル部分の最後
    elif ";" in line and state["is_definition"]:
        indivisual_definition_statement.append(line)
        state["is_definition"] = False
        item["text"] = ' '.join(common_definition_statement) + " " + ' '.join(indivisual_definition_statement)
        if item["label"]:
            abs_dictionary_file.write(f"{item['title']} {item['line_no']} {item['filename']} {item['label']} {item['text']}\n")
        clear_item(item, file)
        indivisual_definition_statement = []

def on_definition_label(item, line, line_no, common_definition_statement, indivisual_definition_statement):
    # line.split('::')[1].replace(' ','')はラベル名、のちの処理を簡略するためラベル名にある" "を除いている
    # 例
    # ABCMIZ_0:def 1 -> ABCMIZ_0:def1
    item["title"] = "definition"
    item["line_no"] = line_no
    if bool(re.search(r"\w+:\w+", line.split('::')[1].replace(' ',''))): # コメント部分がラベル名かどうか判断している
        item["label"] = line.split('::')[1].replace(' ','')
    if common_definition_statement:
        while common_definition_statement[-1][-1] != ";":
            indivisual_definition_statement.append(common_definition_statement.pop())
            if not common_definition_statement:
                break

def rename_variable_and_symbol(line, lexer):
    """
    変数を___に変更し、最期に変数の種類の____を入れている
    例
    line
    let T be RelStr;   attr T is Noetherian means   the InternalRel of T is co-well_founded; 
    return
    let ___ be RelStr ; attr ___ is Noetherian means the InternalRel of ___ is co-well_founded ; ____
    """

    variable2appearance = defaultdict(int)

    lines = ("begin\n " + " ".join(line)).split(" ")
    lines = lexer.remove_comment(lines)
    tokenized_lines, position_map = lexer.lex(lines)

    for i, token in enumerate(tokenized_lines):
        if is_variable(token):
            variable2appearance[token] += 1
            tokenized_lines[i] = "___"
        tokenized_lines[i] = re.sub("__[^_]+_", "", tokenized_lines[i]) #symbolは除く

    return f"{' '.join(tokenized_lines[1:])} {'____ '*len(variable2appearance)}"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

def create_document_vectors():
    """
    abs_dictionary.txt からdocument_vectors.txtを作成する関数
    変数を___に変更し、最期に変数の種類数の____を入れている
    例
    abs_dictionary.txt
    definition 51 abcmiz_0.abs BCMIZ_0:def 1   let T be RelStr;   attr T is Noetherian means   the InternalRel of T is co-well_founded; 
        
    document_vectors.txt
    let ___ be RelStr ; attr ___ is Noetherian means the InternalRel of ___ is co-well_founded ; ____ 
    """

    with open(os.path.join(DATA_FOR_SEARCH_DIR, 'document_vectors.txt'), "w") as file_document_vectors:
        with open(os.path.join(DATA_FOR_SEARCH_DIR, 'abs_dictionary.txt'), "r") as f:
            lines = f.readlines()
            for line in lines:
                # "," ";" は、ほぼすべての定理に存在しておりノイズになる可能性が高いため除いている
                line = line.replace(",", " ") 
                line = line.replace(";", "")
                line = line.split()
                file_document_vectors.write(f"{rename_variable_and_symbol(line[4:], lexer)} \n")

def save_byte_index_of_lines(input, output):
    """
    inputを行ごとにバイト数を求め、outputに保存する関数
    """
    with open(input, "rb") as f:
        byte_indices = []
        byte_indices.append(0)
        with open(output, "wb") as fi:
            while True:
                a = f.readline()
                if not a:
                    break
                byte_indices.append(f.tell())

            pickle.dump(byte_indices, fi)