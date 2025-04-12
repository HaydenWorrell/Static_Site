import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    
    # props_to_html() functionality testing
    
    
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
    
    
    # leaf_to_html() functionality testing
    
            
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(), 
            "<p>Hello, world!</p>"
        )            
            
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(
            node.to_html(), 
            "Hello world!"
        )
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            "<a href=\"https://www.google.com\">Click me!</a>"
        )
        
    def test_leaf_to_html_special(self):
        node = LeafNode("div", "Chicken & Waffles")
        self.assertEqual(
            node.to_html(), 
            "<div>Chicken & Waffles</div>"
        )
    
    def test_leaf_to_html_multiple(self):
        node = LeafNode("input", "", {"type": "text", "id": "username", "placeholder": "Enter username"})
        self.assertEqual(
            node.to_html(), 
            '<input type=\"text\" id=\"username\" placeholder=\"Enter username\"></input>'
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    
    # parent_to_html() functionality testing
    
    
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span></div>"
        )

    def test_parent_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_parent_to_html_with_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p", "grandchild2")
        grandchild_node3 = LeafNode(None, "grandchild3")
        grandchild_node4 = LeafNode("i", "grandchild4")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2, grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><p>grandchild2</p>grandchild3<i>grandchild4</i></span></div>",
        )
        
    def test_parent_to_html_props(self):
        child_node1 = LeafNode("a", "child node 1", {"href": "https://boot.dev", "class": "button"})
        child_node2 = LeafNode("span", "Hello")
        parent_node = ParentNode("div", [child_node1, child_node2], {"id": "container", "class": "wrapper"})
        self.assertEqual(
            parent_node.to_html(),
            "<div id=\"container\" class=\"wrapper\"><a href=\"https://boot.dev\" class=\"button\">child node 1</a><span>Hello</span></div>"
        )
        
    def test_parent_to_html_notag(self):
        child = LeafNode("p", "child")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_parent_to_html_nochild(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_parent_to_html_emptychild(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()
            
    
if __name__ == "__main__":
    unittest.main()