# ----------------------
#   Code by Radimich   
#   Date: 2025
#   Land:Larnevsk     
# ----------------------
import os
import gc
import re
import gradio as gr
import numpy as np
import subprocess

# Убедитесь, что папка существует
if not os.path.exists("./Эталонный звук/"):
    os.makedirs("./Эталонный звук/")

os.environ['HF_HOME'] = os.path.join(os.path.dirname(__file__), 'hf_download')
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

reference_wavs = ["Пожалуйста, выберите эталонное аудио или загрузите его самостоятельно"]
for name in os.listdir("./Эталонный звук/"):
    reference_wavs.append(name)


def change_choices():
    reference_wavs = ["Пожалуйста, выберите эталонное аудио или загрузите его самостоятельно"]

    for name in os.listdir("./Эталонный звук/"):
        reference_wavs.append(name)

    return {"choices": reference_wavs, "__type__": "update"}


def change_wav(audio_path):
    text = audio_path.replace(".wav", "").replace(".mp3", "").replace(".WAV", "")
    return f"./Эталонный звук/{audio_path}", text


def do_cloth(gen_text_input, ref_audio_input, model_choice_text, model_choice_re, ref_text_input):
    cmd = fr'.\py311_cu118\python.exe local_test.py -t "{gen_text_input}" -p "{ref_text_input}" -a "{ref_audio_input}" -l {model_choice_re} -lt {model_choice_text} '
    print(cmd)
    res = subprocess.Popen(cmd)
    res.wait()
    return "output.wav"


with gr.Blocks() as app_demo:
    gr.Markdown(
        """  
        project_url:https://github.com/Saburay/web_ui.git  
        """
    )
    gen_text_input = gr.Textbox(label="Proj", lines=4)
    model_choice_text = gr.Radio(
        choices=["ru", "en"], label="Сгенерировать текст", value="ru", interactive=True)
    wavs_dropdown = gr.Dropdown(label="Список эталонных аудиозаписей", choices=reference_wavs,
                                value="Выберите эталонное аудио или загрузите его самостоятельно", interactive=True)
    refresh_button = gr.Button("Обновите звук")
    refresh_button.click(fn=change_choices, inputs=[], outputs=[wavs_dropdown])
    ref_audio_input = gr.Audio(label="Reference Audio", type="filepath")
    ref_text_input = gr.Textbox(
        label="Reference Text",
        info="Leave blank to automatically transcribe the reference audio. If you enter text it will override automatic transcription.",
        lines=2,
    )
    model_choice_re = gr.Radio(
        choices=["ru", "en"], label="Эталонный звуковой язык", value="ru", interactive=True
    )
    wavs_dropdown.change(change_wav, [wavs_dropdown], [ref_audio_input, ref_text_input])
    generate_btn = gr.Button("Synthesize", variant="primary")

    audio_output = gr.Audio(label="Synthesized Audio")

    generate_btn.click(do_cloth, [gen_text_input, ref_audio_input, model_choice_text, model_choice_re, ref_text_input],
                       [audio_output])


def main():
    global app_demo
    print(f"Starting app...")
    app_demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()

#-------------------------------------------
# import os
# import gc
# import re
# import gradio as gr
# import numpy as np
# import subprocess
# #Конечно, не забудьте установить зависимости grado:  pip install -U gradio
# os.environ['HF_HOME'] = os.path.join(os.path.dirname(__file__), 'hf_download')
# # Установите переменную окружения HF_ENDPOINT
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
#
# reference_wavs = ["Пожалуйста, выберите эталонное аудио или загрузите его самостоятельно"]
# for name in os.listdir("./Эталонный звук/"):
#     reference_wavs.append(name)
#
#
# def change_choices():
#     reference_wavs = ["Пожалуйста, выберите эталонное аудио или загрузите его самостоятельно"]
#
#     for name in os.listdir("./Эталонный звук/"):
#         reference_wavs.append(name)
#
#     return {"choices": reference_wavs, "__type__": "update"}
#
#
# def change_wav(audio_path):
#     text = audio_path.replace(".wav", "").replace(".mp3", "").replace(".WAV", "")
#
#     # text = replace_speaker(text)
#
#     return f"./Эталонный звук/{audio_path}", text
#
#
# def do_cloth(gen_text_input, ref_audio_input, model_choice_text, model_choice_re, ref_text_input):
#     cmd = fr'.\py311_cu118\python.exe local_test.py -t "{gen_text_input}" -p "{ref_text_input}" -a "{ref_audio_input}" -l {model_choice_re} -lt {model_choice_text} '
#
#     print(cmd)
#     res = subprocess.Popen(cmd)
#     res.wait()
#
#     return "output.wav"
#
#
# with gr.Blocks() as app_demo:
#     gr.Markdown(
#         """
# project_url:https://github.com/open-mmlab/Amphion/tree/main/models/tts/maskgct
#
# """
#     )
#     gen_text_input = gr.Textbox(label="Proj", lines=4)
#     model_choice_text = gr.Radio(
#         choices=["ru", "en"], label="Сгенерировать текст", value="ru", interactive=True)
#     wavs_dropdown = gr.Dropdown(label="Список эталонных аудиозаписей", choices=reference_wavs, value="Выберите эталонное аудио или загрузите его самостоятельно",
#                                 interactive=True)
#     refresh_button = gr.Button("Обновите  звук")
#     refresh_button.click(fn=change_choices, inputs=[], outputs=[wavs_dropdown])
#     ref_audio_input = gr.Audio(label="Reference Audio", type="filepath")
#     ref_text_input = gr.Textbox(
#         label="Reference Text",
#         info="Leave blank to automatically transcribe the reference audio. If you enter text it will override automatic transcription.",
#         lines=2,
#     )
#     model_choice_re = gr.Radio(
#         choices=["ru", "en"], label="Эталонный звуковой язык", value="ru", interactive=True
#     )
#     wavs_dropdown.change(change_wav, [wavs_dropdown], [ref_audio_input, ref_text_input])
#     generate_btn = gr.Button("Synthesize", variant="primary")
#
#     audio_output = gr.Audio(label="Synthesized Audio")
#
#     generate_btn.click(do_cloth, [gen_text_input, ref_audio_input, model_choice_text, model_choice_re, ref_text_input],
#                        [audio_output])
#
#
# def main():
#     global app_demo
#     print(f"Starting app...")
#     app_demo.launch(inbrowser=True)
#
#
# if __name__ == "__main__":
#     main()
