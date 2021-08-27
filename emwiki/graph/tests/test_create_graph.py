import json

from django.test import TestCase
from emwiki.settings import GRAPH_ELS_DIR
from graph import create_graph, retrieve_dependency


class CreateGraphTest(TestCase):
    def test_create_graph(self):
        # 準備
        with open(GRAPH_ELS_DIR + "/graph_attrs/dot_graph.json", "r") as f_in:
            dot_graph_copy = json.load(f_in)

        node2targets_mml = retrieve_dependency.make_miz_dependency()
        create_graph.create_graph(node2targets_mml)
        with open(GRAPH_ELS_DIR + "/graph_attrs/dot_graph.json", "r") as f_in:
            dot_graph_new = json.load(f_in)

        with open(GRAPH_ELS_DIR + "/graph_attrs/dot_graph.json", "w") as f_out:
            f_out.write(json.dumps(dot_graph_copy, indent=4))

        # テスト
        nodes = dot_graph_new["elements"]["nodes"]
        self.assertEqual(len(node2targets_mml), len(nodes))
