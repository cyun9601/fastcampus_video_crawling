import pandas as pd 
import copy

class Node:
    def __init__(self, parent=None, children=[]):
        self.children = []
        
        if parent != None : 
            parent.add_child(self)
        for child in children :
            self.add_child(child)
        
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        
    @property
    def get_children(self):
        return self.children
        
    @property
    def get_parent(self):
        return self.parent
    
    def get_children_df(self, type, attributes:list):
        df = pd.DataFrame()
        print(f'{self.title}.children : ', self.children)
        for child in self.children:
            if isinstance(child, type):
                df = pd.concat([df, pd.DataFrame([self.get_attributes(child, attributes)], columns = attributes)], axis=0)
            else:
                df = pd.concat([df, child.get_children_df(type, attributes)], axis=0)
        return df
    
    def get_attributes(self, node, attributes:list):
        return [self.get_attribute(node, attribute) for attribute in attributes]
    
    def get_attribute(self, node, attribute:str):
        ret = node.copy()
        for attr in attribute.split('.'):
            if hasattr(ret, attr):
                ret = getattr(ret, attr)
            else:
                return None
        return ret
    
    def copy(self):
        return copy.deepcopy(self)
    
    def get_children_by_condition(self, condition):
        return [child for child in self.children if all([getattr(child, key) == value for key, value in condition.items()])]

    def print_node(self, level=0):
        if level == 0:
            print(self)
            
        for child in self.children:
            if level != 0:
                print('|', end='')
                print('       ' * level + '|────' , child)
            else : 
                print('|      ' * level + '|────' , child)
            child.print_node(level + 1)

class OrderedNode(Node):
    def __init__(self, seq:int, title:str, parent=None, children=[]):
        super().__init__(parent, children)
        self.seq = seq
        self.title = title
        
    def __repr__(self):
        return f'OrderedNode({self.title})'
    
class ClassroomNode(Node):
    def __init__(self, url:str, title:str, children=[]):
        super().__init__(children = children)
        self.url = url
        self.title = title
        
    def __repr__(self):
        return f'Class({self.title})'

class PartNode(OrderedNode):
    def __init__(self, seq:int, title:str, parent=None, children=[]):
        super().__init__(seq, title, parent, children)
        
    def __repr__(self):
        return f'Part({self.title})'

class ChapterNode(OrderedNode):
    def __init__(self, seq:int, title:str, parent=None, children=[]):
        super().__init__(seq, title, parent, children)
        
    def __repr__(self):
        return f'Chapter({self.title})'

class LectureNode(OrderedNode):
    def __init__(self, seq:int, title:str, url:str, parent=None, children=[]):
        super().__init__(seq, title, parent, children)
        self.url = url
        
    def __repr__(self):
        return f'LectureNode({self.title})'
    
if __name__=='__main__':
    '''
    Class | Part | Lecture
    A
    |---------B
    |         |------C
    |         |------D
    |---------E
    |----------------F
    '''
    # 기본적인 Node 생성 및 연결 
    A = ClassroomNode(url='https://google.com', title='A')
    
    B = PartNode(seq=1, title='B', parent=A)
    E = PartNode(seq=2, title='E')
    A.add_child(E)
    
    print("A.child: ", A.get_children)
    print("B.parent: ", B.get_parent)
    
    C = LectureNode(seq=1, title='C', url='https://google.com')
    D = LectureNode(seq=2, title='D', url='https://google.com')
    F = LectureNode(seq=3, title='F', url='https://google.com', parent=A)
    
    B.add_child(C)
    B.add_child(D)
    
    print("B.child: ", B.get_children)
    print("C.parent: ", C.get_parent)
    
    # 하위 노드 필터링 
    filtered_child = A.get_children_by_condition({'title':'C'})
    print("filtered_child: ", filtered_child)
    
    # 트리의 노드 정보들을 data frame으로 변환 
    # df1 = A.get_children_df(type = PartNode, attributes = ['seq', 'title']).reset_index(drop=True)
    df2 = A.get_children_df(type = LectureNode, attributes = ['seq', 'title', 'url']).reset_index(drop=True)
    
    # Tree 구조의 시각화
    A.print_node()