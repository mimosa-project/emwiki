import json
import os

from django.conf import settings
from django.test import TestCase
from graph import create_graph, retrieve_dependency


class CreateGraphTest(TestCase):
    def test_create_graph(self):

        node2targets_mml = retrieve_dependency.make_miz_dependency()
        create_graph.create_graph(node2targets_mml, "test_dot_graph.json")

        with open(settings.GRAPH_ELS_DIR + "/graph_attrs/test_dot_graph.json", "r") as f_in:
            dot_graph = json.load(f_in)

        # テスト
        nodes_num = 0
        for els in dot_graph["eleObjs"]:
            if els["group"] == "nodes":
                nodes_num += 1
        self.assertEqual(len(node2targets_mml), nodes_num)

    def tearDown(self):
        os.remove(settings.GRAPH_ELS_DIR + "/graph_attrs/test_dot_graph.json")
