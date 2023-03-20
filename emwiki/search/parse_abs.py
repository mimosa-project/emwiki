import copy
import glob
import os
import pickle

import py_miz_controller
from django.conf import settings


def is_variable(token):
    return (token.token_type == py_miz_controller.TokenType.IDENTIFIER
            and (token.identifier_type == py_miz_controller.IdentifierType.RESERVED
                 or token.identifier_type == py_miz_controller.IdentifierType.VARIABLE))


def create_theorem_and_definition_tokens_list(token_table, file_name):
    """
    入力: absファイルのtoken_table
    出力: 定義または定理ごとに分割されたtoken列のリスト
    例: [[定理1のtoken1, 定理1のtoken2, 定理1のtoken3], [定理2のtoken1, 定理2のtoken2, 定理2のtoken3], ...]
    """
    upper_article_name = file_name.upper().split('.')[0]
    state = {
        "is_theorem": False,  # theoremの中にあるかどうか　theorem ~ ; までの部分
        "is_definition_block": False,  # definitionのブロック内にあるかどうか  definition ~~ end; までの部分
        "is_definition": False  # definitionのラベル内かどうか
    }
    token_num = token_table.token_num
    tokens_list = []
    current_statement = []
    common_definition_statement = []
    for i in range(token_num):
        token = token_table.token(i)
        if (state["is_theorem"]):
            current_statement.append(token)
            # 定理は";"で終了する
            if (token.text == ";"):
                state["is_theorem"] = False
                tokens_list.append(current_statement)
                current_statement = []
        if (state["is_definition_block"]):
            if (token.text == "end"):
                state["is_definition_block"] = False
                common_definition_statement = []
            elif (token.text == ";"):
                current_statement.append(token)
                # 定義は共通部分とラベルがついた部分から成る
                if (state["is_definition"]):
                    state["is_definition"] = False
                    tokens_list.append(common_definition_statement + current_statement)
                    current_statement = []
                # ラベル内でない場合, 共通部分として保存
                else:
                    common_definition_statement.extend(current_statement)
                    current_statement = []
            # コメントの始まりがarticle名と一致するかどうかで, ラベル名か判断.
            # :: ABCMIZ_0:def 1 -> ABCMIZ_0:def1
            elif (token.token_type == py_miz_controller.TokenType.COMMENT
                  and token.text.replace('::', '').replace(' ', '').startswith(upper_article_name + ":def")):
                current_statement.append(token)
                state["is_definition"] = True
            else:
                current_statement.append(token)
        elif (token.text == "theorem"):
            state["is_theorem"] = True
        elif (token.text == "definition"):
            state["is_definition_block"] = True

    return tokens_list


def convert_to_abs_dictionary_line(theorem_and_definition_tokens, file_name):
    """
    入力: 定義または定理のtoken列
    出力: abs_dictionary.txtのフォーマット(definition/theorem 行数 ファイル名 ラベル 定理本文)の
    例: definition 51 abcmiz_0.abs ABCMIZ_0:def1 let T be RelStr ; attr T is Noetherian means the InternalRel of T is co-well_founded ;
    """
    upper_article_name = file_name.upper().split('.')[0]
    title = ""
    line_no = ""
    label = ""
    text = ""
    for token in theorem_and_definition_tokens:
        if (token.token_type == py_miz_controller.TokenType.COMMENT):
            split_token_text = token.text.split()
            # ラベルを表すコメントの場合
            # 例「:: ABCMIZ_0:def 1」
            if (len(split_token_text) > 1 and split_token_text[1].startswith(upper_article_name)):
                if ("def" in split_token_text[1]):
                    title = "definition"
                    label = split_token_text[1] + split_token_text[2]
                else:
                    title = "theorem"
                    label = split_token_text[1]
                line_no = str(token.line_number)
            else:
                pass
        else:
            text += token.text + " "
    return f"{title} {line_no} {file_name} {label} {text}"


def resolve_variable_type(token, variables):
    """
    入力: 変数のtokenと, 定理で出現する変数の情報
    出力:
      variablesにtokenの型情報がある場合: 型のトークン列(type_tokens)
      variablesにtokenの型情報がない場合: 空のリスト
    """
    for variable in variables:
        # token本体の型情報があるか調査する
        if (token.id == variable["variable_token"].id):
            return variable["type_tokens"]
        # ref_tokenの型情報があるか再帰的に調査
        ref_token = token.ref_token
        previous_tokens = [token]
        while (True):
            if (ref_token is None):
                break
            # 循環的に参照されていないか調べる
            elif (ref_token in previous_tokens):
                break
            elif (ref_token.id == variable["variable_token"].id):
                return variable["type_tokens"]
            previous_tokens.append(ref_token)
            ref_token = ref_token.ref_token
    return []


