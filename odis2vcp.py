#!/usr/bin/python
# ODIS2VCP
# Dataset extractor
# Converts datasets from ODIS XML format to VCP XML format
# by Jille

from xml.dom.minidom import *
import binascii, argparse, sys
import xml.etree.cElementTree as ET

# variables
dataset_counter = 0
extracted_dataset_counter = 0
version = "1.0"

# parse arguments
ap = argparse.ArgumentParser(description="ODIS2VCP Dataset extractor v%s" % version)
ap.add_argument("-i", "--in", required=True, help="Input file path")
ap.add_argument("-f", "--fmt", required=False, help="Output format: vcp (default) or raw.")
ap.add_argument("-d", "--desc", required=True, help="Output file description. E.g. \"Seat Leon 2016\" ")

args = vars(ap.parse_args())
file_output_format = args['fmt']
file_prefix = args['desc']
input_file = args['in']


# extract dataset to a raw export of the dataset
def extract_to_raw(dataset, filename, diagnostic_address):
   global extracted_dataset_counter
   extracted_dataset_counter=extracted_dataset_counter+1
 
   filename = diagnostic_address + " " + filename + ".bin"
   print(" Extracting raw data to \"%s\"" % filename)
   print()
   output_file = open(filename,"wb")
   binary_data = binascii.unhexlify(dataset)
   output_file.write(binary_data)
  
   output_file.close()

# extract dataset to VCP dataset XML format
def convert_to_vcp(dataset_data, diagnostic_address, start_address, zdc_name, zdc_version, login, filename):
   global extracted_dataset_counter
   extracted_dataset_counter=extracted_dataset_counter+1
 
   doc = Document();
   root = doc.createElement("SW-CNT")
   doc.appendChild(root)
   
   ident = doc.createElement("IDENT")
   root.appendChild(ident)
   
   login_data			= doc.createElement("LOGIN")
   dateiid 			= doc.createElement("DATEIID")
   version_inhalt 	= doc.createElement("VERSION-INHALT")
   ident.appendChild(login_data)
   ident.appendChild(dateiid)
   ident.appendChild(version_inhalt)
   
   login_data.appendChild (doc.createTextNode(login))
   dateiid.appendChild (doc.createTextNode(zdc_name))
   version_inhalt.appendChild (doc.createTextNode(zdc_version))

   
   datasets = doc.createElement("DATENBEREICHE")
   root.appendChild(datasets)
   
   dataset = doc.createElement("DATENBEREICH")
   datasets.appendChild (dataset)
   
   dataname = zdc_name + " address - " + start_address
   dataset_name = doc.createElement("DATEN-NAME")
   dataset.appendChild (dataset_name)
   dataset_name.appendChild(doc.createTextNode(zdc_name))

   dataset_format = doc.createElement("DATEN-FORMAT-NAME")
   dataset.appendChild (dataset_format)
   dataset_format.appendChild(doc.createTextNode("DFN_HEX"))

   dataset_start = doc.createElement("START-ADR")
   dataset.appendChild (dataset_start)
   dataset_start.appendChild(doc.createTextNode(start_address))  
   
   dataset_raw = dataset_data.replace("0x","")
   dataset_raw = dataset_raw.replace(",","")
   
   #some quick and dirty calculations to determine the right size and string format for file size
   dataset_size_calc = len(dataset_raw.encode('utf-8'))
   dataset_size_calc = dataset_size_calc/2
   dataset_size_calc = hex(int(dataset_size_calc))
   dataset_size_calc = str(dataset_size_calc)

   dataset_size = doc.createElement("GROESSE-DEKOMPRIMIERT")
   dataset.appendChild (dataset_size)
   dataset_size.appendChild(doc.createTextNode(dataset_size_calc))   
   
   data_data = doc.createElement("DATEN")
   dataset.appendChild (data_data)
   data_data.appendChild(doc.createTextNode(dataset_data))
       
# write xml data
   filename = diagnostic_address + " VCP " + filename + ".xml"
   
   print(" Extracting VCP data to \"%s\"" % filename)
   print()
   
   doc.writexml( open(filename, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
			   
   
# Parse single OE XML file
# Print detail of each dataset in small OE XML file
def parse_small_oe_file():
    global dataset_counter
    
# Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(input_file) #todo: use file input argument
    collection = DOMTree.documentElement

#get data from XML
    parameter_datas = collection.getElementsByTagName("PARAMETER_DATA")
    for parameter_data in parameter_datas:
       if parameter_data.hasAttribute("DIAGNOSTIC_ADDRESS"):
          diagnostic_address = parameter_data.getAttribute("DIAGNOSTIC_ADDRESS")
          diagnostic_address = diagnostic_address.replace ("0x00","")
          print(" Module: %s" % diagnostic_address)
       if parameter_data.hasAttribute("START_ADDRESS"):
          start_address = parameter_data.getAttribute("START_ADDRESS")
          print(" Start_Address: %s" % start_address)       
       if parameter_data.hasAttribute("ZDC_NAME"):
          zdc_name = parameter_data.getAttribute("ZDC_NAME")
          print(" ZDC Name: %s" % zdc_name)
       if parameter_data.hasAttribute("ZDC_VERSION"):
          zdc_version = parameter_data.getAttribute("ZDC_VERSION")
          print(" ZDC version: %s" % zdc_version)
       if parameter_data.hasAttribute("LOGIN"):
          login = parameter_data.getAttribute("LOGIN")
          print(" Login: %s" % login)
#set filename, e.g. 19 ZL12345 - Seat Leon 2016		  
          filename = start_address + " " + zdc_name + " - " + file_prefix
	   
       dataset_counter=dataset_counter+1
       dataset = parameter_data.childNodes[0].data
       
       #clean the data from all the 0x and commas
       if file_output_format == "raw":
          dataset = dataset.replace('0x','')
          dataset = dataset.replace(",","")
          extract_to_raw(dataset,filename,diagnostic_address)
	  
       else:
          convert_to_vcp(dataset, diagnostic_address, start_address, zdc_name, zdc_version, login, filename)
 
# run the parser. 
parse_small_oe_file()   

print()

if file_output_format == "raw":
   print(" %s of %s datasets extracted to %s format" % (extracted_dataset_counter, dataset_counter, file_output_format))
else:
   print(" %s of %s datasets extracted to VCP format" % (extracted_dataset_counter, dataset_counter))
