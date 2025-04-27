import unittest

from textnode import TextNode, TextType
from text_to_nodes import text_to_textnodes


class TestTextNode(unittest.TestCase):
    
    
    #Test functonality of text_to_textnodes()
    
    
    def test_text_to_textnodes_comprehensive(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        #print(f"{text_to_textnodes(text)}")
        
        self.assertEqual(text_to_textnodes(text),
                         
                         [  
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                         ]
        )
        
    def test_text_to_textnodes_empty(self):
        text = ""
        
        self.assertEqual(text_to_textnodes(text), [TextNode("", TextType.TEXT)])
        
    def test_text_to_textnodes_basic(self):
        text = "Just plain text"
        
        self.assertEqual(text_to_textnodes(text), [TextNode("Just plain text", TextType.TEXT)])
        
        
    #Test case for later, not within the scope of the project
    
    
    # def test_text_to_textnodes_nested(self):
    #     text = "**Bold _and italic_**"
        
    #     self.assertEqual(text_to_textnodes(text), 
                         
    #                      [  
    #                         TextNode("Bold ", TextType.BOLD),
    #                         TextNode("and italic", TextType.ITALIC)
    #                      ]

    #     )
        
if __name__ == "__main__":
    unittest.main()
        