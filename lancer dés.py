# Importing necessary libraries
import tkinter as tk  # For creating the GUI
from tkinter import ttk  # Additional Tkinter widgets 
import random  # For generating random dice values
import time  # For adding delay during animation

# Constants for dice size and spacing between dice
TAILLE_DE = 100
ESPACEMENT = 20

# === Main interface after welcome screen ===
def lancer_interface_principale(nom_utilisateur):
    # Function to draw a dice on the canvas
    def dessiner_de(canvas, x, y, valeur, faces):
        # Draw the outer square (the dice)
        canvas.create_rectangle(x, y, x + TAILLE_DE, y + TAILLE_DE, fill="white", outline="black", width=3)

        # Define the positions of the dots for dice faces 1-6
        points = {
            1: [(0.5, 0.5)],
            2: [(0.2, 0.2), (0.8, 0.8)],
            3: [(0.2, 0.2), (0.5, 0.5), (0.8, 0.8)],
            4: [(0.2, 0.2), (0.2, 0.8), (0.8, 0.2), (0.8, 0.8)],
            5: [(0.2, 0.2), (0.2, 0.8), (0.5, 0.5), (0.8, 0.2), (0.8, 0.8)],
            6: [(0.2, 0.2), (0.2, 0.5), (0.2, 0.8), (0.8, 0.2), (0.8, 0.5), (0.8, 0.8)]
        }

        # If the die has 6 sides or less, draw dots
        if faces <= 6:
            for px, py in points.get(valeur, []):
                canvas.create_oval(
                    x + px * TAILLE_DE - 10, y + py * TAILLE_DE - 10,
                    x + px * TAILLE_DE + 10, y + py * TAILLE_DE + 10,
                    fill="black"
                )
        else:
            # For dice with more than 6 faces, display the number instead
            canvas.create_text(x + TAILLE_DE / 2, y + TAILLE_DE / 2, text=str(valeur), font=("Georgia", 20, "bold"))

    # Function to roll the dice
    def lancer_des():
        try:
            # Get the number of dice from user input
            nb_des = int(entry_des.get())
            if nb_des <= 0:
                label_resultat.config(text="You must roll at least 1 die!", fg="red")
                return

            # Get number of faces for each die
            faces_par_de = []
            for i in range(nb_des):
                faces = int(entry_faces[i].get())
                if faces < 2:
                    label_resultat.config(text=f"Die {i+1} must have at least 2 sides!", fg="red")
                    return
                faces_par_de.append(faces)

            # Simulate rolling animation (10 quick random rolls)
            for _ in range(10):
                valeurs_temp = [random.randint(1, f) for f in faces_par_de]
                canvas.delete("all")  # Clear previous drawings
                for i, (valeur, faces) in enumerate(zip(valeurs_temp, faces_par_de)):
                    x = ESPACEMENT + (TAILLE_DE + ESPACEMENT) * i
                    dessiner_de(canvas, x, 10, valeur, faces)
                canvas.update()
                time.sleep(0.1)

            # Final dice values
            valeurs_finales = [random.randint(1, f) for f in faces_par_de]
            canvas.delete("all")
            for i, (valeur, faces) in enumerate(zip(valeurs_finales, faces_par_de)):
                x = ESPACEMENT + (TAILLE_DE + ESPACEMENT) * i
                dessiner_de(canvas, x, 10, valeur, faces)

            # Display result
            label_resultat.config(text=f"Result: {valeurs_finales}", fg="black")
            canvas.xview_moveto(0)  # Scroll to the start if needed

            # Clear inputs
            entry_des.delete(0, tk.END)
            for widget in frame_faces_inner.winfo_children():
                widget.destroy()
            entry_faces.clear()

        except ValueError:
            label_resultat.config(text="Please enter valid numbers!", fg="red")

    # Function to generate input fields for each die's number of faces
    def generer_champs_faces():
        try:
            nb_des = int(entry_des.get())
            if nb_des <= 0:
                label_resultat.config(text="Enter at least 1 die.", fg="red")
                return

            # Clear previous fields
            for widget in frame_faces_inner.winfo_children():
                widget.destroy()
            entry_faces.clear()

            # Create new entry fields for each die
            for i in range(nb_des):
                label = tk.Label(frame_faces_inner, text=f"Die {i+1} sides:", font=("Georgia", 10), bg="#F0F0F0")
                label.pack()
                entry = tk.Entry(frame_faces_inner, width=5, font=("Georgia", 10))
                entry.pack(pady=2)
                entry_faces.append(entry)

        except ValueError:
            label_resultat.config(text="Please enter a valid number!", fg="red")

    # === GUI setup ===

    main_window = tk.Tk()
    main_window.title("🎲 Dice Rolling Simulator 🎲")
    main_window.geometry("900x600")
    main_window.resizable(False, False)

    # Left panel with inputs
    frame_global = tk.Frame(main_window, bg="#F0F0F0")
    frame_global.pack(fill="both", expand=True)

    frame_gauche = tk.Frame(frame_global, width=250, bg="#F0F0F0")
    frame_gauche.pack(side=tk.LEFT, fill="y", padx=10, pady=10)

    label_titre = tk.Label(frame_gauche, text="🎲 Dice Simulator", font=("Georgia", 16, "bold"), bg="#F0F0F0")
    label_titre.pack(pady=10)

    label_des = tk.Label(frame_gauche, text="Number of dice:", font=("Georgia", 12), bg="#F0F0F0")
    label_des.pack()
    entry_des = tk.Entry(frame_gauche, width=5, font=("Arial", 12))
    entry_des.pack(pady=5)

    # Button to validate number of dice
    bouton_faces = tk.Button(frame_gauche, text="Validate dice number", font=("Arial", 10), bg="pink", fg="white", command=generer_champs_faces)
    bouton_faces.pack(pady=5)

    # Scrollable area for dice face entries
    frame_faces_zone = tk.Frame(frame_gauche, bg="#F0F0F0")
    frame_faces_zone.pack(fill="both", expand=True)

    faces_canvas = tk.Canvas(frame_faces_zone, height=200, bg="#F0F0F0")
    faces_scroll = tk.Scrollbar(frame_faces_zone, orient="vertical", command=faces_canvas.yview)
    faces_canvas.configure(yscrollcommand=faces_scroll.set)

    faces_scroll.pack(side=tk.RIGHT, fill="y")
    faces_canvas.pack(side=tk.LEFT, fill="both", expand=True)

    frame_faces_inner = tk.Frame(faces_canvas, bg="#F0F0F0")
    faces_canvas.create_window((0, 0), window=frame_faces_inner, anchor="nw")
    frame_faces_inner.bind("<Configure>", lambda e: faces_canvas.configure(scrollregion=faces_canvas.bbox("all")))

    entry_faces = []  # List to store the Entry widgets for each die

    bouton_lancer = tk.Button(frame_gauche, text="🎲 Roll Dice 🎲", font=("Georgia", 12), bg="green", fg="white", command=lancer_des)
    bouton_lancer.pack(pady=10)

    label_resultat = tk.Label(frame_gauche, text="", font=("Georgia", 12), bg="#F0F0F0")
    label_resultat.pack(pady=5)

    # Right panel to draw the dice
    frame_droit = tk.Frame(frame_global, bg="#F0F0F0")
    frame_droit.pack(side=tk.LEFT, fill="both", expand=True)

    canvas_frame = tk.Frame(frame_droit)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, width=600, height=200, bg="#F0F0F0", scrollregion=(0, 0, 2000, 200))
    h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=h_scroll.set)

    canvas.pack(side=tk.TOP, fill="both", expand=True)
    h_scroll.pack(side=tk.BOTTOM, fill="x")

    main_window.mainloop()

# === Welcome screen where user enters name ===
def interface_bienvenue():
    accueil = tk.Tk()
    accueil.title("Bienvenue")
    accueil.geometry("400x300")
    accueil.resizable(False, False)

    # Function to validate name and start main interface
    def valider_nom():
        nom = entry_nom.get().strip()
        if nom:
            label_msg.config(text=f"Bienvenue {nom} !", fg="green")
            # Wait 2 seconds, then start main interface
            accueil.after(2000, lambda: (accueil.destroy(), lancer_interface_principale(nom)))
        else:
            label_msg.config(text="Please enter your name.", fg="red")

    tk.Label(accueil, text="Entrez votre nom :", font=("Georgia", 12)).pack(pady=20)
    entry_nom = tk.Entry(accueil, font=("Arial", 12))
    entry_nom.pack()

    bouton_valider = tk.Button(accueil, text="Commencer", font=("Arial", 11), bg="blue", fg="white", command=valider_nom)
    bouton_valider.pack(pady=10)

    label_msg = tk.Label(accueil, text="", font=("Georgia", 12))
    label_msg.pack(pady=10)

    accueil.mainloop()

# === Start the program with the welcome screen ===
interface_bienvenue()
