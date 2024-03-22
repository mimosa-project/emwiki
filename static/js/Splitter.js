/**
 * splitter
 */
export const Splitter = {
  props: {
    drawerWidth: Number,
    drawerExists: Boolean,
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
      // 幅を調整する際に、テキストが選択される動作を防ぐ
      event.preventDefault();
      // 指定した最小幅を下回った場合、drawerを閉じる
      if (event.clientX < this.minDrawerWidth) {
        this.$emit('update:drawerExists', false);
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
      id='splitter' 
      @mousedown='startChangeWidth' 
      @mouseup='endChangeWidth'
    />`,
};
