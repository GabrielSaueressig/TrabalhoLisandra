# Padrão State (GoF) — material de referência

Palavras-chave: Design Patterns, GoF, padrão comportamental, State, máquina de estados, polimorfismo, Context, State, ConcreteState, transição de estados.

## Intenção
Permitir que um objeto altere seu comportamento quando o seu estado interno muda. Para quem usa o objeto, ele parece ter mudado de classe.
O State é um padrão comportamental do catálogo GoF (Gamma, Helm, Johnson e Vlissides, 1994). Também é conhecido como "Objects for States" (objetos para estados).

## Problema que o State resolve
Uma classe precisa se comportar de forma diferente conforme o seu estado atual. Exemplo: um Pedido pode estar Novo, Pago, Enviado ou Cancelado, e "pagar" ou "enviar" fazem coisas diferentes em cada um.
Sem o padrão, cada método testa o estado com if/else ou switch, e esse mesmo teste se repete em vários métodos:

```java
class Pedido {
    private String status = "NOVO";
    public void pagar() {
        if (status.equals("NOVO")) { status = "PAGO"; }
        else if (status.equals("PAGO")) { throw new IllegalStateException("Ja pago."); }
        else if (status.equals("ENVIADO")) { throw new IllegalStateException("Ja pago."); }
    }
    public void enviar() {
        if (status.equals("NOVO")) { throw new IllegalStateException("Pague antes de enviar."); }
        else if (status.equals("PAGO")) { status = "ENVIADO"; }
        else if (status.equals("ENVIADO")) { throw new IllegalStateException("Ja enviado."); }
    }
}
```

Problemas desse código: adicionar um estado novo obriga a alterar todos os métodos (viola o princípio aberto/fechado), as regras de um mesmo estado ficam espalhadas por vários métodos e as transições ficam escondidas em atribuições de uma variável.
O State resolve isso colocando o comportamento de cada estado em uma classe própria. O objeto principal (Context) apenas delega para o objeto de estado atual.

## Quando usar (aplicabilidade)
- O comportamento de um objeto depende do seu estado e precisa mudar em tempo de execução conforme esse estado.
- As operações têm condicionais grandes, com várias partes, que dependem do estado do objeto, e o mesmo teste de estado aparece repetido em vários métodos.
- Existem vários estados com regras de transição relevantes (ex.: pedido, documento em fluxo de aprovação, conexão de rede, máquina de venda, personagem de jogo).

## Quando evitar
- Poucos estados (por exemplo, dois), estáveis e com pouca lógica: um boolean ou um enum com switch é mais simples e suficiente.
- Quando o comportamento quase não varia entre os estados, a única diferença é um valor ou um rótulo.
- Quando os estados e as transições mudam com frequência por configuração (dados), e não por código: uma tabela de transições pode ser mais adequada.
- Exemplo de quando evitar: um interruptor com apenas dois estados (ligado/desligado) e uma única operação (alternar). Um boolean resolve; criar interface e duas classes só adiciona complexidade.
- Aplicar o State nesses casos aumenta o número de classes sem trazer benefício (excesso de engenharia).

## Participantes
- Context (ex.: Pedido): define a interface usada pelos clientes e mantém uma referência para uma instância de ConcreteState que representa o estado atual.
- State (ex.: interface EstadoPedido): define a interface que encapsula o comportamento associado a um estado particular do Context.
- ConcreteState (ex.: EstadoNovo, EstadoPago, EstadoEnviado): cada classe implementa o comportamento associado a um estado do Context.

## Colaborações
- O Context delega as requisições específicas de estado para o objeto ConcreteState atual.
- O Context pode passar a si mesmo como argumento para o objeto State, para que o estado acesse o Context quando necessário (por exemplo, para trocar o estado).
- O Context é a interface principal para os clientes. Os clientes podem configurar o Context com um estado inicial, mas depois disso não precisam lidar diretamente com os objetos State.
- Tanto o Context quanto as subclasses ConcreteState podem decidir qual estado sucede outro e em que circunstâncias.

## Estrutura (UML em texto)
```
Cliente --> Context
Context  - estado : State
Context  + requisicao()  { estado.tratar(this) }
Context  o--> State            (Context tem um State: composição/associação)
<<interface>> State + tratar(ctx : Context)
ConcreteStateA ..|> State      (implementa)
ConcreteStateB ..|> State      (implementa)
```

