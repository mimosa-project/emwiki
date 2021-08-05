import os
import shutil
import urllib.parse
from symbol.models import Symbol
from symbol.symbol_maker.processor import Processor

from django.conf import settings


class SymbolComponentsBuilder:
    from_dir = Symbol.get_htmlfile_dir()
    # あとでsettingsから呼び出すように変更
    PRODUCT_SYMBOL_COMPONENTS_DIR = os.path.join(
        settings.BASE_DIR, 'symbol', 'static', 'symbol', 'components')
    to_dir = PRODUCT_SYMBOL_COMPONENTS_DIR

    def delete_files(self):
        if os.path.exists(self.to_dir):
            shutil.rmtree(self.to_dir)
        os.mkdir(self.to_dir)

    def create_files(self):
        print('Building Components Files')
        print(f'    from {self.from_dir}')
        print(f'    to   {self.to_dir}')
        files = os.listdir(self.from_dir)
        route = "const routes = [\n"
        for file in files:
            # htmlファイルを元にcomponentsファイルを作成
            with open(os.path.join(self.from_dir, file), encoding='utf-8') as html_file:
                html_context = html_file.read()
                # コンポーネントが記述されるファイルの名前: "0.js" "1.js" ...
                output_file = file.replace(".html", ".js")
                file_num = file.replace(".html", "")
                with open(os.path.join(self.to_dir, output_file), mode='w', encoding='utf-8') as component_file:
                    # コンポーネントの名前: "component_0" "component_1" ...

                    # component_file.write("<template>\n")
                    # component_file.write(html_context)
                    # component_file.write("</template>\n<script>module.exports = {}</script>")

                    component_file.write("const component_" + file_num + "= { template: `")
                    component_file.write(html_context)
                    component_file.write("` }")


            # routeを作成(例: {path: '/symbol/FixPoints', components: component-4557},)
            # urlエンコード(ピリオドはデフォルトでエンコードされないため手動)
            # symbol_name = Symbol.objects.get(filename=file).name
            # symbol_name_quote = urllib.parse.quote(symbol_name)
            # symbol_name_quote = symbol_name_quote.replace(".", "%2E")
            # route += ("{path: \'/symbol/" + symbol_name_quote + "\', component: httpVueLoader('/static/symbol/components_vue/" + file.replace(".html", ".vue") + "')},\n")


            

            # # routeを作成(例: {path: '/symbol/FixPoints', components: component-4557},)
            # # urlエンコード(ピリオドはデフォルトでエンコードされないため手動)
            # symbol_name = Symbol.objects.get(filename=file).name
            # symbol_name_quote = urllib.parse.quote(symbol_name)
            # symbol_name_quote = symbol_name_quote.replace(".", "%2E")
            # route += ("{path: \'/symbol/" + symbol_name_quote + "\', components: component_" + file_num + "},\n")
        
        # routeを書き込み
        # with open(os.path.join(settings.BASE_DIR, "symbol", "static", "symbol", "JavaScript", "route-2.js"), mode='w', encoding='utf-8') as f:
        #     f.write(route + "]")

        #     def write(self, path):
        # with codecs.open(path, 'w', 'utf-8-sig') as fp:
        #     fp.write("{% verbatim %}<!DOCTYPE html>\n"
        #              "<html lang='en'>\n")
        #     self.write_header(fp)
        #     self.write_body(fp)
        #     fp.write("</html>{% endverbatim %}\n")
        # processor = Processor()
        # processor.execute(self.from_dir, self.to_dir)
