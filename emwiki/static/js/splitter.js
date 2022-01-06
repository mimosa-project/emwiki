/**
 * splitter
 */
export const splitter = {
  props: {
    drawerWidth: Number,
    drawer: Boolean,
  },
  data: () => ({
    minDrawerWidth: 128,
    splitterElement: null,
  }),
  mounted() {
    this.splitterElement = document.getElementById('splitter');
    if (this.splitterElement) {
      this.splitterElement.style.left = `${this.drawerWidth}px`;
    }
  },
  methods: {
    changeWidth(event) {
      // 指定した最小幅を下回った場合、drawerを閉じる
      if (event.clientX < this.minDrawerWidth) {
        this.$emit('update:drawer', false);
        this.endChangeWidth();
      } else {
        this.$emit('update:drawerWidth', event.clientX);
        this.splitterElement.style.left = `${event.clientX}px`;
      }
    },
    startChangeWidth() {
      window.addEventListener('mousemove', this.changeWidth);
    },
    endChangeWidth() {
      window.removeEventListener('mousemove', this.changeWidth);
    },
  },
  template: `
    <div 
      id="splitter" 
      @mousedown="startChangeWidth" 
      @mouseup='endChangeWidth'
    />`,
};
