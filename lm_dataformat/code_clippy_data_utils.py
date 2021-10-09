#Utils to filter files based on extension and 
#basic quality of the file.
from os import path
from json import load
from typing import Dict, List

file_path = path.abspath(__file__)
def load_extension_manage_file(file_path=path.join(r"lm_dataformat",r"extension.json")):
    """
    Loads the extension managememnt file for filtering..
    """
    return load(open(file_path,"r"))



class FilterData:
    def __init__(self,ext_file_path=None) -> None:
        if ext_file_path != None:
            self.filter_extension = load_extension_manage_file(ext_file_path)
        else:
            self.filter_extension = load_extension_manage_file()
        # generate volume statistics
        self.stat_extension = {ext:0 for ext in self.filter_extension["additive_extensions"]+["total"]}
    
    def filter_file_extension(self,datapoint):
        """
        Given a datapoint takes 'file_name' key and filters based on
        the 'extension.json'
        """
        file_name  =  datapoint["file_name"]
        if file_name.split(".")[-1] in self.filter_extension["additive_extensions"]:
            self.stat_extension[file_name.split(".")[-1]] += 1
            self.stat_extension["total"] += 1
            return True
        else:
            return False
    def __call__(self,datapoint_list:List[Dict]):
        """
        Complete Filtering Criteria of the datapoint_list(List[Dict])
        """
        check_dict = {}
        filtered_datapoint = []
        for datapoint in datapoint_list:
            check_dict["filter_path_check"] = self.filter_file_extension(datapoint) #should have "file_name" key
            if set(list(check_dict.values())) == set([True]) :
                filtered_datapoint.append(datapoint)
            else:
                pass
        return filtered_datapoint

if __name__ == "__main__":
    print(FilterData()([{"file_name":"ast.py"},{"file_name":"ast.json"}]))