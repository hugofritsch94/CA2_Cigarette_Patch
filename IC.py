# IC V8
from pathlib import Path

print("=" * 50)
print("Integrity Check V8")
print("=" * 50)

# ==================================================
# RULE-V8-001
# Carregamento da Rule Matrix
# ==================================================

rule_matrix = Path("IC_RULE_MATRIX.txt")

if not rule_matrix.exists():

    print("ERRO DE CONFIGURAÇÃO")
    print("Rule Matrix não encontrada.\n")

    print("=" * 50)
    print("DECISÃO DO PROTOCOLO")
    print("=" * 50)

    print("STATUS.............: REPROVADO")
    print("PROTOCOLO..........: BLOQUEADO")
    print("PARSER.............: NÃO AUTORIZADO")
    print("MOTIVO.............: Rule Matrix ausente.")

    print("=" * 50)

    raise SystemExit

try:

    rule_matrix_texto = rule_matrix.read_text(
        encoding="utf-8",
        errors="ignore"
    )

except Exception:

    print("ERRO DE CONFIGURAÇÃO")
    print("Não foi possível carregar a Rule Matrix.\n")

    print("=" * 50)
    print("DECISÃO DO PROTOCOLO")
    print("=" * 50)

    print("STATUS.............: REPROVADO")
    print("PROTOCOLO..........: BLOQUEADO")
    print("PARSER.............: NÃO AUTORIZADO")
    print("MOTIVO.............: Rule Matrix ilegível.")

    print("=" * 50)

    raise SystemExit

print("Rule Matrix OK\n")

# ==================================================
# INÍCIO DO IC V7.1
# ==================================================

arquivos = list(Path(".").glob("*.txt"))
if not arquivos:
    print("Arquivo .txt não encontrado.")
    raise SystemExit

arquivo = arquivos[0]
print(f"Arquivo encontrado : {arquivo.name}")

texto = arquivo.read_text(encoding="utf-8", errors="ignore")
linhas = texto.splitlines()

print(f"Tamanho           : {len(texto)} caracteres")
print(f"Total de linhas   : {len(linhas)}")

linha_atual = 0
blocos = 0
erros = []

dentro_bloco = False
campo_encontrado = False
nome_bloco = ""
linha_inicio_bloco = 0

tem_NumItems = False
tem_BitSize = False
tem_size = False


def validar():
    global erros

    if not campo_encontrado:
        erros.append(f"""RULE-001

Bloco.............: {nome_bloco}
Linha inicial.....: {linha_inicio_bloco}
Linha detectada...: {linha_atual}

Descrição.........:
Bloco vazio.
""")

    if not tem_NumItems:
        erros.append(f"""RULE-002

Bloco.............: {nome_bloco}
Linha inicial.....: {linha_inicio_bloco}
Linha detectada...: {linha_atual}

Campo ausente.....:
m_NumItems
""")

    if not tem_BitSize:
        erros.append(f"""RULE-003

Bloco.............: {nome_bloco}
Linha inicial.....: {linha_inicio_bloco}
Linha detectada...: {linha_atual}

Campo ausente.....:
m_BitSize
""")

    if not tem_size:
        erros.append(f"""RULE-004

Bloco.............: {nome_bloco}
Linha inicial.....: {linha_inicio_bloco}
Linha detectada...: {linha_atual}

Campo ausente.....:
size
""")


for linha in linhas:

    linha_atual += 1

    if "PackedBitVector" in linha:

        if dentro_bloco:
            validar()

        blocos += 1

        nome_bloco = linha.split()[-1]
        linha_inicio_bloco = linha_atual

        dentro_bloco = True

        campo_encontrado = False
        tem_NumItems = False
        tem_BitSize = False
        tem_size = False

        continue

    if not dentro_bloco:
        continue

    if "=" in linha:

        campo_encontrado = True

        campo = linha.split("=", 1)[0].strip().split()[-1]

        if campo == "m_NumItems":
            tem_NumItems = True

        elif campo == "m_BitSize":
            tem_BitSize = True

        elif campo == "size":
            tem_size = True

if dentro_bloco:
    validar()

print("\nInspeção estrutural concluída.\n")

print(f"Linhas percorridas : {linha_atual}")
print(f"PackedBitVector    : {blocos}\n")

if erros:

    print("=" * 50)
    print("ERROS ENCONTRADOS")
    print("=" * 50)

    for erro in erros:
        print(erro)
        print("-" * 50)

    protocolo = "BLOQUEADO"
    parser = "NÃO AUTORIZADO"
    status = "REPROVADO"

else:

    print("Nenhum erro encontrado.\n")

    protocolo = "LIBERADO"
    parser = "AUTORIZADO"
    status = "APROVADO"

print("=" * 50)
print("DECISÃO DO PROTOCOLO")
print("=" * 50)

print(f"STATUS.............: {status}")
print(f"PROTOCOLO..........: {protocolo}")
print(f"PARSER.............: {parser}")

if status == "APROVADO":
    print("MOTIVO.............: Estrutura íntegra.")
else:
    print("MOTIVO.............: Foram encontrados erros estruturais.")

print("=" * 50)

print("\n" + "=" * 50)
print("STATUS : IC V8 OPERACIONAL")
print("=" * 50)