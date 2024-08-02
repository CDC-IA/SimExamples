import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Sufixo dos dados e imagens
suffix = "TEST"

## Abrindo os dados
vel =np.load(f"data/vel{suffix}.npy")

samples = len(vel)

# Configurando o sinal no domínio da frequência e normalizando
n = 10
freq = fftfreq(samples, (n*60)/samples)[:samples//2]

vel_fft = fft(vel)

amp = 2.0/samples * np.abs(vel_fft[0:samples//2])
amp = amp/max(amp)

## Plotando FFT para análise
fig_fft = plt.figure()
plt.plot(freq,amp)
plt.suptitle("Avaliação do Sinal no Domínio da Frequência.")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Amplitude")
plt.xlim([0,0.6])
fig_fft.savefig(f"fft{suffix}.svg")