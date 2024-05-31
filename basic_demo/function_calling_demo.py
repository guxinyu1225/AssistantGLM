import os
import json
import platform
from transformers import AutoTokenizer, AutoModel
import function_tools
import function_api

MODEL_PATH = os.environ.get('MODEL_PATH', 'your_path_to_chatglm_model')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map="auto").eval()

def run_conv_glm(query,tokenizer, history, model,functions_list=None, functions=None, return_function_call=True):
 
    # 如果没有外部函数库，则执行普通的对话任务
    if functions_list == None:
        response, history = model.chat(tokenizer, query, history=history)
        final_response = response
 
    # 若存在外部函数库，则需要灵活选取外部函数并进行回答
    else:
        # 创建调用外部函数的system_message
        system_info = {
            "role": "system",
            "content": "Answer the following questions as best as you can. You have access to the following tools:",
            "tools": functions,
        }
 
        # 创建外部函数库字典
        available_functions = {func.__name__: func for func in functions_list}
        history=[system_info]
 
        ## 第一次调用，目的是获取函数信息
        response,history = model.chat(tokenizer, query, history=history)

        if not isinstance(response,str):
             # 需要调用外部函数
            function_call = response
 
            # 获取函数名
            function_name = function_call["name"]
 
            # 获取函数对象
            fuction_to_call = available_functions[function_name]
 
            # 获取函数参数
            function_args = function_call['parameters']
 
            # 将函数参数输入到函数中，获取函数计算结果
            function_response = fuction_to_call(**function_args)
       
 
            ## 第二次调用，带入进去函数
            # role="observation" 表示输入的是工具调用的返回值而不是用户输入
            # role:user,system,assistant,observation
            if return_function_call:
                print(function_response)

            history=[]
            history.append(
                {
                    "role": "observation",#设置观察着角色
                    "name": function_name,
                    "content": function_response,#将函数调用返回的结果再次给到大模型，由模型进行整理后再给出更加易用理解，可读性更强的答案，否则返回的就是API直接返回的内容。
                }
            )  
            response, history = model.chat(tokenizer, query, history=history)
            final_response=response
        
        else:
            final_response = response
 
    return final_response,history

def chat_with_glm(tokenizer, model, functions_list=None, functions=None, return_function_call=True):
    
    welcome_prompt = "Welcome to use ChatGLM, input 'stop' to terminate chat."
    print(welcome_prompt)

    history=[]
    while True:
        query = input("user: ")
        if query == "stop":
            break
        
        response,history = run_conv_glm(query, tokenizer, history, model,functions_list, functions, return_function_call)
        print(f"GLM: {response}")


def main():
    history=[]
    functions_list = [function_tools.get_weather, function_tools.convert_currency, function_tools.get_date]
    functions=[function_api.weather_api_spec, function_api.exchange_rate_api_spec, function_api.date_api_spec]
    chat_with_glm(tokenizer, model, functions_list=functions_list, functions=functions, return_function_call=True)

if __name__ == "__main__":
    main()