## Quem controla as transições
1. Os próprios ConcreteStates (forma mais comum): cada estado sabe qual é o próximo e chama `context.setEstado(new ProximoEstado())`. É flexível, mas cria dependência entre as classes de estado.
2. O Context: o Context centraliza as regras de transição. Funciona bem quando as regras são fixas e simples.
3. Tabela de transições: as transições ficam em uma estrutura de dados (estado atual + evento -> próximo estado). Facilita mudar regras, mas torna o comportamento menos explícito no código.

## Diagrama de transição do exemplo Pedido
```
[inicio] --> Novo
Novo    --pagar()-->   Pago
Novo    --cancelar()--> Cancelado
Pago    --enviar()-->  Enviado
Pago    --cancelar()--> Cancelado
Enviado: estado final (pagar, enviar e cancelar sao recusados)
Cancelado: estado final (pagar, enviar e cancelar sao recusados)
```

## Consequências
- (+) Localiza o comportamento específico de cada estado em uma classe e separa o comportamento de estados diferentes. Adicionar um estado novo é criar uma nova classe.
- (+) Torna as transições de estado explícitas: trocar o estado é trocar o objeto, em vez de atribuir valores a variáveis internas.
- (+) Elimina condicionais grandes e repetidas sobre o estado.
- (+) Objetos State podem ser compartilhados: se um estado não guarda variáveis de instância próprias, uma única instância pode ser reutilizada por vários Contexts (relação com Flyweight e Singleton).
- (-) Aumenta o número de classes, e o código fica mais espalhado do que um switch único.
- (-) Quando os ConcreteStates decidem as transições, eles passam a conhecer uns aos outros, o que aumenta o acoplamento entre as classes de estado.

## Exemplo em Java 1: Pedido
```java
interface EstadoPedido {
    void pagar(Pedido p);
    void enviar(Pedido p);
    void cancelar(Pedido p);
}

class Pedido {                                   // Context
    private EstadoPedido estado = new EstadoNovo();
    void setEstado(EstadoPedido e) { this.estado = e; }
    public void pagar()    { estado.pagar(this); }
    public void enviar()   { estado.enviar(this); }
    public void cancelar() { estado.cancelar(this); }
}

class EstadoNovo implements EstadoPedido {       // ConcreteState
    public void pagar(Pedido p)    { System.out.println("Pago."); p.setEstado(new EstadoPago()); }
    public void enviar(Pedido p)   { throw new IllegalStateException("Pague antes de enviar."); }
    public void cancelar(Pedido p) { System.out.println("Cancelado."); p.setEstado(new EstadoCancelado()); }
}

class EstadoPago implements EstadoPedido {
    public void pagar(Pedido p)    { throw new IllegalStateException("Ja pago."); }
    public void enviar(Pedido p)   { System.out.println("Enviado."); p.setEstado(new EstadoEnviado()); }
    public void cancelar(Pedido p) { System.out.println("Cancelado, valor estornado."); p.setEstado(new EstadoCancelado()); }
}

class EstadoEnviado implements EstadoPedido {
    public void pagar(Pedido p)    { throw new IllegalStateException("Ja pago."); }
    public void enviar(Pedido p)   { throw new IllegalStateException("Ja enviado."); }
    public void cancelar(Pedido p) { throw new IllegalStateException("Pedido ja enviado nao pode ser cancelado."); }
}

class EstadoCancelado implements EstadoPedido {
    public void pagar(Pedido p)    { throw new IllegalStateException("Pedido cancelado."); }
    public void enviar(Pedido p)   { throw new IllegalStateException("Pedido cancelado."); }
    public void cancelar(Pedido p) { throw new IllegalStateException("Ja cancelado."); }
}

public class Main {
    public static void main(String[] args) {
        Pedido pedido = new Pedido();   // comeca em EstadoNovo
        pedido.pagar();                 // Novo -> Pago
        pedido.enviar();                // Pago -> Enviado
    }
}
```
Por que funciona: Pedido (Context) não tem nenhum if sobre o estado; ele delega para o objeto em `estado`. Cada ConcreteState decide o que a operação faz naquele estado e qual é o próximo estado. Para adicionar o estado "Devolvido", cria-se uma nova classe sem alterar os métodos do Pedido.
Papéis: Context = Pedido; State = EstadoPedido; ConcreteStates = EstadoNovo, EstadoPago, EstadoEnviado, EstadoCancelado.

