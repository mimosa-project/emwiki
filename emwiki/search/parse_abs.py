import copy
import glob
import os
import pickle

import py_miz_controller
from django.conf import settings


def is_variable(token):
    return (token.token_type == py_miz_controller.TokenType.IDENTIFIER and
            (token.identifier_type == py_miz_controller.IdentifierType.RESERVED or
             token.identifier_type == py_miz_controller.IdentifierType.VARIABLE))


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
            elif (token.token_type == py_miz_controller.TokenType.COMMENT and
                  token.text.replace('::', '').replace(' ', '').startswith(upper_article_name + ":def")):
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


def resolve_reserve_block(variables, current_variable_tokens, current_type_tokens):
    """
    reserve文での変数宣言終了時の処理
    変数と型の対応を保存し, 一時リストを初期化する
    """
    for variable_token in current_variable_tokens:
        variables.append({"variable_token": variable_token, "type_tokens": copy.copy(current_type_tokens)})
    current_variable_tokens.clear()
    current_type_tokens.clear()


def create_common_variables(token_table):
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
    state = {
        "is_reserve_block": False,  # reserveのblock内にあるかどうか  reserve ~ ;までの部分
        "for_has_appeared": False  # reserveのblock内でforが出現したかどうか
    }
    token_num = token_table.token_num
    variables: list[dict] = []  # 変数の型情報を保存した辞書のリスト(この関数の出力)
    current_variable_tokens = []  # 宣言された変数を一時的に保存するリスト
    current_type_tokens = []  # 宣言された変数の型のtoken列を保存するリスト
    # 変数宣言終了時の処理
    for i in range(token_num):
        token = token_table.token(i)
        if (state["is_reserve_block"]):
            if (state["for_has_appeared"]):
                # reserve blockは";"で終了
                if (token.text == ";"):
                    resolve_reserve_block(variables, current_variable_tokens, current_type_tokens)
                    state["is_reserve_block"] = False
                    state["for_has_appeared"] = False
                    continue
                """
                forが出現し";"が出現する前に, 再びforが出現する場合の処理
                例1:
                reserve q for pure expression of C, a_Type C,
                  A, B for finite Subset of QuasiAdjs C;
                例2:
                reserve X for ARS, a,b,c,u,v,w,x,y,z for Element of X;
                """
                if (token.text == "for"):
                    # 例1で2回目のforが出現した時点のtype_tokensは["pure", "expression", "of", "C", ",", "a_Type", "C", "," "A", "," "B"]
                    # このとき, type_tokens[8]以降は新しい変数宣言となる
                    # 新しい変数宣言部が始まる境界のindexを特定する(例1だと, 8)
                    divide_index = len(current_type_tokens) - 1
                    for current_type_token in reversed(current_type_tokens):
                        # 改行があった場合はそこを境界とする(例1)
                        if (current_type_token.line_number < token.line_number):
                            break
                        # 変数以外のトークン(","を除く)が出現する箇所を境界とする(例2)
                        elif (current_type_token.text == ","):
                            pass
                        elif (not is_variable(current_type_token)):
                            break
                        divide_index -= 1
                    # 特定したindex以降のトークンを新しい変数宣言部として保存
                    new_tokens = current_type_tokens[divide_index:]
                    del current_type_tokens[divide_index:]
                    resolve_reserve_block(variables, current_variable_tokens, current_type_tokens)
                    # 新しい変数宣言部から変数を抽出
                    current_variable_tokens = [token for token in new_tokens if is_variable(token)]
                else:
                    current_type_tokens.append(token)
            # reserve block内でforが出現する前の処理. 出現した変数を記録する(複数宣言される場合もある)
            else:
                if (token.text == "for"):
                    state["for_has_appeared"] = True
                elif (is_variable(token)):
                    current_variable_tokens.append(token)
        elif (token.text == "reserve"):
            state["is_reserve_block"] = True
    return variables


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


