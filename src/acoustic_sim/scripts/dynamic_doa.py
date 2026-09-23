import pyroomacoustics as pra
import numpy as np
from scipy.io import wavfile
import os

audio_filename = "listen_test.wav" 

if not os.path.exists(audio_filename):
    print(f"Error: Could not find {audio_filename}.")
    exit()

fs, audio_signal = wavfile.read(audio_filename)

if len(audio_signal.shape) > 1:
    audio_signal = audio_signal[:, 0]
audio_signal = audio_signal.astype(np.float32)

room_dim = [10, 10, 5]
room = pra.ShoeBox(room_dim, fs=fs, max_order=0)

# إعداد المصفوفة
center = [5, 5, 0.1]
num_mics = 8
radius = 0.1
angles = np.arange(0, 2 * np.pi, 2 * np.pi / num_mics)
mic_positions = np.zeros((3, num_mics))
mic_positions[0, :] = center[0] + radius * np.cos(angles)
mic_positions[1, :] = center[1] + radius * np.sin(angles)
mic_positions[2, :] = center[2]
room.add_microphone_array(pra.MicrophoneArray(mic_positions, room.fs))

# إعداد المسار الحركي (مسار دائري حول المصفوفة)
flight_radius = 2.0
flight_height = 2.0
num_points = 50 
theta = np.linspace(0, 2 * np.pi, num_points)

trajectory_x = center[0] + flight_radius * np.cos(theta)
trajectory_y = center[1] + flight_radius * np.sin(theta)
trajectory_z = np.full(num_points, flight_height)

# تقسيم الصوت على نقاط المسار لتوليد تأثير الحركة
chunk_size = len(audio_signal) // num_points

print(f"Simulating dynamic flight path across {num_points} waypoints...")

for i in range(num_points):
    pos = [trajectory_x[i], trajectory_y[i], trajectory_z[i]]
    
    # تفريغ الصوت بالكامل إلا في الجزء الزمني الخاص بهذه النقطة
    chunk_signal = np.zeros_like(audio_signal)
    start_idx = i * chunk_size
    end_idx = (i + 1) * chunk_size if i < num_points - 1 else len(audio_signal)
    chunk_signal[start_idx:end_idx] = audio_signal[start_idx:end_idx]
    
    # إضافة المصدر الصوتي في هذه النقطة
    room.add_source(pos, signal=chunk_signal)

room.simulate()

output_audio = room.mic_array.signals.T
output_audio = output_audio / np.max(np.abs(output_audio))
output_audio = np.int16(output_audio * 32767)

wavfile.write('output_dynamic.wav', fs, output_audio)
print("Dynamic simulation complete! Saved as 'output_dynamic.wav'")
