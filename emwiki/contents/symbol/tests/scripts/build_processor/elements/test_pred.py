from contents.symbol.scripts.build_processor.elements.element import Element
from contents.symbol.tests.scripts.build_processor.elements.test_element import TestElement


class TestPred(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        preds = self.filter_by_type(reader.elements, 'pred')
        self.assertEqual(6, len(preds))

        # basics
        names = ['is_applicable_to', 'is_applicable_to', 'is_applicable_to',
                 'is_properly_applicable_to', 'is_properly_applicable_to', 'is_properly_applicable_to']

        for i in range(len(preds)):
            self.assertEqual(names[i], preds[i].symbol, i)
            self.assertEqual('kw', preds[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('pred', preds[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", preds[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual("oo:Definition", preds[i].main_sentence.attrib.get("typeof"), i)
            self.assertEqual("abcmiz_0", preds[i].filename)
            self.assertEqual("R" + str(i+1), preds[i].anchor)

    def test_read_redefine(self):
        reader = self.read_by_name("abian")
        preds = self.filter_by_type(reader.elements, 'pred')
        self.assertEqual(2, len(preds))

        names = ['is_a_fixpoint_of', 'is_a_fixpoint_of']
        redefine_indices = [1]
        for i in range(len(preds)):
            self.assertEqual(names[i], preds[i].symbol, i)
            self.assertEqual(i in redefine_indices, preds[i].is_redefine(), i)
            self.assertEqual("abian", preds[i].filename)
            self.assertEqual("R" + str(i+1), preds[i].anchor)

    def test_read_synonym(self):
        reader = self.read_by_name("altcat_3")
        preds = self.filter_by_type(reader.elements, 'pred')
        self.assertEqual(3, len(preds))

        names = ['is_left_inverse_of', 'is_right_inverse_of', 'are_iso']
        anchors = ['R1', 'NR2', 'R2']
        synonym_indices = [1]
        for i in range(len(preds)):
            self.assertEqual(names[i], preds[i].symbol, i)
            self.assertEqual(i in synonym_indices, preds[i].is_synonym(), i)
            self.assertEqual("altcat_3", preds[i].filename)
            self.assertEqual(anchors[i], preds[i].anchor)

    def test_read_antonym(self):
        reader = self.read_by_name("boolealg")
        preds = self.filter_by_type(reader.elements, 'pred')
        self.assertEqual(5, len(preds))

        names = ['=', 'meets', 'misses', 'meets', 'misses']
        anchors = ['R1', 'R2', 'NR3', 'R3', 'R4']
        redefine_indices = [0, 3, 4]
        antonym_indices = [2]
        for i in range(len(preds)):
            self.assertEqual(names[i], preds[i].symbol, i)
            self.assertEqual(i in redefine_indices, preds[i].is_redefine(), i)
            self.assertEqual(i in antonym_indices, preds[i].is_antonym(), i)
            self.assertEqual("boolealg", preds[i].filename)
            self.assertEqual(anchors[i], preds[i].anchor)

