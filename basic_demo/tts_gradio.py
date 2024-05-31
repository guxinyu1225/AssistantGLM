import ChatTTS
import torch
import gradio as gr
import numpy as np

chat = ChatTTS.Chat()
chat.load_models()

spk_stat = torch.load('/home/ma-user/work/model/ChatTTS/asset/spk_stat.pt')
rand_spk = torch.randn(768) * spk_stat.chunk(2)[0] + spk_stat.chunk(2)[1] 

params_infer_code = {
    'spk_emb': rand_spk, # add sampled speaker 
    'temperature': .3, # using custom temperature
    'top_P': 0.7, # top P decode
    'top_K': 20, # top K decode
}
params_refine_text = {'prompt': '[oral_2][laugh_0][break_6]'}
    
def infer(text):
    wav = chat.infer(text, 
        skip_refine_text=True, 
        params_refine_text=params_refine_text, 
        params_infer_code=params_infer_code
    )

    audio_data = np.array(wav[0]).flatten()
    sample_rate = 24000

    return (sample_rate, audio_data)

# text = ["最近深圳老是下雨，好烦哦，希望明天不会再下雨了",]
def main():

    with gr.Blocks() as demo:
        
        with gr.Column():
            input=gr.Textbox()
            output=gr.Audio(label="Transcription")
         
        submit_btn = gr.Button("Submit")
        submit_btn.click(
            infer,
            inputs=input,
            outputs=output
        )

    demo.launch(share=True)
   

if __name__ == '__main__':
    main()
