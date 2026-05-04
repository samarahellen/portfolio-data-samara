import yfinance as yf
import pandas as pd

# ============ EXTRACT ============
tickers = ["PETR4.SA", "ITUB4.SA", "BBDC4.SA"]
df = yf.download(tickers, start="2024-01-01", end="2025-01-01")

# Deixando o DataFrame mais limpo (só Close e Volume)
close = df["Close"].copy()
volume = df["Volume"].copy()

close.columns = [col.replace(".SA", "") for col in close.columns]
volume.columns = [col.replace(".SA", "") for col in volume.columns]

print("=== PREÇOS DE FECHAMENTO ===")
print(close.head(10))
print(f"\nShape: {close.shape}")
print(f"\nValores nulos:\n{close.isnull().sum()}")

print("\n=== ESTATÍSTICAS ===")
print(close.describe())

# Salvando em CSV para usar depois
close.to_csv("precos.csv")
volume.to_csv("volume.csv")
print("\nArquivos salvos: precos.csv e volume.csv")

# ============ TRANSFORM ============

# 1. Retorno diário (%)
retorno_diario = close.pct_change() * 100

# 2. Média móvel de 20 dias
media_movel_20 = close.rolling(window=20).mean()

# 3. Melhor e pior dia de cada ação
print("\n=== MELHOR DIA DE CADA AÇÃO ===")
for col in close.columns:
    idx = retorno_diario[col].idxmax()
    val = retorno_diario[col].max()
    print(f"{col}: {idx.date()} → +{val:.2f}%")

print("\n=== PIOR DIA DE CADA AÇÃO ===")
for col in close.columns:
    idx = retorno_diario[col].idxmin()
    val = retorno_diario[col].min()
    print(f"{col}: {idx.date()} → {val:.2f}%")

# 4. Salvando os transformados
retorno_diario.to_csv("retorno_diario.csv")
media_movel_20.to_csv("media_movel_20.csv")
print("\nTransform concluído! Arquivos salvos.")

# ============ LOAD ============
import sqlite3

conn = sqlite3.connect("acoes_b3.db")

# Salvando as 3 tabelas no banco
close.reset_index().to_sql("precos", conn, if_exists="replace", index=False)
retorno_diario.reset_index().to_sql("retornos", conn, if_exists="replace", index=False)
media_movel_20.reset_index().to_sql("media_movel", conn, if_exists="replace", index=False)

# Testando com uma query SQL
query = """
    SELECT Date, BBDC4, ITUB4, PETR4
    FROM retornos
    WHERE BBDC4 = (SELECT MIN(BBDC4) FROM retornos)
       OR PETR4 = (SELECT MIN(PETR4) FROM retornos)
    ORDER BY Date
"""
resultado = pd.read_sql(query, conn)
print("\n=== PIORES DIAS VIA SQL ===")
print(resultado)

conn.close()
print("\nLoad concluído! Banco acoes_b3.db criado.")