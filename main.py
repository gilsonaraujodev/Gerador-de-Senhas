import secrets
import string

# Classe simples para guardar as configurações do perfil
class Profile:
    def __init__(self, length, use_lower=True, use_upper=True,
                 use_digits=True, use_symbols=False, avoid_ambiguous=False):
        self.length = length
        self.use_lower = use_lower
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.avoid_ambiguous = avoid_ambiguous


# Caracteres que podem confundir na leitura
AMBIGUOUS = set("O0Il1")


def build_alphabet(profile):
    chars = ""

    if profile.use_lower:
        chars += string.ascii_lowercase

    if profile.use_upper:
        chars += string.ascii_uppercase

    if profile.use_digits:
        chars += string.digits

    if profile.use_symbols:
        chars += "!@#$%&*_-+=?<>"

    if profile.avoid_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)

    if chars == "":
        print("Erro: nenhum tipo de caractere foi selecionado.")
        exit()

    return chars


def generate_password(profile):
    alphabet = build_alphabet(profile)

    password = []

    # Garante pelo menos um caractere de cada tipo escolhido
    if profile.use_lower:
        password.append(secrets.choice(string.ascii_lowercase))

    if profile.use_upper:
        password.append(secrets.choice(string.ascii_uppercase))

    if profile.use_digits:
        password.append(secrets.choice(string.digits))

    if profile.use_symbols:
        password.append(secrets.choice("!@#$%&*_-+=?<>"))

    if len(password) > profile.length:
        print("Erro: tamanho da senha muito pequeno para esse perfil.")
        exit()

    # Completa o restante da senha
    while len(password) < profile.length:
        password.append(secrets.choice(alphabet))

    # Embaralha para não ficar previsível
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# Perfis disponíveis
PROFILES = {
    "basico": Profile(length=12),
    "padrao": Profile(length=14),
    "forte": Profile(length=20, use_symbols=True, avoid_ambiguous=True)
}


def main():
    print("Perfis disponíveis:")
    for name in PROFILES:
        print("-", name)

    choice = input("Escolha um perfil: ").strip().lower()

    if choice not in PROFILES:
        print("Perfil inválido.")
        return

    senha = generate_password(PROFILES[choice])
    print("\nSenha gerada:")
    print(senha)


if __name__ == "__main__":
    main()
