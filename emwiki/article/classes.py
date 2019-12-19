import glob
import os
import re
import textwrap
from emwiki.settings import BASE_DIR


class ArticleHandler():
    HTML_DIR = "static/mizar_html/"
    MML_DIR = "static/mml/"
    MML_COMMENTED_DIR = "article/data/commentedMizar/"
    COMMENT_DIR = "article/data/comment/"

    def __init__(self, article_name):
        self.article_name = article_name

    @classmethod
    def bundle_create(cls):
        """create ArticleHandler bandle
        
        Returns:
            List: List of all ArticleHandler
        """
        article_handler_list = []
        mizfile_list = cls.mizfile_bundle_create()
        for mizfile in mizfile_list:
            article_handler = ArticleHandler(mizfile.name)
            article_handler_list.append(article_handler)
        return article_handler_list

    @classmethod
    def mizfile_bundle_create(cls):
        """return List of all MizFile
        
        Returns:
            List: [MizFile, MizFile, ...]
        """
        MizFile_list = []
        mizfile_path_list = glob.glob(os.path.join(BASE_DIR, cls.MML_DIR, "*"))
        for path in mizfile_path_list:
            mizfile = MizFile()
            mizfile.load(path)
            MizFile_list.append(mizfile)
        return MizFile_list

    def comment_bundle_create(self):
        """return List of comment bundle
        
        Returns:
            List: [Comment, Comment, Comment,...]
        """
        comment_list = []
        comment_path_list = glob.glob(os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name, "*"))
        mizfile = MizFile().load(os.path.join(BASE_DIR, self.MML_DIR, f'{self.article_name}.miz'))
        for path in comment_path_list:
            comment = Comment(mizfile)
            comment.load(path)
            comment_list.append(comment)
        return comment_list

    def store_comment(self, block, block_order, text):
        """store comment to COMMENT_DIR
        
        Args:
            block (string): block name
            block_order (number): number of block order
            text (string): content text of Comment
        """
        mizfile_path = os.path.join(BASE_DIR, self.MML_DIR, f'{self.article_name}.miz')
        mizfile = MizFile()
        mizfile.load(mizfile_path)
        comment = Comment(mizfile)
        comment.block = block
        comment.block_order = block_order
        comment.text = text
        comment_file_name = f'{block}_{block_order}'
        comment_path = os.path.join(BASE_DIR, self.COMMENT_DIR, comment.mizfile.name, comment_file_name)
        comment.save(comment_path)

    def embed_comment_to_mml(self):
        """embed comment to MML and save
        """
        mizfile = MizFile()
        mizfile_name = f'{self.article_name}.miz'
        mizfile_load_path = os.path.join(BASE_DIR, self.MML_DIR, mizfile_name)
        mizfile_save_path = os.path.join(BASE_DIR, self.MML_COMMENTED_DIR, mizfile_name)
        mizfile.load(mizfile_load_path)
        comments = self.comment_bundle_create()
        mizfile.embed_comments(comments)
        mizfile.save(mizfile_save_path)

    def get_comment_dict(self):
        """get comment dictionary
        
        Returns:
            dictionary: {
                "<block>": {
                    "<block_order>": "<text>",
                    "<block_order>": "<text>",
                    ...
                }
                ...
            }
        """
        comments_dir = os.path.join(BASE_DIR, self.COMMENT_DIR, self.article_name)
        comment_path_list = glob.glob(os.path.join(comments_dir, "*"))
        mizfile_path = os.path.join(BASE_DIR, self.MML_DIR, f'{self.article_name}.miz')
        mizfile = MizFile()
        mizfile.load(mizfile_path)
        comment_list = [Comment(mizfile).load(path) for path in comment_path_list]
        return_dict = {block: {} for block in MizFile.TARGET_BLOCK}
        for comment in comment_list:
            return_dict[comment.block][comment.block_order] = comment.text
        return return_dict


class MizFile():
    TARGET_BLOCK = (
        "theorem",
        "definition",
        "registration",
        "scheme",
        "notation",
        "proof",
    )

    def __init__(self):
        self.name = ""
        self.text = ""

    def load(self, path):
        """load Mizar File from path
        
        Args:
            path (path): Mizar file exist
        
        Returns:
            MizFile: self
        """
        self.name = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r") as f:
            self.text = f.read()
        return self

    def save(self, path):
        """save Mizar File to path
        
        Args:
            path (path): save self.text to path
        """
        with open(path, "w") as f:
            f.write(self.text)

    def collect_comment_locations(self):
        """collect comment locations

        Returns:
            list: comment location list like [{
                                        "block": "theorem",
                                        "block_order": 3,
                                        "line_number": 12(0 origin)
                                    },
                                    ...
        """
        comment_locations = []
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
        for line_number, line in enumerate(self.text.splitlines()):
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
                    comment_locations.append({
                        "block": block,
                        "block_order": count_dict[block],
                        "line_number": line_number
                    })
        return comment_locations

    def embed_comments(self, comments):
        """embed comments to MizFile text
        
        Args:
            comments (List of Comment): List of Comment which embed
        """

        if not comments:
            print(f"skipped {self.name} becasue comment not exist")
            return
        print(f"embeded {len(comments)} comments to {self.name}")
        commented_mizar = ""
        mizar_lines = self.text.splitlines()
        comment_location_list = self.collect_comment_locations()
        comment_dict = {block: {} for block in self.TARGET_BLOCK}
        for comment in comments:
            comment_dict[comment.block][comment.block_order] = comment
        while len(comment_location_list):
            comment_location_dict = comment_location_list.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]
            comment = comment_dict[block].get(str(block_order), Comment(self))
            if comment.text == "":
                continue
            if block == "proof":
                mizar_lines.insert(line_number + 1, comment.format_text())
            else:
                mizar_lines.insert(line_number, comment.format_text())
        commented_mizar = '\n'.join(mizar_lines)
        self.text = commented_mizar


class Comment():
    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def __init__(self, mizfile):
        self.mizfile = mizfile
        self.block = ""
        self.block_order = 0
        self.text = ""

    def load(self, path):
        """load comment from path
        
        Args:
            path (path): path where comment exist
        """
        basename = os.path.basename(path)
        self.article_name = os.path.splitext(basename)[0]
        self.block, self.block_order = basename.split("_")
        with open(path, "r") as f:
            self.text = f.read()
        return self

    def save(self, path):
        """save comment to path

        Args:
            path (path): path where save comment
        """
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        with open(path, 'w') as f:
            f.write(self.text)

    def format_text(self):
        """format comment text
        
        Returns:
            string: format comment text
        """
        comment_lines = []
        for line in self.text.splitlines():
            for cut_line in textwrap.wrap(line, self.LINE_MAX_LENGTH):
                comment_lines.append(f'{self.HEADER}{cut_line}')
        return '\n'.join(comment_lines)
