from collections import deque
import re


class MizTextConverter:
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
    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def remove_comments(self, text):
        """remove comment in commented_text

        Args:
            text(string): commented text of mizfile
        Returns:
            raw_text(string): raw text of mizfile
        """
        comment_lines = []
        mizar_lines = text.split('\n')
        push_pattern = re.compile(f'(\\s*){self.HEADER}(?P<comment>.*)')
        locations = self.collect_locations(text)
        while len(locations):
            comment_location_dict = locations.pop(-1)
            block = comment_location_dict["block"]
            line_number = comment_location_dict["line_number"]
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
                    comment_lines.append(start + (step * index))
                else:
                    break
        mizar_lines_without_comment = \
            [
                mizar_lines[i]
                for i in range(len(mizar_lines)) if i not in comment_lines
            ]
        raw_text = '\n'.join(mizar_lines_without_comment)
        return raw_text

    def embed_comments(self, text, comments):
        """embed comments in text

        Args:
            text(string): raw text of mizfile
            comments(list of comments dict): like [
                {'block': 'theorem', 'block_order': 1, 'text': 'sample'},
                ...
            ]
        Returns:
            commented_text(string): commented text
        """
        mizar_lines = text.split('\n')
        locations = self.collect_locations(text)
        while len(locations):
            comment_location_dict = locations.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]
            comment_text_candidates = [
                comment['text']
                for comment in comments
                if comment['block'] == block
                and comment['block_order'] == block_order
            ]
            comment_text = comment_text_candidates[0] if comment_text_candidates else None
            if comment_text is None or comment_text == '':
                continue
            else:
                insert_text = self.add_comment_header(comment_text)
                self.verify_comment_text(insert_text)
            if block == "proof":
                insert_line_number = line_number + 1
            else:
                insert_line_number = line_number
            mizar_lines.insert(insert_line_number, insert_text)
        commented_text = '\n'.join(mizar_lines)
        return commented_text

    def extract_comments(self, text):
        """extract comments in commented_text

        Args:
            text(string): commented text of mizfile
        Returns:
            comments(list of comments dict): extracted comments like
                [
                    {'text': 'sample text', 'block': 'theorem', 'block_order': 1},
                    ...
                ]
        """

        mizar_lines = text.split('\n')
        locations = self.collect_locations(text)
        comments = list()
        while len(locations):
            comment_location_dict = locations.pop(-1)
            block = comment_location_dict["block"]
            block_order = comment_location_dict["block_order"]
            line_number = comment_location_dict["line_number"]

            # Except for "proof", the comment is written before block,
            # but in "proof",     the comment is written after block
            if block == "proof":
                start = line_number + 1
                step = 1
            else:
                start = line_number - 1
                step = -1

            # Add comment_one_line_text to comment_deque if match push_pattern
            # Then, add comment made by comment_deque to comments
            comment_deque = deque()
            push_pattern = re.compile(f'(\\s*){self.HEADER}(?P<comment>.*)')
            for index, line in enumerate(mizar_lines[start::step]):
                line_match = push_pattern.match(line)
                if line_match:
                    comment_one_line_text = line_match.group('comment')
                    if block == "proof":
                        comment_deque.append(comment_one_line_text)
                    else:
                        comment_deque.appendleft(comment_one_line_text)
                else:
                    comment = {
                        'block': block,
                        'block_order': block_order,
                        'text': '\n'.join(comment_deque)
                    }
                    comments.append(comment)
                    break
        return comments

    def collect_locations(self, text):
        """collect comment locations

        Args:
            text(string): .miz file text
        Returns:
            locations(list): comment location list like [{
                                        "block": "theorem",
                                        "block_order": 3,
                                        "line_number": 12(0 origin)
                                    },
                                    ...
        """
        locations = []
        # To count the number of times each block appears
        count_dict = dict([[block, 0] for block in list(self.TARGET_BLOCK)])
        # this pattern match like "theorem", "  proof", "theorem :Th1:"
        target_pattern = re.compile(
            f"([^a-zA-Z_]|^)+(?P<block>{'|'.join(self.TARGET_BLOCK)})([^a-zA-Z_]|$)"
        )
        # stack block keyword like ["definition", "proof", "proof"]
        # ["difinition", "proof", "proof"] means "definition proof proof <-here-> end end end"
        block_stack = []
        stack_rules = {
            "Text-Item": {
                "push": "",
                "pop": ""
            },
            "Definitional-Block": {
                "push": "definition",
                "pop": "end;"
            },
            "Registration-Block": {
                "push": "registration",
                "pop": "and"
            },
            "Notaion-Block": {
                "push": "notation",
                "pop": "end"
            },
            "Theorem": {
                "push": "theorem",
                "pop": ";"
            },
            "Scheme-Item": {
                "push": "scheme",
                "pop": "end;"
            },
            "proof": {
                "push": "proof",
                "pop": "end"
            }
        }
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
        for line_number, line in enumerate(text.split('\n')):
            # print(block_stack)
            line = re.sub('::.*', "", line)
            target_match = target_pattern.match(line)
            push_list = push_pattern.findall(line)
            pop_list = pop_pattern.findall(line)
            if len(block_stack) > 0 and block_stack[-1] == "scheme" and re.search(r"proof|;", line):
                block_stack.append("proof")
                target_match = re.match("(?P<block>proof)", "proof")
            elif push_list:
                for block in push_list:
                    block_stack.append(block)
            if pop_list:
                if len(block_stack) > 1 and block_stack[-2] == "scheme" and block_stack[-1] == "proof":
                    block_stack.pop()
                for block in pop_list:
                    block_stack.pop()
            if target_match:
                if block_stack.count("proof") == 1 or target_match.group('block') != 'proof':
                    block = target_match.group('block')
                    count_dict[block] += 1
                    locations.append({
                        "block": block,
                        "block_order": count_dict[block],
                        "line_number": line_number
                    })
        return locations

    def add_comment_header(self, text):
        """add HEADER to comment text

        Args:
            text(string): comment text without header
        Returns:
            text(string): text added HEADER
        """

        comment_lines = []
        if text == '':
            lines = []
        else:
            lines = text.split('\n')
        for line in lines:
            comment_lines.append(f'{self.HEADER}{line}')
        return '\n'.join(comment_lines)

    def verify_comment_text(self, text):
        """Verify Comment text

        Args:
            text(string): comment text with header
        """
        for line in text.split('\n'):
            if len(line) > self.LINE_MAX_LENGTH:
                raise Exception
            if not re.match(f'^{self.HEADER}.*', line):
                raise Exception
