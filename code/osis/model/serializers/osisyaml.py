# <License type="Aserver BSD" version="2.0">
#
# Copyright (c) 2005-2009, Aserver NV.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name Aserver nor the names of other contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ASERVER "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ASERVER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

import sys
import time
sys.path.append('/usr/local/lib/python2.6/dist-packages')

import yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

#from syck import *



import logging
from thrift.Thrift import TType

import osis.model
from osis.model.fields import EmptyObject

logger = logging.getLogger('osis.model.yaml')

try:
    from pymonkey.baseclasses import BaseEnumeration
except ImportError:
    logger.info('No PyMonkey Enumeration support')
    BaseEnumeration = None

from osis.model.model import DEFAULT_FIELDS
#import osis.model

TYPE_SPEC_CACHE = dict()

def struct_args(attr):
    return (attr.type_, generate_thrift_spec(attr.type_.OSIS_MODEL_INFO))

def dict_args(attr):
    return (TType.STRING, None,
            FIELD_TYPE_THRIFT_TYPE_MAP[type(attr.type_)](attr.type_),
            FIELD_TYPE_ATTR_ARGS_MAP[type(attr.type_)](attr.type_))

def list_args(attr):
    return (FIELD_TYPE_THRIFT_TYPE_MAP[type(attr.type_)](attr.type_),
            FIELD_TYPE_ATTR_ARGS_MAP[type(attr.type_)](attr.type_))




FIELD_TYPE_ATTR_ARGS_MAP = {
    osis.model.GUID: lambda o: None,
    osis.model.String: lambda o: None,
    osis.model.Integer: lambda o: None,
    osis.model.Boolean: lambda o: None,
    osis.model.Object: struct_args,
    osis.model.Float: lambda o: None,
    osis.model.Dict: dict_args,
    osis.model.List: list_args,
    osis.model.Enumeration: lambda o: None,
}

# Please keep FIELD_TYPE_THRIFT_TO_OSIS_MAP and FIELD_TYPE_THRIFT_TYPE_MAP always in Sync

FIELD_TYPE_THRIFT_TYPE_MAP = {
    osis.model.GUID: lambda o: TType.STRING,
    osis.model.String: lambda o: TType.STRING,
    osis.model.Integer: lambda o: TType.I64,
    osis.model.Boolean: lambda o: TType.BOOL,
    osis.model.Object: lambda o: TType.STRUCT,
    osis.model.Float: lambda o: TType.DOUBLE,
    osis.model.Dict: lambda o: TType.MAP,
    osis.model.List: lambda o: TType.LIST,
    osis.model.Enumeration: lambda o: TType.STRING,
}

FIELD_TYPE_THRIFT_TO_OSIS_MAP = {
    osis.model.GUID: lambda o: "string",
    osis.model.String: lambda o: "string",
    osis.model.Integer: lambda o: "i64",
    osis.model.Boolean: lambda o: "BOOL",
    osis.model.Object: lambda o: "struct",
    osis.model.Float: lambda o: "double",
    osis.model.Dict: lambda o: "map",
    osis.model.List: lambda o: "list",
    osis.model.Enumeration: lambda o: "string",
}

file_suffix1="arif"



class_dict={} 
root_class=""
class_order_dict={}
class_order_count=0

def thrift_to_osis(name_info, attributes):

    var='struct' + ' ' + name_info + '' + '{' + '\n'
    global class_order_dict
    global class_order_count
    class_order_dict[class_order_count]=name_info
    global class_order_count
    class_order_count+=1
    global file_suffix1
    file_path='/opt/qbase3/lib/python/site-packages/osis/model/serializers/'+file_suffix1
    var1=""
    for attribute in attributes:
        name = attribute.name
        attr = attribute.attribute
        aid = attr.kwargs['thrift_id']

        args = FIELD_TYPE_ATTR_ARGS_MAP[type(attr)](attr)
        thrift_type = FIELD_TYPE_THRIFT_TO_OSIS_MAP[type(attr)](attr)

        var1=var1+'  ' + str(thrift_type) + '  ' + name + '  ' 

	global class_dict
	class_dict[name_info]=var1



