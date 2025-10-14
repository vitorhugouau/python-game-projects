import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 14

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

def criar_banco_e_tabela(con):
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS desempenho_escolar;")
    cursor.execute("USE desempenho_escolar;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas_alunos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            aluno VARCHAR(50),
            disciplina VARCHAR(50),
            bimestre VARCHAR(10),
            nota DECIMAL(3,1)
        );
    """)
    con.commit()
    cursor.close()

def inserir_dados(con):
    cursor = con.cursor()
    cursor.execute("USE desempenho_escolar;")

    dados = [
        ("Ana", "Matemática", "1º", 8.5),
        ("Ana", "Português", "1º", 7.0),
        ("Ana", "História", "1º", 9.0),
        ("Ana", "Matemática", "2º", 8.0),
        ("Ana", "Português", "2º", 7.5),
        ("Ana", "História", "2º", 8.5),

        ("Bruno", "Matemática", "1º", 6.5),
        ("Bruno", "Português", "1º", 8.0),
        ("Bruno", "História", "1º", 7.5),
        ("Bruno", "Matemática", "2º", 7.0),
        ("Bruno", "Português", "2º", 7.5),
        ("Bruno", "História", "2º", 8.0),

        ("Carla", "Matemática", "1º", 9.0),
        ("Carla", "Português", "1º", 8.5),
        ("Carla", "História", "1º", 9.5),
        ("Carla", "Matemática", "2º", 9.2),
        ("Carla", "Português", "2º", 8.8),
        ("Carla", "História", "2º", 9.0)
    ]

    cursor.executemany("""
        INSERT INTO notas_alunos (aluno, disciplina, bimestre, nota)
        VALUES (%s, %s, %s, %s)
    """, dados)

    con.commit()
    cursor.close()

def buscar_medias_por_bimestre(con):
    query = """
        SELECT bimestre, ROUND(AVG(nota),2) AS media_geral
        FROM notas_alunos
        GROUP BY bimestre
        ORDER BY bimestre;
    """
    df = pd.read_sql(query, con)
    return df

def gerar_grafico_medias(df):
    colors = sns.color_palette("coolwarm", len(df)) 
    medias = df["media_geral"]
    bimestres = df["bimestre"]

    plt.figure(figsize=(10,6))
    bars = plt.bar(bimestres, medias, color=colors, edgecolor="black", linewidth=1.2)

    media_total = medias.mean()
    plt.axhline(media_total, color="green", linestyle="--", linewidth=1.5, label=f"Média geral: {media_total:.2f}")

    for bar, valor in zip(bars, medias):
        plt.text(bar.get_x() + bar.get_width()/2, valor + 0.1, f"{valor:.1f}", ha="center", va="bottom", fontweight="bold")

    plt.title("📊 Média Geral de Notas por Bimestre", fontsize=18, fontweight="bold")
    plt.xlabel("Bimestre")
    plt.ylabel("Média das Notas")
    plt.ylim(0, 10)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    con = conectar_mysql()
    criar_banco_e_tabela(con)
    inserir_dados(con)
    df = buscar_medias_por_bimestre(con)
    print(df)
    gerar_grafico_medias(df)
    con.close()

if __name__ == "__main__":
    main()
