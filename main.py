import random
import copy

################################################################
### CLASSES ####   Merci d'initialiser toutes les classes ici. #
################################################################

class Carte:                                                                # Classe pour instancer des objets cartes
    def __init__(self, suite, valeur):                                      # contenant leur suite, numéro, une méthode
        self.suite = suite                                                  # pour calculer le nombre de points
        self.valeur = valeur                                                # et afficher leur nom complet

    def affiche_carte(self):
        return(str(self.valeur) + " de " + self.suite)

    def points(self,joueur):
        if self.valeur == "valet" or self.valeur == "dame" or self.valeur == "roi":
            return 10
        elif self.valeur == "as":
            if joueur.difficulte == 0:
                choix = int(input("1 ou 11 points ? "))
                while choix != 1 and choix != 11:
                    choix = int(input("1 ou 11 points ? "))
                return choix
            else:
                if joueur.score <= 10:
                    print(joueur.name,"choisit que son",self.affiche_carte(),"vaut 11 points !")
                    return 11
                else:
                    print(joueur.name,"choisit que son",self.affiche_carte(),"vaut 11 points !")
                    return 1
        else:
            return self.valeur
    
class Joueur:
    def __init__(self,name="player",difficulte=0,score=0,liste_cartes=[],en_jeu=True,argent=100,mise=0):
        self.name = name
        self.score = score
        self.liste_cartes = liste_cartes
        self.argent = argent
        self.en_jeu = en_jeu
        self.mise = mise
        self.difficulte = difficulte                                        # Si difficulte = 0, le joueur est contrôlé par l'utilisateur
                                                                            # Si difficulte est supérieur, il sera contrôlé par l'IA

                                                                            # Affiche une phrase aléatoire lorsque le joueur est éliminé.
    def phrase_elimination(self):
        Phrases =   [self.name+" est terriblement endetté. Il est obligé de quitter la table.",
                    self.name+" reçoit un appel de son banquier et doit s'absenter. Il est probable qu'il ne revienne pas.",
                    "Une trappe s'ouvre brusquement sous la chaise de "+self.name+". Plus personne ne le revit après cet incident.",
                    "Des hommes habillés en noir attrapent "+self.name+" par les bras, et l'emmènent en dehors du bar.",
                    self.name+" dit qu'il doit faire un tour au petit coin. Étrangement, il passe par la porte d'entrée. Il s'est sûrement discrètement éclipsé du bar.",
                    self.name+" commence à s'énerver, mais il renverse son verre de whisky sur sa chemise Lacoste. Dépité, il se retire de la table.",
                    '"Attendez ! Je peux encore gagner !"'+" s'exclame "+self.name+". Alors qu'il dit cela, un as de trèfle tombe de sa manche. "+self.name+" est expulsé du bar pour tentative de tricherie.",
                    "Des agents de police arrêtent "+self.name+" pour évasion fiscale. Ces parties de Blackjack ne lui ont pas permis d'échapper au fisc.",
                    self.name+" est retiré du bar car il a présenté un faux pass sanitaire",
                    self.name+", ruiné, retire son masque : il s'agissait en réalité de Jack Black, qui était en asile politique, et qui pensait que la chance allait lui sourire en jouant à son jeu éponyme !"]
        print(Phrases[random.randint(0,len(Phrases)-1)])
                        
                 

###################################################################
### FONCTIONS ###   Merci d'initialiser toutes les fonctions ici. #
###################################################################

#-------Fonctions concernant les cartes---------#

def paquet():                                                               # crée un paquet de 52 cartes rangées dans une liste
    L = []
    suites = ["pique", "carreau", "coeur", "trèfle"]
    for i in suites:
        L.append(Carte(i,"as"))
        for k in range(2,11):
            L.append(Carte(i,k))
        L.append(Carte(i,"valet"))
        L.append(Carte(i,"dame"))
        L.append(Carte(i,"roi"))
    return L

def initPioche(n):                                                          # Créé une pioche faite de n paquets de 52 cartes mélangées
    L = []
    for i in range(n):
        L.extend(paquet())
    random.shuffle(L)
    return L

