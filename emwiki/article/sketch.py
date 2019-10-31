import re
import os
import glob
import math
from emwiki.settings import BASE_DIR

TARGET_BLOCK = (
    "theorem",
    "definition",
    "registration",
    "scheme",
    "notation",
    "proof",
)
MAX_LENGTH = 75


def make_sketchedmizar_file(article_name):
    mizar_path = os.path.join(BASE_DIR, f'static/mml/{article_name}.miz')
    sketched_mizar_path = os.path.join(BASE_DIR, f'article/data/sketchedMizar/{article_name}.miz')
    sketched_mizar = ""
    with open(mizar_path, "r", encoding="utf-8") as f:
        sketched_mizar = make_sketchedmizar_string(f.read(), fetch_sketch(article_name))
    with open(sketched_mizar_path, "w", encoding="utf-8") as f:
        f.write(sketched_mizar)


def make_sketchedmizar_string(miz_string, sketches):
    """make mizar string written sketches
    
    Args:
        miz_string (string): mizar file string
        sketches (dictionary): {"TARGET_BLOCK": {1: "sketch text", 2, ...}
                                ...
                               }
    
    Returns:
        String: mizar file string whitten sketch
    """
    miz_string_written_sketch = ''
    miz_lines = miz_string.splitlines()
    count_dict = dict([[block, 0] for block in list(TARGET_BLOCK)])
    target_pattern = r"(?P<block>"
    target_pattern += f"{TARGET_BLOCK[0]}"
    for block in TARGET_BLOCK[1:]:
        target_pattern += f'|{block}'
    target_pattern += r')(\s|\r|\n\r|\n|$)'
    print(target_pattern)
    for line in miz_lines:
        target_match = re.match(target_pattern, line)
        if target_match:
            block = target_match.group('block')
            count_dict[block] += 1
            if count_dict[block] in sketches[block]:
                miz_string_written_sketch += format_sketch(sketches[block][count_dict[block]])
        miz_string_written_sketch += f'{line}\n'
    return miz_string_written_sketch


def format_sketch(sketch):
    def _split_line(line):
        """Split to less than MAX_LENGTH characters per line
        
        Args:
            line (string): raw to validate
        """
        lines = []
        for i in range(0, math.ceil(len(line) / MAX_LENGTH)):
            lines.append(line[MAX_LENGTH * i: MAX_LENGTH * (i + 1)])
        return lines

    return_sketch = ""
    sketch_lines = sketch.splitlines()
    for line in sketch_lines:
        for new_line in _split_line(line):
            return_sketch += f'::: {new_line}\n'
    return return_sketch


def fetch_sketch(article_name):
    """return sketches dictionary
    
    Args:
        article_name (String): miz file name like "abcmiz_0"
    
    Returns:
        dictionary: {'theorem': {1: "sketch text theorem_1", 2: "sketch text theorem_2", 3...}
                     'definition': {1: "", 2: "", 3...}
                     ...
                    }
    """

    return_dict = {}
    sketches_path = os.path.join(BASE_DIR, f'article/data/sketch/{article_name}/')
    sketches_path_list = glob.glob(sketches_path + '*')

    for initial in TARGET_BLOCK:
        return_dict[initial] = {}

    for sketch_path in sketches_path_list:
        sketch_name = sketch_path.rsplit("/", 1)[1]
        content = sketch_name.split("_")[0]
        content_number = int(sketch_name.split("_")[1])
        with open(sketch_path, "r", encoding="utf-8") as f:
            return_dict[content][content_number] = f.read()
    return return_dict
