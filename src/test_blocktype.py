import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

        # Test too many # characters
        block = "############# Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_code(self):
        block = """\
```
def code(self):
    pass
```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(block))
        # Missing end ticks
        block = """\
```
def code(self):
    pass
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_quote(self):
        block = ">This is a quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_unordered_list(self):
        block = "- List item"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ordered_list(self):
        block = "1. List item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_paragraph(self):
        block = "paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()
