class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        if self.props == {}:
            return ""
        
        prop_str = ' '.join([f'{key}=\"{value}\"' for key, value in self.props.items() if value is not None])
        prop_str = prop_str + ' '.join([f'{key}' for key, value in self.props.items() if value is None])
        prop_str = ' ' + prop_str
        
        return prop_str
               
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={str(self.props)})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.props and len(self.props) > 1:
            html_str = self.props_to_html()         
            return f'<{self.tag}{html_str}></{self.tag}>'
        
        if not self.value:
            raise ValueError("LeafNode must have value")
        
        if self.tag == None:
            return self.value
        
        html_props = self.props_to_html()
        if html_props:    
            return f'<{self.tag}{html_props}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        
        if not self.children:
            raise ValueError("ParentNode must have children")
            
        html_str = f'<{self.tag}>'        
        
        for child in self.children:
            child_str = child.to_html()
            html_str = html_str + f'{child_str}'
            
        html_str = html_str + f'</{self.tag}>'
        
        return html_str
    
        