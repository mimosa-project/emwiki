class GraphService {
  static getModel() {
    return axios.get('/static/graph/graph_attrs/dot_graph.json').then((response) => {
      return response.data
    })
  }

  static getCytoscapeStyle() {
    return [
      // Initial style
      {
        selector: "node",
        css: {
          "background-color": "#000000", "shape": "ellipse", "width": "150", "height": "150",
          "content": "data(name)", "font-size": 40, "opacity": 1, "z-index": 1,
          "text-halign": "center", "text-valign": "center", "font-style": "normal",
          "font-weight": "bold", "color": "#ffffff",
          "text-outline-color": "#000000", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "edge",
        css: {
          "line-color": "black", "target-arrow-shape": "triangle", "curve-style": "straight",
          "target-arrow-color": "black", "arrow-scale": 3, "width": 5, "opacity": 0.3, "z-index": 1
        }
      },
      // Style of highlight nodes
      {
        selector: "node.highlight",
        css: {
          "font-size": 20, "width": 250, "height": 250, "font-size": 100,
          "content": "data(name)", "opacity": 1, "z-index": 10
        }
      },
      // Style of selected(clicked) node
      {
        selector: "node.selected",
        css: {
          "background-color": "#99ff00", "color": "#006633", "width": 300, "height": 300,
          "text-outline-color": "#99ff00", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      // Style of ancestor nodes
      {
        selector: "node.ancestor0",
        css: {
          "background-color": "#ff0000", "color": "#ffffff",
          "text-outline-color": "#ff0000", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.ancestor1",
        css: {
          "background-color": "#ff4400", "color": "#ffffff",
          "text-outline-color": "#ff4400", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.ancestor2",
        css: {
          "background-color": "#ff7700", "color": "#ffffff",
          "text-outline-color": "#ff7700", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.ancestor3",
        css: {
          "background-color": "#ff9900", "color": "#ffffff",
          "text-outline-color": "#ff9900", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.ancestor4",
        css: {
          "background-color": "#ffbb00", "color": "#ffffff",
          "text-outline-color": "#ffbb00", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      // Style of descendant nodes.
      {
        selector: "node.descendant0",
        css: {
          "background-color": "#0000ff", "color": "#ffffff",
          "text-outline-color": "#0000ff", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.descendant1",
        css: {
          "background-color": "#0077ff", "color": "#ffffff",
          "text-outline-color": "#0077ff", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.descendant2",
        css: {
          "background-color": "#00bbff", "color": "#ffffff",
          "text-outline-color": "#00bbff", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.descendant3",
        css: {
          "background-color": "#00ddff", "color": "#000000",
          "text-outline-color": "#00ddff", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      {
        selector: "node.descendant4",
        css: {
          "background-color": "#00ffff", "color": "#000000",
          "text-outline-color": "#00ffff", "text-outline-opacity": 1, "text-outline-width": 10
        }
      },
      // Style of highlight edges
      {
        selector: "edge.highlight",
        css: {
          "line-color": "#004400", "curve-style": "straight",
          "target-arrow-color": "#004400", "arrow-scale": 5, "width": 10, "opacity": 1, "z-index": 20
        }
      },
      // Style of not highlight nodes
      {
        selector: "node.faded",
        css: { "background-color": "#808080", "text-outline-color": "#808080", "color": "#ffffff" }
      },
      // Style of not highlight nodes and edges
      {
        selector: ".faded",
        css: { "opacity": 0.4, "z-index": 0 }
      },
    ]
  }
}