def add_variable2type(variable_tokens, type_tokens, variables):
    """
    変数と, 型のtoken列の, 対応マッピングを追加する関数.
    ただし, 型のtoken列に変数が含まれる場合は, その変数の型に置き換えてマッピングする.
    入力例:
      variable_tokens: [b]
      type_tokens: [element, of, a]
      variables: [{"variable_token": a, "type_token", [set]}]
    処理後:
      variables: [{"variable_token": a, "type_token", [set]},
                  {"variable_token": b, "type_token", [element, of, set]}]
    """
    replaced_type_tokens = []
    for type_token in type_tokens:
        if (is_variable(type_token)):
            replaced_type_tokens.extend(resolve_variable_type(type_token, variables))
        else:
            replaced_type_tokens.append(type_token)
    # マッピングを追加
    for variable_token in variable_tokens:
        variables.append({"variable_token": variable_token, "type_tokens": replaced_type_tokens})


def extract_reserve_statements(token_table):
    """
    入力: token_table
    出力: reserveで始まる文のトークン列のリスト
    出力例: [["reserve", "a", "for", "set"], ["reserve", "b", "for", "object"]]
    """
    state = {
        "is_reserve_block": False,  # reserveのblock内にあるかどうか  reserve ~ ;までの部分
    }
    reserve_statements: list[list[py_miz_controller.token]] = []
    reserve_statement: list[py_miz_controller.token] = []
    for i in range(token_table.token_num):
        token = token_table.token(i)
        if (state["is_reserve_block"]):
            reserve_statement.append(token)
            if (token.text == ";"):
                state["is_reserve_block"] = False
                reserve_statements.append(copy.copy(reserve_statement))
                reserve_statement.clear()
        elif (token.text == "reserve"):
            state["is_reserve_block"] = True
            reserve_statement.append(token)
    return reserve_statements


def extract_declarations_from_reserve_statements(reserve_statements):
    """
    入力: reserveで始まる文のトークン列のリスト
    出力: 変数宣言部分ごとに分割したトークン列のリスト
    入力例:[["reserve", "a", ",", "b", "for", "set", ",", "c", "for", "object", ";"], ["reserve", "d", "for", "object", ";"]]
    出力例:[["a", "b", "for", "set", ","], ["c", "for", "object"], ["d", "for", "object"]]
    """
    state = {
        "for_has_appeared": False  # forが出現したかどうか
    }
    variable_declaration_statements: list[list[py_miz_controller.token]] = []
    variable_declaration_statement: list[py_miz_controller.token] = []
    for reserve_statement in reserve_statements:
        for token in reserve_statement:
            if (token.text == "reserve"):
                continue
            # 変数宣言部の終了条件:
            # 1. ";"が出現,
            # 2. forが出現した後, ref_tokenを持たない変数が出現した場合. 下の例ではaの前で一つの変数宣言部が終了
            # 例: reserve X for ARS, a,b,c,u,v,w,x,y,z for Element of X;
            if (token.text == ";"
               or (state["for_has_appeared"] and is_variable(token) and token.ref_token is None)):
                variable_declaration_statements.append(copy.copy(variable_declaration_statement))
                variable_declaration_statement.clear()
                state["for_has_appeared"] = False
                # 終了条件2の場合, 変数を新しい変数宣言部に追加
                if (is_variable(token)):
                    variable_declaration_statement.append(token)
            else:
                variable_declaration_statement.append(token)
                if (token.text == "for"):
                    state["for_has_appeared"] = True

    return variable_declaration_statements


