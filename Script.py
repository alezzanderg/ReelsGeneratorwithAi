import os
import openai
import requests
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import (AudioFileClip, VideoFileClip, concatenate_videoclips, 
                            CompositeVideoClip, TextClip, ColorClip)
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las claves API desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
pexels_api_key = os.getenv("PEXELS_API_KEY")

# Directorios
BIBLIOTECA_DIR = 'biblioteca'
CONTENIDO_DIR = 'contenido'

# Crear carpeta contenido si no existe
if not os.path.exists(CONTENIDO_DIR):
    os.makedirs(CONTENIDO_DIR)

# Crear carpeta con fecha y hora actual dentro de contenido
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(CONTENIDO_DIR, timestamp)
os.makedirs(output_dir)

def generate_motivational_message():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente motivacional. Genera un mensaje motivacional para personas que quieren ser millonarios, con al menos 8 oraciones."},
            {"role": "user", "content": "Por favor, proporciona un mensaje motivacional."}
        ]
    )

    message = response.choices[0].message["content"]
    print("Mensaje Generado: ", message)
    return message

def convert_text_to_speech(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
    querystring = {"output_format": "mp3_44100_128"}

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2", 
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.00,
            "use_speaker_boost": True
        }
    }
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        audio_path = os.path.join(output_dir, "message.mp3")
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        print("Archivo de audio guardado como 'message.mp3'")
        return audio_path
    else:
        print("Error al convertir texto a voz:", response.status_code, response.text)
        return None

