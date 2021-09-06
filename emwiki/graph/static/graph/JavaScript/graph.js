// jQueryは読み込み済み
$(function () {
    let cy = window.cy = cytoscape({
        container: document.getElementById('graph'),
        elements: [],
        boxSelectionEnabled: true,
        autounselectify: false,
        selectionType: "additive",
        wheelSensitivity: 0.1
    });
    let graph = JSON.parse(document.getElementById('graph_elements').textContent);
    let nodes = graph["elements"]["nodes"];
    let edges = graph["elements"]["edges"];
    let nodes_and_edges = [];

    for (let i in nodes) {
        for (let j in nodes[i]) {
            let node = {};
            node["group"] = "nodes";
            node["data"] = { "id": nodes[i][j]["id"], "name": nodes[i][j]["name"], "href": nodes[i][j]["href"] };
            node["position"] = { "x": (nodes[i][j]["x"] + 1) * 300, "y": (nodes[i][j]["y"] + 1) * 300 };
            nodes_and_edges.push(node);
        }
    }
    for (let i in edges) {
        for (let j in edges[i]) {
            let edge = {};
            edge["group"] = "edges";
            edge["data"] = { "source": edges[i][j]["source"], "target": edges[i][j]["target"] };
            nodes_and_edges.push(edge);
        }
    }
    cy.add(nodes_and_edges);
    // Set graph style
    cy.style([
        // Initial style
        {
            selector: "node",
            css: {
                "background-color": "#ff0000", "shape": "ellipse", "width": 150, "height": 150,
                "content": "data(name)", "font-size": 40, "opacity": 1, "z-index": 1,
                "text-halign": "center", "text-valign": "center", "font-style": "normal",
                "font-weight": "bold", "color": "#ffffff",
                "text-outline-color": "red", "text-outline-opacity": 1, "text-outline-width": 10
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
                "background-color": "#fff100", "color": "#ff0000", "width": 300, "height": 300,
                "text-outline-color": "#fff100", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        // Style of ancestor nodes
        {
            selector: "node.selected_ancestors0",
            css: {
                "background-color": "#fcc800", "color": "#ffffff",
                "text-outline-color": "#fcc800", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors1",
            css: {
                "background-color": "#f39800", "color": "#ffffff",
                "text-outline-color": "#f39800", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors2",
            css: {
                "background-color": "#eb6100", "color": "#ffffff",
                "text-outline-color": "#eb6100", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors3",
            css: {
                "background-color": "#e60012", "color": "#ffffff",
                "text-outline-color": "#e60012", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors4",
            css: {
                "background-color": "#ff4477", "color": "#ffffff",
                "text-outline-color": "#ff4477", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors5",
            css: {
                "background-color": "#ff6699", "color": "#ffffff",
                "text-outline-color": "#ff6699", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors6",
            css: {
                "background-color": "#cc4499", "color": "#ffffff",
                "text-outline-color": "#cc4499", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors7",
            css: {
                "background-color": "#be0081", "color": "#ffffff",
                "text-outline-color": "#be0081", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors8",
            css: {
                "background-color": "#920783", "color": "#ffffff",
                "text-outline-color": "#920783", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_ancestors9",
            css: {
                "background-color": "#601986", "color": "#ffffff",
                "text-outline-color": "#601986", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        // Style of descendant nodes
        {
            selector: "node.selected_descendants0",
            css: {
                "background-color": "#cfdb00", "color": "#ffffff",
                "text-outline-color": "#cfdb00", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants1",
            css: {
                "background-color": "#8fc31f", "color": "#ffffff",
                "text-outline-color": "#8fc31f", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants2",
            css: {
                "background-color": "#22ac38", "color": "#ffffff",
                "text-outline-color": "#22ac38", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants3",
            css: {
                "background-color": "#009944", "color": "#ffffff",
                "text-outline-color": "#009944", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants4",
            css: {
                "background-color": "#009b6b", "color": "#ffffff",
                "text-outline-color": "#009b6b", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants5",
            css: {
                "background-color": "#009e96", "color": "#ffffff",
                "text-outline-color": "#009e96", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants6",
            css: {
                "background-color": "#00a0c1", "color": "#ffffff",
                "text-outline-color": "#00a0c1", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants7",
            css: {
                "background-color": "#00a0e9", "color": "#ffffff",
                "text-outline-color": "#00a0e9", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants8",
            css: {
                "background-color": "#0086d1", "color": "#ffffff",
                "text-outline-color": "#0086d1", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        {
            selector: "node.selected_descendants9",
            css: {
                "background-color": "#0068b7", "color": "#ffffff",
                "text-outline-color": "#0068b7", "text-outline-opacity": 1, "text-outline-width": 10
            }
        },
        // Style of highlight edges
        {
            selector: "edge.highlight",
            css: {
                "line-color": "#006400", "curve-style": "straight",
                "target-arrow-color": "#006400", "arrow-scale": 5, "width": 10, "opacity": 1, "z-index": 20
            }
        },
        // Style of not highlight nodes
        {
            selector: "node.faded",
            css: { "background-color": "#808080" }
        },
        // Style of not highlight nodes and edges
        {
            selector: ".faded",
            css: { "opacity": 0.4, "z-index": 0 }
        },
    ]);

    /* 初期状態の設定 */
    cy.fit(cy.nodes().orphans());

    // 強調表示する祖先、子孫の世代数の初期化
    let ancestor_generations = 1;
    let descendant_generations = 1;


    /* 検索機能の追加 */
    // 全ノード名の取得
    let all_article_names = [];
    cy.nodes().forEach(function (node) {
        all_article_names.push(node.data("name"));
    });
    all_article_names.sort();
    // datalistに全ノード名を追加
    for (let article_name of all_article_names) {
        $("#article_list").append($("<option/>").val(article_name).html(article_name));
    }
    // searchボタンをクリックしたら検索開始
    $("#search").click(function () {
        // dropdownで選択したノード名、または記述したノード名を取得
        let select_node_name = $("#article_name").val();
        let select_node = cy.nodes().filter(function (ele) {
            return ele.data("name") === select_node_name;
        });
        // ノードが存在するか確認し、処理
        if (select_node.length) {
            reset_elements_style(cy);
            cy.$(select_node).addClass("selected");
            highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations);
            $("#select_article").text("SELECT: " + select_node_name);
        }
        else {
            alert("ERROR: Don't have '" + select_node_name + "' node. Please select existed nodes.");
        }
    });

    // 強調表示したい祖先、子孫の世代数を取得
    $("#ancestor_generations").on("change", function () {
        ancestor_generations = $("#ancestor_generations").val();
    });
    $("#descendant_generations").on("change", function () {
        descendant_generations = $("#descendant_generations").val();
    });

    // 背景をクリックしたときの処理
    cy.on("tap", function (event) {
        let clicked_point = event.target;
        if (clicked_point === cy) {
            reset_elements_style(cy);
        }
    });

    // ノードをクリックした場合、リンクに飛ぶ(htmlリンクの設定)
    // faded状態ならば反応しない
    cy.nodes().on("cxttap", function (event) {
        try {  // your browser may block popups
            window.open(this.data("href"));
        } catch (e) {  // fall back on url change
            window.location.href = this.data("href");
        }
    });

    // クリックしたノードの親と子、自身を色変更
    cy.nodes().on("tap", function (e) {
        // 全ノードをクラスから除外
        reset_elements_style(cy);
        // クリックしたノードをselectedクラスに入れる
        let clicked_node = e.target;
        highlight_select_elements(cy, clicked_node, ancestor_generations, descendant_generations);
        let clicked_node_name = clicked_node.data("name");
        $("#select_article").text("SELECT: " + clicked_node_name);
    });

    // reloadボタンでリロードにする
    $(document).ready(function () {
        $("#reload").click(function () {
            location.reload();
        });
    });
});


/**
 * グラフの要素のスタイルを初期状態(ノード：赤い丸、エッジ：黒矢印)に戻す。
 * ただし、移動したノードの位置は戻らない。
 * @param {cytoscape object} cy グラフ本体
 * @return
**/
function reset_elements_style(cy) {
    let all_class_names = ["highlight", "faded", "selected"];
    for (let i = 0; i < 10; i++) {
        all_class_names.push("selected_ancestors" + i);
        all_class_names.push("selected_descendants" + i);
    }
    cy.elements().removeClass(all_class_names);
    cy.nodes().unlock();
}


/**
 * 選択されたノードとそのノードの親子を強調表示させる(selectedクラスに追加する)
 * @param {cytoscape object} cy グラフ本体
 * @param {cytoscape object} select_node cy内の単一のノード
 * @param {int} ancestor_generations 辿りたい祖先の数
 * @param {int} descendant_generations 辿りたい子孫の数
 * @return
**/
function highlight_select_elements(cy, select_node, ancestor_generations, descendant_generations) {
    // 選択したノードの処理
    cy.$(select_node).addClass("highlight");
    cy.$(select_node).addClass("selected");

    // 選択したノードの祖先、子孫を強調表示する
    is_ancestor = true;
    highlight_connected_elements(cy, ancestor_generations, select_node, is_ancestor);
    highlight_connected_elements(cy, descendant_generations, select_node, !is_ancestor);

    // highlightクラス以外の物はfadedクラスに入れる
    fade_out_faded_elements(cy);

    // fadedクラスの物は、動かせないようにする
    cy.$(".faded").lock();

}


/**
 * 選択したノード(select_node)とその祖先または子孫を任意の世代数(generation)までを
 * 強調表示するクラスに追加する。
 * アルゴリズム
 *      次の処理を辿りたい世代数まで繰り返す
            1. first_connected_elementsの親(もしくは子)ノードとそのエッジを強調表示させるクラスに追加する
            2. 1でクラスに追加したノードをfirst_connected_elementsとして更新する
            3. 2でfirst_connected_elementsが空ならループを中断する
 * @param {cytoscape object} cy cytoscapeのグラフ本体
 * @param {int} generation 辿りたい世代数
 * @param {cytoscape object} select_node 選択したノード
 * @param {boolean} is_ancestor 辿りたいのは祖先かどうか。trueなら祖先、falseなら子孫を強調表示させていく。
 * @return
**/
function highlight_connected_elements(cy, generation, select_node, is_ancestor) {
    let first_connected_elements = cy.collection();  // 親(もしくは子)を取得したいノードのコレクション（≒リスト）
    first_connected_elements = first_connected_elements.union(select_node);
    for (let i = 0; i < generation; i++) {
        let class_name = is_ancestor ? "selected_ancestors" : "selected_descendants";
        class_name += Math.min(9, i);
        let second_connected_elements = cy.collection();
        cy.$(first_connected_elements).forEach(function (n) {
            let connect_elements = is_ancestor ? n.outgoers() : n.incomers();
            connect_elements = connect_elements.difference(cy.$(connect_elements).filter(".highlight"));
            cy.$(connect_elements).addClass("highlight");
            cy.$(connect_elements).nodes().addClass(class_name);
            second_connected_elements = second_connected_elements.union(connect_elements.nodes());
        });
        first_connected_elements = second_connected_elements;
        if (first_connected_elements.length === 0) {
            break;
        }
    }
}


/**
 * 強調表示されていない(highlightクラスに属していない)ノード、エッジをfadedクラスに入れる。
 * @param {cytoscape object} cy cytoscapeグラフ本体
 * @return
**/
// convert style to fade
function fade_out_faded_elements(cy) {
    let other = cy.elements();
    other = other.difference(cy.elements(".highlight"));
    cy.$(other).addClass("faded");
}
