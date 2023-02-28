import copy
import glob
import os
import pickle
import py_miz_controller

from django.conf import settings


def is_variable(token):
    return token.token_type == py_miz_controller.TokenType.IDENTIFIER and (token.identifier_type == py_miz_controller.IdentifierType.RESERVED or token.identifier_type == py_miz_controller.IdentifierType.VARIABLE)


def get_theorem_and_definition_tokens_list(token_table, file_name):
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
        token_text = token.text
        token_type = token.token_type
        if (state["is_theorem"]):
            current_statement.append(token)
            # 定理は";"で終了する
            if (token_text == ";"):
                state["is_theorem"] = False
                tokens_list.append(current_statement)
                current_statement = []
        if (state["is_definition_block"]):
            if (token_text == "end"):
                state["is_definition_block"] = False
                common_definition_statement = []
            elif (token_text == ";"):
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
            elif (token_type == py_miz_controller.TokenType.COMMENT and token_text.replace('::', '').replace(' ', '').startswith(upper_article_name + ":def")):
                current_statement.append(token)
                state["is_definition"] = True
            else:
                current_statement.append(token)
        elif (token_text == "theorem"):
            state["is_theorem"] = True
        elif (token_text == "definition"):
            state["is_definition_block"] = True

    return tokens_list


def get_abs_dictionary_line(theorem_and_definition_tokens, file_name):
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
        token_text = token.text
        token_type = token.token_type
        if (token_type == py_miz_controller.TokenType.COMMENT):
            split_token_text = token_text.split()
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
            text += token_text + " "
    return f"{title} {line_no} {file_name} {label} {text}"


def get_common_variable_dict_list(token_table):
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
        "the_for_has_appeared": False  # reserveのblock内でforが出現したかどうか
    }
    token_num = token_table.token_num
    variable_dict_list = []  # 変数の型情報を保存した辞書のリスト(この関数の出力)
    current_variable_dict_list = []  # 宣言された変数を一時的に保存するリスト
    current_type_tokens = []  # 宣言された変数の型のtoken列を保存するリスト

    # 変数宣言終了時の処理
    def resolve_reserve_block():
        for dict in current_variable_dict_list:
            dict["type_tokens"] = copy.copy(current_type_tokens)
        variable_dict_list.extend(current_variable_dict_list)
        current_variable_dict_list.clear()
        current_type_tokens.clear()

    for i in range(token_num):
        token = token_table.token(i)
        token_line_number = token.line_number
        token_text = token.text
        if (state["is_reserve_block"]):
            if (state["the_for_has_appeared"]):
                # reserve blockは";"で終了
                if (token_text == ";"):
                    resolve_reserve_block()
                    state["is_reserve_block"] = False
                    state["the_for_has_appeared"] = False
                    continue
                """
                forが出現し";"が出現する前に, 再びforが出現する場合の処理
                例1:
                reserve q for pure expression of C, a_Type C,
                  A for finite Subset of QuasiAdjs C;
                例2:
                reserve X for ARS, a,b,c,u,v,w,x,y,z for Element of X;
                """
                if (token_text == "for"):
                    new_variable_tokens = []
                    # 変数と","以外のtokenが出現するまで, ひとつの変数宣言部分とする
                    # それ以降に出現した変数は新しい変数宣言部分として処理を再開する
                    while (len(current_type_tokens)):
                        # 改行があった場合はそこを境界とする(例1)
                        if (current_type_tokens[-1].line_number < token_line_number):
                            resolve_reserve_block()
                            for new_variable_token in new_variable_tokens:
                                current_variable_dict_list.append({"variable_token": new_variable_token})
                            break
                        else:
                            popped_token = current_type_tokens.pop()
                            if (popped_token.text == ","):
                                pass
                            elif (is_variable(popped_token)):
                                new_variable_tokens.append(popped_token)
                            else:
                                current_type_tokens.append(popped_token)
                                resolve_reserve_block()
                                for new_variable_token in new_variable_tokens:
                                    current_variable_dict_list.append({"variable_token": new_variable_token})
                else:
                    current_type_tokens.append(token)
            # reserve block内でforが出現する前の処理. 出現した変数を記録する(複数宣言される場合もある)
            else:
                if (token_text == "for"):
                    state["the_for_has_appeared"] = True
                elif (is_variable(token)):
                    current_variable_dict_list.append({"variable_token": token})
        elif (token_text == "reserve"):
            state["is_reserve_block"] = True
    return variable_dict_list


