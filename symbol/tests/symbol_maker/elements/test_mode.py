from symbol.tests.symbol_maker.elements.test_element import TestElement


class TestMode(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        modes = self.filter_by_type(reader.elements, 'mode')

        self.assertEqual(2, len(modes))
        # names = ['type of', 'adjective of']
        names = ['type', 'adjective']
        for i in range(len(modes)):
            self.assertEqual(names[i], modes[i].symbol, i)
            self.assertEqual('kw', modes[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('mode', modes[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", modes[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual(None, modes[i].main_sentence, i)
            self.assertEqual("abcmiz_0", modes[i].filename)
            self.assertEqual("NM" + str(i + 1), modes[i].anchor)

        reader = self.read_by_name("abcmiz_1")
        modes = self.filter_by_type(reader.elements, 'mode')
        self.assertEqual(13, len(modes))

        # names = ['Subset of', 'FinSequence of', 'variable', 'quasi-loci',
        #         'ConstructorSignature', 'expression of', 'expression of',
        #         'OperSymbol of', 'quasi-term of', 'quasi-adjective of',
        #         'quasi-type of', 'term-transformation of', 'valuation of']
        names = ['Subset', 'FinSequence', 'variable', 'quasi-loci',
                 'ConstructorSignature', 'expression', 'expression',
                 'OperSymbol', 'quasi-term', 'quasi-adjective',
                 'quasi-type', 'term-transformation', 'valuation']
        anchors = ['NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'M1', 'M2', 'NM9', 'NM10',
                   'M3', 'M4', 'NM13']
        for i in range(len(modes)):
            self.assertEqual(names[i], modes[i].symbol, i)
            self.assertEqual('kw', modes[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('mode', modes[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", modes[i].defblock.xpath("./span")[0].text, i)
            # self.assertEqual(None, modes[i].main_sentence, i)
            self.assertEqual("abcmiz_1", modes[i].filename)
            self.assertEqual(anchors[i], modes[i].anchor)

    def test_read_redefine(self):
        reader = self.read_by_name("altcat_5")
        modes = self.filter_by_type(reader.elements, 'mode')
        self.assertEqual(3, len(modes))

        # names = ['ObjectsFamily of', 'MorphismsFamily of', 'MorphismsFamily of']
        names = ['ObjectsFamily', 'MorphismsFamily', 'MorphismsFamily']
        anchors = ['NM1', 'M1', None]   # 'redefine mode' does not hove anchor
        redefine_indices = [2]
        for i in range(len(modes)):
            self.assertEqual(names[i], modes[i].symbol, i)
            self.assertEqual('kw', modes[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('mode', modes[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", modes[i].defblock.xpath("./span")[0].text, i)
            # self.assertEqual(None, modes[i].main_sentence, i)
            self.assertEqual(i in redefine_indices, modes[i].is_redefine())
            self.assertEqual("altcat_5", modes[i].filename)
            self.assertEqual(anchors[i], modes[i].anchor)

    def test_read_synonym(self):
        reader = self.read_by_name("filerec1")
        modes = self.filter_by_type(reader.elements, 'mode')
        self.assertEqual(1, len(modes))

        # names = ['File of']
        names = ['File']
        anchors = ['NM1']
        synonym_indices = [0]
        for i in range(len(modes)):
            self.assertEqual(names[i], modes[i].symbol, i)
            self.assertEqual('kw', modes[i].keyword_node.attrib.get('class'), i)
            # self.assertEqual('mode', modes[i].keyword_node.text.strip(), i)
            # self.assertEqual("definition", modes[i].defblock.xpath("./span")[0].text, i)
            # self.assertEqual(None, modes[i].main_sentence, i)
            self.assertEqual(i in synonym_indices, modes[i].is_synonym())
            self.assertEqual("filerec1", modes[i].filename)
            self.assertEqual(anchors[i], modes[i].anchor)
