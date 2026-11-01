# Tutor multiagente do padrão State (LangGraph + Ollama)

Sistema multiagente em Python que ensina o padrão de projeto **State** (GoF) a um estudante iniciante.
Trabalho final de ELC1070 – Análise e Projeto de Sistemas OO (UFSM).

- Framework de orquestração: **LangGraph**
- Modelo de linguagem: **qwen2.5:7b** rodando localmente no **Ollama**. Embeddings: **nomic-embed-text**, também local.
- **Custo zero**: não usa API paga, chave de API nem serviço em nuvem. A internet só é usada para baixar as bibliotecas e os modelos.

## Requisitos
- Python 3.11 ou mais novo
- [Ollama](https://ollama.com/download) instalado e em execução
- Cerca de 6 GB livres em disco para os modelos e 16 GB de RAM para o `qwen2.5:7b` (com 8 GB, use o `qwen2.5:3b`, veja abaixo)

## Instalação
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

python -m venv .venv
# Windows:     .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Execução (contrato da seção 5 do enunciado)
```bash
python -m agente "Explique o que é o padrão State e qual problema ele resolve."
```
Sem argumentos, o sistema abre o modo conversa, que mantém a memória entre os turnos. Digite `sair` para encerrar:
```bash
python -m agente
```

### Interface web (opcional)
Um chat no navegador, para as demonstrações. Ele abre sozinho em http://localhost:8000:
```bash
python -m agente.web              # opções: --porta 8001, --sem-navegador
```
A interface usa só a biblioteca padrão do Python e não carrega nada da internet, então roda offline como o resto do sistema. Ela mostra qual agente respondeu e quanto tempo levou, e traz atalhos com as perguntas do roteiro. Cada aba do navegador é uma conversa com memória própria, e o botão "Nova conversa" zera a memória. A CLI acima continua sendo o ponto de entrada oficial.

Para usar outro modelo local sem mudar o código, defina a variável `AGENTE_MODELO`:
```bash
# Windows PowerShell: $env:AGENTE_MODELO="qwen2.5:3b"
# Linux/macOS:        export AGENTE_MODELO=qwen2.5:3b
```

Na primeira execução o índice do material (`agente/faiss_index/`) é criado automaticamente. Ele é recriado sozinho sempre que `agente/conhecimento/state.md` muda.

## Testes
```bash
pytest                            # testes automatizados (não precisam do Ollama: usam um LLM falso)
python scripts/rodar_roteiro.py   # roda o roteiro de cenários do enunciado com o modelo real
                                  # e salva as respostas em docs/resultados_roteiro.md
```

## Arquitetura
```
pergunta -> [Roteador] -> Tutor | Exemplificador | Inquiridor -> [Guardião] -> resposta
               |                                                    |
               +-> recusa (padrão inventado / fora de escopo)        +-> pede revisão (no máximo 1 vez)
```

| Arquivo | Responsabilidade |
|---|---|
| `agente/__main__.py` | CLI (comando único e modo conversa) |
| `agente/web.py`, `agente/static/index.html` | Interface web opcional (servidor local + página de chat) |
| `agente/sistema.py` | Fachada `sistema.resposta(pergunta)`, memória por sessão e tratamento de erros |
| `agente/grafo.py` | Grafo LangGraph: roteamento, agentes, guardião e regras determinísticas anti-alucinação |
| `agente/prompts.py` | Prompts de sistema de cada agente (formato do Anexo B) |
| `agente/rag.py` | Recuperação dos trechos relevantes do material (FAISS + embeddings locais) |
| `agente/conhecimento/state.md` | Material de referência: a única fonte de fatos dos agentes |
| `agente/config.py` | Modelo, limites e parâmetros |

## Documentação
- [docs/agentes.md](docs/agentes.md): prompt de sistema completo de cada agente e como eles se coordenam (gerado por `python scripts/gerar_doc_agentes.py`)
- [docs/justificativa_design.md](docs/justificativa_design.md): justificativa das decisões de design
- [docs/mini_relatorio.md](docs/mini_relatorio.md): mini-relatório do processo de construção
- [docs/caderno_evidencias.md](docs/caderno_evidencias.md): modelo do caderno de evidências da avaliação entre pares
- [docs/resultados_roteiro.md](docs/resultados_roteiro.md): respostas do nosso sistema ao roteiro de cenários
