import sys
import os

# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import main as src

def trees_are_equal():
    tree1 = src.run("src/example_dir", opt_shuffle=True)
    tree2 = src.run("src/example_dir", opt_shuffle=True)
    tree3 = src.run("src/example_dir", opt_shuffle=True)
    tree4 = src.run("src/example_dir", opt_shuffle=True)
    tree5 = src.run("src/example_dir", opt_shuffle=True)
    tree6 = src.run("src/example_dir", opt_shuffle=True)
    tree1_str = tree1.__str__()
    tree2_str = tree2.__str__()
    tree3_str = tree3.__str__()
    tree4_str = tree4.__str__()
    tree5_str = tree5.__str__()
    tree6_str = tree6.__str__()

    # Add all strings to a set
    strings = {tree1_str, tree2_str, tree3_str, tree4_str, tree5_str, tree6_str}

    assert len(strings) == 1, "ERROR : Not all strings are equal"   



trees_are_equal()