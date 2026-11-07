import os
from datetime import datetime
import pandas as pd
from jobspy import scrape_jobs

def executar_scraping():
    print("🔍 Iniciando a varredura automatizada de vagas...")
    
    # Executa a extração via JobSpy com as colunas completas solicitadas
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin"], # "zip_recruiter", "glassdoor"],
        search_term="software engineer",
        location="San Francisco, CA",
        results_wanted=20,
        hours_old=72,
        country_indeed="USA",
    )
    
    print(f"✅ Sucesso! Encontradas {len(jobs)} vagas.")
    
    # Define e filtra as colunas na exata estrutura solicitada
    colunas_desejadas = [
        "site", "title", "company", "location", 
        "job_type", "interval", "min_amount", "max_amount", 
        "job_url", "description"
    ]
    
    # Mantém apenas as colunas que existem no DataFrame gerado
    df_filtrado = jobs[[col for col in colunas_desejadas if col in jobs.columns]]
    
    # 📄 Salva ou apensa no arquivo MARKDOWN (jobs.md)
    apendar_no_arquivo_markdown(df_filtrado)
    
    # 📝 Atualiza o README.md injetando a tabela atualizada
    atualizar_readme(df_filtrado)

def apendar_no_arquivo_markdown(df):
    md_path = "jobs.md"
    timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M (UTC)")
    
    # Converte o DataFrame para tabela Markdown (sem o cabeçalho padrão do pandas se o arquivo já existir)
    incluir_cabecalho = not os.path.exists(md_path) or os.path.getsize(md_path) == 0
    tabela_markdown = df.to_markdown(index=False, header=incluir_cabecalho)
    
    modo = "a" if not incluir_cabecalho else "w"
    
    with open(md_path, modo, encoding="utf-8") as f:
        if incluir_cabecalho:
            f.write(f"# 📋 Histórico de Vagas Coletadas\n\n")
        
        f.write(f"\n\n### 🕒 Coleta realizada em: {timestamp}\n\n")
        f.write(tabela_markdown)
        
    print("💾 Novas vagas apendadas com sucesso no arquivo 'jobs.md'.")

def atualizar_readme(df):
    readme_path = "README.md"
    
    # Seleciona uma prévia resumida (primeiras 15 linhas) para o README principal
    tabela_resumo = df.head(15).to_markdown(index=False)
    
    if not os.path.exists(readme_path):
        print("⚠️ Arquivo README.md não encontrado. Criando um novo...")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# 📊 Vagas de Emprego Automatizadas\n\n<!--START_SECTION:jobs-->\n<!--END_SECTION:jobs-->\n")

    with open(readme_path, "r", encoding="utf-8") as f:
        conteudo = f.read()

    inicio_tag = "<!--START_SECTION:jobs-->"
    fim_tag = "<!--END_SECTION:jobs-->"
    
    timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M (UTC)")
    novo_bloco = f"{inicio_tag}\n\n*Última atualização automatizada: **{timestamp}***\n\n{tabela_resumo}\n\n{fim_tag}"

    if inicio_tag in conteudo and fim_tag in conteudo:
        partes = conteudo.split(inicio_tag)
        resto = partes[1].split(fim_tag)[1]
        novo_conteudo = partes[0] + novo_bloco + resto
    else:
        novo_conteudo = conteudo + f"\n\n## 📋 Vagas Recentes\n\n{novo_bloco}"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(novo_conteudo)
    
    print("✨ README.md atualizado com sucesso!")

if __name__ == "__main__":
    executar_scraping()
