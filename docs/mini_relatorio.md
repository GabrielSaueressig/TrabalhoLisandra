# Mini-relatório do processo de construção

> **RASCUNHO.** O enunciado exige que este relatório seja escrito pela dupla, com reflexão própria. Os fatos abaixo saem do histórico do repositório e dos testes. Completem os trechos [PREENCHER] e reescrevam com a experiência de vocês.

## Ambiente de execução

| Item | Configuração |
|---|---|
| Modelo de linguagem | `qwen2.5:7b` (Ollama, quantizado Q4, ~4,7 GB) |
| Modelo de embeddings | `nomic-embed-text` (Ollama, ~274 MB) |
| Framework | LangGraph 1.2 + LangChain 1.x |
| Máquina | AMD Ryzen 7 5700X (8 núcleos), 32 GB de RAM, GPU NVIDIA RTX 3060 Ti 8 GB, Windows 10 Pro |
| Python | 3.11.9 |
| Custo | Zero: tudo roda localmente, sem chave de API nem serviço em nuvem |

[PREENCHER: se a demonstração for feita em outra máquina, informar também a configuração dela.]

## Iterações

1. **Versão 1 (commit `1c8c358`).** Grafo LangGraph com Roteador, Tutor, Exemplificador, Inquiridor e Guardião. O material inteiro era injetado no prompt. Já tinha CLI, memória (`MemorySaver`) e tratamento de erros.
2. **Versão 2 (commit `020e153`, RAG).** O material passou a ser indexado com FAISS e embeddings locais (`nomic-embed-text`), e os agentes recebem só os trechos relevantes.
3. **Versão 3 (revisão contra o enunciado).** [PREENCHER: descrever com as palavras de vocês.] Principais mudanças:
   - O índice era criado no `import`. Sem o Ollama no ar, até os testes quebravam e o programa morria com um traceback, sem a mensagem amigável. Agora ele é criado na primeira busca e é recriado quando o material muda (controle por hash).
   - O material (`state.md`) foi ampliado: problema com código "antes", colaborações, estrutura, segundo exemplo (ConexaoTCP, do livro GoF), quatro usos incorretos com correção, State vs Strategy, exercícios com resposta esperada e erros comuns, e um checklist de fechamento. Na versão anterior, o modelo inventava o que faltava (por exemplo, um `EstadoNovo.pagar()` que recusava o pagamento).
   - Todos os prompts passaram a seguir o Anexo B, incluindo a seção EXEMPLOS, e o Roteador e o Guardião ganharam ROLE/GOAL/BACKSTORY.
   - Novas intenções: `selecao`, `comparacao`, `uso_incorreto` e `fechamento`, uma para cada categoria do roteiro.
   - Regras determinísticas para padrão inventado ("padrão Zeta") e para pedido de código pronto. Também foi corrigido um bug: "state" não estava na lista de padrões GoF.
   - Janela de contexto do modelo aumentada para 8192 tokens, porque o padrão do Ollama cortava parte do prompt.
   - Saída em UTF-8 na CLI: no Windows, os acentos quebravam quando a saída era redirecionada.
   - Versões das dependências pinadas e testes ampliados de 3 para 13.
