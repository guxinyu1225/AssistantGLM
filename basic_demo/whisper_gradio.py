import faster_whisper
import gradio as gr 

model_path = "./model/faster-whisper-v3"
model = faster_whisper.WhisperModel(model_path)


def transcribe(audio):

    segments, info = model.transcribe(audio, beam_size=5)
    result_text = ""
    for segment in segments:
        result_text += segment.text
    
    return result_text

def main():

    iface = gr.Interface(
        title = 'ASR Gradio Web UI', 
        fn=transcribe, 
        inputs=gr.Audio(sources="microphone", type="filepath"),
        outputs=gr.Textbox(label="Transcription"),
        live=True
    )
    iface.launch(share=True)

if __name__ == '__main__':
    main()