# implementation of utilities for converting a model to xml mapping for compass
# added on 25-08-09
	

class_xml={}
def prepare_indexing_xml(class_dict,rootclass):
    global class_order_dict
    #~ logger.info(' class _ordr_dict %s' %str(class_order_dict))

    final_string=""
    final_string+="<root-json-object alias=\"" + rootclass + "\">@"
    global class_order_count
    count=class_order_count-1
    index=0
    while count>=0 :
        global class_order_dict
        item=class_order_dict[count]
        global class_xml
        class_xml[item]=convert_class_to_xml(class_dict[item],item)
    #~ logger.info('After first call value of class_xml is  %s' %str(class_xml))
    count=count-1

    final_string+=class_xml[rootclass]
    final_string+="@"
    final_string+="<json-content name=\"content\" />@"
    final_string+="</root-json-object>"
    return final_string
				
def convert_class_to_xml(class_string,class_name):
	
    	#~ logger.info('convert_class_to_xml called with argument 1  %s' %class_string)
    	#~ logger.info('convert_class_to_xml called with argument 2  %s' %class_name)
	import re
	splitter = re.compile(r'[ ]*')
	list=splitter.split(class_string)
	final_list=[];
	for items in list:
		if items!='\'' and items!=' ' and items!='' :	
			final_list.append(items)
	#even indexes will be type, odd indexes will be object
	list_len=len(final_list)
	end_index=list_len-1
	count=0
	to_return=""
	while count<end_index :
		if final_list[count] != 'struct' and final_list[count] != 'struct\n' and final_list[count]!='list' and final_list[count]!='list\n' and final_list[count] != 'object' and final_list[count] != 'object\n':
			to_return+="<json-property name=\""+final_list[count+1]+"\"/>@"
		else:
			if final_list[count] == 'object' or final_list[count] == 'object\n' or final_list[count] == 'struct' or final_list[count]=='struct\n' :
				to_return+="<json-object name=\""+final_list[count+1]+"\">@"
				global class_xml
				global root_class
				list_type=get_list_type(final_list[count+1],root_class,class_name )
				to_return+=class_xml[list_type]
				to_return+="@</json-object>@"
			else:
				if final_list[count]=='list':
					global root_class
					list_type=get_list_type(final_list[count+1],root_class,class_name )
					to_return+="<json-array name=\"" + final_list[count+1] + "\">@"

					if list_type=="String" or list_type=="string":
						#to_return+="<json-array name=\"" + final_list[count+1] + "\">@"
						to_return+="<json-property />@"
						#to_return+="</json-array>@"
					else:
						global class_xml
    						#~ logger.info('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD %s' %str(class_xml))
    						#~ logger.info('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD %s' %list_type)
    						#~ logger.info('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD %s' %to_return)
						#to_return+="<json-array name=\"" + final_list[count+1] + "\"" + "  dynamic=\"true\"/>@"
						global class_xml
						to_return+="<json-object>@"
						to_return+=class_xml[list_type]
						to_return+="@"
						to_return+="</json-object>@"
					to_return+="</json-array>@"
		count+=2
    	#~ logger.info('convert_class_to_xml returning result  %s' %to_return)
	return to_return
		

def get_list_type(variable_name,rootclass,class_name):
    	#~ logger.info('get_list_type called with argument 1  %s' %variable_name)
    	#~ logger.info('get_list_type called with argument 2  %s' %rootclass)
    	#~ logger.info('get_list_type called with argument 3  %s' %class_name)
	result="NNNNNNNN"
	import os
	path="/opt/qbase3/libexec/osis"
	potential_files = os.listdir(path)
	for filename in potential_files:
        	filepath = os.path.join(path, filename)
            	if filepath.endswith('.py') and os.path.isfile(filepath):
			if rootclass_found_in_file(filepath,rootclass)=="True": # finding the file name which is having the mentioned rootclass
				result = helper_f_get_list_type(filepath,variable_name,class_name)		
    				#~ logger.info('get_list_type returing result  %s' %result)
				return result
    	
	#~ logger.info('get_list_type returing result  %s' %result)
	return result
				

				
