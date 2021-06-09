# University of Washington Drone Detection Capstone
This repository is split into three main folders. 

The first folder, "data_collection", includes scripts to capture RSSI, RSRP, RSRQ, position, and other data points to be used in our classification algorithms. All scripts in this folder must be run on the hardware descripted in our Research Paper below. 

The second folder, “raw_data”, contains the data captured by our hardware solution. Descriptions about each scenario are given in the file name of each csv file. 

The third folder, “classification_algorithm”, takes data captured from outputCSV.py, trains machine learning algorithms, and provides “drone” and “non_drone” classifications to the input data. The scripts in this folder do not have any hardware requirement.

For more information about code in the repository as well as more information on our overall project, please refer to our Research Paper at: https://docs.google.com/document/d/1UZdfwo9G25XeWGr4er4OTKV95EArZICvN_1oDFDAoE4/edit?usp=sharing

Additionally, feel free to visit our website for more background information at: 
https://sites.google.com/uw.edu/is-this-sim-a-drone/home
