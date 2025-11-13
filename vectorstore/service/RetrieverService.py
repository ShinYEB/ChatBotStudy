from component.builder import build_index
from component.spliter import split_large_pdfs_in_folder

def build():
    try:
        build_index()
        return True
    except:
        return False

def split():
    try:
        split_large_pdfs_in_folder("./database")
        return True
    except:
        return False