#Utils to filter files based on extension and 
#basic quality of the file.
from os import path
from json import load
from typing import Dict, List
import magic
from dataclasses import dataclass
file_path = path.abspath(__file__)
def load_extension_manage_file(file_path=path.join(r"lm_dataformat",r"extension.json")):
    """
    Loads the extension managememnt file for filtering..
    """
    return load(open(file_path,"r"))

@dataclass
class FileType:
    file_extension_hash = {
            "lisp" : "Lisp",
            "lsp" : "Lisp",
            "f" : "ASCII text",
            "fs" : "ASCII text",
            "sh" : "ASCII text",
            "groovy" : "ASCII text",
            "r" : "ASCII text",
            "pl" : "Perl script",
            "html" : "HTML",
            "css" : "ASCII text",
            "sql" : "ASCII text",
            "py" : "Python script",
            "c" : "c program",
            "cpp" : "C++ source",
            "h" : "c program",
            "hpp" : "c program",
            "jl" : "ASCII text",
            "java" : "ASCII text",
            "js" : "ASCII text",
            "ts" : "ASCII text",
            "cs" : "ASCII text",
            "go" : "ASCII text",
            "rs" : "ASCII text",
            "swift" : "ASCII text",
            "php" : "ASCII text",
            "dart" : "ASCII text",
            "kt" : "ASCII text",
            "m" : "ASCII text"
    }




class FilterData:
    def __init__(self,ext_file_path=None) -> None:
        if ext_file_path != None:
            self.filter_extension = load_extension_manage_file(ext_file_path)
        else:
            self.filter_extension = load_extension_manage_file()
        # generate volume statistics
        self.stat_extension = {ext:0 for ext in self.filter_extension["additive_extensions"]+["total"]}
        self.look_up_magic = list(set(list(FileType.file_extension_hash.values())))
    def filter_file_extension(self,datapoint):
        """
        Given a datapoint takes 'file_name' key and filters based on
        the 'extension.json'
        """
        file_name  =  datapoint["meta"]["file_name"]
        file_type = magic.from_buffer(datapoint["text"])
        for file_type_idt in self.look_up_magic:
            if file_type_idt in file_type:
                return True
        return  False
        #Change Log | Reshinth (31/10/2021) - Since file_name has issues depreceating this 
        # and adding temporary Lib-Magic based Extension.
        # if file_name.split(".")[-1] in self.filter_extension["additive_extensions"]:
        #     #TODO(reshinth) : Adding magic support
            
        #     self.stat_extension[file_name.split(".")[-1]] += 1
        #     self.stat_extension["total"] += 1
        #     return True
        # else:
        #     return False
    def __call__(self,datapoint_list:List[Dict],file):
        """
        Complete Filtering Criteria of the datapoint_list(List[Dict])
        """
        check_dict = {}
        filtered_datapoint = []
        for datapoint in datapoint_list:
            check_dict["filter_path_check"] = self.filter_file_extension(datapoint) #should have "file_name" key
            if set(list(check_dict.values())) == set([True]) :
                filtered_datapoint.append(datapoint)
        print(len(filtered_datapoint))
        return filtered_datapoint

if __name__ == "__main__":
    print(FilterData()([{"file_name":"ast.py"},{"file_name":"ast.json"}]))