from collections import deque
import re
import os

from contents.article.models import Comment


class MizFile():
    """.mizファイル

    入出力を担当
    """

    def __init__(self):
        self.text = ''

    def read(self, from_dir):
        with open(from_dir, 'r') as f:
            self.text = f.read()

    def write(self, to_dir):
        with open(to_dir, 'w') as f:
            f.write(self.text)


class CommentLocationCollector:
    """テキスト内のComment追加位置を収集
    """
    TARGET_BLOCK = (
        "theorem",
        "definition",
        "registration",
        "scheme",
        "notation",
        "proof",
    )
    
    def __init__(self):
        self.locations = []

    def collect(self, mizfile):
        """collect comment locations

        Returns:
            list: comment location list like [{
                                        "block": "theorem",
                                        "block_order": 3,
                                        "line_number": 12(0 origin)
                                    },
                                    ...
        """
        # To count the number of times each block appears
        count_dict = dict([[block, 0] for block in list(self.TARGET_BLOCK)])
        # this pattern match like "theorem", "  proof", "theorem :Th1:"
        target_pattern = re.compile(
            f"([^a-zA-Z_]|^)+(?P<block>{'|'.join(self.TARGET_BLOCK)})([^a-zA-Z_]|$)"
        )
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
        for line_number, line in enumerate(mizfile.text.splitlines()):
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
                    self.locations.append({
                        "block": block,
                        "block_order": count_dict[block],
                        "line_number": line_number
                    })


class ArticleArchiver:
    """Articleの保管，読み込みを担当
    """

    def __init__(self, article):
        self.article = article
        self.mizfile = MizFile()
        self.commentlocationcollector = CommentLocationCollector()

    def archive(self):
        """コメントを埋め込み保存
        """
        self.mizfile.read(self.article.get_original_path())
        self._embed(self.article.objects.comment_set.all())
        self.mizfile.write(self.article.get_commented_path())

    def extract(self):
        """コメントを取り出す
        """
        comments = []
        if os.path.exists(self.article.get_commented_path()):
            self.mizfile.read(self.article.get_commented_path())
            comments = self._excavate()
        return comments

    def _embed(self, comments):
        """embed to MizFile text
        """
        commented_mizar = ""
        mizar_lines = self.mizfile.text.splitlines()
        self.commentlocationcollector.collect(self.mizfile)
        comment_dict = {block: {} for block in self.TARGET_BLOCK}
        for comment in comments:
            comment_dict[comment.block][comment.block_order] = comment
        while len(self.commentlocationcollector.locations):
            comment_location_dict = self.commentlocationcollector.locations.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]
            comment = comment_dict[block].get(block_order, None)
            if comment is None or comment.text == '':
                continue
            if block == "proof":
                mizar_lines.insert(line_number + 1, comment.format_text())
            else:
                mizar_lines.insert(line_number, comment.format_text())
        commented_mizar = '\n'.join(mizar_lines)
        self.mizfile.text = commented_mizar

    def _excavate(self):
        """extract comment in mizar string
        """
        comments = []
        comment_lines = []
        mizar_lines = self.mizfile.text.splitlines()
        push_pattern = re.compile(f'(\\s*){Comment.HEADER}(?P<comment>.*)')
        self.commentlocationcollector.collect(self.mizfile)
        while len(self.commentlocationcollector.locations):
            comment_location_dict = self.commentlocationcollector.locations.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]
            comment_deque = deque()
            # Except for "proof", the comment is written before block,
            # but in "proof", the comment is written after block
            start = line_number - 1
            step = -1
            if block == "proof":
                start = line_number + 1
                step = 1

            # Check each line matches push_pattern
            for index, line in enumerate(mizar_lines[start::step]):
                line_match = push_pattern.match(line)
                if line_match:
                    if block == "proof":
                        comment_deque.append(line_match.group("comment"))
                    else:
                        comment_deque.appendleft(line_match.group("comment"))
                    comment = Comment(
                        article=self.article,
                        block=block,
                        block_order=block_order,
                        text='\n'.join(comment_deque)
                    )
                    comments.append(comment)
                    comment_lines.append(start + step * index)
                else:
                    break
        mizar_lines_without_comment = \
            [mizar_lines[i] for i in range(len(mizar_lines)) if i not in comment_lines]
        self.mizfile.text = '\n'.join(mizar_lines_without_comment)
        return comments
