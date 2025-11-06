import numpy as np

# Encontrar as intensidades máximas
def peak_intensity(intensity):
    intensity_max = np.max(intensity)
    intensity_ind = np.argmax(intensity)
    return intensity_max, intensity_ind

# Encontrar os números de onda associados
def peak_wavenumber(wavenumbers, ind):
    wnmax = wavenumbers[ind]
    return wnmax

# calcula a largura a meia altura
def fwhm_calculate(intensity, wavenumbers):
    # Encontrar valores relevantes
    maxind = np.argmax(intensity)
    intmax = intensity[maxind]
    inthalf = intmax/2
    # dividir o espectro entre o lado esquerdo e o lado direito
    leftintensity = intensity[0:maxind]
    rightintensity = intensity[maxind:]
    lefthalfid = np.argmin(abs(leftintensity - inthalf))
    righthalfid = np.argmin(abs(rightintensity - inthalf))
    leftwnhalf = wavenumbers[lefthalfid]
    rightwnhalf = wavenumbers[maxind+righthalfid]
    return abs(rightwnhalf - leftwnhalf)


if __name__ == "__main__":
    wavenumbers = (np.array(np.linspace(500, 800))).T
    intensity = 1e7 * np.exp(-4 * np.log(2) * ((wavenumbers - 570) / 40) ** 2)
    intensitymax, intensitymaxid = peak_intensity(intensity)
    wnmax = peak_wavenumber(wavenumbers, intensitymaxid)
    fwhm = fwhm_calculate(intensity, wavenumbers)
    print("Intensidade máxima: ", intensitymax, "\nWavenumber at maximum intensity:", wnmax, "\nFWHM:", fwhm)
