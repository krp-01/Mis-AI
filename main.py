from personality_test import run_personality_test
from profile_manager import save_profile, load_profile, user_exists
from response_engine import generate_local_response
from ai_connector import generate_ai_response

def sign_up():
    print("\n=== SIGN UP ===")

    while True:
        username = input("Alege un username unic: ").strip().lower()

        if username == "":
            print("Username-ul nu poate fi gol.")
            continue

        if user_exists(username):
            print("Acest username exista deja. Alege altul.")
        else:
            break

    display_name = input("Scrie numele tau afisat: ").strip()

    profile = run_personality_test()
    profile["display_name"] = display_name
    profile["username"] = username

    save_profile(username, profile)

    print("\nCont creat cu succes.")
    return username, profile

def sign_in():
    print("\n=== SIGN IN ===")

    username = input("Username: ").strip().lower()
    profile = load_profile(username)

    if profile is None:
        print("Nu exista niciun cont cu acest username.")
        return None, None

    print(f"\nBun venit inapoi, {profile['display_name']}!")
    return username, profile

def main():
    print("=== MIS - Memory Identity Stratified ===")

    while True:
        print("\nAlege o optiune:")
        print("1. Sign up")
        print("2. Sign in")

        choice = input("Scrie 1 sau 2: ").strip()

        if choice == "1":
            username, profile = sign_up()
            break
        elif choice == "2":
            username, profile = sign_in()
            if profile is not None:
                break
        else:
            print("Optiune invalida. Incearca din nou.")

    print("\n=== Profil activ ===")
    for key, value in profile.items():
        print(f"- {key}: {value}")

    while True:
        question = input("\nScrie o intrebare pentru MIS (sau 'exit'): ").strip()

        if question.lower() == "exit":
            print("La revedere!")
            break

        mode = input("Alege modul de raspuns: local / ai : ").strip().lower()

        if mode == "ai":
            try:
                answer = generate_ai_response(
                    question,
                    profile,
                    profile["display_name"],
                    profile["username"]
                )
            except Exception as e:
                print(f"\nEroare AI: {e}")
                print("Folosesc raspuns local.")
                answer = generate_local_response(question, profile)
        else:
            answer = generate_local_response(question, profile)

        print("\n=== Raspuns MIS ===")
        print(answer)

if __name__ == "__main__":
    main()
