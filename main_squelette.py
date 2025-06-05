# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:00:28 2025

@author: JDION
"""

import sys
import os


dist_dir = os.path.join(os.path.dirname(__file__), "dist")
sys.path.insert(0, dist_dir)

import simulateur

SimulateurTraitement = simulateur.SimulateurTraitement
    
if __name__ == "__main__":
    simulateur = SimulateurTraitement()
    while True:
        t = input("Choisissez un traitement (A, B, C, D, E) ou 'Q' pour quitter : ").strip().upper()
        if t == 'Q':
            break
        try:
            resultat = simulateur.administrer_traitement(t)
            print(f"Traitement {t}: {'Succès' if resultat else 'Échec'}")
        except ValueError as e:
            print(e)
    


