import glob
import os
import textwrap
from emwiki.settings import BASE_DIR


class Article():
    TARGET_BLOCK = (
        "theorem",
        "definition",
        "registration",
        "scheme",
        "notation",
        "proof",
    )
    HTML_DIR = "static/mizar_html/"
    MML_DIR = "static/mml/"

    def __init__(self, name):
        self.name = name
        self.html_path = os.path.join(BASE_DIR, self.HTML_DIR, f"{name}.html")
        self.mml_path = os.path.join(BASE_DIR, self.HTML_DIR, f"{name}.miz")

    @classmethod
    def all_names(cls):
        absolute_path_list = glob.glob(os.path.join(BASE_DIR, cls.MML_DIR, f"*.miz"))
        basename_list = [os.path.basename(absolute_path) for absolute_path in absolute_path_list]
        name_tuple = tuple([os.path.splitext(extention_name)[0] for extention_name in basename_list])
        return name_tuple

    @classmethod
    def all(cls):
        Article_tuple = tuple([Article(name) for name in cls.all_names()])
        return Article_tuple

    def exist(self):
        return self.name in self.all_names()

    def miz(self):
        with open(self.mml_path, "r") as f:
            return f.read()

    def find_block(self):
        """find block in  mizar file

        Returns:
            list: comment location list like [{
                                        "block": "theorem",
                                        "block_order": 3,
                                        "line_number": 12(0 origin)
                                    },
                                    {}...
        """
        comment_location_list = []
        # To count the number of times each block appears
        count_dict = dict([[block, 0] for block in list(self.TARGET_BLOCK)])
        # this pattern match like "theorem", "  proof", "theorem :Th1:"
        target_pattern = re.compile(f"([^a-zA-Z_]|^)+(?P<block>{'|'.join(self.TARGET_BLOCK)})([^a-zA-Z_]|$)")
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
        for line_number, line in enumerate(self.miz().splitlines()):
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
                    comment_location_list.append({
                        "block": block,
                        "block_order": count_dict[block],
                        "line_number": line_number
                    })
        return comment_location_list

    def embed(self):
        pass

    def extract(self):
        pass

    def comments(self):
        """convert comments file to dictionary
        
        Returns:
            list: Comment list [Comment, Comment, ...]
        """

        comments = []
        comments_path_list = glob.glob(os.path.join(BASE_DIR, Comment.COMMENT_DIR, self.name, "*"))
        for comment_path in comments_path_list:
            comment_name = os.path.basename(comment_path)
            block, block_order = comment_name.split("_")
            with open(comment_path, "r", encoding="utf-8") as f:
                comments.append(Comment(self.name, block, block_order, f.read()))
        return comments

    def comment(self, block, order):
        comment_path = os.path.join(BASE_DIR, Comment.COMMENT_DIR, self.name, f'{block}_{order}')
        if os.path.exists(comment_path):
            with open(comment_path, "r", encoding="utf-8") as f:
                if f.read() == "":
                    return False
                else:
                    return Comment(self.name, block, order, f.read())
        else:
            return False


class Comment():
    HEADER = "::: "
    LINE_MAX_LENGTH = 75
    COMMENT_DIR = "article/data/comment/"

    def __init__(self, article_name, block, order, text):
        self.article_name = article_name
        self.block = block
        self.order = order
        self.text = text

    def save(self):
        if not os.path.exists(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name)):
            os.mkdir(os.path.exists(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name)))
        if not self.text == "":
            with open(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name, f'{self.block}_{self.order}'), 'w') as f:
                f.write(self.text)

    def format_text(self):
        comment_lines = []
        for line in self.text.splitlines():
            for cut_line in textwrap.wrap(line, self.LINE_MAX_LENGTH):
                comment_lines.append(f'{self.COMMENT_HEADER}{cut_line}')
        return '\n'.join(comment_lines)
