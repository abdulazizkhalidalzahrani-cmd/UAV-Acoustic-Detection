import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
import matplotlib.pyplot as plt

# 1. قراءة الملف
fs, audio_signal = wavfile.read('output_dynamic.wav')
audio_signal = audio_signal.T 

# 2. إعداد مصفوفة الميكروفونات
center = [5, 5, 0.1]
num_mics = 8
radius = 0.1
angles = np.arange(0, 2 * np.pi, 2 * np.pi / num_mics)
mic_positions = np.zeros((3, num_mics))
mic_positions[0, :] = center[0] + radius * np.cos(angles)
mic_positions[1, :] = center[1] + radius * np.sin(angles)
mic_positions[2, :] = center[2]

# 3. إعداد خوارزمية تحديد الاتجاه
nfft = 512  
doa = pra.doa.srp.SRP(L=mic_positions, fs=fs, nfft=nfft, c=343.0, num_src=1)

frame_step = fs // 10  
num_frames = audio_signal.shape[1] // frame_step
estimated_angles = []

window = np.hanning(nfft)

print("Running TDOA-based Direction Estimation (SRP-PHAT)...")

for i in range(num_frames):
    start_idx = i * frame_step
    end_idx = start_idx + nfft
    
    if end_idx > audio_signal.shape[1]:
        break
        
    frame = audio_signal[:, start_idx:end_idx]
    
    # تحويل الإشارة إلى نطاق الترددات (FFT)
    frame_windowed = frame * window
    X = np.fft.rfft(frame_windowed, axis=1)
    
    # === الحل هنا: إضافة البعد الثالث (عدد الإطارات = 1) ===
    X = X[:, :, np.newaxis] 
    
    # تطبيق الخوارزمية
    doa.locate_sources(X)
    
    angle_rad = doa.azimuth_recon[0]
    angle_deg = np.degrees(angle_rad)
    estimated_angles.append(angle_deg)

# 5. رسم النتائج
plt.figure(figsize=(10, 5))
plt.plot(estimated_angles, marker='.', linestyle='-', color='b')
plt.title('Estimated Drone Direction (DOA) over Time')
plt.xlabel('Time (Frames - 10 per sec)')
plt.ylabel('Angle (Degrees)')
plt.grid(True)
plt.yticks(np.arange(0, 361, 45)) 
plt.show()