## Exemplo em Java 2: Conexão TCP (exemplo clássico do livro GoF)
```java
interface EstadoTCP {
    void abrir(ConexaoTCP c);
    void fechar(ConexaoTCP c);
    void enviar(ConexaoTCP c, String dados);
}

class ConexaoTCP {                               // Context
    private EstadoTCP estado = new TCPFechada();
    void mudarEstado(EstadoTCP e) { this.estado = e; }
    public void abrir()              { estado.abrir(this); }
    public void fechar()             { estado.fechar(this); }
    public void enviar(String dados) { estado.enviar(this, dados); }
}

class TCPFechada implements EstadoTCP {          // ConcreteState
    public void abrir(ConexaoTCP c)  { System.out.println("Conectando..."); c.mudarEstado(new TCPEstabelecida()); }
    public void fechar(ConexaoTCP c) { System.out.println("Ja esta fechada."); }
    public void enviar(ConexaoTCP c, String d) { throw new IllegalStateException("Conexao fechada."); }
}

class TCPEstabelecida implements EstadoTCP {
    public void abrir(ConexaoTCP c)  { System.out.println("Ja esta aberta."); }
    public void fechar(ConexaoTCP c) { System.out.println("Encerrando."); c.mudarEstado(new TCPFechada()); }
    public void enviar(ConexaoTCP c, String d) { System.out.println("Enviando: " + d); }
}
```
Por que funciona: a mesma chamada `enviar()` lança erro quando a conexão está fechada e transmite dados quando está estabelecida, sem nenhum if na ConexaoTCP. No livro GoF o exemplo usa TCPConnection (Context), TCPState (State) e TCPEstablished, TCPListen e TCPClosed (ConcreteStates).

## Usos incorretos (erros comuns) e como corrigir
### Erro 1: o cliente troca o estado manualmente
```java
// ERRADO: o cliente decide a transicao
pedido.setEstado(new EstadoEnviado());
pedido.enviar();
```
Problema: a regra de transição sai do padrão e vai para o cliente, que pode pular estados (enviar sem pagar). Correção: deixar `setEstado` com visibilidade restrita (pacote ou privada) e fazer as transições acontecerem dentro dos ConcreteStates ou do Context, como resposta às operações (`pedido.pagar()`, `pedido.enviar()`).

### Erro 2: reintroduzir condicionais sobre o estado
```java
// ERRADO: o Context continua testando o tipo do estado
public void enviar() {
    if (estado instanceof EstadoPago) { estado.enviar(this); }
    else { System.out.println("Nao pode enviar."); }
}
```
Problema: volta o if/else que o padrão deveria eliminar, e cada estado novo exige mudar o Context. Correção: o Context apenas delega (`estado.enviar(this)`), e cada ConcreteState decide o que fazer, inclusive recusar a operação.

### Erro 3: usar State onde um enum basta
Criar interface e várias classes para um interruptor com dois estados (ligado/desligado) e uma operação. Correção: usar boolean ou enum. O State compensa quando há vários estados com comportamentos diferentes em várias operações.

### Erro 4: ConcreteStates acoplados aos detalhes internos do Context
Estados que acessam e alteram diretamente muitos atributos internos do Context. Correção: o Context oferece operações bem definidas (como `setEstado` e métodos de negócio) e os estados usam somente essas operações.

## Confusões comuns
### State vs Strategy (a confusão mais comum)
Os dois têm a mesma estrutura de classes: um Context com referência para uma interface e várias implementações. A confusão acontece justamente porque o diagrama UML é praticamente igual. A diferença está na intenção e em quem troca o objeto:
- State: o objeto de estado muda durante a vida do Context, normalmente por decisão dos próprios estados ou do Context (transições internas). O cliente geralmente não escolhe o estado. Os estados costumam conhecer uns aos outros. Pergunta-chave: "o comportamento muda sozinho conforme o objeto evolui?".
- Strategy: o cliente escolhe o algoritmo e o injeta no Context. A estratégia não troca a si mesma, e as estratégias não se conhecem. Pergunta-chave: "existem formas alternativas de fazer a mesma tarefa e quem usa escolhe uma?".
Exemplos de Strategy: frete calculado por Sedex ou PAC, escolhido pelo cliente; ordenar uma lista por nome ou por data, conforme a escolha do usuário.
Exemplos de State: Pedido que passa de Novo para Pago e para Enviado conforme as operações; conexão TCP que fica aberta ou fechada conforme as chamadas a abrir() e fechar().

