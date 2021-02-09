#include "coreir.h"

//This function will take in a coreir module and return the following:
//  a mapped module with instances of PEs
//  a std::map<string,int> name of instances to number of cycles of latency it has

struct MappedRetStruct {
  CoreIR::Module* mapped;
  std::map<string,int> latency_map;
};

class Mapper {
  std::string pe_name
  public:
    Mapper(std::string pe) : pe(pe) {}

    bool map_app(CoreIR::Module* module) {
      
      //Save this module to a coreir file
      string tmpfile_name = "tmp.json";
      if (!saveToFile(g, "_add12.json",module)) {
        cout << "Could not save to json!!" << endl;
        c->die();
      }
     
      //Call an external script to run the mapper pythonscript
      
      //Load the mapped coreir json file to a module

  } 
}