def helper_f_get_list_type(filepath,variable_name,class_name):
    	#~ logger.info('helper_f_get_list_type called with argument 1  %s' %filepath)
    	#~ logger.info('helper_f_get_list_type called with argument 2  %s' %variable_name)
    	#~ logger.info('helper_f_get_list_type called with argument 3  %s' %class_name)
	import re
	file=open(filepath)
	result="BBBBBB"
	splitter=re.compile(r'[ ]*')
	flag="0"
	while 1 and  flag=="0":
		line = file.readline()
		if not line:
       			break
		list=splitter.split(line)
		count=0
		final_list=""

		for items in list:
			final_list+=items

		if final_list.find("class")!=-1 or final_list.find("Class")!=-1:
			count=count+1	
		if final_list.find("model.Model")!=-1 or final_list.find("model.RootObjectModel")!=-1:
			count=count+1	
		if final_list.find(class_name)!=-1:
			count=count+1	
		if count==3: # found the class
    			#~ logger.info('helper_f_get_list_type internal data --> found the class  %s' %class_name)
			while 1 and  flag=="0":
				line1=file.readline()
				if not line:
					flag="1"
					break
				list1=splitter.split(line1)
				full_line=""
				for items1 in list1:
					full_line+=items1	
    				#~ logger.info('helper_f_get_list_type internal data --> full_line  %s' %full_line)
				variable_index=full_line.find(variable_name)
				if variable_index!= -1:
    					#~ logger.info('helper_f_get_list_type internal data --> variable found  %s' %variable_name)
					variable_index+=len(variable_name)
					if full_line[variable_index]=='=' :
						#check if it is list or object 
						if full_line.find("model.List")!=-1: # it is a list
    							#~ logger.info('helper_f_get_list_type internal data --> equalto found  ')
							start_index=full_line.find('.',full_line.find('.')+1)
							end_index=full_line.find('(',full_line.find('(')+1)
							ret_string=""
							if start_index==-1 or end_index==-1:
    								#~ logger.info('Error in processing ... is model file in correct format?')
								file.close()
								return "CCCCCCCCCCCCCCCCCCCC"
							index=start_index+1
							while index<end_index:
								ret_string+=full_line[index]
								index=index+1
    							#~ logger.info('helper_f_get_list_type internal data ret_string  at place 1 is  %s' %ret_string)
							if ret_string=="String":
								file.close()
    								#~ logger.info('helper_f_get_list_type returning result  %s' %ret_string)
								return ret_string
							if ret_string=="Object":
								start_index=full_line.find('(',full_line.find('(')+1)
								end_index=full_line.find(')')
								ret_string=""	
								if start_index==-1 or end_index==-1:
    									#~ logger.info('Error in processing ... is model file in correct format?')
									file.close()
									return "CCCCCCCCCCCCCCCCCCCC"
								index=start_index+1
								while index<end_index:
									ret_string+=full_line[index]
									index=index+1
								if ret_string=="":
									ret_string="AAAAAAAAAAAAAAA"
    									#~ logger.info('helper_f_get_list_type returning result  %s' %ret_string)
									return "AAAAAAAAAAAAAAAA"
								file.close()
    								#~ logger.info('helper_f_get_list_type returning result  %s' %ret_string)
								return ret_string
    							#~ logger.info('helper_f_get_list_type internal data ret_string at place 2 is %s' %ret_string)
						else: # it is an object or struct
    							#~ logger.info('helper_f_get_list_type internal data --> searching for object  ')
							start_index=full_line.find('(')
							end_index=full_line.find(',')
							ret_string=""
							if start_index==-1 or end_index==-1:
    								#~ logger.info('Error in processing ... is model file in correct format?')
								return "CCCCCCCCCCCCCCCCCCCC"
							index=start_index+1
							while index<end_index:
								ret_string+=full_line[index]
								index=index+1
    							#~ logger.info('helper_f_get_list_type internal data ret_string  at place 3 is  %s' %ret_string)
							return ret_string

	file.close()
    	#~ logger.info('helper_f_get_list_type returning result  %s' %result)
	return result

