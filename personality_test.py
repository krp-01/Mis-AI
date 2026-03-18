def run_personality_test():
    print("=== Test de personalitate MIS ===")
    print("Raspunde cu un numar de la 1 la 5.")
    print("1 = deloc")
    print("5 = foarte mult")

    risc = int(input("\nCat de mult iti place sa iti asumi riscuri? "))
    social = int(input("Cat de sociabil esti? "))
    organizare = int(input("Cat de organizat esti? "))
    emotie = int(input("Cat de emotional esti? "))
    rabdare = int(input("Cat de rabdator esti? "))
    adaptare = int(input("Cat de usor te adaptezi la schimbari? "))
    disciplina = int(input("Cat de disciplinat esti? "))
    incredere = int(input("Cat de multa incredere ai in tine? "))

    profil_risc = "curajos" if risc >= 4 else "prudent"
    profil_social = "extrovertit" if social >= 4 else "rezervat"
    profil_organizare = "organizat" if organizare >= 4 else "spontan"
    profil_emotie = "emotional" if emotie >= 4 else "rational"
    profil_rabdare = "rabdator" if rabdare >= 4 else "nerabdator"
    profil_adaptare = "flexibil" if adaptare >= 4 else "constant"
    profil_disciplina = "disciplinat" if disciplina >= 4 else "relaxat"
    profil_incredere = "increzator" if incredere >= 4 else "retinut"

    profil = {
        "risc": profil_risc,
        "social": profil_social,
        "organizare": profil_organizare,
        "emotie": profil_emotie,
        "rabdare": profil_rabdare,
        "adaptare": profil_adaptare,
        "disciplina": profil_disciplina,
        "incredere": profil_incredere
    }

    return profil
