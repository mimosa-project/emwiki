import re
from contents.article.models import Comment
from collections import deque


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
        self.text = ''

    def read(self, from_dir):
        with open(from_dir, 'r') as f:
            self.text = f.read()

    def write(self, to_dir):
        with open(to_dir, 'w') as f:
            f.write(self.text)

    def _collect_comment_locations(self):
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
        """embed  to MizFile text
        """

        commented_mizar = ""
        mizar_lines = self.text.splitlines()
        comment_locations = self._collect_comment_locations()
        comment_dict = {block: {} for block in self.TARGET_BLOCK}
        for comment in comments:
            comment_dict[comment.block][comment.block_order] = comment
        while len(comment_locations):
            comment_location_dict = comment_locations.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]
            comment = comment_dict[block].get(str(block_order), None)
            if comment is None or comment.text == '':
                continue
            if block == "proof":
                mizar_lines.insert(line_number + 1, comment.format_text())
            else:
                mizar_lines.insert(line_number, comment.format_text())
        commented_mizar = '\n'.join(mizar_lines)
        self.text = commented_mizar

    def extract_comments(self, article):
        """extract comment in mizar string
        """
        print(f"extract {article.name}")
        comments = []
        comment_lines = []
        mizar_lines = self.text.splitlines()
        push_pattern = re.compile(f'(\\s*){Comment.HEADER}(?P<comment>.*)')
        comment_locations = self._collect_comment_locations()
        self.comments = []
        while len(comment_locations):
            comment_location_dict = comment_locations.pop(-1)
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
        self.text = '\n'.join(mizar_lines_without_comment)
        return comments
