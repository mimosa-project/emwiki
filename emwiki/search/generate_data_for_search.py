import parse_abs
import svd

parse_abs.create_abs_dictionary()
parse_abs.create_document_vectors()
parse_abs.save_abs_dictionary_by_byte()
svd.singular_value_analysis("search/data/document_vectors.txt")