def download_pexels_videos(query, num_videos=5):
    url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": pexels_api_key
    }
    params = {
        "query": query,
        "per_page": num_videos
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        videos = response.json().get('videos', [])
        video_paths = []
        for i, video in enumerate(videos):
            video_url = video['video_files'][0]['link']
            video_path = os.path.join(output_dir, f"background_{i}.mp4")
            video_data = requests.get(video_url)
            with open(video_path, 'wb') as f:
                f.write(video_data.content)
            video_paths.append(video_path)
        return video_paths
    else:
        print("Error al descargar videos de Pexels:", response.status_code, response.text)
        return []

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_mp3(audio_path)
    audio.export("temp.wav", format="wav")
    audio_file = sr.AudioFile("temp.wav")

    with audio_file as source:
        audio_data = recognizer.record(source)

    # Using Google's speech recognition
    result = recognizer.recognize_google(audio_data, show_all=True)
    return result

def get_audio_duration(audio_file_path):
    audio = AudioFileClip(audio_file_path)
    duration = audio.duration
    return audio, duration

def check_video_durations(video_files, required_duration):
    total_duration = 0
    selected_videos = []
    for video_file in video_files:
        if total_duration >= required_duration:
            break
        clip = VideoFileClip(video_file)
        duration = clip.duration
        total_duration += duration
        selected_videos.append((video_file, duration))
    return total_duration, selected_videos

def format_duration(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes} minutos y {remaining_seconds} segundos"

def apply_opacity_and_aspect_ratio(clip, opacity=0.5, width=608, height=1080):
    clip = clip.set_opacity(opacity)
    clip = clip.resize(height=height)
    clip = clip.crop(width=width, height=height, x_center=clip.w / 2, y_center=clip.h / 2)
    return clip

def generate_subtitles(transcription_result):
    if not transcription_result or 'alternative' not in transcription_result:
        return []

    subtitles = []
    for alternative in transcription_result['alternative']:
        if 'transcript' in alternative and 'timestamps' in alternative:
            for timestamp in alternative['timestamps']:
                word = timestamp['word']
                start_time = timestamp['start_time']
                end_time = timestamp['end_time']
                subtitles.append((word, start_time, end_time))
    return subtitles

def create_subtitle_clips(subtitles, font_size=24, font_color='white', font='Arial', video_width=608):
    subtitle_clips = []
    for word, start_time, end_time in subtitles:
        txt_clip = TextClip(word, fontsize=font_size, color=font_color, font=font)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(start_time).set_end(end_time)
        subtitle_clips.append(txt_clip)
    return subtitle_clips

if __name__ == "__main__":
    # Generar mensaje motivacional usando OpenAI API
    message = generate_motivational_message()
    
    # Guardar mensaje en archivo de texto
    message_path = os.path.join(output_dir, "message.txt")
    with open(message_path, "w", encoding="utf-8") as text_file:
        text_file.write(message)
    print(f"Mensaje guardado como '{message_path}'")
    
    # Convertir texto a voz usando ElevenLabs API
    audio_file_path = convert_text_to_speech(message)
    
    if audio_file_path:
        # Descargar videos de Pexels
        video_files = download_pexels_videos("motivational landscape")

        # Obtener duración del audio
        audio_clip, audio_duration = get_audio_duration(audio_file_path)
        formatted_audio_duration = format_duration(audio_duration)
        print(f"La duración del archivo de audio '{audio_file_path}' es de {formatted_audio_duration}.")

        required_video_duration = audio_duration + 4

        total_video_duration, selected_videos = check_video_durations(video_files, required_video_duration)

        while total_video_duration < required_video_duration and len(video_files) > len(selected_videos):
            remaining_videos = [v for v in video_files if v not in [sv[0] for sv in selected_videos]]
            additional_duration, additional_videos = check_video_durations(remaining_videos, required_video_duration - total_video_duration)
            total_video_duration += additional_duration
            selected_videos.extend(additional_videos)

        if total_video_duration > required_video_duration:
            excess_duration = total_video_duration - required_video_duration
            selected_videos = sorted(selected_videos, key=lambda x: x[1], reverse=True)
            for i in range(len(selected_videos)):
                if selected_videos[i][1] > excess_duration:
                    selected_videos[i] = (selected_videos[i][0], selected_videos[i][1] - excess_duration)
                    break
                else:
                    excess_duration -= selected_videos[i][1]
                    selected_videos[i] = (selected_videos[i][0], 0)
            selected_videos = [v for v in selected_videos if v[1] > 0]
            total_video_duration = required_video_duration

        formatted_video_duration = format_duration(total_video_duration)
        print(f"\nLa duración total de los videos es de {formatted_video_duration}.")

        if total_video_duration >= required_video_duration:
            # Calcular y mostrar el tiempo de participación de cada video
            participation_time = required_video_duration / len(selected_videos)
            formatted_participation_time = format_duration(participation_time)
            print(f"Cada video tendrá una participación de {formatted_participation_time}.")

            for video_file, duration in selected_videos:
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                print(f"Video: {video_file}, Duración: {minutes} minutos y {seconds} segundos")

            # Aplicar opacidad y aspecto a los videos seleccionados
            video_clips = [apply_opacity_and_aspect_ratio(VideoFileClip(v[0]).subclip(0, v[1])) for v in selected_videos]

            # Combinar los clips de video y ajustar la duración del video combinado
            final_video = concatenate_videoclips(video_clips)
            final_video = final_video.set_duration(required_video_duration)

            # Añadir el audio al video, asegurando que comience en el segundo 2 del video
            final_video = CompositeVideoClip([final_video.set_audio(audio_clip.set_start(2))])

            # Transcribir el audio y generar los subtítulos
            transcription_result = transcribe_audio(audio_file_path)
            subtitles = generate_subtitles(transcription_result)
            subtitle_clips = create_subtitle_clips(subtitles)

            # Añadir subtítulos al video
            final_video = CompositeVideoClip([final_video] + subtitle_clips)

            # Renderizar el video combinado
            output_path = os.path.join(output_dir, 'background_combined.mp4')
            final_video.write_videofile(output_path, codec='libx264', fps=24)
            print(f"\nVideo combinado guardado como '{output_path}'.")

            # Simular la inserción del audio en el video
            audio_start_time = 2
            audio_end_time = audio_start_time + audio_duration
            print(f"El audio se reproducirá desde el segundo {audio_start_time} hasta el segundo {audio_end_time}.")
        else:
            print("Se necesitan más videos para cumplir con la duración requerida.")
