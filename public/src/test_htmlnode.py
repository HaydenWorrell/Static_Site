import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
#    props_input1 = {"href": "https://www.google.com", "target": "_blank"}
    
#    test_node1 = HTMLNode(None, None, None, props_input1)
    
    def test_prop_base(self):
        props_input = {"href": "https://www.google.com", "target": "_blank"}
        test_node = HTMLNode(None, None, None, props_input)
                
        expected_output = " href=\"https://www.google.com\" target=\"_blank\""
        actual_output = test_node.props_to_html()

        self.assertEqual(expected_output, actual_output)
    
    def test_prop_empty(self):
        props_input = {}
        test_node = HTMLNode(None, None, None, props_input)
        
        expected_output = ""
        actual_output = test_node.props_to_html()
        
        self.assertEqual(expected_output, actual_output)
        
    def test_prop_special(self):
        props_input = {"data-item": "value", "aria-label": "close"}
        test_node = HTMLNode(None, None, None, props_input)
        
        expected_output = ' data-item="value" aria-label="close"'
        actual_output = test_node.props_to_html()
        
        self.assertEqual(expected_output, actual_output)
        
    def test_prop_ints(self):
        props_input = {"width": 200, "height": 100}
        test_node = HTMLNode(None, None, None, props_input)
        
        expected_output = ' width="200" height="100"'
        actual_output = test_node.props_to_html()
        
        self.assertEqual(expected_output, actual_output)
        
    def test_prop_bool(self):
        props_input = {"checked": None, "readonly": None}
        test_node = HTMLNode(None, None, None, props_input)
        
        expected_output = ' checked readonly'
        actual_output = test_node.props_to_html()
        
        self.assertEqual(expected_output, actual_output)
        
    def test_prop_bool_single(self):
        props_input = {"checked": None}
        test_node = HTMLNode(None, None, None, props_input)
        
        expected_output = ' checked'
        actual_output = test_node.props_to_html()
        
        self.assertEqual(expected_output, actual_output)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")
        
    def test_leaf_to_html_a(self):
        #props = {"href": "https://www.google.com"}
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        #print(node.__repr__())
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
    
if __name__ == "__main__":
    unittest.main()
    
    
#LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
#"<a href="https://www.google.com">Click me!</a>"