4. **Versão 4 (ajustes a partir do roteiro com o modelo real).** Rodamos `scripts/rodar_roteiro.py` três vezes e analisamos as respostas:
   - *1ª rodada:* respostas cortadas no meio do código (limite de 700 tokens), "reprodutor de música" classificado como Strategy (errado) e o Inquiridor entregando a solução completa do exercício e dizendo "você está correto" para uma resposta errada. Ajustes: limite de 1200 tokens, limites de código por agente no prompt, exemplos de State e Strategy explícitos no material, proibição de elogiar resposta errada.
   - *2ª rodada:* a comparação State × Strategy e os cortes foram corrigidos, mas o modelo **continuou ignorando** "não escreva código" no pedido de código pronto e na conversa de exercício. Concluímos que, com um modelo de 7B, uma instrução no prompt não basta. Criamos uma regra determinística no Guardião: limite de linhas de código por agente, com revisão e, se preciso, remoção do código (16 testes).
   - *3ª rodada:* o pedido de código pronto passou a ser recusado com orientação em passos, sem código. Na conversa de exercício, porém, a tentativa do aluno ("Acho que é Strategy...") foi classificada pelo Roteador como pergunta conceitual ou de exemplo e caiu em agentes que podem mostrar código, que entregaram a solução. Ajuste: a mensagem logo depois de um exercício é tratada como tentativa (`avaliacao`, Inquiridor), e enquanto o aluno está praticando vale o limite de código do Inquiridor para todos os agentes (17 testes).
   - *4ª rodada:* a conversa de exercício passou a funcionar: a tentativa errada do aluno foi diagnosticada como confusão State/Strategy, com pista e sem solução. Na pergunta de comparação, porém, o modelo às vezes chamava o "reprodutor de música" de Strategy e, numa execução, **trocou para chinês** no meio da resposta. Rodamos essa pergunta 3 vezes para medir a variação. Ajustes: tiramos da seção de comparação o exemplo ambíguo (ficaram Pedido × frete), criamos uma regra determinística no Guardião para respostas que mudam de idioma e reforçamos "somente português" no formato (18 testes). Depois disso, 3 de 3 execuções saíram corretas e em português.
   - *5ª rodada (versão final):* os 8 cenários responderam conforme o esperado, em 1 a 47 s cada (`docs/resultados_roteiro.md`). A comparação usou Pedido × frete corretamente, o padrão inventado foi recusado sem chamar o modelo e o código pronto foi recusado com perguntas guiadas. **Limitações que ainda observamos:** na conversa de exercício, o Inquiridor às vezes reformula o exercício (acrescentando um estado "Entregue" que não está no material) e escreve "Resposta esperada" antes de omitir o código. O Guardião também às vezes acrescenta o aviso de imprecisão em respostas corretas, um falso positivo que preferimos a deixar passar um erro. [PREENCHER: a avaliação de vocês.]

## Testes realizados

- **Automatizados:** 18 testes com `pytest`, usando um LLM falso (rodam em menos de 1 s, sem Ollama). Cobrem o tratamento de erros, as regras anti-alucinação, o roteamento, o laço de revisão do Guardião, o limite de código, a troca de idioma e a memória.
- **Roteiro de cenários:** `python scripts/rodar_roteiro.py` executa as 7 categorias do enunciado e uma conversa de 3 turnos com o modelo real. As respostas estão em `docs/resultados_roteiro.md`.
- [PREENCHER: análise de vocês sobre as respostas, o que estava bom e o que ajustaram.]

## Dificuldades e soluções

| Dificuldade | Solução |
|---|---|
| Modelo local lento: várias chamadas por pergunta (roteador, agente, guardião) | Limite de 1 revisão do Guardião, recusa de padrão inventado sem chamar o modelo, limite de 700 tokens por resposta, histórico de no máximo 8 mensagens |
| Modelo inventando exemplos e participantes | Material mais completo, RAG com trechos maiores (por seção) e o Guardião conferindo contra o material |
| Roteador devolvendo texto fora do formato ("Acho que é: exemplo.") | `interpretar_rotulo` procura um rótulo válido dentro da saída; se não acha, usa `conceito` |
| Agente entregando código pronto, mesmo instruído a não fazer isso | Detecção determinística do pedido + limite de linhas de código por agente aplicado pelo Guardião (revisão e, se preciso, remoção do código) |
| Prompt cortado em silêncio pelo Ollama | `num_ctx=8192` |
| Modelo "simulando" o diálogo (faz uma pergunta ao aluno e ele mesmo responde) | Regra no FORMATO: terminar na pergunta e parar ali |
| Modelo trocando para chinês no meio da resposta (característica do Qwen) | Regra determinística no Guardião (detecta caracteres CJK, pede revisão e, se preciso, descarta a parte em outro idioma) |
| Respostas variando entre execuções (certa numa, errada noutra) | Rodar o mesmo cenário várias vezes e remover do material os exemplos que geravam ambiguidade |
| Respostas cortadas no meio do código | Limite de tokens aumentado para 1200 e limite de tamanho de código por agente |
| [PREENCHER: outras dificuldades de vocês] | |

## Declaração do uso de IA

[PREENCHER e revisar: descrevam com honestidade quais ferramentas usaram e para quê.] Exemplo: usamos o assistente Claude (Anthropic), via Claude Code, para revisar o código contra o enunciado, corrigir o carregamento do RAG, ampliar o material de referência, escrever os testes automatizados e gerar rascunhos da documentação. Todo o conteúdo foi revisado pela dupla: conferimos o material sobre o padrão State com o livro GoF, executamos os testes e o roteiro e reescrevemos os textos com as nossas palavras. O sistema em si usa somente o modelo local `qwen2.5:7b`.
