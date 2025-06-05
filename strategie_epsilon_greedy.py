# fichier : simulateur/strategie_epsilon_greedy.py

from dist.simulateur import SimulateurTraitement
import matplotlib.pyplot as plt
import random
import csv

def enregistrer_resultats(nom_fichier, lignes):
   # with open(nom_fichier, mode='w', newline='') as f:
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)
        writer.writerow(["Patient", "Traitement", "Succes", "Strategie"])
        writer.writerows(lignes)

def strategie_epsilon_greedy(n=1000, epsilon=0.1):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    compte_admin = {t: 0 for t in traitements}
    compte_succes = {t: 0 for t in traitements}
    succes_total = 0
    lignes_csv = []

    # ⚙️ Initialisation : 1 essai de chaque traitement
    for i, t in enumerate(traitements):
        resultat = simulateur.administrer_traitement(t)
        compte_admin[t] += 1
        if resultat:
            compte_succes[t] += 1
            succes_total += 1
        lignes_csv.append([i + 1, t, int(resultat), "ε-Greedy"])

    # 🔁 Boucle principale
    for i in range(len(traitements), n):
        if random.random() < epsilon:
            t = random.choice(traitements)
        else:
            estimations = {
                t: compte_succes[t] / compte_admin[t]
                for t in traitements
            }
            t = max(estimations, key=estimations.get)

        resultat = simulateur.administrer_traitement(t)
        compte_admin[t] += 1
        if resultat:
            compte_succes[t] += 1
            succes_total += 1

        lignes_csv.append([i + 1, t, int(resultat), "ε-Greedy"])

    enregistrer_resultats("csv/resultats_epsilon_greedy.csv", lignes_csv)



    # 📊 Résultats
    print(f"\n📊 Résultats stratégie ε-greedy (ε = {epsilon}):")
    print(f"Patients totaux : {n}")
    print(f"Succès totaux : {succes_total}")
    print(f"Taux de succès global : {100 * succes_total / n:.2f}%\n")

    for t in traitements:
        print(f"Traitement {t} : utilisé {compte_admin[t]} fois, succès {compte_succes[t]}")

    # 📉 Graphique
    taux_par_traitement = [
        100 * compte_succes[t] / compte_admin[t]
        if compte_admin[t] > 0 else 0
        for t in traitements
    ]

    plt.bar(traitements, taux_par_traitement, color='cornflowerblue', edgecolor='black')
    plt.title(f"Taux de succès par traitement (ε-greedy, ε={epsilon})")
    plt.xlabel("Traitement")
    plt.ylabel("Taux de succès (%)")
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.savefig("images/epsilon_greedy.png")
    plt.close()

   # plt.show()



if __name__ == "__main__":
    strategie_epsilon_greedy(n=1000, epsilon=0.1)
