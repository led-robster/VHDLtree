import os



class Tree:
    # attributes
        # tree : list of nodes => [NodeA, NodeB, ..., NodeX]

    # constructor
    def __init__(self):
        self.listNodes = []


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




def main():
    tree = Tree()
    # cd in directory, read file by file
    dir_path = "example_dir"
    all_files = os.listdir(dir_path)
    vhd_files = [f for f in all_files if f.endswith('.vhd') and os.path.isfile(os.path.join(dir_path, f))]
    # parse file for entity allocations
    for file in vhd_files:
        file_path = os.path.join(dir_path, file)

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
                                        if child_node.level>highest_level :
                                            highest_level = child_node.level

                                actNode.moveUP(highest_level+1)
                                tree.addNode(actNode)

                        break
                    else:
                        continue
                else :
                    continue
                                    
                    
                            
                    



        # if no allocation then addNode in ROOT
    # newNode = Node(name, ROOT)
        # if yes allocation then
    # imaginaryNode = queryNode()
    # imaginaryNode.up() 
    return True




if __name__=="__main__":
    main()