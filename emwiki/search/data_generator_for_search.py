import os
from search.parse_abs import create_abs_dictionary, create_document_vectors, save_abs_dictionary_by_byte
from search.svd import singular_value_analysis
from emwiki.settings import DATA_FOR_SEARCH_DIR

class DataGeneratorForSearch:
    def generate_data_for_search(self):
        create_abs_dictionary()
        create_document_vectors()
        save_abs_dictionary_by_byte()
        singular_value_analysis(os.path.join(DATA_FOR_SEARCH_DIR, 'document_vectors.txt'))
