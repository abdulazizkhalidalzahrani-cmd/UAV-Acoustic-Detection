import pyroomacoustics as pra
import numpy as np
from scipy.io import wavfile
import os

audio_filename = "listen_test.wav" 

if not os.path.exists(audio_filename):
    print(f"Error: Could not find {audio_filename}. Please check the file name.")
    exit()

# 1. قراءة ملف الصوت
fs, audio_signal = wavfile.read(audio_filename)

# === الحل هنا: تحويل الصوت إلى مسار واحد (Mono) إذا كان ستيريو ===
if len(audio_signal.shape) > 1:
    audio_signal = audio_signal[:, 0]  # نأخذ المسار الأول فقط

# توحيد نوع البيانات لتجنب أخطاء الحسابات الرياضية
audio_signal = audio_signal.astype(np.float32)
# ==========================================================

# 2. إعداد الغرفة والمصفوفة
room_dim = [10, 10, 5]
room = pra.ShoeBox(room_dim, fs=fs, max_order=0)

center = [5, 5, 0.1]
num_mics = 8
radius = 0.1
angles = np.arange(0, 2 * np.pi, 2 * np.pi / num_mics)

mic_positions = np.zeros((3, num_mics))
mic_positions[0, :] = center[0] + radius * np.cos(angles)
mic_positions[1, :] = center[1] + radius * np.sin(angles)
mic_positions[2, :] = center[2]
room.add_microphone_array(pra.MicrophoneArray(mic_positions, room.fs))

# 3. وضع الدرون في وضع التحليق الثابت
hover_point = [7.0, 5.0, 2.0]
room.add_source(hover_point, signal=audio_signal)

print("Starting acoustic simulation... This might take a moment.")
# 4. تشغيل المحاكاة الفيزيائية
room.simulate()

# 5. حفظ المخرجات كملف صوتي واحد يحتوي على 8 قنوات
output_audio = room.mic_array.signals.T
output_audio = output_audio / np.max(np.abs(output_audio))
output_audio = np.int16(output_audio * 32767)

wavfile.write('output_8_channels.wav', fs, output_audio)
print("Simulation complete! Saved as 'output_8_channels.wav'")
