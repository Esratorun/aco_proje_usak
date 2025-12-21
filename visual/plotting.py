import matplotlib.pyplot as plt

def plot_convergence(gecmis, kaydet=False, dosya_yolu=None):
    plt.figure(figsize=(10, 5))
    plt.plot(gecmis, color='indigo', marker='o')
    plt.title("ACO: En Kısa Süre Yakınsama Grafiği")
    plt.xlabel("İterasyon")
    plt.ylabel("Süre (Dakika)")
    plt.grid(True)
    if kaydet: plt.savefig(dosya_yolu)
    plt.show()