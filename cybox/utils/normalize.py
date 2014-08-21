# CybOX Object Normalization Methods
# For normalizing certain CybOX Objects to enable better correlation

# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import re
from cybox.objects.file_object import File
from cybox.objects.win_registry_key_object import WinRegistryKey
from cybox.objects.process_object import Process
from cybox.objects.mutex_object import Mutex

# Normalization-related mappings

# Windows-specific file normalization mappings
# Replace with CSIDL values, if possible
# As a backup, replace with Windows environment variable values
file_path_normalization_mapping = [{'regex_string' : '%[S|s][Y|y][S|s][T|t][E|e][M|m]%', 
                                    'replacement' : 'CSIDL_SYSTEM'},
                                    {'regex_string' : '%[A|a][P|p][P|p][D|d][A|a][T|t][A|a]%', 
                                     'replacement' : 'CSIDL_APPDATA'},
                                    {'regex_string' : '%[C|c][O|o][M|m][M|m][O|o][N|n][A|a][P|p][P|p][D|d][A|a][T|t][A|a]%', 
                                     'replacement' : 'CSIDL_COMMON_APPDATA'},
                                    {'regex_string' : '%[C|c][O|o][M|m][M|m][O|o][N|n][P|p][R|r][O|o][G|g][R|r][A|a][M|m][S|s]%', 
                                     'replacement' : 'CSIDL_COMMON_PROGRAMS'},
                                    {'regex_string' : '%[P|p][R|r][O|o][G|g][R|r][A|a][M|m][F|f][I|i][L|l][E|s][S|s]%',  
                                     'replacement' : 'CSIDL_PROGRAM_FILES'},
                                    {'regex_string' : '%[P|p][R|r][O|o][G|g][R|r][A|a][M|m][S|s]%',  
                                     'replacement' : 'CSIDL_COMMON_PROGRAMS'},
                                    {'regex_string' : '%[T|t][E|e][M|m][P|p]%', 
                                     'replacement' : 'TEMP'},
                                    {'regex_string' : '%[U|u][S|s][E|e][R|r][P|p][R|r][O|o][F|f][I|i][L|l][E|e]%', 
                                     'replacement' : 'CSIDL_PROFILE'},
                                    {'regex_string' : '%[P|p][R|r][O|o][F|f][I|i][L|l][E|e][S|s]%', 
                                     'replacement' : 'CSIDL_PROFILE'},
                                    {'regex_string' : '%[W|w][I|i][N|n][D|d][I|i][R|r]%', 
                                     'replacement' : 'CSIDL_WINDOWS'},
                                    {'regex_string' : '%[S|s][Y|y][S|s][T|t][E|e][M|m][R|r][O|o][O|o][T|t]%', 
                                     'replacement' : 'CSIDL_WINDOWS'},
                                    {'regex_string' : '[\w][:]\\\\[W|w][I|i][N|n][D|d][O|o][W|w][S|s]\\\\[S|s][Y|y][S|s][T|t][E|e][M|m]32', 
                                     'replacement' : 'CSIDL_SYSTEM'},
                                    {'regex_string' : '[\w][:]\\\\[W|w][I|i][N|n][D|d][O|o][W|w][S|s](?:(?!\\\\[S|s][Y|y][S|s][T|t][E|e][M|m]32))', 
                                     'replacement' : 'CSIDL_WINDOWS'},
                                    {'regex_string' : '[\w][:]\\\\[A-Z+a-z~ ()0-9\\\\]+\\\\[A|a][P|p][P|p][L|l][I|i][C|c][A|a][T|t][I|i][O|o][N|n] [D|d][A|a][T|t][A|a]', 
                                     'replacement' : 'CSIDL_APPDATA'},
                                    {'regex_string' : '[\w][:]\\\\[A-Z+a-z~ ()0-9\\\\]+\\\\[A|a][L|l][L|l] [U|u][S|s][E|e][R|r][S|s]\\\\[A|a][P|p][P|p][L|l][I|i][C|c][A|a][T|t][I|i][O|o][N|n] [D|d][A|a][T|t][A|a]', 
                                     'replacement' : 'CSIDL_COMMON_APPDATA'},
                                    {'regex_string' : '[\w][:]\\\\[A-Z+a-z~ ()0-9\\\\]+\\\\[A|a][L|l][L|l] [U|u][S|s][E|e][R|r][S|s]\\\\[S|s][T|t][A|a][R|r][T|t] [M|m][E|e][N|n][U|u]\\\\[P|p][R|r][O|o][G|g][R|r][A|a][M|m][S|s]', 
                                     'replacement' : 'CSIDL_COMMON_PROGRAMS'},
                                    {'regex_string' : '[\w][:]\\\\[A-Z+a-z~ ()0-9\\\\]+\\\\[T|t][E|e][M|m][P|p]', 
                                     'replacement' : 'TEMP'},
                                    {'regex_string' : '[\w][:]\\\\[U|u][S|s][E|e][R|r][S|s]\\\\[A-Z+a-z~ ()0-9]+', 
                                     'replacement' : 'CSIDL_PROFILE'},
                                    {'regex_string' : '^\w:\\\\{0,2}$', 
                                     'replacement' : '%SystemDrive%'},
                                    {'regex_string' : '^\w:\\\\[D|d][O|o][C|c][U|u][M|m][E|e][N|n][T|t][S|s] [A|a][N|n][D|d] [S|s][E|e][T|t][T|t][I|i][N|n][G|g][S|s]\\\\[A|a][L|l][L|l] [U|u][S|s][E|e][R|r][S|s]', 
                                     'replacement' : '%ALLUSERSPROFILE%'},
                                    {'regex_string' : '^\w:\\\\[P|p][R|r][O|o][G|g][R|r][A|a][M|m][D|d][A|a][T|t][A|a]', 
                                     'replacement' : '%ALLUSERSPROFILE%'}]

