import unittest

from textnode import TextNode, TextType
from html_converter import text_node_to_html_node
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    
    
    #Test functionality of TextNode.__eq__()
    
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_both_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "fakeurl")
        self.assertNotEqual(node, node2)

    
    #Test functionality of text_node_to_html_node()
    
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is a text node"},
        )


    #Test functionality of split_nodes_delimiter()


    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.CODE)

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_bold(self):
        node = TextNode("This is text with a **BOLD** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple(self):
        node1 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        node2 = TextNode("This is a generic node", TextType.ITALIC)
        node3 = TextNode("This is text with more _italic_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("This is a generic node", TextType.ITALIC),
                TextNode("This is text with more ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,
        )
    
            
    #Test functionality of split_nodes_image()


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_three(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another ![third image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),                
            ],
            new_nodes,
        )
        
    def test_split_images_already_image_node(self):
        node = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
        
    def test_split_images_with_list(self):
        nodes = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
                 TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another ![third image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT)]
        
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with an ", TextType.TEXT, None),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),                
            ],
            new_nodes
        )
    
    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_images_no_images(self):
        node = TextNode("This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_images_at_beginning(self):
        node = TextNode("![image](https://example.com/img.jpg) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
                TextNode(" followed by text", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_images_at_end(self):
        node = TextNode("Text followed by ![image](https://example.com/img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg")
            ],
            new_nodes
        )
    
    
    #Test functionality of split_nodes_link()
    
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links_three(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and another [third link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "third link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),                
            ],
            new_nodes,
        )
        
    def test_split_links_already_link_node(self):
        node = TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
        
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
        
    def test_split_links_with_list(self):
        nodes = [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"), 
                 TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and another [third link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT)]
        
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT, None),
                TextNode(
                    "third link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),                
            ],
            new_nodes
        )
    
    def test_split_links_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_links_no_images(self):
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_links_at_beginning(self):
        node = TextNode("[link](https://example.com/img.jpg) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com/img.jpg"),
                TextNode(" followed by text", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_links_at_end(self):
        node = TextNode("Text followed by [link](https://example.com/img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/img.jpg")
            ],
            new_nodes
        )    
    
    
if __name__ == "__main__":
    unittest.main()