def piocheCarte(pioche,nb_cartes):                                          # Pioche nb_cartes dans une liste de cartes donnée en argument, supprime ces cartes de la liste
    L = []                                                                  # et renvoie la liste des cartes piochées
    for i in range(nb_cartes):
        L.append(pioche[0])
        pioche.pop(0)
    return L


#--Fonctions concernant la gestion de la partie-#

def init_joueur(nb_joueurs,nb_ia):                                                         # Crée une liste de n joueurs (classe Joueur) nommés par l'utilisateur
    L = []

    for i in range(nb_joueurs):
        print("Joueur",i+1,":",end=" ")
        L.append(Joueur(input()))
        print("=" * 75)
    for i in range(nb_ia):
        print("Joueur",nb_joueurs+i+1,"(IA) :",end=" ")
        nom = input()
        difficulte = int(input("Quelle difficulté ? (de 1 à 4) : "))
        while difficulte < 1 or difficulte > 4:
            print("Veuillez entrer une difficulté correcte.")
            difficulte = int(input("Quelle difficulté ? (de 1 à 4) :"))
        L.append(Joueur(nom,difficulte))
        print("=" * 75)

    return L

def premierTour(joueurs):                                                   # Réinitialise le score de chaque joueur, leur fait piocher 2 cartes chacun, les ajoute à leur main et modifie leur score
    for i in range(len(joueurs)):
        joueurs[i].score = 0
        joueurs[i].liste_cartes = []
        cartes_piochees = piocheCarte(pioche,2)
        joueurs[i].liste_cartes.extend(cartes_piochees)
        print(joueurs[i].name," pioche un ",cartes_piochees[0].affiche_carte()," et un ",cartes_piochees[1].affiche_carte(),". ",sep = "")
        for f in range(2):
            joueurs[i].score += cartes_piochees[f].points(joueurs[i])
        if joueurs[i].score > 21:                                           # Au cas où un joueur pioche directement 2 as et décide d'avoir 22 points
            joueurs[i].en_jeu == False
            print(joueurs[i].name,"a perdu !")
        if joueurs[i].score == 21:
            print(joueurs[i].name,"a 21 points ! Il reçoit 20% de l'argent qu'il lui reste et ne jouera pas lors de cette partie.")
            joueurs[i].en_jeu = False
            joueurs[i].score = 1
            joueurs[i].argent += int(0.2*joueur.argent)
            
def gagnants(joueurs):                                                       # Renvoie l'objet joueur qui a le plus haut score en dessous de 21
    for i in joueurs:
        if i.score <= 21:
            gagnant = i
    for i in range(len(joueurs)):
        if joueurs[i].score > gagnant.score and joueurs[i].score <= 21:
            gagnant = joueurs[i]
    liste_gagnants = []
    for joueur in joueurs:
        if joueur.score == gagnant.score:
            liste_gagnants.append(joueur)
    return liste_gagnants

def continuer(joueur,liste_joueurs):                                        # Demande au joueur si il souhaite continuer, renvoie True si oui et False si non
    if joueur.difficulte == 0:                                              # Si le joueur est une IA, la fonction renvoie automatiquement sa réponse
        entree = input("Souhaitez-vous continuer ? (oui/non) ")
        while entree != 'oui' and entree != 'non':
            entree = input("Souhaitez-vous continuer ? (oui/non) ")
        if entree == 'oui':
            return True
        else:
            return False
    elif joueur.difficulte == 1:
        if IA_alea():
            print(joueur.name,"continue.")
            return True
        else:
            print(joueur.name,"s'arrête.")
            return False
    elif joueur.difficulte == 2:
        if IA_stupide():
            print(joueur.name,"continue.")
            return True
        else:
            print(joueur.name,"s'arrête.")
            return False
    elif joueur.difficulte == 3:
        if IA_intelligent(joueur.score):
            print(joueur.name,"continue.")
            return True
        else:
            print(joueur.name,"s'arrête.")
            return False
    elif joueur.difficulte == 4:
        if IA_supreme(joueur.score,liste_joueurs):
            print(joueur.name,"continue.")
            return True
        else:
            print(joueur.name,"s'arrête.")
            return False