def extract_declarations_from_tokens(tokens):
    """
    入力: 定理のtoken列
    出力: 変数宣言部分ごとに分割されたtoken列
    入力例: ["for", "l", "being", "set", ",", "x", "being", "object", "holds"]
    出力例: [["l", "being", "set", ","], ["x", "being", "object"]]
    """
    state = {
        "is_variable_declaration_statement": False,  # 変数宣言部分内にあるかどうか(for|let|given|ex ~~ st|holds|;|suchまでの部分)
        "being_has_appeared": False  # 変数宣言部分内でbeing|beが出現したかどうか
    }
    KEYWORDS_OF_END_OF_VARIABLE_DECLARATION_STATEMENT = ["st", "holds", ";", "such", "for", "let", "given", "ex"]  # 変数宣言の部分が終了するキーワード
    variable_declaration_statements: list[list[py_miz_controller.token]] = []
    variable_declaration_statement: list[py_miz_controller.token] = []
    for token in tokens:
        if not state["is_variable_declaration_statement"]:
            if (is_variable(token) and (token.ref_token is None)):
                state["is_variable_declaration_statement"] = True
                variable_declaration_statement.append(token)
            continue
        if (state["being_has_appeared"]):
            # 変数宣言部分で, be/beingが出現した後の処理
            if (token.text in KEYWORDS_OF_END_OF_VARIABLE_DECLARATION_STATEMENT):
                variable_declaration_statements.append(copy.copy(variable_declaration_statement))
                variable_declaration_statement.clear()
                state["is_variable_declaration_statement"] = False
                state["being_has_appeared"] = False
            # 変数宣言終了のキーワードが出現せずに, 新しい変数宣言開始
            # 例: for l being set, x being object holds
            elif (is_variable(token) and (token.ref_token is None)):
                variable_declaration_statements.append(copy.copy(variable_declaration_statement))
                variable_declaration_statement.clear()
                state["being_has_appeared"] = False
                variable_declaration_statement = [token]
            else:
                variable_declaration_statement.append(token)
        elif (token.text == "be" or token.text == "being"):
            variable_declaration_statement.append(token)
            state["being_has_appeared"] = True
        else:
            variable_declaration_statement.append(token)

    return variable_declaration_statements


def listup_declared_variable2type(variable_declaration_statements):
    """
    入力: 変数宣言部分ごとに分割されたトークン列のリスト
    出力: 変数と型のマッピング
    入力例: [["a", "b", "for", "set", ","], ["c", "for", "object"], ["d", "for", "object"]]
    出力例: [
        {"variable_token": a, "type_token", [set]},
        {"variable_token": b, "type_token", [set]},
        {"variable_token": c, "type_token", [object]},
        {"variable_token": d, "type_token", [object]}]
    """
    variables: list[dict] = []  # 変数の型情報を保存した辞書のリスト(この関数の出力)
    current_variable_tokens = []  # 宣言された変数を一時的に保存するリスト
    current_type_tokens = []  # 宣言された変数の型のtoken列を保存するリスト
    SEPARATORS = ["for", "be", "being"]  # 分割するためのキーワード
    state = {
        "keywords_has_appeared": False  # forが出現したかどうか
    }
    for variable_declaration_statement in variable_declaration_statements:
        for token in variable_declaration_statement:
            if (state["keywords_has_appeared"]):
                current_type_tokens.append(token)
                # 宣言部分の最後のトークンの場合
                if (token == variable_declaration_statement[-1]):
                    add_variable2type(current_variable_tokens, current_type_tokens, variables)
                    [list.clear() for list in [current_variable_tokens, current_type_tokens]]
                    state["keywords_has_appeared"] = False
            elif (is_variable(token) and (token.ref_token is None)):
                current_variable_tokens.append(token)
            elif (token.text in SEPARATORS):
                state["keywords_has_appeared"] = True

    return variables


def listup_reserved_variable2type(token_table):
    """
    入力: absファイルを解析して得られたtoken_table
    出力: reserveで宣言された変数の情報

    absファイルの例:
    reserve i for Nat,
      j for Element of NAT,
      X,Y,x,y,z for set;

    出力例:
    [{variable_token: i, type_tokens: [Nat]},
     {variable_token: j, type_tokens: [Element, of, NAT]},
     {variable_token: X, type_tokens: [set]},
     {variable_token: Y, type_tokens: [set]},
     ...]
    """
    # reserveで始まる文をreserve_statementsに集める
    reserve_statements = extract_reserve_statements(token_table)
    # reserve_statementsから変数宣言部分ごとに分割したリストを得る
    variable_declaration_statements = extract_declarations_from_reserve_statements(reserve_statements)
    return listup_declared_variable2type(variable_declaration_statements)


def count_number_of_variable(tokens):
    """
    入力: 定義または定理のtoken列
    出力: 変数の種類数
    """
    # variable_token_listの中に, new_tokenと同じ変数が存在する場合Trueを返す
    def is_duplicate_variable_in_list(new_token, variable_token_list):
        for variable_token in variable_token_list:
            if (new_token.ref_token == variable_token or new_token.ref_token == variable_token.ref_token):
                return True
        return False

    # 定理で出現した変数を保存するリスト
    variable_token_list = []
    for token in tokens:
        if (is_variable(token) and not is_duplicate_variable_in_list(token, variable_token_list)):
            variable_token_list.append(token)
    return len(variable_token_list)


def replace_variable_with_type_string(token, variables):
    """
    token(変数)のテキストを作成する関数
    入力: 変数のtokenと, 定理で出現する変数の情報
    出力:
      型情報がある場合: 変数の型の文字列
      型情報がない場合: "___"
    """
    type_tokens = resolve_variable_type(token, variables)
    if (len(type_tokens)):
        type_text = ""
        for type_token in type_tokens:
            type_text += type_token.text + " "
        return type_text
    else:
        return "___" + " "


