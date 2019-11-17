import re
import os
import glob
from emwiki.settings import BASE_DIR
import textwrap

TARGET_BLOCK = (
    "theorem",
    "definition",
    "registration",
    "scheme",
    "notation",
    "proof",
)
COMMENT_HEADER = "::: "
LINE_MAX_LENGTH = 75


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

    commented_mizar = ''
    # To count the number of times each block appears
    count_dict = dict([[block, 0] for block in list(TARGET_BLOCK)])
    # this pattern match like "theorem", "  proof", "theorem :Th1:"
    target_pattern = re.compile(f"([^a-zA-Z_]|^)+(?P<block>{'|'.join(TARGET_BLOCK)})([^a-zA-Z_]|$)")
    # stack block keyword like ["definition", "proof", "proof"]
    # ["difinition", "proof", "proof"] means "definition proof proof <-here-> end end end"
    block_stack = []
    push_keywords = (
        "definition",
        "registration",
        "notation",
        "scheme",
        "case",
        "suppose",
        "hereby",
        "now",
        "proof",
    )
    push_pattern = re.compile(f"(?:[^a-zA-Z_]|^)(?P<block>{'|'.join(push_keywords)})(?=[^a-zA-Z_]|$)")
    pop_pattern = re.compile(r'(?:[^a-zA-Z_]|^)end(?=[^a-zA-Z_]|$)')
    for line in mizar_string.splitlines():
        commented_mizar += f'{line}\n'
        line = re.sub('::.*', "", line)
        target_match = target_pattern.match(line)
        push_list = push_pattern.findall(line)
        pop_list = pop_pattern.findall(line)
        if len(block_stack) > 0 and block_stack[-1] == "scheme" and re.search("(proof)|;", line):
            block_stack.append("proof")
            target_match = re.match("(?P<block>proof)", "proof")
        elif push_list:
            for block in push_list:
                block_stack.append(block)
        if pop_list:
            if len(block_stack) > 0 and block_stack[-2:-1] == ["scheme", "proof"]:
                block_stack.pop(-1)
            for block in pop_list:
                block_stack.pop(-1)
        if target_match:
            if block_stack.count("proof") == 1 or target_match.group('block') != 'proof':
                block = target_match.group('block')
                count_dict[block] += 1
                if count_dict[block] in comments[block]:
                    commented_mizar += format_comment(comments[block][count_dict[block]])
    return commented_mizar


def format_comment(comment):
    """format comment for adding comment to mizar file
    
    Args:
        comment (string): a comment
    
    Returns:
        string: a comment was formated
    """
    return_comment = ""
    for line in comment.splitlines():
        for cut_line in textwrap.wrap(line, LINE_MAX_LENGTH):
            return_comment += f'{COMMENT_HEADER}{cut_line}\n'
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

    comments = {block: {} for block in TARGET_BLOCK}
    comments_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}/')
    comments_path_list = glob.glob(comments_path + '*')
    for comment_path in comments_path_list:
        comment_name = os.path.basename(comment_path)
        block, comment_number = comment_name.split(("_"))
        with open(comment_path, "r", encoding="utf-8") as f:
            comments[block][int(comment_number)] = f.read()
    return comments
