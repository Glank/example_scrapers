import hashlib
import pickle
import os, os.path

CACHE_INDEX_FILE = "cache_index.pkl"
CACHE_DIRECTORY = "cache"

CACHE_INDEX = None
def __get_cache_index__():
    global CACHE_INDEX
    if CACHE_INDEX is None:
        if os.path.isfile(CACHE_INDEX_FILE):
            with open(CACHE_INDEX_FILE, 'r') as f:
                CACHE_INDEX = pickle.load(f)
        else:
            CACHE_INDEX = {}
    return CACHE_INDEX

def __save_cache_index__():
    index = __get_cache_index__()
    with open(CACHE_INDEX_FILE, 'w') as f:
        pickle.dump(index, f)

def __get_hash__(key):
    key = pickle.dumps(key)
    return hashlib.md5(key).hexdigest()

class __Cache__:
    def clear(self):
        if os.path.isdir(CACHE_DIRECTORY):
            os.system("rm -r "+CACHE_DIRECTORY)
        if os.path.isfile(CACHE_INDEX_FILE):
            os.system("rm "+CACHE_INDEX_FILE)
    def __contains__(self, key):
        h = __get_hash__(key)
        index = __get_cache_index__()
        return index.get(h, None) == key
    def __getitem__(self, key):
        h = __get_hash__(key)
        index = __get_cache_index__()
        if index.get(h, None) != key:
            raise KeyError()
        file_name = os.path.join(CACHE_DIRECTORY, h)
        with open(file_name, 'r') as f:
            return pickle.load(f)
    def __setitem__(self, key, item):
        h = __get_hash__(key)
        index = __get_cache_index__()
        index[h] = key
        if not os.path.isdir(CACHE_DIRECTORY):
            os.system("mkdir "+CACHE_DIRECTORY)
        file_name = os.path.join(CACHE_DIRECTORY, h)
        with open(file_name, 'w') as f:
            pickle.dump(item, f)
        __save_cache_index__()

Cache = __Cache__()

if __name__=="__main__":
    import sys
    if len(sys.argv)!=2:
        exit()
    if sys.argv[1]!="clear":
        exit()
    Cache.clear()
    
