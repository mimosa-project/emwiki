from contents.symbol.tests.scripts.build_processor.elements.test_element import TestElement


class TestFunc(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        funcs = self.filter_by_type(reader.elements, 'func')
        self.assertEqual(12, len(funcs))

        names = ['non-', 'adjs', 'types', 'types', 'ast', 'ast',
                 'apply', 'ast', 'sub', 'sub', '@-->', 'radix']
        for i in range(len(funcs)):
            self.assertEqual(names[i], funcs[i].symbol, i)
            self.assertEqual('kw', funcs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('func', funcs[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", funcs[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual("oo:Definition", funcs[i].main_sentence.attrib.get("typeof"), i)
            self.assertEqual("abcmiz_0", funcs[i].filename)
            self.assertEqual("K" + str(i+1), funcs[i].anchor)

    def test_read_bracket(self):
        reader = self.read_by_name("afinsq_1")
        funcs = self.filter_by_type(reader.elements, 'func')
        self.assertEqual(19, len(funcs))

        names = ['len', 'len', 'dom', '<%%>', '<%>', '^', '<%%>', '<%%>', '<%%>', '^omega', 'Replace',
                 'FS2XFS', 'XFS2FS', 'FS2XFS*', 'XFS2FS*', 'Down', '^', '^', '<%%>']
        anchors = ['NK1', 'K1', 'K2', 'K3', 'K4', None, 'K5', 'K6', 'K7', 'K8',
                   'NK11', 'K9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16']
        redefine_indices = [1, 2, 5, 6, 16, 17]
        synonym_indices = [0, 10]
        for i in range(len(funcs)):
            self.assertEqual(names[i], funcs[i].symbol, i)
            self.assertEqual('kw', funcs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual(i in redefine_indices, funcs[i].is_redefine(), i)
            self.assertEqual(i in synonym_indices, funcs[i].is_synonym(), i)
            self.assertEqual("afinsq_1", funcs[i].filename)
            self.assertEqual(anchors[i], funcs[i].anchor)

    def test_read_redefine(self):
        reader = self.read_by_name("abcmiz_1")
        funcs = self.filter_by_type(reader.elements, 'func')
        self.assertEqual(71, len(funcs))

        redefine_indices = [3, 6, 22, 23, 25, 26, 34, 35, 43, 46, 47, 56, 57, 58, 63, 64, 65, 66, 67]
        for i in range(len(funcs)):
            self.assertEqual('kw', funcs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual(i in redefine_indices, funcs[i].is_redefine(), i)
            self.assertEqual("abcmiz_1", funcs[i].filename)

    def test_read_synonym(self):
        reader = self.read_by_name("abcmiz_1")
        funcs = self.filter_by_type(reader.elements, 'func')
        self.assertEqual(71, len(funcs))

        synonym_indices = [2, 4, 24, 42, 44, 45]
        for i in range(len(funcs)):
            self.assertEqual('kw', funcs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual(i in synonym_indices, funcs[i].is_synonym(), i)
            self.assertEqual("abcmiz_1", funcs[i].filename)

"""
    def test_read_funct_1(self):
        reader = self.read_by_name("funct_1")
        funcs = self.filter_by_type(reader.elements, 'func')
        self.assertEqual(7, len(funcs))

        redefine_indices = [1, 4, 5]
        synonym_indices = [2]
        names = ['.', 'rng', '*', '"', '.:', '"', 'the_value_of']
        for i in range(len(funcs)):
            self.assertEqual(names[i], funcs[i].symbol)
            self.assertEqual('kw', funcs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual(i in redefine_indices, funcs[i].is_redefine(), i)
            self.assertEqual(i in synonym_indices, funcs[i].is_synonym(), i)
            self.assertEqual("funct_1", funcs[i].filename)
"""
