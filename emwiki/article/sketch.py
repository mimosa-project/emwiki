import re
import os
import glob
from emwiki.settings import BASE_DIR

TARGET_BLOCK = (
    "theorem",
    "definition",
    "registration",
    "scheme",
    "notation",
    "proof",
)

makeSketchedMizar_file("abcmiz_0")

def makeSketchedMizar_file(article_name):
    mizar_path = os.path.join(BASE_DIR, f'static/mml/{article_name}.miz')
    sketchedMizar_path = os.path.join(BASE_DIR, f'article/data/sketchedMizar/{article_name}.miz')
    sketchedMizar = ""
    with open(mizar_path, "r") as f:
        sketchedMizar = makeSketchedMizar_string(f.read(), sketch_dict(article_name))
    with open(sketchedMizar_path, "w") as f:
        f.write(sketchedMizar)



def makeSketchedMizar_string(miz_string, sketches):
    """make mizar string written sketches

    make mizar string written sketches

    Args:
        miz_string: .miz file's all string
        sketches: sketches dict like 
        {
            'theorem': {1: "sketch_text", 2: "sketch_text", 3...},
            'definition': {1: "sketch_text", 2: "sketch_text", 3...},
            ...
        }

    Returns:
        mizar string written sketch

    Raises:
        
    """
    miz_string_written_sketch = ''
    miz_lines = miz_string.splitlines()
    count_dict = dict([[initial,0] for initial in list(TARGET_INITIALs)])


    for line in miz_lines:
        for initial in TARGET_INITIALs:
            if re.match(initial, line):
                count_dict[initial] += 1
                sketch_name = f'{initial}_{count_dict[initial]}'
                if sketch_name in sketches:
                    miz_string_written_sketch += formalizeSketch(sketches[initial][count_dict[initial]])
        miz_string_written_sketch += line

    return miz_string_written_sketch

def formalizeSketch(sketch):
    return_sketch = ""
    sketch_lines = sketch.splitlines()
    for line in sketch_lines:
        return_sketch += f':::{line}\n'
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
