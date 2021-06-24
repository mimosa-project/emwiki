import os

from django.conf import settings
from search.parse_abs import create_abs_dictionary, create_document_vectors, save_byte_index_of_lines
from search.svd import singular_value_analysis


class DataGeneratorForSearch:
    def generate_data_for_search(self):
        os.makedirs(settings.index_dir, exist_ok=True)
        create_abs_dictionary()
        create_document_vectors()
        save_byte_index_of_lines(os.path.join(
            settings.index_dir, 'abs_dictionary.txt'), os.path.join(settings.index_dir, 'tell.pkl'))
        singular_value_analysis(os.path.join(
            settings.index_dir, 'document_vectors.txt'))