def extract_variables_with_type_in_tokens(tokens, common_variables):
    # variablesは定理ごとにcommon_variablesを上書きする
    variables: list[dict] = copy.copy(common_variables)
    # 変数宣言部分をvariable_declaration_statementsに集める(","は後の処理で消すのでそのまま)
    variable_declaration_statements = extract_declarations_from_tokens(tokens)
    variables.extend(listup_declared_variable2type(variable_declaration_statements))
    return variables


def replace_variables_with_types_in_tokens(tokens, common_variables):
    """
    入力: 定義または定理のtokenのリスト, ファイル共通の変数情報のリスト
    出力: モデルへ入力するための処理を行った定理本文(変数を型名に置き換え, ","と";"を削除, 変数の種類の数だけ末尾に"____"を追加)
    処理前: let T be RelStr ; attr T is Noetherian means the InternalRel of T is co-well_founded ;
    処理後: let RelStr be RelStr  attr RelStr is Noetherian means the InternalRel of RelStr is co-well_founded   ____
    """
    number_of_variable = count_number_of_variable(tokens)
    variables = extract_variables_with_type_in_tokens(tokens, common_variables)
    processed_text = ""
    for token in tokens:
        # コメントは無視
        if (token.token_type == py_miz_controller.TokenType.COMMENT):
            pass
        elif (is_variable(token)):
            processed_text += replace_variable_with_type_string(token, variables)
        else:
            processed_text += token.text + " "
    # "," ";" は, ほぼすべての定理に存在しておりノイズになる可能性が高いため除く
    # 変数が何種類出現したかを考慮するために, 末尾に変数の種類の数だけ"____"を追加する
    return f"{processed_text.replace(',', '').replace(';', '')} {'____ '*number_of_variable}"


def create_abs_dictionary_and_document_vectors(output_dir):
    """
    output_dirにabs_dictionary.txtとdocument_vectors.txtを生成する関数.
    abs_dictionary.txt: absファイルから定義と定理を抽出し, 以下の形式でファイルに書き込み
        (definition or theorem)  (行数)  (ファイル名)  (ラベル名)       (テキスト)
        definition               51      abcmiz_0.abs  BCMIZ_0:def 1   let T be RelStr;   attr T is Noetherian means   the InternalRel of T is co-well_founded;

    document_vectors.txt: 検索に使われる定義と定理の文字列を保存. ","と";"は削除され, 変数は型に置換, 末尾に変数の種類数"____"が追加される.
        let RelStr be RelStr  attr RelStr is Noetherian means the InternalRel of RelStr is co-well_founded   ____
    """
    cwd = os.getcwd()
    try:
        os.chdir(settings.MML_ABSTR_DIR)
        abs_files = sorted(glob.glob("*.abs"))
    finally:
        os.chdir(cwd)

    with open(os.path.join(output_dir, "abs_dictionary.txt"), "w", encoding='utf-8') as file_abs_dictionary, open(os.path.join(output_dir, "document_vectors.txt"), "w", encoding='utf-8') as file_document_vectors:
        miz_controller = py_miz_controller.MizController()
        for file_name in abs_files:
            miz_controller.exec_file(os.path.join(settings.MML_ABSTR_DIR, file_name), settings.MML_VCT_PATH)
            token_table = miz_controller.token_table
            theorem_and_definition_tokens_list = create_theorem_and_definition_tokens_list(token_table, file_name)
            common_variables = listup_reserved_variable2type(token_table)
            # abs_dictionary.txtとdocument_vectors.txtに1行(1つの定理)づつ書き込み
            for theorem_and_definition_tokens in theorem_and_definition_tokens_list:
                file_abs_dictionary.write(
                    f"{convert_to_abs_dictionary_line(theorem_and_definition_tokens, file_name)} \n")
                file_document_vectors.write(
                    f"{replace_variables_with_types_in_tokens(theorem_and_definition_tokens, common_variables)} \n")


# 検索時に実行
def transform_query(query):
    miz_controller = py_miz_controller.MizController()
    miz_controller.exec_buffer(query, settings.MML_VCT_PATH)
    token_table = miz_controller.token_table
    common_variables = listup_reserved_variable2type(token_table)
    # replace_variables_with_types_in_tokens関数の入力形式に合わせるための処理
    token_list = []
    for i in range(token_table.token_num):
        token = token_table.token(i)
        token_list.append(token)
    return replace_variables_with_types_in_tokens(token_list, common_variables)


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