def tourJoueur(joueur,num_tour):                                            # Fait le tour d'un joueur : il choisit s'il continue ou non, et si il continue il
    print("\n" + "="*33 + "Tour n°",num_tour, "="*33,sep="")                # pioche une carte. La fonction vérifie si le joueur a perdu ou non, et supprime
    print("Tour de",joueur.name)                                            # le joueur de la liste s'il abandonne ou dépasse 21.
    print("Score :",joueur.score)
    if continuer(joueur,liste_joueurs):
        carte_piochee = piocheCarte(pioche,1)
        print(joueur.name,'pioche un',carte_piochee[0].affiche_carte())
        joueur.liste_cartes.extend(carte_piochee)
        joueur.score += carte_piochee[0].points(joueur)

        if joueur.score > 21:
            print(joueur.name,"a perdu !")
            joueur.en_jeu = False
    else:
        joueur.en_jeu = False

def tourComplet(liste_joueurs,num_tour) :                                   # Fait faire un tour à chaque joueur
    for i in liste_joueurs:
        if i.en_jeu and partieFinie(liste_joueurs) == False:
            tourJoueur(i,num_tour)
    print("=" * 75)
        
def partieFinie(liste_joueurs) :                                            # Test pour savoir si la partie est finie (s'il reste ou non un seul joueur ou si un joueur a 21 points); renvoie True si elle est finie
    total_en_jeu = 0
    for joueur in liste_joueurs:
        if joueur.en_jeu:
            total_en_jeu += 1
        if joueur.score == 21:
            return True
    if total_en_jeu < 1:
        return True
    else:
        return False

def partieComplete(liste_joueurs):                                                      # Appelle la fonction tourComplet jusqu'à-ce que la partie soit finie
    num_tour = 1
    premierTour(liste_joueurs)
    mises = 0
    for joueur in liste_joueurs:
        if joueur.difficulte == 0 and partieFinie(liste_joueurs) == False and joueur.en_jeu:
            print(joueur.name,"a",joueur.score,"points. Il lui reste",joueur.argent,"kopecs. Combien misez-vous ? ",end="")
            mise_joueur = int(input())
            while mise_joueur < 0 or mise_joueur > joueur.argent:                       # Demande au joueur combien il mise et filtre sa mise tant qu'elle est négative ou
                mise_joueur = int(input("Veuillez entrer une valeur correcte."))        # supérieure à son argent.
            joueur.mise = mise_joueur
        elif joueur.difficulte == 1 and partieFinie(liste_joueurs) == False and joueur.en_jeu:  # On appelle les fonctions pour déterminer la mise de chaque IA
            mise_joueur = choix_mise_fixe(joueur.argent)
            print(joueur.name,"a",joueur.score,"points. Il lui reste",joueur.argent,"kopecs. Il mise",mise_joueur,"kopecs.")
            joueur.mise = mise_joueur
        elif joueur.difficulte == 2 and partieFinie(liste_joueurs) == False and joueur.en_jeu:
            mise_joueur = choix_mise_pourcentage(joueur.argent)
            print(joueur.name,"a",joueur.score,"points. Il lui reste",joueur.argent,"kopecs. Il mise",mise_joueur,"kopecs.")
            joueur.mise = mise_joueur
        elif partieFinie(liste_joueurs) == False and joueur.en_jeu:
            mise_joueur = choix_mise_supreme(joueur.argent,joueur.score)
            print(joueur.name,"a",joueur.score,"points. Il lui reste",joueur.argent,"kopecs. Il mise",mise_joueur,"kopecs.")
            joueur.mise = mise_joueur
        mises += joueur.mise                                                            # On ajoute la somme de chaque mise dans une variable
        joueur.argent -= joueur.mise                                                    # On retire la mise de chaque joueur de leur porte-feuille
    while partieFinie(liste_joueurs) == False:                                          # Des tours se lancent en boucle jusqu'à ce que l'utilisateur décide d'arrêter
        tourComplet(liste_joueurs,num_tour)
        num_tour += 1
        
    liste_gagnants = gagnants(liste_joueurs)
    for gagnant in liste_gagnants:
        gagnant.argent += int(mises / len(liste_gagnants)) + gagnant.mise       # Les mises sont réparties entre chaque gagnant et chaque gagnant remporte
                                                                                # sa mise initiale.
        
