import unittest
from block_functions import markdown_to_blocks, block_to_block_type
from block_types import BlockType

class TestMarkdownBlocks(unittest.TestCase):

    #Test functionality of markdown_to_blocks()
    
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_extra_newlines_and_whitespace(self):
        md = """
    This is **bolded** paragraph         



    This is another paragraph with _italic_ text and `code` here        
    This is the same paragraph on a new line       




    - This is a list  
    - with items
    """
    
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    #Test functionalicty of block_to_block_type()
        
    def test_block_to_block_type_code(self):
        block = '```this is some code in a code block```'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )
            
    def test_block_to_block_type_heading(self):
        block = '###### This is a heading'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
        
    def test_block_to_block_type_uo_list(self):
        block = '- This is an unordered list\n- with a new line'

        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )
        
    def test_block_to_block_type_o_list(self):
        block = '1. This is an ordered list\n2. with a new line'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )
        
    def test_block_to_block_type_quote(self):
        block = '> This is a quote block'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )
        
    def test_block_to_block_type_paragraph(self):
        block = 'This is just a normal paragraph block'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_7hashes(self):
        block = '####### This should be treated as a normal paragraph'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_invalid_code_block(self):
        block = '```this is an invalid code block`'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_o_list_invalid(self):
        block = '1. This is an ordered list\n3. with a new line'
        
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
        
if __name__ == "__main__":
    unittest.main()