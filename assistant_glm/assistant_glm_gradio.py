import gradio as gr
import faster_whisper
import torch
import os
from transformers import AutoTokenizer, AutoModel
import function_tools
import function_api
import ChatTTS
import zhconv
import numpy as np

def get_t2s(text):
    return zhconv.convert(text, 'zh-cn')

def transcribe(audio_file):
    segments, info = asr_model.transcribe(audio_file, beam_size=5)
    result_text = ""
    for segment in segments:
        result_text += segment.text

    result_text = get_t2s(result_text)
    return result_text

def run_conv_glm(query, tokenizer, history, model, functions_list=None, functions=None, return_function_call=True):
    if functions_list is None:
        response, history = model.chat(tokenizer, query, history=history)
        final_response = response
    else:
        system_info = {
            "role": "system",
            "content": "Answer the following questions as best as you can. You have access to the following tools:",
            "tools": functions,
        }
        available_functions = {func.__name__: func for func in functions_list}
        history = [system_info]

        response, history = model.chat(tokenizer, query, history=history)

        if not isinstance(response, str):
            function_call = response
            function_name = function_call["name"]
            function_to_call = available_functions[function_name]
            function_args = function_call['parameters']
            function_response = function_to_call(**function_args)

            if return_function_call:
                print(function_response)

            history = [{
                "role": "observation",
                "name": function_name,
                "content": function_response,
            }]
            response, history = model.chat(tokenizer, query, history=history)
            final_response = response
        else:
            final_response = response

    return final_response, history

def generate_audio(text, chat_model):
    wav = chat_model.infer(text, 
                     skip_refine_text=True, 
                     params_refine_text=params_refine_text, 
                     params_infer_code=params_infer_code
                     )
    
    audio_data = np.array(wav[0]).flatten()
    sample_rate = 24000

    return (sample_rate, audio_data)

# Initialize the ASR model
asr_model_path = "/home/ma-user/work/model/faster-whisper-base"
asr_model = faster_whisper.WhisperModel(asr_model_path)

# Initialize the chat model
MODEL_PATH = os.environ.get('MODEL_PATH', '/home/ma-user/work/model/chatglm3-6b')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map="auto").eval()

# Function call parameters
functions_list = [function_tools.get_weather, function_tools.convert_currency, function_tools.get_date]
functions=[function_api.weather_api_spec, function_api.exchange_rate_api_spec, function_api.date_api_spec]
return_function_call=True

# Initialize the TTS model
chat_tts = ChatTTS.Chat()
chat_tts.load_models()

# Initialize tts parameters
spk_stat = torch.load('/home/ma-user/work/model/ChatTTS/asset/spk_stat.pt')
rand_spk = torch.randn(768) * spk_stat.chunk(2)[0] + spk_stat.chunk(2)[1]   

params_infer_code = {
    'spk_emb': rand_spk, # add sampled speaker 
    'temperature': .3, # using custom temperature
    'top_P': 0.7, # top P decode
    'top_K': 20, # top K decode
}
params_refine_text = {'prompt': '[oral_2][laugh_0][break_6]'}

def chat_process(audio_file, history, chatbot_history):
    transcript = transcribe(audio_file)
    response, new_history = run_conv_glm(transcript, tokenizer, history, model, functions_list, functions, return_function_call)
    chatbot_history.append((transcript, response))
    audio_data = generate_audio(response, chat_tts)
    return chatbot_history, new_history, audio_data, transcript


def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Chat with a Large Language Model using Speech-to-Text and Text-to-Speech")
        chatbot = gr.Chatbot()
        history = gr.State([])

        with gr.Column():
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Speak to the model")
            transcribe_text = gr.Textbox(label="Transcription")
         
        submit_btn = gr.Button("Submit")
        audio_output = gr.Audio(label="Response Audio", autoplay=True)
        
        
        submit_btn.click(
            chat_process,
            inputs=[audio_input, history, chatbot],
            outputs=[chatbot, history, audio_output, transcribe_text]
        )

    demo.launch(share=True)

if __name__ == '__main__':
    main()
