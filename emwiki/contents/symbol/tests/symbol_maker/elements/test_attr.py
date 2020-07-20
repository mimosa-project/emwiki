from contents.symbol.tests.symbol_maker.elements.test_element import TestElement


class TestAttr(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        attrs = self.filter_by_type(reader.elements, 'attr')
        self.assertEqual(14, len(attrs))

        names = ['Noetherian', 'Noetherian', 'Mizar-widening-like', 'void', 'involutive', 'without_fixpoints',
                 'consistent', 'adj-structured', 'adj-structured', 'adjs-typed', 'non-absorbing', 'subjected',
                 'non-absorbing', 'commutative']
        anchors = ['V1', None, 'V2', 'V4', 'V5', 'V6', 'V8', 'V9', None, 'V10',
                   'V12', 'V13', None, 'V14']
        redefine_indices = [1, 8, 12]

        for i in range(len(attrs)):
            self.assertEqual(names[i], attrs[i].symbol, i)
            self.assertEqual('kw', attrs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('attr', attrs[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", attrs[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual("oo:Definition", attrs[i].main_sentence.attrib.get("typeof"), i)
            self.assertEqual(i in redefine_indices, attrs[i].is_redefine())
            self.assertEqual("abcmiz_0", attrs[i].filename)
            self.assertEqual(anchors[i], attrs[i].anchor)

    def test_read_synonym_and_antonym(self):
        reader = self.read_by_name("armstrng")
        attrs = self.filter_by_type(reader.elements, 'attr')
        self.assertEqual(19, len(attrs))

        names = ['(B1)', '(B2)', '(F2)', '(DC1)', '(F1)', '(DC2)', '(F3)', '(F4)',
                 'full_family', '(DC3)', '(M1)', '(M2)', '(M3)', '(C1)',
                 'without_proper_subsets', '(C2)', '(DC4)', '(DC5)', '(DC6)']
        anchors = ['V1', 'NV2', 'NV4', 'NV5', 'V3', 'NV7', 'V4', 'V5', 'V6',
                   'V7', 'V8', 'V9', 'V10', 'NV15', 'V11', 'NV17', 'V12', 'V13', 'V14', 'V15']
        synonym_indices = [1, 2, 3, 5, 15]
        antonym_indices = [13]
        for i in range(len(attrs)):
            self.assertEqual(names[i], attrs[i].symbol, i)
            self.assertEqual('kw', attrs[i].keyword_node.attrib.get('class'), i)
            #self.assertEqual('attr', attrs[i].keyword_node.text.strip(), i)
            #self.assertEqual("definition", attrs[i].defblock.xpath("./span")[0].text, i)
            #self.assertEqual("oo:Definition", attrs[i].main_sentence.attrib.get("typeof"), i)
            self.assertEqual(i in synonym_indices, attrs[i].is_synonym())
            self.assertEqual(i in antonym_indices, attrs[i].is_antonym())
            self.assertEqual("armstrng", attrs[i].filename)
            self.assertEqual(anchors[i], attrs[i].anchor)
