import librosa
import numpy as np
import csv
import os

def load_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    return y, sr

def calculate_seconds(y, sr):
    return len(y) // sr

def process_audio(y, sr, num_seconds):
    fft_data = np.zeros((num_seconds, 768))
    rgb_scores = np.zeros((num_seconds, 3))

    for i in range(num_seconds):
        audio_data = y[i * sr:(i + 1) * sr]
        fft = np.abs(np.fft.fft(audio_data)[:768])
        fft_data[i, :] = fft

        r_freqs, g_freqs, b_freqs = np.split(fft, 3)
        r_avg, g_avg, b_avg = np.mean(r_freqs), np.mean(g_freqs), np.mean(b_freqs)

        total = r_avg + g_avg + b_avg
        r_norm, g_norm, b_norm = (r_avg / total, g_avg / total, b_avg / total) if total != 0 else (0, 0, 0)
        rgb_scores[i, :] = [r_norm, g_norm, b_norm]

    return fft_data, rgb_scores

def calculate_rgb_statistics(rgb_scores):
    mean_rgb = np.mean(rgb_scores, axis=0)
    avg_rgb = np.average(rgb_scores, axis=0)
    unique_rgbs, counts = np.unique(rgb_scores, axis=0, return_counts=True)
    least_frequent_rgb = unique_rgbs[np.argmin(counts), :]
    top_12_rgbs = unique_rgbs[np.argsort(-counts)[:12], :]

    return mean_rgb, avg_rgb, least_frequent_rgb, top_12_rgbs

def normalize_rgb_256(rgb_values):
    return np.round(rgb_values * 255) + 1

def save_data_to_csv(filename, headers, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

def process_audio_file(audio_file):
    y, sr = load_audio_file(audio_file)
    num_seconds = calculate_seconds(y, sr)
    fft_data, rgb_scores = process_audio(y, sr, num_seconds)
    mean_rgb, avg_rgb, least_frequent_rgb, top_12_rgbs = calculate_rgb_statistics(rgb_scores)

    rgb_scores_256 = normalize_rgb_256(rgb_scores)
    fft_data_256 = normalize_rgb_256(fft_data)

    save_data_to_csv("fft_data.csv", ["Time (s)"] + [f"Frequency {i}" for i in range(768)], [[i] + row.tolist() for i, row in enumerate(fft_data_256)])
    save_data_to_csv("rgb_scores.csv", ["Time (s)", "R", "G", "B"], [[i] + row.tolist() for i, row in enumerate(rgb_scores_256)])

    rgb_stats = np.array([mean_rgb, avg_rgb, least_frequent_rgb] + top_12_rgbs.tolist())
    rgb_stats_256 = normalize_rgb_256(rgb_stats)
    labels = ["Mean", "Average", "Least Frequent"] + [f"Top {i+1}" for i in range(12)]
    save_data_to_csv("rgb_stats.csv", ["Metric", "R", "G", "B"], [[label] + row.tolist() for label, row in zip(labels, rgb_stats_256)])

