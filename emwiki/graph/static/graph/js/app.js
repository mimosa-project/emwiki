new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {'graph-drawer': GraphDrawer},
  data: () => ({
    drawer: true,
    drawerWidth: 256,
    headers: [{text: 'name', value: 'name'}],
    searchText: '',
    graphModel: null,
    articleName: null,
    upperLevel: 0,
    lowerLevel: 0,
    selectors: [
      'highlight',
      'faded',
      'selected',
      'ancestor',
      'ancestor0',
      'ancestor1',
      'ancestor2',
      'ancestor3',
      'ancestor4',
      'ancestor5',
      'ancestor6',
      'ancestor7',
      'ancestor8',
      'ancestor9',
      'descendant',
      'descendant0',
      'descendant1',
      'descendant2',
      'descendant3',
      'descendant4',
      'descendant5',
      'descendant6',
      'descendant7',
      'descendant8',
      'descendant9',
    ],
  }),
  delimiters: ['$(', ')'],
  watch: {
    articleName(newVal) {
      this.resetElements();
      if (newVal) {
        this.highlightElements(newVal, this.upperLevel, this.lowerLevel);
      }
    },
    upperLevel(newVal) {
      this.resetElements();
      if (this.articleName) {
        this.highlightElements(this.articleName, newVal, this.lowerLevel);
      }
    },
    lowerLevel(newVal) {
      this.resetElements();
      if (this.articleName) {
        this.highlightElements(this.articleName, this.upperLevel, newVal);
      }
    },
  },
  mounted() {
    GraphService.getModel(context['dot_graph_uri']).then((graphModel) => {
      this.graphModel = graphModel;
      this.createGraph(graphModel).then((cyto) => {
        window.cy = cyto;
        if (this.articleName) {
          this.highlightElements(
              this.articleName,
              this.upperLevel,
              this.lowerLevel);
        }
      });
    });
  },
  methods: {
    createGraph(graphModel) {
      return new Promise((resolve) => {
        const cyto = cytoscape({
          container: document.getElementById('graph'),
          elements: [],
          boxSelectionEnabled: true,
          autounselectify: false,
          selectionType: 'additive',
          wheelSensitivity: 0.1,
        });
        cyto.add(graphModel.eleObjs);
        cyto.style(GraphService.getCytoscapeStyle());
        cyto.fit(cyto.nodes().orphans());
        cyto.nodes().on('tap', (event) => {
          this.clickElement(event.target.data('name'));
        });
        cyto.contextMenus({
          evtType: ['cxttap'],
          menuItems: [
            {
              id: 'select',
              content: 'select',
              tooltipText: 'select',
              selector: 'node',
              onClickFunction: (event) => {
                this.clickElement(event.target.data('name'));
              },
              hasTrailingDivider: true,
            },
            {
              id: 'open',
              content: 'open',
              tooltipText: 'open',
              selector: 'node',
              hasTrailingDivider: true,
              onClickFunction: (event) => {
                window.open(
                    context.article_base_uri +
                      event.target.data('name').toLowerCase(),
                    '_blank');
              },
            },
          ],
        }),
        resolve(cyto);
      });
    },
    resetElements() {
      window.cy.elements().removeClass(this.selectors);
      window.cy.nodes().unlock();
    },
    highlightElements(articleName, upperLevel, lowerLevel) {
      const element = cy.nodes().filter((element) => {
        return element.data('name') === articleName.toUpperCase();
      })[0];
      element.addClass('highlight');
      element.addClass('selected');
      let currentElements = cy.collection().union(element);
      for (let i = 0; i < upperLevel; i++) {
        const connectedElements = [];
        currentElements.find((element) => {
          element.outgoers().difference().find((element) => {
            element.addClass('highlight');
            element.addClass(`ancestor${Math.min(9, i)}`);
            connectedElements.push(element);
          });
        });
        currentElements = connectedElements;
      }
      currentElements = cy.collection().union(element);
      for (let i = 0; i < lowerLevel; i++) {
        const connectedElements = [];
        currentElements.find((element) => {
          element.incomers().difference().find((element) => {
            element.addClass('highlight');
            element.addClass(`descendant${Math.min(9, i)}`);
            connectedElements.push(element);
          });
        });
        currentElements = connectedElements;
      }
      this.fadeElements(cy.elements().difference(cy.elements('.highlight')));
    },
    setArticleModel(articleName) {
      const element = cy.nodes().filter((element) => {
        return element.data('name') === articleName.toUpperCase();
      })[0];
      element.addClass('highlight');
      element.addClass('selected');
    },
    fadeElements(elements) {
      elements.addClass('faded');
      elements.lock();
    },
    clickElement(articleName) {
      this.articleName = articleName;
      this.resetElements();
      this.highlightElements(articleName, this.upperLevel, this.lowerLevel);
      this.$emit('article-model-changed', {name: articleName});
    },
    reset() {
      this.articleName = '';
      this.upperLevel = 0;
      this.lowerLevel = 0;
      this.createGraph(this.graphModel).then((cyto) => {
        window.cy = cyto;
      });
    },
    changeArticleName(name) {
      this.articleName = name;
    },
    changeUpperLevel(upperLevel) {
      this.upperLevel = upperLevel;
    },
    changeLowerLevel(lowerLevel) {
      this.lowerLevel = lowerLevel;
    },
  },
});