def get_number_of_variable(tokens):
    """
    入力: 定義または定理のtoken列
    出力: 変数の種類数
    """
    # variable_token_listの中に, new_tokenと同じ変数が存在しないことをチェックする関数
    def check_no_duplicate_variable_in_list(new_token, variable_token_list):
        for variable_token in variable_token_list:
            if (new_token.ref_token == variable_token or new_token.ref_token == variable_token.ref_token):
                return False
        return True

    # 定理で出現した変数を保存するリスト
    variable_token_list = []
    for token in tokens:
        if (is_variable(token) and check_no_duplicate_variable_in_list(token, variable_token_list)):
            variable_token_list.append(token)
    return len(variable_token_list)


def get_variable_declaration_statement_text(variable_declaration_statement_token_list, variable_dict_list):
    # 変数宣言部分の変数を型に置き換える処理
    """
    入力: 変数宣言部分のtoken列
    出力: 変数の種類数
    """
    processed_text = ""
    for variable_declaration_statement_token in variable_declaration_statement_token_list:
        filtered_list = list(filter(lambda variable_dict: variable_dict["variable_token"] == variable_declaration_statement_token, variable_dict_list))
        if (len(filtered_list) > 0):
            variable_dict = filtered_list[0]
            # variable_dict["type_tokens"]には型のtokenリストが格納されている
            for type_token in variable_dict["type_tokens"]:
                processed_text += type_token.text + " "
        else:
            processed_text += variable_declaration_statement_token.text + " "
    return processed_text


