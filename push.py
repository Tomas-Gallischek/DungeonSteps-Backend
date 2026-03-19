import subprocess
import datetime
import os

# TEST: Tento řádek se musí vypsat VŽDY, i kdyby zbytek skriptu nefungoval
print("--- Python skript se prave spustil ---")

def run_git_commands():
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Automaticke ulozeni: {now}"

        # Výpis cesty, kde se skript nachází
        print(f"Pracovni slozka: {os.getcwd()}")

        # 1. Přidání souborů
        print("Pridavam zmeny (git add)...")
        subprocess.run(["git", "add", "."], check=True)

        # 2. Commit
        print(f"Vytvarim commit: {commit_message}")
        # Tady nepoužíváme check=True, protože pokud nejsou změny, Git vyhodí chybu
        subprocess.run(["git", "commit", "-m", commit_message])

        # 3. Push
        print("Odesilam na GitHub (git push)...")
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ VSE USPESNE ULOZENO")

    except Exception as e:
        print(f"❌ Nastala chyba: {e}")

# TOTO JE KLICOVE: Bez techto dvou radku se funkce run_git_commands() nikdy nespusti!
if __name__ == "__main__":
    run_git_commands()