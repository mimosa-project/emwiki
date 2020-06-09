"""Save and load MizFile

Todo:
    * Article,MizFileに依存したくない(Adaptor?要検討)
    * Module感がない
"""


from collections import deque
import re
import os

from contents.contents.scripts.files import MizFile
from contents.article.models import Comment
from emwiki.settings import RAW_MIZFILE_DIR, COMMENTED_MIZFILE_DIR


class MizFileArchiver:
    """Save and load MizFile using Model

    Attributes:
        raw_mizfile_dir(string): The directory where the original MizFile is stored
        commented_mizfile_dir(string): The directory where the commented MizFile is stored
        commentlocationcollector(CommentLocationCollector): Collecting additional comment locations in the text
    """

    def __init__(self):
        self.raw_mizfile_dir = RAW_MIZFILE_DIR
        self.commented_mizfile_dir = COMMENTED_MIZFILE_DIR
        self.commentlocationcollector = CommentLocationCollector()

    def push(self, article):
        """Embed and save Comment in the MizFile indicated by the argument

        Args:
            article(Article): target article
        """
        basename = article.name + '.miz'
        raw_mizfile = MizFile(
            os.path.join(self.raw_mizfile_dir, basename)
        )
        commented_mizfile = MizFile(
            os.path.join(self.commented_mizfile_dir, basename)
        )

        raw_mizfile.read()
        if article.comment_set.all():
            commented_mizfile.text = self._embed(
                raw_mizfile.text, article.comment_set.all()
            )
        else:
            commented_mizfile.text = raw_mizfile.text
        commented_mizfile.write()

    def pull(self, article):
        """Extract and load Comment in the MizFile indicated by the argument

        Args:
            article(Article): target article
        Returns:
            comments(list of Comment): Extracted comments
        """
        comments = []
        basename = article.name + '.miz'
        commented_mizfile_path = os.path.join(self.commented_mizfile_dir, basename)
        if os.path.exists(commented_mizfile_path):
            commented_mizfile = MizFile(commented_mizfile_path)
            commented_mizfile.read()
            raw_text, comments = self._extract(commented_mizfile.text, article)
        return comments

    def _embed(self, raw_text, comments):
        """embed comments in raw_text

        Args:
            raw_text(string): raw text of mizfile
            comments(list of Comments): Embedded Comments
        Returns:
            commented_text(string): commented text
        """
        mizar_lines = raw_text.splitlines()
        self.commentlocationcollector.collect(raw_text)
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
        commented_text = '\n'.join(mizar_lines)
        return commented_text

    def _extract(self, text, article):
        """extract comment in commented_text

        Args:
            text(string): commented text of mizfile
            article(string): article key of the extracted comments
        Returns:
            raw_text(string): raw text of mizfile
            comments(list of comments): extracted comments
        """
        comments = []
        comment_lines = []
        mizar_lines = text.splitlines()
        push_pattern = re.compile(f'(\\s*){Comment.HEADER}(?P<comment>.*)')
        self.commentlocationcollector.collect(text)
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
                        article=article,
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
        raw_text = '\n'.join(mizar_lines_without_comment)
        return raw_text, comments


class CommentLocationCollector:
    """Collecting additional comment locations
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

    def collect(self, text):
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
        for line_number, line in enumerate(text.splitlines()):
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
