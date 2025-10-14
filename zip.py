import os
import zipfile

# Configurações
num_files = 15
file_size = 1_400_000_000  # 1,4 GB
chunk_size = 10_000_000    # escreve em blocos de 10 MB
output_dir = "big_files"
zip_name = "big_archive.zip"

# Cria pasta para os arquivos temporários
os.makedirs(output_dir, exist_ok=True)

# Cria os arquivos grandes
print("Criando arquivos grandes...")
for i in range(1, num_files + 1):
    filename = os.path.join(output_dir, f"file{i}.txt")
    with open(filename, "wb") as f:
        written = 0
        while written < file_size:
            # escreve blocos de zeros até atingir o tamanho desejado
            write_size = min(chunk_size, file_size - written)
            f.write(b"0" * write_size)
            written += write_size
    print(f"  {filename} criado")

# Compacta todos os arquivos em um zip
print("\nCompactando arquivos...")
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
    for i in range(1, num_files + 1):
        filename = os.path.join(output_dir, f"file{i}.txt")
        zf.write(filename, arcname=f"file{i}.txt")
        print(f"  {filename} adicionado ao zip")

print(f"\nArquivo zip criado: {zip_name}")
