import re
import os
import glob
from emwiki.settings import BASE_DIR
import textwrap
from collections import deque

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


def push_comment(article_name):
    """push comment to mizar file
    
    Args:
        article_name (string): article name ex."abcmiz_0"
    """
    print(f'push -> {article_name}')
    mizar_path = os.path.join(BASE_DIR, f'static/mml/{article_name}.miz')
    commented_mizar_path = os.path.join(BASE_DIR, f'article/data/commentedMizar/{article_name}.miz')
    commented_mizar = ""
    with open(mizar_path, "r", encoding="utf-8") as f:
        commented_mizar = write_comment(f.read(), fetch_comment(article_name))
    with open(commented_mizar_path, "w", encoding="utf-8") as f:
        f.write(commented_mizar)

def pull_comment(article_name):
    """pull comment from mizar file
    
    Args:
        article_name (string): article name ex."abcmiz_0"
    """
    print(f'pull -> {article_name}')
    mizar_path = os.path.join(BASE_DIR, f'static/mml/{article_name}.miz')
    with open(mizar_path, 'r', encoding="utf-8") as f:
        mizar_string = f.read()
        save_comment(article_name, read_comment(mizar_string))

def read_comment(mizar_string):
    """read comment in mizar string
    
    Args:
        mizar_string (string): string of mizar file
    
    Returns:
        dict: comments dictionary like {
                                            'theorem': {1: "comment text theorem_1", 2: "comment text theorem_2", 3...}
                                            'definition': {1: "", 2: "", 3...}
                                            ...
                                        }
    """ 
    comments = dict([[block, {}] for block in list(TARGET_BLOCK)])
    mizar_lines = mizar_string.splitlines()
    push_pattern = re.compile(f'(\\s*){COMMENT_HEADER}(?P<comment>.*)')
    comment_location_stack = find_block(mizar_string)
    while len(comment_location_stack):
        line_number = comment_location_stack.pop(-1)
        block = comment_location_stack.pop(-1)
        comment_number = comment_location_stack.pop(-1)
        comment_deque = deque()
        start = line_number - 2
        step = -1
        if block == "proof":
            start = line_number
            step = 1
        for line in mizar_lines[start::step]:
            line_match = push_pattern.match(line)
            if line_match:
                if block == "proof":
                    comment_deque.append(line_match.group("comment"))
                else:
                    comment_deque.appendleft(line_match.group("comment"))
            else:
                break
        comment = '\n'.join(comment_deque)
        comments[block][comment_number] = comment
    return comments

def write_comment(mizar_string, comments):
    """write comments to mizar string
    
    Args:
        mizar_string (string): mizar file string
        comments (dictionary): {"TARGET_BLOCK": {1: "comment text", 2, ...}
                                ...
                               }
    
    Returns:
        String: string of mizar file whitten comment
    """
    commented_mizar = ""
    mizar_lines = mizar_string.splitlines()
    comment_location_stack = find_block(mizar_string)
    while len(comment_location_stack):
        line_number = comment_location_stack.pop(-1)
        block = comment_location_stack.pop(-1)
        comment_number = comment_location_stack.pop(-1)
        if comments[block].get(comment_number, "") == "":
            continue
        if block == "proof":
            mizar_lines.insert(line_number, format_comment(comments[block][comment_number]))
        else:
            mizar_lines.insert(line_number - 1, format_comment(comments[block][comment_number]))
    commented_mizar = '\n'.join(mizar_lines)
    return commented_mizar

def find_block(mizar_string):
    """find block in  mizar file
    
    Args:
        mizar_string (string): mizar string ex."abcmiz_0"

    Returns:
        list: comment location stack that is Combinations of <comment_number>, "<block>", and <line_number> are stacked in order from the top
    """
    comment_location_stack = []
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
    for line_number, line in enumerate(mizar_string.splitlines()):
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
                comment_location_stack.append(count_dict[block])
                comment_location_stack.append(block)
                comment_location_stack.append(line_number + 1)
    return comment_location_stack

def save_comment(article_name, comments):
    """save comments
    
    Args:
        article_name (string): article name ex."abcmiz_0"
        comments (dict): {
                            'theorem': {1: "comment text theorem_1", 2: "comment text theorem_2", 3...}
                            'definition': {1: "", 2: "", 3...}
                            ...
                        }
    """
    comments_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}/')
    for block in comments.keys():
        for comment_number, comment in comments[block].items():
            if not os.path.exists(comments_path):
                os.mkdir(comments_path)
            with open(os.path.join(comments_path, f'{block}_{comment_number}'), 'w') as f:
                f.write(comment)

def format_comment(comment):
    """format comment for adding comment to mizar file
    
    Args:
        comment (string): a comment
    
    Returns:
        string: a comment was formated
    """
    return_comment = ""
    comment_stack = []
    for line in comment.splitlines():
        for cut_line in textwrap.wrap(line, LINE_MAX_LENGTH):
            comment_stack.append(f'{COMMENT_HEADER}{cut_line}')
    return_comment = '\n'.join(comment_stack)
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