def create_text(token, variables):
    """
    入力: tokenと定理で出現する変数の情報
    出力:
      tokenが変数の場合: 変数の型の文字列, 型情報がない場合は"___"
      tokenが変数ではない場合: tokenのテキスト
    """
    if (is_variable(token)):
        text_of_type = ""
        # variablesの中に, tokenまたは, tokenのref_tokenの型情報があるか調査する
        for variable in variables:
            if ((token.id == variable["variable_token"].id) or
               (token.ref_token and token.ref_token.id == variable["variable_token"].id)):
                # variable["type_tokens"]には型のtoken列が格納されている
                for type_token in variable["type_tokens"]:
                    text_of_type += type_token.text + " "
                return text_of_type
        return "___" + " "
    else:
        return token.text + " "


def resolve_variable_declaration_statement_text(variables, variable_declaration_statement, current_variables, current_type_tokens):
    """
    変数宣言終了時の処理
    変数と型の対応の保存, 変数宣言部分のテキストの生成, 一時リストの初期化を行う
    出力: 変数宣言部分のテキスト
    """
    # 型の情報がないまま変数宣言部分が終了した場合. 例: let c;
    if (len(current_type_tokens) == 0):
        for variable_token in current_variables:
            ref_token = variable_token.ref_token
            if (ref_token is None):
                continue
            # variable_tokenがref_tokenを持っており, variablesに存在する場合, その情報を元に新しく変数を登録
            filtered_list = list(filter(lambda variable_dict: variable_dict["variable_token"] == ref_token, variables))
            if (len(filtered_list) > 0):
                variables.append({"variable_token": variable_token, "type_tokens": copy.copy(filtered_list[0]["type_tokens"])})
    else:
        for variable_token in current_variables:
            variables.append({"variable_token": variable_token, "type_tokens": copy.copy(current_type_tokens)})
    # 変数宣言部分のテキストを生成
    variable_declaration_statement_text = ""
    for token in variable_declaration_statement:
        variable_declaration_statement_text += create_text(token, variables)
    # 一時リストの初期化
    variable_declaration_statement.clear()
    current_variables.clear()
    current_type_tokens.clear()
    return variable_declaration_statement_text


