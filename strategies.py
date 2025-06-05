# fichier : simulateur/strategies.py

import random
import math
import matplotlib.pyplot as plt
from dist.simulateur import SimulateurTraitement

def strategie_uniforme(n=1000, return_only_score=False):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    succes_total = 0

    for _ in range(n):
        t = random.choice(traitements)
        if simulateur.administrer_traitement(t):
            succes_total += 1

    if return_only_score:
        return succes_total / n

    print("\nStrat. uniforme :", f"Succès totaux : {succes_total}")
    return succes_total / n

def strategie_greedy(n=1000, return_only_score=False):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    admin = {t: 0 for t in traitements}
    succes = {t: 0 for t in traitements}
    total = 0

    for t in traitements:
        if simulateur.administrer_traitement(t):
            succes[t] += 1
            total += 1
        admin[t] += 1

    for _ in range(len(traitements), n):
        estimations = {t: succes[t] / admin[t] for t in traitements}
        best = max(estimations, key=estimations.get)
        if simulateur.administrer_traitement(best):
            succes[best] += 1
            total += 1
        admin[best] += 1

    if return_only_score:
        return total / n

    print("\nStrat. greedy :", f"Succès totaux : {total}")
    return total / n

def strategie_epsilon_greedy(n=1000, epsilon=0.1, return_only_score=False):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    admin = {t: 0 for t in traitements}
    succes = {t: 0 for t in traitements}
    total = 0

    for t in traitements:
        if simulateur.administrer_traitement(t):
            succes[t] += 1
            total += 1
        admin[t] += 1

    for _ in range(len(traitements), n):
        if random.random() < epsilon:
            t = random.choice(traitements)
        else:
            estimations = {t: succes[t] / admin[t] for t in traitements}
            t = max(estimations, key=estimations.get)

        if simulateur.administrer_traitement(t):
            succes[t] += 1
            total += 1
        admin[t] += 1

    if return_only_score:
        return total / n

    print("\nStrat. ε-greedy :", f"Succès totaux : {total}")
    return total / n

def strategie_hoeffding(n=1000, return_only_score=False):
    simulateur = SimulateurTraitement()
    traitements = ['A', 'B', 'C', 'D', 'E']
    admin = {t: 0 for t in traitements}
    succes = {t: 0 for t in traitements}
    total = 0

    for t in traitements:
        if simulateur.administrer_traitement(t):
            succes[t] += 1
            total += 1
        admin[t] += 1

    for i in range(len(traitements), n):
        ucb = {
            t: (succes[t] / admin[t]) + math.sqrt(math.log(i + 1) / (2 * admin[t]))
            for t in traitements
        }
        best = max(ucb, key=ucb.get)
        if simulateur.administrer_traitement(best):
            succes[best] += 1
            total += 1
        admin[best] += 1

    if return_only_score:
        return total / n

    print("\nStrat. Hoeffding (UCB) :", f"Succès totaux : {total}")
    return total / n