def replace_variable_with_type(tokens, common_variable_dict_list):
    """
    入力: 定義または定理のtokenのリスト, ファイル共通の変数情報のリスト
    出力: モデルへ入力するための処理を行った定理本文(変数を型名に置き換え, ","と";"を削除, 変数の種類の数だけ末尾に"____"を追加)
    処理前: let T be RelStr ; attr T is Noetherian means the InternalRel of T is co-well_founded ;
    処理後: let RelStr be RelStr  attr RelStr is Noetherian means the InternalRel of RelStr is co-well_founded   ____
    """
    state = {
        "is_variable_declaration_statement": False,  # 変数宣言部分内にあるかどうか(for|let|given|ex ~~ st|holds|;|suchまでの部分)
        "the_being_has_appeared": False  # 変数宣言部分内でbeing|beが出現したかどうか
    }
    number_of_variable = get_number_of_variable(tokens)
    variable_dict_list = copy.copy(common_variable_dict_list)  # variable_dict_listは定理ごとにcommon_variable_dict_listを上書きする
    variable_declaration_statement_token_list = []  # 変数宣言されている部分のtoken列を一時的に保存するリスト
    current_variable_list = []  # 宣言された変数を一時的に保存するリスト
    current_type_tokens = []  # 宣言された変数の型のtoken列を保存するリスト
    keywords_of_start_of_variable_declaration_statement = ["for", "let", "given", "ex"]  # 変数宣言の部分が開始されるキーワード
    keywords_of_end_of_variable_declaration_statement = ["st", "holds", ";", "such"]  # 変数宣言の部分が終了するキーワード
    processed_text = ""

    # 変数宣言部分が終了するときに呼ばれる. 変数と型の対応の保存, 変数宣言部分のテキストの生成, 一時リストの初期化を行う
    def resolve_variable_declaration_statement_text():
        nonlocal processed_text
        current_variable_dict_list = []
        # 型の情報がないまま変数宣言部分が終了した場合. 例: let c;
        if (len(current_type_tokens) == 0):
            for variable_token in current_variable_list:
                ref_token = variable_token.ref_token
                if (ref_token is None):
                    continue
                # variable_tokenがref_tokenを持っており, variable_dict_listに存在する場合, その情報を元に新しく変数を登録
                filtered_list = list(filter(lambda variable_dict: variable_dict["variable_token"] == ref_token, variable_dict_list))
                if (len(filtered_list) > 0):
                    variable_dict_list.append({"variable_token": variable_token, "type_tokens": copy.copy(filtered_list[0]["type_tokens"])})
        else:
            for variable_token in current_variable_list:
                current_variable_dict_list.append({"variable_token": variable_token, "type_tokens": copy.copy(current_type_tokens)})
            variable_dict_list.extend(current_variable_dict_list)
        processed_text += get_variable_declaration_statement_text(variable_declaration_statement_token_list, variable_dict_list)
        variable_declaration_statement_token_list.clear()
        current_variable_list.clear()
        current_type_tokens.clear()

    for token in tokens:
        token_text = token.text
        token_type = token.token_type
        ref_token = token.ref_token
        # コメントは無視
        if (token_type == py_miz_controller.TokenType.COMMENT):
            continue
        # ここから変数宣言部分の処理
        elif (state["is_variable_declaration_statement"]):
            variable_declaration_statement_token_list.append(token)
            # 変数宣言部分で, be/beingが出現した後の処理
            if (state["the_being_has_appeared"]):
                # 変数宣言部分の終了
                if (token_text in keywords_of_end_of_variable_declaration_statement):
                    resolve_variable_declaration_statement_text()
                    state["is_variable_declaration_statement"] = False
                    state["the_being_has_appeared"] = False
                # 新しい変数が続けて宣言される場合(for, let等のキーワードが出現する場合)
                # 例: for T being Noetherian sup-Semilattice for I being Ideal of T holds ...
                elif (token_text in keywords_of_start_of_variable_declaration_statement):
                    resolve_variable_declaration_statement_text()
                    state["the_being_has_appeared"] = False
                # 新しい変数が続けて宣言される場合(for, let等のキーワードが出現しない場合)
                # 例: for l being quasi-loci, x being variable holds ...
                elif (token_text == "be" or token_text == "being"):
                    current_type_tokens.pop()
                    # beingのひとつ前のtoken(新しい変数)を取り出す.
                    # 例: for l being quasi-loci, x being までがリストにあるので2回popする
                    variable_declaration_statement_token_list.pop()
                    new_variable_token = variable_declaration_statement_token_list.pop()
                    resolve_variable_declaration_statement_text()
                    current_variable_list.append(new_variable_token)
                    variable_declaration_statement_token_list.extend([new_variable_token, token])
                # 変数宣言部分で, be/beingが出現した後, 上記の条件に該当しない場合は型として識別
                else:
                    current_type_tokens.append(token)
            elif (token_text == "be" or token_text == "being"):
                state["the_being_has_appeared"] = True
            # 変数宣言部分で, be/beingが出現しておらず, 変数が出現した際の処理
            # 例: let c
            elif (is_variable(token)):
                current_variable_list.append(token)
            # 変数宣言部分で, be/beingがまだ出現しておらず, 終了のキーワードが出現したときの処理
            # 例: let c;
            elif (token_text in keywords_of_end_of_variable_declaration_statement):
                resolve_variable_declaration_statement_text()
                state["is_variable_declaration_statement"] = False
        # ここから変数宣言ではない部分の処理
        # let, for等の変数宣言部分開始のキーワードが出現したときの処理
        elif (token_text in keywords_of_start_of_variable_declaration_statement):
            state["is_variable_declaration_statement"] = True
            variable_declaration_statement_token_list.append(token)
        # tokenが既に宣言された変数である場合(すなわち, ref_tokenをもっている場合), 型の文字列に置き換える
        elif (ref_token):
            have_type_info = False
            for variable_dict in variable_dict_list:
                if (ref_token.id == variable_dict["variable_token"].id):
                    # variable_dict["type_tokens"]には型のtokenリストが格納されている
                    for type_token in variable_dict["type_tokens"]:
                        processed_text += type_token.text + " "
                    have_type_info = True
                    break
            # 型の情報が存在しない変数は"___"に置き換える
            if not (have_type_info):
                processed_text += "___" + " "
        else:
            processed_text += token_text + " "

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
            theorem_and_definition_tokens_list = get_theorem_and_definition_tokens_list(token_table, file_name)
            common_variable_dict_list = get_common_variable_dict_list(token_table)
            # abs_dictionary.txtとdocument_vectors.txtに1行(1つの定理)づつ書き込み
            for theorem_and_definition_tokens in theorem_and_definition_tokens_list:
                file_abs_dictionary.write(
                    f"{get_abs_dictionary_line(theorem_and_definition_tokens, file_name)} \n")
                file_document_vectors.write(
                    f"{replace_variable_with_type(theorem_and_definition_tokens, common_variable_dict_list)} \n")


# 検索時に実行
def process_for_search_word(query):
    miz_controller = py_miz_controller.MizController()
    miz_controller.exec_buffer(query, settings.MML_VCT_PATH)
    token_table = miz_controller.token_table
    common_variable_dict_list = get_common_variable_dict_list(token_table)
    # replace_variable_with_type関数の入力形式に合わせるための処理
    token_list = []
    for i in range(token_table.token_num):
        token = token_table.token(i)
        token_list.append(token)
    return replace_variable_with_type(token_list, common_variable_dict_list)


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
