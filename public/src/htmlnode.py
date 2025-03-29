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
            pass
        
        if self.props == {}:
            return ""
        
        prop_str = ' '.join([f'{key}=\"{value}\"' for key, value in self.props.items() if value is not None])
        prop_str = prop_str + ' '.join([f'{key}' for key, value in self.props.items() if value is None])
        prop_str = ' ' + prop_str
        
        return prop_str
               
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={str(self.props)})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super(LeafNode, self).__init__()
        self.tag = tag
        self.value = value
        
    def to_html(self):
        if self.value == None:
            raise ValueError()
        
        if self.tag == None:
            return self.value
        
        return f'<{self.tag}>{self.value}</{self.tag}>'
        
        