#---------Fonctions concernant les IA-----------#

def IA_alea():
    A = random.randint(0,1)     
    if A == 0 :
        return True      # IA continue
    else :
        return False     # IA arrête

def IA_stupide():
    L=[0,0.5,1]
    i = random.randint(0,2)
    if L[i] == 0 :
        return False       # IA s'arrête
    elif L[i] == 1 :
        return True        # IA continue
    elif L[i] == 0.5 :
        return(IA_alea())  # IA a 1 chance sur 2 de continuer / s'arrêter

def IA_intelligent(valeur_main):   
    proba = round((valeur_main-2)*0.0556,1)
    if proba < 0.5 :
        return True         # IA continue --> il pioche
    elif proba > 0.5 :
        return False        # IA s'arrête
    else :
        return(IA_alea())   # IA a 1 chance sur 2 de continuer / s'arrêter

def IA_supreme(valeur_main,liste_joueurs):
    compteur = 0
    for joueur in liste_joueurs:                    # L'IA continue si son score est inférieur à celui d'un des autres joueurs
        if valeur_main < joueur.score and joueur.en_jeu:
            compteur += 1
    if compteur == len(liste_joueurs) :
        return True
    elif valeur_main < 15 :                         # Si personne n'a un meilleur score que l'IA, elle s'arrête dès qu'elle a plus de 15 points.  
        return True         # IA continue
    else :
        return False        # IA s'arrête
    
#----------------Fonctions choix de mise pour IA-----------------#
    
def choix_mise_fixe(mise_initiale):                                     # L'IA choisit de miser 10, sauf si il lui reste moins de 10 kopecs.
    if mise_initiale >= 10 :
        return 10
    else :
        return 1

def choix_mise_pourcentage(mise_initiale):                              # L'IA mise toujours 20% de son argent
    return(int(mise_initiale*0.2))

def choix_mise_intelligent(mise_initiale,valeur_main):                  # L'IA choisit de miser selon une formule trouvée par Arthur
    if valeur_main <= 20 :
        mise = round((valeur_main-2)*5.556,1)
    else :
        mise = mise_initiale
    return(mise)
    
def choix_mise_supreme(mise_initiale,valeur_main):                      # L'IA mise un certain pourcentage de son argent en fonction de son score
    if 10 <= valeur_main <= 14:                                         # et de ses chances de gagner avec une telle main
        mise = int(mise_initiale * 0.15)
    elif valeur_main < 10 or 16 <= valeur_main <= 18 :
        mise = int(mise_initiale * 0.05)
    elif valeur_main == 21:
        mise = int(mise_initiale * 0.95)
    else:
        mise = int(mise_initiale * 0.25)
    return(mise)

#-----------------Fonctions phrases aléatoires-------------------#

def phraseDebutPartie(liste_joueurs):
    Phrases =   ["Alors que le barista tente de faire comprendre aux joueurs que le bar va bientôt fermer, ces derniers se lancent dans une nouvelle partie.",
                "Les perdants grincent des dents. Mais, loin d'être défaitistes, ils espèrent obtenir leur revanche dans une nouvelle partie.",
                """"La partie était truquée !", s'exclame un des clients du bar. Qu'il ait raison ou non, les joueurs reprennent leurs paris.""",
                "La maison offre un verre au gagnant du tour précédent. Ce dernier, un peu saoul, ne compte pas en rester là !",
                "La tension monte, alors que les joueurs relancent une nouvelle partie !",
                "Une nouvelle partie commence. Des hommes habillés en noir observent d'un air impatient les joueurs à qui il reste le moins d'argent.",
                liste_joueurs[random.randint(0,len(liste_joueurs)-1)].name+" tente de glisser discrètement quelque chose dans la boisson de "+liste_joueurs[random.randint(0,len(liste_joueurs)-1)].name+", mais une nouvelle partie commence avant qu'il n'ait eu le temps de faire quoi que ce soit."]
    print(Phrases[random.randint(0,len(Phrases)-1)])
                
                 


