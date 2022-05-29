/* eslint-disable max-len */
export const CopyUrlButton = {
  props: {
    url: String,
  },
  data: () => ({
    copying: false,
  }),
  methods: {
    async copyUrl(url) {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        this.copying = true;
        setTimeout(() => {
          this.copying = false;
        }, 2000);
      }
    },
  },
  template: `
    <v-btn class="px-0 d-block" v-on:click="copyUrl(url)" height="1.2rem">
      <p v-if="copying">Copied</p>
      <svg v-else style="width:1rem; height:1rem" viewBox="0 0 24 24">
        <path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" />
      </svg>
    </v-btn>
  `,
};