### State vs enum com switch
O enum com switch concentra toda a lógica em um lugar e é ótimo para poucos estados simples. O State distribui a lógica em classes, e isso compensa quando há muitos estados e muitas operações dependentes do estado.

## Padrões relacionados
- Flyweight: explica quando e como objetos State podem ser compartilhados.
- Singleton: estados sem atributos próprios costumam ser implementados com uma única instância.
- Strategy: mesma estrutura, intenção diferente (ver Confusões comuns).

## Exercícios (com critérios de correção)
### Exercício 1: identificar os participantes
Enunciado: no exemplo da ConexaoTCP, quem é o Context, quem é o State e quem são os ConcreteStates? O que acontece ao chamar `enviar()` com a conexão fechada?
Resposta esperada: Context = ConexaoTCP; State = EstadoTCP; ConcreteStates = TCPFechada e TCPEstabelecida. Com a conexão fechada, a chamada é delegada para TCPFechada, que lança IllegalStateException.
Erros comuns: dizer que a interface EstadoTCP é o Context; achar que a ConexaoTCP testa o estado com if.

### Exercício 2: adicionar um estado novo
Enunciado: adicione ao exemplo do Pedido o estado "Devolvido", que pode ser alcançado a partir de Enviado por uma operação `devolver()`. Quais classes mudam?
Resposta esperada: criar a classe EstadoDevolvido; adicionar `devolver(Pedido p)` à interface EstadoPedido e implementá-lo em todos os ConcreteStates (só EstadoEnviado faz a transição, os outros recusam); adicionar `devolver()` no Pedido apenas delegando. Nenhum if novo no Pedido.
Erros comuns: colocar um if no Pedido para checar se está Enviado; deixar o cliente chamar `setEstado(new EstadoDevolvido())`.

### Exercício 3: State ou Strategy?
Enunciado: um reprodutor de música tem os modos Tocando, Pausado e Parado, e o botão "play" faz coisas diferentes em cada modo. Outro sistema permite ao usuário escolher entre ordenar uma lista por nome ou por data. Qual padrão cabe em cada caso e por quê?
Resposta esperada: reprodutor = State, porque o comportamento do botão depende do modo atual e o modo muda conforme o uso. Ordenação = Strategy, porque o cliente escolhe o algoritmo e ele não muda sozinho.
Erros comuns: escolher pela estrutura de classes (que é igual nos dois) em vez da intenção.

### Exercício 4: refatorar condicionais
Enunciado: transforme o Pedido com if/else da seção "Problema que o State resolve" em uma solução com o padrão State. Descreva as classes antes de escrever o código.
Resposta esperada: interface EstadoPedido com pagar e enviar; classes EstadoNovo, EstadoPago e EstadoEnviado; Pedido guardando um EstadoPedido e delegando as chamadas, com as transições feitas nos ConcreteStates.

## O que lembrar antes de usar o State (checklist)
1. Existem vários estados e várias operações cujo comportamento muda conforme o estado? Se forem poucos e simples, prefira enum ou boolean.
2. Identifique os papéis: Context (o objeto que o cliente usa), State (interface comum) e ConcreteStates (um por estado).
3. Desenhe primeiro o diagrama de transições (estados, eventos e próximo estado).
4. Decida quem controla as transições: os ConcreteStates (mais comum) ou o Context.
5. O Context só delega: nenhum if/switch sobre o estado deve sobrar nele.
6. Não deixe o cliente trocar o estado diretamente.
7. Avalie se estados sem atributos podem ser compartilhados (uma instância só).
8. Não confunda com Strategy: no State, quem troca o comportamento é o próprio objeto ao mudar de estado.