########################################################
### PROGRAMME PRINCIPAL ###   Le programme principal ###
########################################################

print("______ _       ___  _____  _   __   ___  ___  _____  _   __    _   _ _    _____ ________  ___  ___ _____ _____ ")
print("| ___ \ |     / _ \/  __ \| | / /  |_  |/ _ \/  __ \| | / /   | | | | |  |_   _|_   _|  \/  | / _ \_   _|  ___|")        # Joli ASCII art (important)
print("| |_/ / |    / /_\ \ /  \/| |/ /     | / /_\ \ /  \/| |/ /    | | | | |    | |   | | | .  . |/ /_\ \| | | |__  ")
print("| ___ \ |    |  _  | |    |    \     | |  _  | |    |    \    | | | | |    | |   | | | |\/| ||  _  || | |  __| ")
print("| |_/ / |____| | | | \__/\| |\  \/\__/ / | | | \__/\| |\  \   | |_| | |____| |  _| |_| |  | || | | || | | |___ ")
print("\____/\_____/\_| |_/\____/\_| \_/\____/\_| |_/\____/\_| \_/    \___/\_____/\_/  \___/\_|  |_/\_| |_/\_/ \____/ ")

print("Bienvenue au BLACKJACK ULTIMATE, la simulation ultime du jeu de Blackjack !")

print("=" * 75)

nb_joueurs = int(input("Combien de joueurs ? "))                                        # Demande le nombre de joueurs, initialise la liste des joueurs et la pioche
nb_IA = int(input("Combien d'IA ? "))
liste_joueurs = init_joueur(nb_joueurs,nb_IA)
print(len(liste_joueurs)," joueurs se réunissent à la table d'un bar réputé pour se livrer à des parties endiablées de Blackjack ULTIMATE, une variante du blackjack\n",
      "spécifique à ce bar, dans laquelle les joueurs jouent les uns contre les autres. Une centaine de kopecs en poche, chaque joueur n'espère qu'une chose ce soir :\n",
      "remporter le gros lot. Mais si certains vont repartir riches, d'autres ne sortiront peut-être jamais de l'enceinte du bar...",sep="")


nb_parties = 0
rejouer = True
while rejouer:                                                                          # Des parties se lancent tant que l'utilisateur souhaite continuer
    print("=" * 75)
    if nb_parties > 0:
        phraseDebutPartie(liste_joueurs)
    for joueur in liste_joueurs:
        joueur.en_jeu = True
    pioche = initPioche(nb_joueurs)
    partieComplete(liste_joueurs)
    print(gagnants(liste_joueurs)[0].name,"a gagné, avec",gagnants(liste_joueurs)[0].score,"points !")
    l_joueurs_2 = []                                                                    # Liste contenant les joueurs qui ne sont pas éliminés
    for joueur in liste_joueurs:                                               
        if joueur.argent == 0:
            joueur.phrase_elimination()                                                 # Les joueurs qui n'ont plus d'argent sont éliminés
        else:
            l_joueurs_2.append(joueur)                                                  # Les joueurs à qui il reste de l'argent sont ajoutés à l_joueurs_2
    liste_joueurs = copy.deepcopy(l_joueurs_2)                                          # liste_joueurs devient une copie profonde de l_joueurs_2
    entree = input("Souhaitez-vous refaire une partie ? (oui/non) ")
    while entree != 'oui' and entree != 'non':                                          # Demande à l'utilisateur s'il souhaite refaire une partie ou non.
        entree = input("Souhaitez-vous refaire une partie ? (oui/non) ")
    if entree == 'oui':
        rejouer = True
    else:
        rejouer = False
    nb_parties += 1

print("Il est temps pour le bar de fermer ses portes. Merci à tous les participants !") # Message de fin (triste)
