import secrets # - secrets: geração de números aleatórios segura 
import string # - string: contém conjuntos prontos de caracteres

from dataclasses import dataclass # - dataclass: para definir classes simples de dados

@dataclass(frozen=True)
class Profile:
    # Tamanho da senha
    length: int

    use_lower: bool = True     # letras minúsculas
    use_upper: bool = True     # letras maiúsculas
    use_digits: bool = True    # números
    use_symbols: bool = False  # simbolos

    # Se for True, remove caracteres que confundem (O/0, I/l/1)
    avoid_ambiguous: bool = False


AMBIGUOUS = set("O0Il1")


def build_alphabet(p: Profile) -> str:
    """
    Monta o 'alfabeto' (lista de caracteres permitidos) com base no perfil.
    Exemplo: se o perfil permitir letras e números, retorna "abc...XYZ...0123..."
    """
    chars = ""  

    if p.use_lower:
        chars += string.ascii_lowercase

    if p.use_upper:
        chars += string.ascii_uppercase

    if p.use_digits:
        chars += string.digits

    if p.use_symbols:
        chars += "!@#$%&*_-+=?<>"

    if p.avoid_ambiguous:
        chars = "".join(c for c in chars if c not in AMBIGUOUS)

    if not chars:
        raise ValueError("Alfabeto vazio: escolha pelo menos um tipo de caractere.")
    return chars


def generate_password(p: Profile) -> str:
    """
    Gera uma senha segura, obedecendo as regras do perfil.
    Importante: ela garante que terá ao menos 1 caractere de cada tipo selecionado.
    """
    alphabet = build_alphabet(p)

    required = []

    if p.use_lower:
        required.append(secrets.choice(string.ascii_lowercase))

    if p.use_upper:
        required.append(secrets.choice(string.ascii_uppercase))

    if p.use_digits:
        required.append(secrets.choice(string.digits))

    if p.use_symbols:
        required.append(secrets.choice("!@#$%&*_-+=?<>"))

    if p.avoid_ambiguous:
        required = [c for c in required if c not in AMBIGUOUS]

    if len(required) > p.length:
        raise ValueError("O tamanho é pequeno demais para cumprir as regras do perfil.")

    remaining = [secrets.choice(alphabet) for _ in range(p.length - len(required))] # Vai preencher o restante da senha

    password_list = required + remaining

    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list)


PROFILES = {
    # básico: 12 caracteres, sem simbolos
    "basico": Profile(length=12, use_symbols=False),

    # padrão: 14 caracteres, sem simbolos
    "padrao": Profile(length=14, use_symbols=False),

    # forte: 20 caracteres, com simbolos
    "forte": Profile(length=20, use_symbols=True, avoid_ambiguous=True),
}


def main():
    """
    Função principal do programa.
    """
    print("Perfis disponíveis:", ", ".join(PROFILES.keys()))

    profile_name = input("Escolha um perfil: ").strip().lower()

    if profile_name not in PROFILES:
        print("Perfil inválido.")
        return 

    profile = PROFILES[profile_name]

    pwd = generate_password(profile)

    print("\nSenha gerada:\n", pwd)

if __name__ == "__main__":
    main()
