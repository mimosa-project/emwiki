import os
from django.test import TestCase

from emwiki.settings import TEST_OUTPUTS_DIR, TEST_MIZFILE_DIR,\
    TEST_RAW_MIZFILE_DIR
from contents.article.miz_text_converter import MizTextConverter


class MizTextConverterTest(TestCase):
    from_path = os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz')
    bad_path = 'abcmiz'
    to_path = os.path.join(TEST_OUTPUTS_DIR, 'abcmiz_0.miz')

    comments = [
        {
            'text': 'This is test\nline 2\nline 3',
            'block': 'registration',
            'block_order': 1,
            'commented_text': '::: This is test\n::: line 2\n::: line 3'
        },
        {
            'text': '\nThis is test\n',
            'block': 'definition',
            'block_order': 1,
            'commented_text': '::: \n::: This is test\n::: '
        },
        {
            'text': '$$This is test of MathJax$$\n$\star $',
            'block': 'definition',
            'block_order': 2,
            'commented_text': '::: $$This is test of MathJax$$\n::: $\star $'
        },
    ]

    @classmethod
    def setUpClass(cls):
        cls.miztextconverter = MizTextConverter()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_remove_comments(self):
        with open(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz'), 'r') as f:
            text = f.read()
        text = self.miztextconverter.remove_comments(text)
        with open(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz')) as f:
            raw_text = f.read()
        self.assertEqual(text, raw_text)

    def test_embed_comments(self):
        with open(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz'), 'r') as f:
            raw_text = f.read()
        with open(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz')) as f:
            text = f.read()
        test_text = self.miztextconverter.embed_comments(raw_text, self.comments)
        self.assertEqual(text, test_text)

    def test_extract_comments(self):
        with open(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz')) as f:
            text = f.read()
        comments = self.miztextconverter.extract_comments(text)
        comments = [comment for comment in comments if comment['text']]
        self.assertEqual(len(comments), 3)
        for comment in comments:
            self.assertIn(comment['block'], [comment['block'] for comment in self.comments])
            self.assertIn(comment['block_order'], [comment['block_order'] for comment in self.comments])
            self.assertIn(comment['text'], [comment['text'] for comment in self.comments])

    def test_add_comment_header(self):
        for comment in self.comments:
            comment_text = self.miztextconverter.add_comment_header(comment['text'])
            self.assertEqual(comment['commented_text'], comment_text)

    def test_restorebility(self):
        with open(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz'), 'r') as f:
            raw_text = f.read()
        with open(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz')) as f:
            text = f.read()

        processed_raw_text = raw_text
        processed_commented_text = text
        for i in range(10):
            comments = self.miztextconverter.extract_comments(processed_commented_text)
            processed_raw_text = self.miztextconverter.remove_comments(processed_commented_text)
            processed_commented_text = self.miztextconverter.embed_comments(processed_raw_text, comments)
            self.assertEqual(processed_raw_text, raw_text)
            self.assertEqual(processed_commented_text, text)
            comments = [comment for comment in comments if comment['text']]
            self.assertEqual(len(comments), 3)
            for comment in comments:
                self.assertIn(comment['block'], [comment['block'] for comment in self.comments])
                self.assertIn(comment['block_order'], [comment['block_order'] for comment in self.comments])
                self.assertIn(comment['text'], [comment['text'] for comment in self.comments])
