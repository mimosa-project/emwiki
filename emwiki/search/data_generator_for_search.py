import os
import glob

from django.conf import settings
from search.parse_abs import create_abs_dictionary_and_document_vectors, save_byte_index_of_lines
from search.svd import singular_value_analysis


class DataGeneratorForSearch:
    def generate_data_for_search(self):
        existing_files = glob.glob(os.path.join(settings.SEARCH_INDEX_DIR, '*'))
        for file in existing_files:
            if file.endswith('.tar.bz2'):
                pass
            else:
                os.remove(file)
        create_abs_dictionary_and_document_vectors(settings.SEARCH_INDEX_DIR)
        save_byte_index_of_lines(os.path.join(
            settings.SEARCH_INDEX_DIR, 'abs_dictionary.txt'), os.path.join(settings.SEARCH_INDEX_DIR, 'tell.pkl'))
        singular_value_analysis(os.path.join(
            settings.SEARCH_INDEX_DIR, 'document_vectors.txt'))
