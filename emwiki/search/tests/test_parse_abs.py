import os

import py_miz_controller
from django.conf import settings
from django.test import TestCase
from search.parse_abs import (convert_to_abs_dictionary_line,
                              count_number_of_variable,
                              create_common_variables,
                              create_theorem_and_definition_tokens_list,
                              replace_variables_with_types_in_tokens,
                              transform_query)


class ParseAbsTest(TestCase):
    def setUp(self):
        self.file_name = "tarski.abs"
        self.miz_controller = py_miz_controller.MizController()
        self.miz_controller.exec_file(os.path.join(settings.TEST_ABS_DIR, self.file_name), settings.TEST_VCT_PATH)

    def test_create_theorem_and_definition_tokens_list(self):
        theorem_and_definition_tokens_list = create_theorem_and_definition_tokens_list(self.miz_controller.token_table, self.file_name)
        # tarski.absには検索対象の定義・定理は9件存在する
        self.assertEqual(len(theorem_and_definition_tokens_list), 9)

    def test_create_common_variables(self):
        common_variables = create_common_variables(self.miz_controller.token_table)
        # tarski.absでは, reserveによって9個の変数が宣言されている
        self.assertEqual(len(common_variables), 9)
        # tarski.absでreserveによって最初に宣言された変数の型は"object"である
        self.assertEqual(common_variables[0]["type_tokens"][0].text, "object")

    def test_convert_to_abs_dictionary_line(self):
        theorem_and_definition_tokens_list = create_theorem_and_definition_tokens_list(self.miz_controller.token_table, self.file_name)

        # テストケース1(TARSKI:1)
        abs_dictionary_line_tarski_1 = convert_to_abs_dictionary_line(theorem_and_definition_tokens_list[0], self.file_name)
        expected_tarski_1 = "theorem 25 tarski.abs TARSKI:1 for x being object holds x is set ;"
        # splitされて使用されるため
        self.assertEqual(abs_dictionary_line_tarski_1.split(), expected_tarski_1.split())

        # テストケース2(TARSKI:def1): 共通部分を含む定義を正しく抽出できているかどうか
        abs_dictionary_line_tarski_def_1 = convert_to_abs_dictionary_line(theorem_and_definition_tokens_list[2], self.file_name)
        expected_tarski_def_1 = "definition 33 tarski.abs TARSKI:def1 let y be object ; func { y } -> set means for x being object holds x in it iff x = y ;"
        self.assertEqual(abs_dictionary_line_tarski_def_1.split(), expected_tarski_def_1.split())

        # テストケース3(TARSKI:def2)
        abs_dictionary_line_tarski_def_2 = convert_to_abs_dictionary_line(theorem_and_definition_tokens_list[3], self.file_name)
        expected_tarski_def_2 = "definition 37 tarski.abs TARSKI:def2 let y be object ; let z be object ; func { y , z } -> set means x in it iff x = y or x = z ;"
        self.assertEqual(abs_dictionary_line_tarski_def_2.split(), expected_tarski_def_2.split())

    def test_count_number_of_variable(self):
        theorem_and_definition_tokens_list = create_theorem_and_definition_tokens_list(self.miz_controller.token_table, self.file_name)
        # tarski.absの1番目の定理では, 変数は1種類出現する. 2番目の定理では3種類, 3番目の定理では2種類出現する.
        self.assertEqual(count_number_of_variable(theorem_and_definition_tokens_list[0]), 1)
        self.assertEqual(count_number_of_variable(theorem_and_definition_tokens_list[1]), 3)
        self.assertEqual(count_number_of_variable(theorem_and_definition_tokens_list[2]), 2)

    def test_replace_variables_with_types_in_tokens(self):
        theorem_and_definition_tokens_list = create_theorem_and_definition_tokens_list(self.miz_controller.token_table, self.file_name)
        common_variables = create_common_variables(self.miz_controller.token_table)
        # テストケース1(TARSKI:1)
        document_vectors_line_tarski_1 = replace_variables_with_types_in_tokens(theorem_and_definition_tokens_list[0], common_variables)
        expected_tarski_1 = "for object being object holds object is set   ____  "
        self.assertEqual(document_vectors_line_tarski_1.split(), expected_tarski_1.split())

        # テストケース2(TARSKI:def1)
        document_vectors_line_tarski_def_1 = replace_variables_with_types_in_tokens(theorem_and_definition_tokens_list[2], common_variables)
        expected_tarski_def_1 = "let object be object  func { object } -> set means for object being object holds object in it iff object = object   ____ ____"
        self.assertEqual(document_vectors_line_tarski_def_1.split(), expected_tarski_def_1.split())

        # テストケース2(TARSKI:def2)
        document_vectors_line_tarski_def_2 = replace_variables_with_types_in_tokens(theorem_and_definition_tokens_list[3], common_variables)
        expected_tarski_def_2 = "let object be object  let object be object  func { object  object } -> set means object in it iff object = object or object = object   ____ ____ ____"
        self.assertEqual(document_vectors_line_tarski_def_2.split(), expected_tarski_def_2.split())

    def test_transform_query(self):
        # テストケース1(ABCMIZ_0:def7)
        query = "for x, y being object ex z being set st for a being object holds ( a in z iff ( a = x or a = y ) ) ;"
        processed_text = transform_query(query)
        expected = "for object  object being object ex set being set st for object being object holds ( object in set iff ( object = object or object = object ) )   ____ ____ ____ ____"
        self.assertEqual(processed_text.split(), expected.split())

        # テストケース2(オリジナル)
        query = "for x be set , y be Element of x holds y is ;"
        processed_text = transform_query(query)
        expected = "for set be set Element of set be Element of set holds Element of set is  ____ ____"
        self.assertEqual(processed_text.split(), expected.split())
