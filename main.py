
class Tree:
    # class members
    # tree : list of nodes => [NodeA, NodeB, ..., NodeX]

    # constructor
    def __init__(self):
        self.listNodes = []

    # grow() : generate new upmost level

    # 
    def addNode(self, node):
        if node in self.listNodes:
            # node already located -> needed update
            pass
        else:
            # NEW node
            self.listNodes.append(node)

    # query node by name
    # return reference
    def queryNode(self, name) -> bool:

        return True

        

class Node:
    #attributes
    # parent
    # child
    # name
    # level
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        parent_str = "
        child_str = ""
        for parent in self.listParents:
            parent_str += str(parent) + '\n'
        for child in self.listChilds:
            child_str += str(child) + '\n'
        
        return f"START Node(name={self.name}, level={self.level}, no_of_parents={len(self.listParents)}, no_of_childs={len(self.listChilds)})\n" + \
                "PARENTS:\n" + parent_str + "CHILDS:\n" + child_str + "END Node"

    def addParent(self, node):
        self.listParents.append(node)

    def addChild(self, node):
        self.listChilds.append(node)

    def up(self):
        self.level = self.level + 1
        for parent in self.listParents:
            parent.up()

    def 



def run():
    # cd in directory, read file by file

    # parse file for entity allocations
        # if no allocation then addNode in ROOT
    # newNode = Node(name, ROOT)
        # if yes allocation then
    # imaginaryNode = queryNode()
    # imaginaryNode.up() 
    return




if __name__=="__main__":
    run()