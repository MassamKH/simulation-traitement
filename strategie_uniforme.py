# simulateur/strategie_uniforme.py

import random
import matplotlib.pyplot as plt
from dist.simulateur import SimulateurTraitement

import csv

def enregistrer_resultats(nom_fichier, lignes):
    with open(nom_fichier, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Patient", "Traitement", "Succes", "Strategie"])
        writer.writerows(lignes)



def strategie_uniforme(n=1000):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    succes_total = 0
    compte_traitements = {t: 0 for t in traitements}
    compte_succes = {t: 0 for t in traitements}

    lignes_csv = []

    for i in range(n):
        t = random.choice(traitements)

        resultat = simulateur.administrer_traitement(t)
        lignes_csv.append([i + 1, t, int(resultat), "Uniforme"])


        compte_traitements[t] += 1
        if simulateur.administrer_traitement(t):
            compte_succes[t] += 1
            succes_total += 1

        enregistrer_resultats("csv/resultats_uniforme.csv", lignes_csv)

    # Résultats textuels
    print("\n📊 Résultats stratégie uniforme :")
    print(f"Nombre total de patients : {n}")
    print(f"Succès total : {succes_total}")
    print(f"Taux de succès global : {100 * succes_total / n:.2f}%\n")


    for t in traitements:
        print(f"Traitement {t} : utilisé {compte_traitements[t]} fois, succès {compte_succes[t]}")

    # Graphique
    taux_par_traitement = [
        100 * compte_succes[t] / compte_traitements[t]
        if compte_traitements[t] > 0 else 0
        for t in traitements
    ]

    plt.bar(traitements, taux_par_traitement, color='lightgreen', edgecolor='black')
    plt.title("Taux de succès par traitement (stratégie uniforme)")
    plt.xlabel("Traitement")
    plt.ylabel("Taux de succès (%)")
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig("images/uniforme.png")
    plt.close()
    #plt.show()

if __name__ == "__main__":
    strategie_uniforme()
