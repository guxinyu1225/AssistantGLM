# AssistantGLM

## Introduction
AssistantGLM是2024-5-25华为昇思MindSpore训练营项目，是一个基于[faster-whisper](https://github.com/SYSTRAN/faster-whisper) + [ChatGLM3](https://github.com/THUDM/ChatGLM3) + [ChatTTS](https://github.com/2noise/ChatTTS) 的语音助手，使用function call实现查询天气、汇率、日期等功能。

[AssistantGLM_figure](/figure/AssistantGLM.png)

Function call 流程

## Usage

### Hardware Requirements
使用`faster-whisper-base`，无量化`chatglm3-6b`以及`ChatTTS`最低显存要求为16GB。

### Environmental Installation
    git clone https://github.com/guxinyu1225/AssistantGLM.git
    cd AssistantGLM
    pip install -r requirements.txt

### Loading checkpoint
请从 [Hugging Face Hub](https://huggingface.co/models) 或 [Model Scope](https://modelscope.cn/)网站下载模型权重文件。
并在代码中添加模型文件的路径。

注意安装完`ChatTTS`后，需要修改`ChatTTS/core.py`中的`_load`函数，添加ChatTTS的文件路径，示例：

    vocos_config_path: str = ‘/model/ChatTTS/config/vocos.yaml’
    ...

### Demo
运行

    python assistant_glm/assistant_glm_gradio

启动Gradio demo。

注意麦克风输入时等一会再点 Submit 按钮，不然可能会出错。

ChatTTS 目前好像说不了数字等字符，并且推理过程较慢，考虑后续可能换一个TTS模型。
