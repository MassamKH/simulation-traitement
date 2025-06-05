# fichier : simulateur/comparaison_strategies.py

from strategies import (
    strategie_uniforme,
    strategie_greedy,
    strategie_epsilon_greedy,
    strategie_hoeffding
)
import matplotlib.pyplot as plt

def main():
    n = 1000
    epsilon = 0.1

    print("\n⏳ Simulation des 4 stratégies en cours...\n")

    scores = {
        "Uniforme": strategie_uniforme(n, return_only_score=True),
        "Greedy": strategie_greedy(n, return_only_score=True),
        f"ε-Greedy ({epsilon})": strategie_epsilon_greedy(n, epsilon, return_only_score=True),
        "Hoeffding (UCB)": strategie_hoeffding(n, return_only_score=True)
    }

    noms = list(scores.keys())
    valeurs = [100 * s for s in scores.values()]

    # 📊 Bar Chart
    plt.figure(figsize=(9, 6))
    plt.bar(noms, valeurs, color=['gray', 'orange', 'cornflowerblue', 'lightcoral'], edgecolor='black')
    plt.title("Comparaison des taux de succès globaux")
    plt.ylabel("Taux de succès (%)")
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    for i, v in enumerate(valeurs):
        plt.text(i, v + 1, f"{v:.1f}%", ha='center')
    plt.tight_layout()
    plt.savefig("images/comparaison.png")
    plt.show()

if __name__ == "__main__":
    main()
