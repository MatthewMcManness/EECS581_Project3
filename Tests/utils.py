"""
    Name: Test Utils
    Description: Utility functions for tests
    Authors: Magaly Camacho [3072618]

    Date Created: 10/26/2024
    Revisions: 
        - None

    Preconditions: 
        - None
    Postconditions:
        - None
    Errors/Exceptions: 
        - None
    Side Effects: 
        - None
    Invariants: 
        - Methods passed to run_module_method() don't have any parameters
    Known Faults: 
        - None
"""


import os


def clean(paths:list[str]):
    """
    Delete all files at each path in paths

    :param paths: A list of file paths to delete
    :type paths: list[str]
    """
    for path in paths:
        # delete file if valid path
        if os.path.isfile(path):
            os.remove(path)
            print(f"Deleted {path}")
        
        # not a file
        else:
            print(f"No file exists at {path}")


def run_module_method(test_name:str, sys_argv:list[str], methods:dict, paths:list[str]):
    """
    Run a module's method if specified. If method wasn't specified, default to help(), if it's defined. 
    Otherwise, print message that no method was run.

    :param test_name: name of the test module
    :type test_name: str

    :param sys_arg: arguments passed when running the file (sys.argv)
    :type sys_arg: list[str]

    :param methods: dictionary of methods, where the key is the name of a method and the value is the method itself (not called)
    :type methods: dict
    
    :param paths: list of paths to the output files of a test module
    :type paths: list[str]
    """
    # check for args
    if len(sys_argv) > 1:
        # run clean method
        if sys_argv[1].lower() == "clean":
            clean(paths)
            return

        # run custom method
        elif sys_argv[1].lower() in methods.keys():
            method = methods[sys_argv[1]]
            method()
            return

        # if custom method not found
        else:
            print(f"Unable to find {test_name}.{sys_argv[1]}")
        
    # default to help()
    if "help" in methods:
        help = methods["help"]
        help()

    # if help() isn't defined, print a message
    else:
        print(f"Help option not found either")

    