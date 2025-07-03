from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from automacao import obter_status_por_nota_fiscal

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="API de Rastreio Portal Postal",
    description="Uma API para consultar o status de um pedido usando web scraping.",
    version="1.0.0"
)

@app.get("/consultar/{nota_fiscal}")
def consultar_nota_fiscal(nota_fiscal: str):
    """
    Endpoint para consultar o status de um pedido pela nota fiscal.
    """
    print(f"Recebida requisição para a nota fiscal: {nota_fiscal}")
    
    resultado = obter_status_por_nota_fiscal(nota_fiscal)
    
    if not resultado:
        print(f"Nenhum resultado encontrado para a nota fiscal: {nota_fiscal}")
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado para a nota fiscal fornecida.")

    if resultado.get("error"):
        print(f"Erro ao processar a nota fiscal {nota_fiscal}: {resultado.get('error')}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {resultado.get('error')}")

    print(f"Retornando sucesso para a nota fiscal {nota_fiscal}: {resultado}")
    return resultado