def replace_variable_with_type(tokens, common_variables):
    """
    入力: 定義または定理のtokenのリスト, ファイル共通の変数情報のリスト
    出力: モデルへ入力するための処理を行った定理本文(変数を型名に置き換え, ","と";"を削除, 変数の種類の数だけ末尾に"____"を追加)
    処理前: let T be RelStr ; attr T is Noetherian means the InternalRel of T is co-well_founded ;
    処理後: let RelStr be RelStr  attr RelStr is Noetherian means the InternalRel of RelStr is co-well_founded   ____
    """
    state = {
        "is_variable_declaration_statement": False,  # 変数宣言部分内にあるかどうか(for|let|given|ex ~~ st|holds|;|suchまでの部分)
        "being_has_appeared": False  # 変数宣言部分内でbeing|beが出現したかどうか
    }
    number_of_variable = count_number_of_variable(tokens)
    variables: list[dict] = copy.copy(common_variables)  # variablesは定理ごとにcommon_variablesを上書きする
    variable_declaration_statement = []  # 変数宣言されている部分のtoken列を一時的に保存するリスト
    current_variables: list[dict] = []  # 宣言された変数を一時的に保存するリスト
    current_type_tokens = []  # 宣言された変数の型のtoken列を保存するリスト
    KEYWORDS_OF_START_OF_VARIABLE_DECLARATION_STATEMENT = ["for", "let", "given", "ex"]  # 変数宣言の部分が開始されるキーワード
    KEYWORDS_OF_END_OF_VARIABLE_DECLARATION_STATEMENT = ["st", "holds", ";", "such"]  # 変数宣言の部分が終了するキーワード
    processed_text = ""
    for token in tokens:
        # コメントは無視
        if (token.token_type == py_miz_controller.TokenType.COMMENT):
            continue
        # ここから変数宣言部分の処理
        elif (state["is_variable_declaration_statement"]):
            variable_declaration_statement.append(token)
            # 変数宣言部分で, be/beingが出現した後の処理
            if (state["being_has_appeared"]):
                # 変数宣言部分の終了
                if (token.text in KEYWORDS_OF_END_OF_VARIABLE_DECLARATION_STATEMENT):
                    processed_text += resolve_variable_declaration_statement_text(variables, variable_declaration_statement, current_variables, current_type_tokens)
                    state["is_variable_declaration_statement"] = False
                    state["being_has_appeared"] = False
                # 新しい変数が続けて宣言される場合(for, let等のキーワードが出現する場合)
                # 例: for T being Noetherian sup-Semilattice for I being Ideal of T holds ...
                elif (token.text in KEYWORDS_OF_START_OF_VARIABLE_DECLARATION_STATEMENT):
                    processed_text += resolve_variable_declaration_statement_text(variables, variable_declaration_statement, current_variables, current_type_tokens)
                    state["being_has_appeared"] = False
                # 新しい変数が続けて宣言される場合(for, let等のキーワードが出現しない場合), beingの1つ前のtokenを新しい変数として扱う
                # 例: for l being quasi-loci, x being variable holds ...
                elif (token.text == "be" or token.text == "being"):
                    # 例の場合, 現時点で以下の状態になっている.
                    # current_type_tokens: ["for", "l", "being", "quasi-loci", ",", "x"]
                    # variable_declaration_statement: ["for", "l", "being", "quasi-loci", ",", "x", "being"]
                    # "x"以降のトークンは新しい変数宣言部分なので, それぞれ適切な回数popし, resolve_variable_declaration_statement_text()を実行する
                    current_type_tokens.pop()
                    being_token = variable_declaration_statement.pop()
                    new_variable_token = variable_declaration_statement.pop()
                    processed_text += resolve_variable_declaration_statement_text(variables, variable_declaration_statement, current_variables, current_type_tokens)
                    current_variables.append(new_variable_token)
                    variable_declaration_statement = [new_variable_token, being_token]
                # 変数宣言部分で, be/beingが出現した後, 上記の条件に該当しない場合は型として識別
                else:
                    current_type_tokens.append(token)
            elif (token.text == "be" or token.text == "being"):
                state["being_has_appeared"] = True
            # 変数宣言部分で, be/beingが出現しておらず, 変数が出現した際の処理
            # 例: let c
            elif (is_variable(token)):
                current_variables.append(token)
            # 変数宣言部分で, be/beingがまだ出現しておらず, 終了のキーワードが出現したときの処理
            # 例: let c;
            elif (token.text in KEYWORDS_OF_END_OF_VARIABLE_DECLARATION_STATEMENT):
                processed_text += resolve_variable_declaration_statement_text(variables, variable_declaration_statement, current_variables, current_type_tokens)
                state["is_variable_declaration_statement"] = False
        # ここから変数宣言ではない部分の処理
        # let, for等の変数宣言部分開始のキーワードが出現したときの処理
        elif (token.text in KEYWORDS_OF_START_OF_VARIABLE_DECLARATION_STATEMENT):
            state["is_variable_declaration_statement"] = True
            variable_declaration_statement.append(token)
        else:
            processed_text += create_text(token, variables)

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
            common_variables = create_common_variables(token_table)
            # abs_dictionary.txtとdocument_vectors.txtに1行(1つの定理)づつ書き込み
            for theorem_and_definition_tokens in theorem_and_definition_tokens_list:
                file_abs_dictionary.write(
                    f"{convert_to_abs_dictionary_line(theorem_and_definition_tokens, file_name)} \n")
                file_document_vectors.write(
                    f"{replace_variable_with_type(theorem_and_definition_tokens, common_variables)} \n")


# 検索時に実行
def transform_query(query):
    miz_controller = py_miz_controller.MizController()
    miz_controller.exec_buffer(query, settings.MML_VCT_PATH)
    token_table = miz_controller.token_table
    common_variables = create_common_variables(token_table)
    # replace_variable_with_type関数の入力形式に合わせるための処理
    token_list = []
    for i in range(token_table.token_num):
        token = token_table.token(i)
        token_list.append(token)
    return replace_variable_with_type(token_list, common_variables)


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
