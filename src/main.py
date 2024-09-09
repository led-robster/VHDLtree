import os
from random import shuffle, seed
from constants import Constants


# singleton TUI
class TUI :
    __instance = None
    _rows=0
    _pushed_words=[] # ex. : [[mv,mz,mx,mw],[mu],[my],...]
                            #[[    L0     ],[L1],[L2],...]

    def __new__(self):
        if self.__instance is None:
            self.instance = super(TUI, self).__new__(self)


    def push(self, string, row):
        pass


class Tree:
    # attributes
        # tree : list of nodes => [NodeA, NodeB, ..., NodeX]

    # constructor
    def __init__(self):
        self.listNodes = []

    def __str__(self) -> str:
        print_str = ""
        for node in self.listNodes:
            nodeName = node.name
            nodeLvl = node.level
            nodeGhost = node.ghost
            if nodeGhost:
                print_str += nodeName + " (ghost) : at level " + str(nodeLvl) + '\n'
            else:
                print_str += nodeName + " (real) : at level " + str(nodeLvl) + '\n'

        return print_str

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
        for node in self.listNodes:
            if node.name==name :
                return node
        
        return None
    
    def list(self, bottom_2_top: True):

        highest_lvl = 0

        for node in self.listNodes:
            if node._level>highest_lvl:
                highest_lvl = node._level
        

        if not bottom_2_top:
            start_level = highest_lvl
        else:
            start_level = 0

        for i in range(0,highest_lvl+1):

            if bottom_2_top:
                for node in self.listNodes:
                    if node._level== (start_level+i):
                        print(node.name + ".vhd")
            else:
                for node in self.listNodes:
                    if node._level== (start_level-i):
                        print(node.name + ".vhd")

            
            

        
class Node:
    # attributes: 
        # parents : [Nodes]
        # childs : [Nodes]
        # name : str
        # level : positive int
        # ghost : bool

    def __init__(self, name, level, ghost):
        self.name = name
        self._level = level
        self._ghost = ghost
        self.listParents = []
        self.listChilds = []

    def __str__(self):
        parent_str = ""
        child_str = ""
        for parent in self.listParents:
            parent_str += str(parent) + '\n'
        for child in self.listChilds:
            child_str += str(child) + '\n'
        
        return f"START Node(name={self.name}, level={self._level}, no_of_parents={len(self.listParents)}, no_of_childs={len(self.listChilds)})\n" + \
                "PARENTS:\n" + parent_str + "CHILDS:\n" + child_str + "END Node"

    def addParent(self, node):
        self.listParents.append(node)

    def addChild(self, node):
        self.listChilds.append(node)

    def moveUP(self, new_level):
        self._level = new_level
        for parent in self.listParents:
            parent.moveUP(new_level+1)
    


    # GETTERS AND SETTERS
    # ################################
    @property
    def ghost(self):
        return self._ghost
    
    @ghost.setter
    def ghost(self, value):
        self._ghost = value

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, new_level):
        if new_level >= 0:  # Example condition to only allow non-negative values
            self._level = new_level
        else:
            raise ValueError("Level cannot be negative")


def hasAllocation(fpath):

    child_list = []

    #lines = fcontent.split('\n')
    with open(fpath, 'r') as f:

        for line in f.readlines():

            line_splitted = line.split()

            if line_splitted:
                if len(line_splitted)>2:
                    if line_splitted[2]=="entity" and line_splitted[1]==":":
                        # i_mx : entity library.my_rtl(rtl)
                            lib_entity = line_splitted[3].split('.')
                            entity = lib_entity[1]
                            child_module_name = entity.split('(')[0]
                            child_list.append(child_module_name)

    return child_list




def run(dir="example_dir", opt_shuffle=False):

    # seed(39)

    tree = Tree()
    # cd in directory, read file by file
    all_files = os.listdir(dir)
    vhd_files = [f for f in all_files if f.endswith('.vhd') and os.path.isfile(os.path.join(dir, f))]

    if opt_shuffle==True:
        shuffle(vhd_files)

    # parse file for entity allocations
    for file in vhd_files:
        file_path = os.path.join(dir, file)

        with open(file_path, 'r') as f:


            for line in f.readlines():

                if line=="\n":
                    continue

                line_splitted = line.split()

                # parse name of entity
                # entity xxx is
                if line_splitted:
                    if line_splitted[0]=="entity" and line_splitted[2]=="is" :

                        module_name = line_splitted[1] 

                        querynode = tree.queryNode(module_name)

                        if querynode!=None:
                            #   NODE EXISTS
                            if querynode.ghost :
                                # NODE EXISTS AS GHOST
                                childs = hasAllocation(file_path)
                                if not childs:
                                    # NODE EXISTS AS GHOST AND HAS NO CHILD
                                    querynode.ghost = False
                                else:
                                    # NODE EXISTS AS GHOST AND HAS CHILDs
                                    highest_level=0
                                    for child in childs:
                                        child_node = tree.queryNode(child)
                                        if child_node==None :
                                            newNode = Node(name=child, level=0, ghost=True)
                                            newNode.addParent(querynode)
                                            tree.addNode(newNode)
                                            querynode.addChild(newNode)
                                        else:
                                            child_node.addParent(querynode)
                                            querynode.addChild(child_node)
                                            if child_node.level>highest_level:
                                                highest_level = child_node.level

                                    querynode.moveUP(highest_level+1)
                                    querynode.ghost = False


                            else:
                                # unfeasible
                                return False


                        else:
                            # NODE SOES NOT EXIST
                            childs = hasAllocation(file_path)

                            if not childs:
                                # no childs
                                newNode = Node(name = module_name, level= 0, ghost = False)
                                tree.addNode(newNode)
                            else:
                                #has childs
                                actNode = Node(name=module_name, level=0, ghost=False)
                                highest_level=0
                                for child in childs:
                                    child_node = tree.queryNode(child)
                                    if child_node==None:
                                        newNode = Node(name = child, level=0, ghost=True)
                                        newNode.addParent(actNode)
                                        tree.addNode(newNode)
                                        actNode.addChild(newNode)
                                    else:
                                        child_node.addParent(actNode)
                                        actNode.addChild(child_node)
                                        if child_node.level>highest_level :
                                            highest_level = child_node.level

                                actNode.moveUP(highest_level+1)
                                tree.addNode(actNode)

                        break
                    else:
                        continue
                else :
                    continue
                                    
    return tree           
                            



if __name__=="__main__":
    #print(Constants.DOWN_ARROW())
    tree = run(dir = "example_dir", opt_shuffle=True)
    tree.list(True)
    pass