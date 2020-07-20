from contents.symbol.tests.symbol_maker.elements.test_element import TestElement


class TestAttr(TestElement):
    def test_read_basic(self):
        reader = self.read_by_name("abcmiz_0")
        clusters = self.filter_by_type(reader.elements, 'cluster')
        self.assertEqual(17, len(clusters))

        anchors = ['CC1', 'CC2', 'CC3', 'CC4', 'RC1', 'FC1', 'RC3', 'FC2', 'FC3', 'FC4', 'RC5',
                   'RC6', 'FC5', 'FC6', 'FC7', 'RC8', 'RC9', 'RC10']
        for i in range(len(clusters)):
            self.assertEqual('kw', clusters[i].keyword_node.attrib.get('class'), i)
            self.assertEqual('cluster', clusters[i].keyword_node.text.strip(), i)
            self.assertEqual("registration", clusters[i].defblock.xpath("./span")[0].text, i)
            self.assertEqual("oo:Theorem", clusters[i].main_sentence.attrib.get("typeof"), i)
            self.assertEqual("abcmiz_0", clusters[i].filename)
            self.assertEqual(anchors[i], clusters[i].anchor)