# Windows Registry Hive Abbreviated -> Full mappings
registry_hive_normalization_mapping = [{'regex_string' : '^[H|h][K|k][L|l][M|m]$',
                                        'replacement' : 'HKEY_LOCAL_MACHINE'},
                                       {'regex_string' : '^[H|h][K|k][C|c][C|c]$',
                                        'replacement' : 'HKEY_CURRENT_CONFIG'},
                                       {'regex_string' : '^[H|h][K|k][C|c][R|r]$',
                                        'replacement' : 'HKEY_CLASSES_ROOT'},
                                       {'regex_string' : '^[H|h][K|k][C|c][U|u]$',
                                        'replacement' : 'HKEY_CURRENT_USER'},
                                       {'regex_string' : '^[H|h][K|k][U|u]$',
                                        'replacement' : 'HKEY_USERS'}]

# Normalization-related methods

def perform_replacement(entity, mapping_list):
    '''Perform a replacement on the value of an entity using a replacement mapping, if applicable.'''
    # Make sure the entity has a value to begin with
    if not entity.value:
        return
    entity_value = entity.value
    # Attempt the replacement
    for mapping_dict in mapping_list:
        # Do the direct replacement, if applicable
        if 'search_string' in mapping_dict.keys():
            search_string = mapping_dict['search_string']
            replacement = mapping_dict['replacement']
            if search_string in entity_value:
                entity.value = entity_value.replace(search_string, replacement)
        # Do the regex replacement, if applicable
        if 'regex_string' in mapping_dict.keys():
            regex_string = mapping_dict['regex_string']
            replacement = mapping_dict['replacement']
            if re.search(regex_string, entity_value):
                entity.value = re.sub(regex_string, replacement, entity_value)

def normalize_object_properties(object_properties):
    '''Normalize the field values of certain ObjectProperties instances.
       
       Currently supports: File Objects
                             --File_Path field. Normalized for common Windows
                                                paths/environment variables.
                           Windows Registry Key Objects
                             --Registry Value/Data field. Normalized for common
                                                          Windows paths/environment
                                                          variables.
                             --Hive field. Normalized for full representation  
                                           from abbreviated form.
                                           E.g., HKLM -> HKEY_LOCAL_MACHINE.
                           Process Objects
                             --Image_Info/Path field. Normalized for common
                                                      Windows paths/environment
                                                      variables. '''
                           
    # Normalize file object properties/subclasses
    if isinstance(object_properties, File):
        # Normalize any windows-related file paths
        if object_properties.file_path:
            perform_replacement(object_properties.file_path, file_path_normalization_mapping)
    # Normalize windows registry key object properties
    elif isinstance(object_properties, WinRegistryKey):
        # Normalize any windows-related file paths in a registry key value
        if object_properties.values:
            for registry_value in object_properties.values:
                if registry_value.data:
                    perform_replacement(registry_value.data, file_path_normalization_mapping)
        # Normalize any short-hand hive values
        if object_properties.hive:
            perform_replacement(object_properties.hive, registry_hive_normalization_mapping)
    # Normalize process object properties/subclasses
    elif isinstance(object_properties, Process):
        # Normalize any windows-related file paths in the process image path
        if object_properties.image_info and object_properties.image_info.path:
            perform_replacement(object_properties.image_info.path, file_path_normalization_mapping)