def rootclass_found_in_file(filepath,rootclass):
    	#~ logger.info('rootclass_found_in_file called with argument 1  %s' %filepath)
    	#~ logger.info('rootclass_found_in_file called with argument 2  %s' %rootclass)
	import re
	file=open(filepath)
	result="False"
	splitter=re.compile(r'[ ]*')
	flag="0"
	while 1 and flag=="0":
		line = file.readline()
		if not line:
       			break
		list=splitter.split(line)
		count=0
		final_list=""
		for items in list:
			final_list+=items

		if final_list.find("class")!=-1 or final_list.find("Class")!=-1:
			count=count+1	
		if final_list.find("model.RootObjectModel")!=-1:
			count=count+1	
		if final_list.find(rootclass)!=-1:
			count=count+1	
			
		if count==3:
			flag="1";
			result="True"
			break;

	file.close()
    	#~ logger.info('rootclass_found_in_file returning result  %s' %result)
	return result



# implementation of utilities for converting a model to xml mapping for compass ends here .............. 


# Modified on 21 august 2009
def generate_thrift_spec(typeinfo):
    try:
        return TYPE_SPEC_CACHE[typeinfo]
    except KeyError:
        pass

    #~ logger.info('Generating thrift spec for %s' % typeinfo.name)

    spec = [None, ]
    id_ = len(spec)


    def get_thrift_id(field):

        if field.attribute in DEFAULT_FIELDS:
            field.attribute.kwargs['thrift_id'] = \
                    list(DEFAULT_FIELDS).index(field.attribute) + 1

        else:
            field.attribute.kwargs['thrift_id'] += 10

        return field.attribute.kwargs['thrift_id']

    attributes = sorted(typeinfo.attributes,
                        key=get_thrift_id)

    global file_suffix1
    thrift_to_osis(typeinfo.name, attributes )

    for attribute in attributes:
        name = attribute.name
        attr = attribute.attribute
        aid = attr.kwargs['thrift_id']

        if aid < id_:
            raise RuntimeError

        while aid > id_:
            spec.append(None)
            id_ += 1

        assert len(spec) == aid

        args = FIELD_TYPE_ATTR_ARGS_MAP[type(attr)](attr)
        thrift_type = FIELD_TYPE_THRIFT_TYPE_MAP[type(attr)](attr)

        spec.append((aid, thrift_type, name, args, None, ))

        id_ = len(spec)
        ret = TYPE_SPEC_CACHE[typeinfo] = tuple(spec)

    return ret





def handle_list(attr, value):
    data = list()
    type_handler = TYPE_HANDLERS[type(attr.type_)]
    for item in value:
        data.append(type_handler(None, item))

    return data

def handle_dict(attr, value):
    data = dict()
    type_handler = TYPE_HANDLERS[type(attr.type_)]
    for k, v in value.iteritems():
        data[k] = type_handler(None, v)

    return data

TYPE_HANDLERS = {
    osis.model.String: lambda a, o: o,
    osis.model.Enumeration: lambda a, o: o,
    osis.model.GUID: lambda a, o: o,
    osis.model.Integer: lambda a, o: o,
    osis.model.Float: lambda a, o: o,
    osis.model.Boolean: lambda a, o: o,
    osis.model.List: handle_list,
    osis.model.Dict: handle_dict,
    osis.model.DateTime: lambda a, o:o,
    osis.model.Object: lambda a, o: object_to_dict(o),
}

def object_to_dict(object_):
    if isinstance(object_, EmptyObject):
        return None

    print 'see what gets printed'
    print object_


    data = dict()
    spec = type(object_).OSIS_MODEL_INFO

    for attribute in spec.attributes:
        attr = attribute.attribute

        try:
            value = getattr(object_, attr.name)
        except AttributeError:
            value = None

        if value is None:
            continue

        handler = TYPE_HANDLERS[type(attr)]

        value = handler(attr, value)
        if value is None:
            continue

        data[attr.name] = value

    return data


