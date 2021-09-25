import json

from django.test import TestCase
from emwiki.settings import GRAPH_ELS_DIR
from graph import create_graph, retrieve_dependency


class CreateGraphTest(TestCase):
    def test_create_graph(self):
        with open(GRAPH_ELS_DIR + "/graph_attrs/layered_graph.json",
                  "r") as f_in:
            layered_graph = json.load(f_in)

        node2targets_mml = retrieve_dependency.make_miz_dependency()
        create_graph.create_graph(node2targets_mml)

        # テスト
        nodes = dot_graph["elements"]["nodes"]
        self.assertEqual(len(node2targets_mml), len(nodes))

    def tearDown(self):
        os.remove(GRAPH_ELS_DIR + "/graph_attrs/test_dot_graph.json")
