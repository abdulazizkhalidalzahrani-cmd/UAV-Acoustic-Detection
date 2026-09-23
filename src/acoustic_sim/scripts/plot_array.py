import numpy as np
import matplotlib.pyplot as plt

# إعدادات المصفوفة (التي استخدمناها في المحاكاة)
center = [0, 0] # نضعها في المركز للرسم
num_mics = 8
radius = 0.1 # 10 سم
angles = np.arange(0, 2 * np.pi, 2 * np.pi / num_mics)

# حساب الإحداثيات (x, y)
x = radius * np.cos(angles)
y = radius * np.sin(angles)

# إعداد الرسم
plt.figure(figsize=(6, 6))
plt.scatter(x, y, c='red', s=150, marker='o', edgecolors='black', label='Microphones')

# رسم دائرة خفيفة لتبين الشكل الدائري
circle = plt.Circle((0, 0), radius, color='blue', fill=False, linestyle='--', alpha=0.5, label='Array Radius (10 cm)')
plt.gca().add_patch(circle)

# إضافة تفاصيل الرسم
plt.title('8-Microphone Uniform Circular Array (UCA)', fontsize=14, fontweight='bold')
plt.xlabel('X Coordinate (m)')
plt.ylabel('Y Coordinate (m)')
plt.axhline(0, color='grey', linewidth=0.5)
plt.axvline(0, color='grey', linewidth=0.5)
plt.grid(True, linestyle=':', alpha=0.7)
plt.axis('equal') # لضمان أن الدائرة تبدو دائرية وليست بيضاوية
plt.legend()

# عرض الرسمة
plt.show()