def load_dict(attr, data):
    result = dict()
    type_ = attr.type_
    handler = TYPE_SET_HANDLERS[type(type_)]

    for key, value in data.iteritems():
        result[key] = handler(type_, value)

    return result

def load_list(attr, data):
    result = list()
    type_ = attr.type_
    handler = TYPE_SET_HANDLERS[type(type_)]

    for item in data:
        result.append(handler(type_, item))

    return result

TYPE_SET_HANDLERS = {
    osis.model.String: lambda a, o: o,
    osis.model.Enumeration: lambda a, o: o,
    osis.model.GUID: lambda a, o: o,
    osis.model.Integer: lambda a, o: o,
    osis.model.Float: lambda a, o: o,
    osis.model.Boolean: lambda a, o: o,
    osis.model.Dict: load_dict,
    osis.model.Object: lambda a, o: dict_to_object(a.type_(), o),
    osis.model.DateTime: lambda a, o:o,
    osis.model.List: load_list,
}

def dict_to_object(object_, data):
    spec = type(object_).OSIS_MODEL_INFO

    for attribute in spec.attributes:
        attr = attribute.attribute

        try:
            value = data[attr.name]
        except KeyError:
            continue

        if value is None:
            continue

        handler = TYPE_SET_HANDLERS[type(attr)]

        value = handler(attr, value)
        if value is None:
            continue

        setattr(object_, attr.name, value)

    return object_

#import dict_time

class YamlSerializer(object):
    NAME = 'yaml'

    @staticmethod
    def serialize(object_):
        #~ logger.info('Object received for serializing: %s' %str(object_))
	t0=time.time()
        data = object_to_dict(object_)
	t1=time.time()
	t2=t1-t0
	#dict_time.td+=t2
        #logger.info('dict time is $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ : %s' %dict_time.td)
        #logger.info('Object before Serializing : %s' %str(data))
        #logger.info('Serializing object using YAML................$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #to_return = yaml.dump(data, default_flow_style=False)
	t0=time.time()
	to_return = dump(data, Dumper=Dumper)
	t1=time.time()
	t2=t1-t0
	#dict_time.ts+=t2
        #logger.info('serial time is $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ : %s' %dict_time.ts)
	#to_return = dump(data)

        #~ logger.info('Serialized object: \n%s' %str(to_return))
       #  file=open('/opt/qbase3/yaml_object', 'a')
        #~ file.write('\n****************************************************************\n')
        #~ file.write(to_return)
        #~ file.write('\n****************************************************************\n')
        #~ file.close()
	#logger.info('**%s**' %str(r_data))
	#logger.info("nothing happened$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
        return to_return
        #return yaml.dump(data, default_flow_style=False)

    @staticmethod
    def deserialize(type_, data):
        object_ = type_()
        #data = yaml.load(data)
	#data = load(data, Loader=Loader)
	data = load(data)
        dict_to_object(object_, data)
        return object_

    @staticmethod
    def class_structure_serialize(object_):
	#initializing the global vars to 0
	global class_dict
	class_dict={}
	global root_class
	root_class=""
	global class_order_dict
	class_order_dict={}
	global class_order_count
	class_order_count=0
        #object_type = type(object_)
        object_type = object_
	#~ logger.info("object type is %s"%object_type);
	#~ logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
	#~ logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
        #~ model_info = object_type.OSIS_MODEL_INFO
        global file_suffix1
        file_suffix1= model_info.get_name()
        spec = generate_thrift_spec(model_info)
	global class_dict
	#~ logger.info("class dict is %s"%str(class_dict));
	global root_class
	root_class=file_suffix1
	#~ logger.info("root class is %s"%file_suffix1);
	global class_dict
	global root_class
	result =  prepare_indexing_xml(class_dict,root_class)
	print result
	return result 
	
    @staticmethod
    def serialize_to_dictionary(object_):
        #~ logger.info('Object received for serializing: %s' %str(object_))
        data = object_to_dict(object_)
	data["id"]=data["guid"]
	to_return=str(data)
        #~ logger.info('Object to return : %s' %to_return)
	return to_return 
	

