from pytube import YouTube
import os
import string
import sys
import subprocess
import tensorflow as tf
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

def get_video_info(video_url):
    yt = YouTube(video_url)
    author = yt.author
    title = yt.title
    directory_name = f"{title}{author}"
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    directory = directory_name.translate(remove_punctuation_map)
    return yt, directory

def create_directory(directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created.")
    except OSError:
        print(f"Failed to create directory '{directory}'.")

def download_video_audio(yt, directory):
    print(f'Downloading "{yt.title}" from the channel "{yt.author}"...')
    print('Please wait for a few minutes.')

    audio_title = yt.streams.filter(only_audio=True).first().download(directory, filename=f'{directory}_audio')
    video_title = yt.streams.filter(adaptive=True).first().download(directory, filename=f'{directory}_video')

    return audio_title, video_title

def merge_audio_video(audio_title, video_title, directory):
    resultant_video_path = os.path.join(os.getcwd(), directory, "resultant_video.mp4")
    cmd = f'ffmpeg -i "{os.path.normpath(video_title)}" -i "{os.path.normpath(audio_title)}" -c copy "{resultant_video_path}" -v quiet'
    subprocess.run(cmd, shell=True)
    return resultant_video_path

def download_subtitles(yt, directory):
    captions = yt.captions
    if len(captions) > 0:
        for subtitle in captions:
            subtitle_name = str(subtitle).split('"')[1]
            subtitle_path = os.path.join(directory, f"{subtitle_name}.srt")
            with open(subtitle_path, "w", encoding="utf-8") as f:
                f.write(subtitle.generate_srt_captions())
                print(f"Subtitle '{subtitle_name}' downloaded.")

def train_neural_network(directory):
    # Additional feature: Train a simple neural network using Tensorflow and Keras
    # Assume a simple dataset for demonstration
    # You can replace this with your own dataset and model
    X, y = prepare_data(directory)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model()
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
    print("Neural network training completed.")

def prepare_data(directory):
    # Additional feature: Prepare dummy data for the neural network
    # Replace this function with your own data preparation logic
    # For demonstration purposes, we assume X and y are features and labels
    X = tf.random.normal((100, 10))  # 100 samples with 10 features each
    y = tf.random.uniform((100, 1), 0, 2, dtype=tf.int32)  # Binary labels (0 or 1)
    return X, y

def build_model():
    # Additional feature: Build a simple neural network model using Keras
    model = tf.keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(10,)),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def main(video_url):
    yt, directory = get_video_info(video_url)
    create_directory(directory)

    audio_title, video_title = download_video_audio(yt, directory)
    resultant_video_path = merge_audio_video(audio_title, video_title, directory)
    download_subtitles(yt, directory)

    train_neural_network(directory)  # Train the neural network using the downloaded data

    print(f'Process completed. Resultant video saved at "{resultant_video_path}".')

if __name__ == "__main__":
    video_url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.youtube.com/watch?v=o2IJaj3nUmU'
    main(video_url)
