import json
import copy

def find_tool_by_function_name(function_name, tools):
    for tool in tools:
        if tool["function"]["name"] == function_name:
            return tool
    return None

def find_missing_parameters(function_name, curr_tools, tools):
    original_tool = find_tool_by_function_name(function_name, tools)
    curr_tool = find_tool_by_function_name(function_name, curr_tools)
    original_keys = set(original_tool["function"]["parameters"]["properties"].keys())
    curr_keys = set(curr_tool["function"]["parameters"]["properties"].keys())
    # Find tools that have been removed from the schema, indicating that they have previously been used
    missing_keys = original_keys - curr_keys
    return missing_keys

def remove_tool(function_name, curr_tools):
    for tool in curr_tools:
        if function_name in tool["function"]["parameters"]["properties"]:
            del tool["function"]["parameters"]["properties"][function_name]
        if function_name in tool["function"]["parameters"]["required"]:
            tool["function"]["parameters"]["required"].remove(function_name)
    return curr_tools

def insert_scratchpad_local(message, scratchpad, curr_tools, tools):
    """This function injects scratchpad values from local memory into the function call"""
    function = message.tool_calls[0].function
    # Appending missing scratchpad parameters to the message
    missing_parameter_keys = find_missing_parameters(function.name, curr_tools, tools)
    if missing_parameter_keys:
        missing_parameters = {}
        for key in missing_parameter_keys:
            missing_parameters[key] = scratchpad[key]
        original_parameters = json.loads(function.arguments)
        original_parameters.update(missing_parameters)
        function.arguments = json.dumps(original_parameters)
    return function

def insert_scratchpad_redis(message, scratchpad, curr_tools, tools):
    """This function injects scratchpad values from Redis into the function call"""
    function = message.tool_calls[0].function
    # Appending missing scratchpad parameters to the message
    missing_parameter_keys = find_missing_parameters(function.name, curr_tools, tools)
    if missing_parameter_keys:
        missing_parameters = {}
        for key in missing_parameter_keys:
            missing_parameters[key] = scratchpad.get(key)
        original_parameters = json.loads(function.arguments)
        original_parameters.update(missing_parameters)
        function.arguments = json.dumps(original_parameters)
    return function   

def store_value_local(scratchpad, function_name, results):
    if isinstance(results, str):
        scratchpad[function_name] = results
    else:
        scratchpad[function_name] = json.dumps(results)
    return scratchpad

def store_value_redis(scratchpad, function_name, results):
    if isinstance(results, str):
        scratchpad.set(function_name, results)
    else:
        scratchpad.set(function_name, json.dumps(results))
    return scratchpad