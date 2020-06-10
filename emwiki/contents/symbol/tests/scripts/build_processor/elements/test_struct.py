from contents.symbol.tests.scripts.build_processor.elements.test_element import TestElement


class TestStruct(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        structs = self.filter_by_type(reader.elements, 'struct')

        # basics
        self.assertEqual(3, len(structs))
        names = ['AdjectiveStr', 'TA-structure', 'TAS-structure']
        for i in range(len(structs)):
            self.assertEqual(names[i], structs[i].symbol, i)
            self.assertEqual('kw', structs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('struct', structs[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", structs[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual(None, structs[i].main_sentence, i)
            self.assertEqual("abcmiz_0", structs[i].filename)
            self.assertEqual("L" + str(i+1), structs[i].anchor)

    def test_read_over(self):
        reader = self.read_by_name("aofa_a00")
        structs = self.filter_by_type(reader.elements, 'struct')
        self.assertEqual(6, len(structs))

        # names = ['VarMSAlgebra over', 'UndefMSAlgebra over', 'ProgramAlgStr over',
        #          'GeneratorSystem over', 'ConnectivesSignature', 'BoolSignature']
        names = ['VarMSAlgebra', 'UndefMSAlgebra', 'ProgramAlgStr',
                 'GeneratorSystem', 'ConnectivesSignature', 'BoolSignature']
        for i in range(len(structs)):
            self.assertEqual(names[i], structs[i].symbol, i)
            self.assertEqual('kw', structs[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('struct', structs[i].keyword_node.text.strip(), i)
            self.assertEqual("definition", structs[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual(None, structs[i].main_sentence, i)
            self.assertEqual("aofa_a00", structs[i].filename)
            self.assertEqual("L" + str(i+1), structs[i].anchor)
