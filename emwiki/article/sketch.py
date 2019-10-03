import re

TARGET_INITIALs = (
    "theorem",
    "definition",
    "registration",
    "scheme",
    "notation",
    "proof",
)

def makeMizarSketched(miz_string, sketches):
    """make mizar string written sketches

    make mizar string written sketches

    Args:
        miz_string: .miz file's all string
        sketches: sketches dict like {theorem_1: "sketch", ...}

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
                    miz_string_written_sketch += formalizeSketch(sketches[sketch_name])
        miz_string_written_sketch += line

    return miz_string_written_sketch

def formalizeSketch(sketch):
    return_sketch = ""
    sketch_lines = sketch.splitlines()
    for line in sketch_lines:
        return_sketch += f':::{line}\n'
    return return_sketch
