import {context} from '../../../js/context.js';

/**
 * help for graph
 */
export const HelpDialog = {
  name: 'Helper',
  data: () => ({
    dialog: false,
    helpImageUrlList: [],
  }),
  created() {
    this.helpImageUrlList = [
      `${context['graph_images_path']}/description-emgraph.png`,
      `${context['graph_images_path']}/description-highlight-coloring.png`,
      `${context['graph_images_path']}/description-highlight-param.png`,
    ];
  },
  template: `
    <div>
        <v-dialog
          v-model="dialog"
          width="800"
        >
            <template
              v-slot:activator="{ on, attrs }"
            >
                <v-btn
                  color="red lighten-2"
                  dark
                  v-bind="attrs"
                  v-on="on"
                >
                    Help
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    <span class="text-h5">Usage</span>
                </v-card-title>
                <v-divider></v-divider>
                <v-carousel>
                    <v-carousel-item
                      v-for="helpImageUrl in helpImageUrlList"
                      :key="helpImageUrl"
                    >
                        <v-img
                          :src="helpImageUrl"
                        ></v-img>
                    </v-carousel-item>
                </v-carousel>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="dialog = false"
                    >
                        Close
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>`,
};
