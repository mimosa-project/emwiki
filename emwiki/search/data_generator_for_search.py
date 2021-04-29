import os

from django.conf import settings
from search.parse_abs import create_abs_dictionary, create_document_vectors, save_byte_index_of_lines
from search.svd import singular_value_analysis


class DataGeneratorForSearch:
    def generate_data_for_search(self):
        try:
            os.mkdir(DATA_FOR_SEARCH_DIR)
        except FileExistError:
            pass
        create_abs_dictionary()
        create_document_vectors()
        save_byte_index_of_lines(os.path.join(
            settings.DATA_FOR_SEARCH_DIR, 'abs_dictionary.txt'), os.path.join(settings.DATA_FOR_SEARCH_DIR, 'tell.pkl'))
        singular_value_analysis(os.path.join(
            settings.DATA_FOR_SEARCH_DIR, 'document_vectors.txt'))
