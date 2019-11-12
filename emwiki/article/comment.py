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


def make_commented_mizar(article_name):
    """make commented mizar file
    
    Args:
        article_name (string): article name ex."abcmiz_0"
    """
    print(article_name)
    mizar_path = os.path.join(BASE_DIR, f'static/mml/{article_name}.miz')
    commented_mizar_path = os.path.join(BASE_DIR, f'article/data/commentedMizar/{article_name}.miz')
    commented_mizar = ""
    with open(mizar_path, "r", encoding="utf-8") as f:
        commented_mizar = add_comment(f.read(), fetch_comment(article_name))
    with open(commented_mizar_path, "w", encoding="utf-8") as f:
        f.write(commented_mizar)


def add_comment(mizar_string, comments):
    """make mizar string written comments
    
    Args:
        mizar_string (string): mizar file string
        comments (dictionary): {"TARGET_BLOCK": {1: "comment text", 2, ...}
                                ...
                               }
    
    Returns:
        String: string of mizar file whitten comment
    """
    miz_string_written_comment = ''
    miz_lines = miz_string.splitlines()
    count_dict = dict([[block, 0] for block in list(TARGET_BLOCK)])
    target_pattern = r"(?P<block>"
    target_pattern += f"{TARGET_BLOCK[0]}"
    for block in TARGET_BLOCK[1:]:
        target_pattern += f'|{block}'
    target_pattern += r')(\s|\r|\n\r|\n|$)'
    for line in miz_lines:
        target_match = re.match(target_pattern, line)
        if target_match:
            block = target_match.group('block')
            count_dict[block] += 1
            if count_dict[block] in commentes[block]:
                miz_string_written_comment += format_comment(commentes[block][count_dict[block]])
        miz_string_written_comment += f'{line}\n'
    return miz_string_written_comment


def format_comment(comment):
    """format comment for adding comment to mizar file
        
        Args:
        comment (string): a comment
    
    Returns:
        string: a comment was formated
        """
        lines = []
        for i in range(0, math.ceil(len(line) / MAX_LENGTH)):
            lines.append(line[MAX_LENGTH * i: MAX_LENGTH * (i + 1)])
        return lines

    return_comment = ""
    comment_lines = comment.splitlines()
    for line in comment_lines:
        for new_line in _split_line(line):
            return_comment += f'::: {new_line}\n'
    return return_comment


def fetch_comment(article_name):
    """return comments dictionary
    
    Args:
        article_name (String): miz file name like "abcmiz_0"
    
    Returns:
        dictionary: {'theorem': {1: "comment text theorem_1", 2: "comment text theorem_2", 3...}
                     'definition': {1: "", 2: "", 3...}
                     ...
                    }
    """

    return_dict = {}
    commentes_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}/')
    commentes_path_list = glob.glob(commentes_path + '*')

    for initial in TARGET_BLOCK:
        return_dict[initial] = {}

    for comment_path in commentes_path_list:
        comment_name = comment_path.rsplit("/", 1)[1]
        content = comment_name.split("_")[0]
        content_number = int(comment_name.split("_")[1])
        with open(comment_path, "r", encoding="utf-8") as f:
            return_dict[content][content_number] = f.read()
    return return_dict
