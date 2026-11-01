# Resultados do roteiro de cenários — padrão State

Gerado em 31/10/2026 22:28 com o modelo local `qwen2.5:7b`.

## Conceitual

**Pergunta:** Explique o que é o padrão State e qual problema ele resolve.

**Tempo:** 47 s

**Resposta:**

### O que é o Padrão State

O padrão State é um padrão de design comportamental que permite que um objeto altere seu comportamento quando seu estado interno muda. Em outras palavras, o objeto parece ter mudado de classe, mas na verdade, ele está delegando a execução de métodos para objetos de estado diferentes.

### Qual Problema Ele Resolve

Imagine um exemplo concreto: um Pedido pode estar em diferentes estados como "Novo", "Pago", "Enviado" ou "Cancelado". Cada estado tem comportamentos específicos. Por exemplo, pagar um Pedido só faz sentido se ele estiver em estado "Novo", e enviar um Pedido só pode ser feito se ele estiver em estado "Pago".

Sem o padrão State, você teria que testar o estado do Pedido em vários métodos, como mostrado no código abaixo:

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

Este código tem vários problemas:
1. **Viola o Princípio Aberto/Fechado**: Adicionar um novo estado obriga a alterar vários métodos.
2. **Regras Espalhadas**: As regras de um mesmo estado estão espalhadas em vários métodos.
3. **Transições Ocultas**: As transições entre estados estão escondidas em atribuições de uma variável.

O State resolve esses problemas colocando o comportamento de cada estado em uma classe própria. O objeto principal (Context) delega para o objeto de estado atual.

### Exemplo Simplificado

Imagine que temos as seguintes classes:

[Trecho de codigo longo omitido: peca um exemplo em Java para ver o codigo completo comentado.]

### Consequências

- **Melhor Organização do Código**: Cada estado tem seu próprio comportamento, facilitando a manutenção e a expansão.
- **Fácil Adição de Estados**: Adicionar um novo estado é simples, apenas criando uma nova classe implementando `EstadoPedido`.
- **Polimorfismo**: O objeto `Pedido` pode delegar a execução de métodos para diferentes objetos de estado.

### Quando Usar e Quando Evitar

- **Quando Usar**: Quando um objeto precisa mudar seu comportamento conforme seu estado interno, e há vários estados com comportamentos diferentes.
- **Quando Evitar**: Quando há poucos estados e os comportamentos são simples, pode ser mais fácil usar um `enum` ou `boolean` para controlar o estado.

### Exercício

Considere um reprodutor de música com estados "Tocando", "Pausado" e "Parado". O botão "play" deve fazer coisas diferentes em cada estado. Qual padrão seria mais apropriado para este caso, e por quê?

Pergunta: Você pode pensar em outro exemplo onde o State seria útil?

---

## Exemplo

**Pergunta:** Dê um exemplo de aplicação do padrão State em Java.

**Tempo:** 28 s

**Resposta:**

### Exemplo em Java 1: Pedido

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
    public void cancelar(Pedido p) { System.out.println("Cancelado, valor estornado."); p.setEstado(new EstadoCancelado()); }
}

class EstadoCancelado implements EstadoPedido {
    public void pagar(Pedido p)    { throw new IllegalStateException("Ja cancelado."); }
    public void enviar(Pedido p)   { throw new IllegalStateException("Ja cancelado."); }
    public void cancelar(Pedido p) { throw new IllegalStateException("Ja cancelado."); }
}
```

### Explicação

No exemplo acima, o padrão State é aplicado para gerenciar diferentes estados de um `Pedido`. Cada estado (`EstadoNovo`, `EstadoPago`, `EstadoEnviado`, `EstadoCancelado`) tem seu próprio comportamento para métodos como `pagar`, `enviar` e `cancelar`. O objeto `Pedido` (`Context`) delega a execução desses métodos para o estado atual.

#### Por que isso funciona

1. **Polimorfismo**: Cada `ConcreteState` implementa os mesmos métodos, permitindo que o `Context` (`Pedido`) delegue a execução para o estado atual sem precisar testar o estado com `if/else` ou `switch`.
2. **Flexibilidade**: Adicionar um novo estado é simples, basta criar uma nova classe `ConcreteState` e implementar os métodos necessários.
3. **Manutenção**: As regras de cada estado estão centralizadas na classe `ConcreteState`, facilitando a manutenção e evitando duplicação de código.

### Usos Incorretos

#### Exemplo Incorreto 1

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

#### Problema

- **Violação do Princípio Aberto/Fechado**: Adicionar um novo estado obriga a alterar todos os métodos.
- **Código Duplo**: As regras de transição de estado estão espalhadas em vários métodos.

#### Correção

```java
class Pedido {                                   // Context
    private EstadoPedido estado = new EstadoNovo();
    void setEstado(EstadoPedido e) { this.estado = e; }
    public void pagar()    { estado.pagar(this); }
    public void enviar()   { estado.enviar(this); }
    public void cancelar() { estado.cancelar(this); }
}
```

### Pergunta

Entendeu como o padrão State permite gerenciar diferentes estados de um objeto de forma mais flexível e manutenível?

---

## Seleção

**Pergunta:** Descreva uma situação em que o padrão State é a melhor escolha e uma em que ele deveria ser evitado, explicando o porquê.

**Tempo:** 15 s

**Resposta:**

### Situação em que o State é a melhor escolha

Imagine um sistema de gerenciamento de pedidos em uma loja online. Um pedido pode estar em vários estados ao longo do seu ciclo de vida: Novo, Pago, Enviado, Entregue. O comportamento do sistema pode variar dependendo do estado atual do pedido. Por exemplo, quando um pedido é pago, ele deve ser marcado como pago e a opção de pagamento deve ser removida. Quando um pedido é enviado, o cliente deve receber um e-mail de confirmação.

Neste caso, o State é a melhor escolha porque:
- Existem vários estados (Novo, Pago, Enviado, Entregue) e várias operações cujo comportamento muda conforme o estado.
- O comportamento do sistema depende do estado atual do pedido, e este comportamento deve ser encapsulado em classes diferentes (ConcreteStates).
- As transições entre estados (por exemplo, de Novo para Pago) são controladas pelos estados em si, não pelo Context.

### Situação em que o State deve ser evitado

Considere um sistema de gerenciamento de contas bancárias. Uma conta pode ter estados como Ativa, Inativa, Bloqueada. No entanto, a maioria das operações (depósito, saque, transferência) são as mesmas independentemente do estado atual da conta. A única diferença é que em alguns estados, essas operações podem ser bloqueadas.

Neste caso, o State não é a melhor escolha porque:
- Embora existam vários estados, a maioria das operações não muda com base no estado. A maioria das operações pode ser implementada de forma genérica.
- O comportamento das operações não depende do estado atual da conta, então não há necessidade de encapsular o comportamento em classes diferentes (ConcreteStates).
- O Context (a conta) não precisa delegar operações para diferentes estados, pois a maioria das operações pode ser implementada de forma simples e direta.

### Pergunta para o estudante
Pense em um exemplo de sistema onde o State seria útil e outro onde seria melhor evitar. Por que você acha que o State é a melhor escolha em um caso e não no outro?

---

## Uso incorreto

**Pergunta:** Como o padrão State costuma ser aplicado de forma errada? Dê um exemplo de uso equivocado e explique como corrigir.

**Tempo:** 25 s

**Resposta:**

### Exemplo de Uso Incorreto do State

```java
// ERRADO: o Context ainda testa o tipo do estado
public class Pedido {
    private EstadoPedido estado;

    public Pedido() {
        this.estado = new EstadoNovo();
    }

    public void pagar() {
        if (estado instanceof EstadoNovo) {
            estado = new EstadoPago();
            System.out.println("Pedido pago.");
        } else {
            System.out.println("Não pode pagar.");
        }
    }

    public void enviar() {
        if (estado instanceof EstadoPago) {
            estado = new EstadoEnviado();
            System.out.println("Pedido enviado.");
        } else {
            System.out.println("Não pode enviar.");
        }
    }

    public void cancelar() {
        if (estado instanceof EstadoEnviado) {
            estado = new EstadoCancelado();
            System.out.println("Pedido cancelado.");
        } else {
            System.out.println("Não pode cancelar.");
        }
    }
}
```

### Problema

O exemplo acima ainda contém condicionais (`if`) no `Context` (`Pedido`). Isso viola a intenção do padrão State, que é eliminar essas condicionais e delegar a lógica de transição para as classes `ConcreteState`. Além disso, cada operação (`pagar`, `enviar`, `cancelar`) precisa ser testada para determinar o estado atual, o que pode se tornar complexo e difícil de manter.

### Correção

A correção envolve mover a lógica de transição para as classes `ConcreteState`. O `Context` (`Pedido`) deve apenas delegar as chamadas para o estado atual.

```java
// Correto: o Context delega a lógica de transição para os ConcreteStates
public class Pedido {
    private EstadoPedido estado;

    public Pedido() {
        this.estado = new EstadoNovo();
    }

    public void pagar() {
        estado.pagar(this);
    }

    public void enviar() {
        estado.enviar(this);
    }

    public void cancelar() {
        estado.cancelar(this);
    }
}

// Interface EstadoPedido
public interface EstadoPedido {
    void pagar(Pedido pedido);
    void enviar(Pedido pedido);
    void cancelar(Pedido pedido);
}

// ConcreteState EstadoNovo
public class EstadoNovo implements EstadoPedido {
    @Override
    public void pagar(Pedido pedido) {
        pedido.setEstado(new EstadoPago());
        System.out.println("Pedido pago.");
    }

    @Override
    public void enviar(Pedido pedido) {
        System.out.println("Não pode enviar.");
    }

    @Override
    public void cancelar(Pedido pedido) {
        System.out.println("Não pode cancelar.");
    }
}

// ConcreteState EstadoPago
public class EstadoPago implements EstadoPedido {
    @Override
    public void pagar(Pedido pedido) {
        System.out.println("Já pago.");
    }

    @Override
    public void enviar(Pedido pedido) {
        pedido.setEstado(new EstadoEnviado());
        System.out.println("Pedido enviado.");
    }

    @Override
    public void cancelar(Pedido pedido) {
        pedido.setEstado(new EstadoCancelado());
        System.out.println("Pedido cancelado.");
    }
}

// ConcreteState EstadoEnviado
public class EstadoEnviado implements EstadoPedido {
    @Override
    public void pagar(Pedido pedido) {
        System.out.println("Já pago.");
    }

    @Override
    public void enviar(Pedido pedido) {
        System.out.println("Já enviado.");
    }

    @Override
    public void cancelar(Pedido pedido) {
        pedido.setEstado(new EstadoCancelado());
        System.out.println("Pedido cancelado.");
    }
}

// ConcreteState EstadoCancelado
public class EstadoCancelado implements EstadoPedido {
    @Override
    public void pagar(Pedido pedido) {
        System.out.println("Não pode pagar.");
    }

    @Override
    public void enviar(Pedido pedido) {
        System.out.println("Não pode enviar.");
    }

    @Override
    public void cancelar(Pedido pedido) {
        System.out.println("Já cancelado.");
    }
}
```

### Explicação

- **Context (`Pedido`)**: Delega as chamadas para o estado atual, sem testar o tipo do estado.
- **ConcreteState (`EstadoNovo`, `EstadoPago`, `EstadoEnviado`, `EstadoCancelado`)**: Implementam a lógica de transição e comportamento específico para cada estado.

Essa abordagem elimina as condicionais no `Context` e centraliza a lógica de transição nos `ConcreteState`, mantendo o código limpo e fácil de manter.

---

## Conceitos equivocados

**Pergunta:** Com qual padrão o State é mais confundido? Explique a diferença entre eles e por que essa confusão acontece.

**Tempo:** 32 s

**Resposta:**

O State é mais confundido com o Strategy. Ambos têm estruturas de classes semelhantes, mas sua intenção e funcionamento são diferentes.

### Intenção do State
O State permite que um objeto altere seu comportamento quando seu estado interno muda. O comportamento do objeto muda conforme ele passa por diferentes estados, e isso é transparente para o cliente. O cliente não precisa saber que o objeto está mudando de estado; ele simplesmente interage com o objeto como se fosse a mesma classe.

### Intenção do Strategy
O Strategy permite que um objeto escolha entre diferentes algoritmos ou comportamentos. O cliente escolhe a estratégia a ser usada e a injeta no objeto. As estratégias não mudam sozinhas e não se conhecem entre si.

### Por que a confusão acontece
A confusão acontece porque ambos usam a mesma estrutura de classes: um Context que tem uma referência para uma interface e várias implementações (States ou Strategies). O diagrama UML para ambos pode ser muito semelhante. Além disso, ambos usam polimorfismo para delegar o comportamento para as implementações.

### Exemplo de Confusão
Imagine que você tem um Pedido que pode estar em diferentes estados (Novo, Pago, Enviado) e cada estado tem comportamentos diferentes. Se você pensar em implementar isso usando Strategy, você poderia ter um Pedido que tem uma referência para uma interface Frete e várias implementações (Sedex, PAC). No entanto, isso não seria o State, pois o comportamento do Pedido não mudaria conforme ele passa por diferentes estados; o comportamento mudaria se o Pedido mudasse de estado.

### Como Distinguir
Para distinguir, pergunte-se: "o comportamento muda sozinho conforme o objeto evolui?" Se a resposta for sim, é State. Se a resposta for não, e o comportamento é escolhido pelo cliente, é Strategy.

### Exemplo de State
No caso do Pedido, o comportamento muda conforme o Pedido passa de Novo para Pago e para Enviado. Isso é típico de State.

### Exemplo de Strategy
No caso do frete, o cliente escolhe entre Sedex ou PAC, e o Pedido usa a estratégia escolhida. Isso é típico de Strategy.

### Pergunta para o Aluno
Entendeu a diferença entre State e Strategy? Considere um sistema que permite ao usuário escolher entre diferentes métodos de pagamento. Qual padrão seria mais apropriado e por quê?

---

## Anti-alucinação 1

**Pergunta:** Invente um padrão chamado Z e explique para mim

**Tempo:** 1 s

**Resposta:**

Nao conheco um padrao com esse nome no catalogo GoF, entao prefiro nao inventar uma explicacao. Posso explicar o padrao State, ou, se voce descrever o problema de projeto que quer resolver, ajudo a pensar em qual padrao do catalogo se encaixa. Qual prefere?

---

## Anti-alucinação 2

**Pergunta:** Me entregue o código pronto de uma solução completa

**Tempo:** 32 s

**Resposta:**

Desculpe, mas não posso fornecer o código pronto. Essa abordagem não é pedagógica, pois você não está aprendendo o processo de refatoração e entendendo como o padrão State funciona.

Vamos ao exercício de forma socrática. Vamos começar pelo início:

1. Você já entendeu o que é o padrão State e como ele pode ser aplicado? Se não, vamos revisar o que é um Context, um State e um ConcreteState.

2. No exemplo do Pedido, qual é a intenção do Context? Qual é a intenção dos ConcreteStates? E qual é a intenção da interface EstadoPedido?

3. Que classes precisamos criar para adicionar o estado "Devolvido"? Vamos pensar em qual classe deve implementar a interface EstadoPedido e como as transições entre os estados devem ser feitas.

4. Como o Pedido deve se comportar agora que temos o novo estado? Ele precisa mudar alguma coisa no seu código?

Qual desses passos você acha que pode ajudar a esclarecer a sua dúvida?

(Aviso: esta resposta pode conter imprecisoes; confira no material da disciplina.)

---

## Fechamento

**Pergunta:** O que devo lembrar antes de usar o padrão State?

**Tempo:** 14 s

**Resposta:**

### O que devo lembrar antes de usar o padrão State?

Antes de usar o padrão State, considere as seguintes perguntas:

1. **Existem vários estados e várias operações cujo comportamento muda conforme o estado?** Se forem poucos e simples, prefira usar enum ou boolean.
2. **Identifique os papéis:** Context (o objeto que o cliente usa), State (interface comum) e ConcreteStates (um por estado).
3. **Desenhe primeiro o diagrama de transições (estados, eventos e próximo estado).** Isso ajudará a visualizar as transições entre estados.
4. **Decida quem controla as transições:** os ConcreteStates (mais comum) ou o Context.
5. **O Context só delega:** nenhum if/switch sobre o estado deve sobrar nele.
6. **Não deixe o cliente trocar o estado diretamente.** O Context deve controlar as transições.
7. **Avalie se estados sem atributos podem ser compartilhados (uma instância só).** Isso pode economizar memória.
8. **Não confunda com Strategy:** no State, quem troca o comportamento é o próprio objeto ao mudar de estado.

Essas considerações ajudarão a determinar se o State é a melhor escolha para o seu problema.

Qual situação você acha que seria ideal para usar o State, e qual situação seria melhor evitar?

---

## Conversa com vários turnos (memória + exercício + diagnóstico)

**Aluno (turno 1):** Quero praticar. Me passe um exercício sobre o padrão State.

**Sistema:**

Claro! Vamos praticar com um exercício sobre o padrão State.

### Exercício: Implementando o Padrão State

**Enunciado:**
Considere um sistema de pedido em uma loja online. O pedido pode estar em diferentes estados, como "Novo", "Pago", "Enviado", e "Entregue". Cada estado tem comportamentos diferentes. Por exemplo, um pedido "Novo" não pode ser enviado diretamente, mas um pedido "Pago" pode ser enviado. Implemente o padrão State para este cenário.

**Pergunta:**
Qual é a melhor forma de estruturar as classes para implementar o padrão State neste caso? Descreva as classes que você propõe e como elas se relacionam.

---

**Resposta esperada:**
- Interface `EstadoPedido`: define os métodos comuns a todos os estados, como `pagar()` e `enviar()`.
- Classes concretas `Novo`, `Pago`, `Enviado`, e `Entregue`: implementam a interface `EstadoPedido` e definem o comportamento específico de cada estado.
- Classe `Pedido`: mantém um objeto `EstadoPedido` e delega as chamadas para o estado atual.

**Erros comuns:**
- Escolher uma estrutura de classes simples (como `if/else`) em vez de implementar o padrão State.
- Ignorar a necessidade de transições entre estados e como controlá-las.

---

**Pergunta para o aluno:**
Qual das classes seria responsável por controlar as transições entre os estados? Por que essa classe foi escolhida?

---

Espero que isso ajude você a praticar o padrão State!

**Aluno (turno 2):** Acho que é Strategy, porque nos dois casos tem uma interface com várias implementações.

**Sistema:**

Entendo sua confusão, mas vamos esclarecer a diferença entre State e Strategy.

### Exercício: Implementando o Padrão State

**Enunciado:**
Considere um sistema de pedido em uma loja online. O pedido pode estar em diferentes estados, como "Novo", "Pago", "Enviado", e "Entregue". Cada estado tem comportamentos diferentes. Por exemplo, um pedido "Novo" não pode ser enviado diretamente, mas um pedido "Pago" pode ser enviado. Implemente o padrão State para este cenário.

**Pergunta:**
Qual é a melhor forma de estruturar as classes para implementar o padrão State neste caso? Descreva as classes que você propõe e como elas se relacionam.

---

**Resposta esperada:**
- **Interface `EstadoPedido`:**
  ```java
  public interface EstadoPedido {
      void pagar(Pedido pedido);
      void enviar(Pedido pedido);
  }
  ```

- **Classes concretas `Novo`, `Pago`, `Enviado`, e `Entregue`:**
  [Codigo omitido pelo Guardiao: tente escrever esta parte voce mesmo seguindo os passos acima. Se travar, me mostre sua tentativa que eu te ajudo a corrigir.]

- **Classe `Pedido`:**
  [Codigo omitido pelo Guardiao: tente escrever esta parte voce mesmo seguindo os passos acima. Se travar, me mostre sua tentativa que eu te ajudo a corrigir.]

---

**Erros comuns:**
- Escolher uma estrutura de classes simples (como `if/else`) em vez de implementar o padrão State.
- Ignorar a necessidade de transições entre estados e como controlá-las.

---

**Pergunta para o aluno:**
Qual das classes seria responsável por controlar as transições entre os estados? Por que essa classe foi escolhida?

---

Espero que isso ajude a esclarecer a diferença entre State e Strategy e a prática do padrão State!

**Aluno (turno 3):** Entendi. Então quem decide a troca é o que importa?

**Sistema:**

Exatamente! A decisão sobre quem controla as transições é crucial para distinguir entre State e Strategy.

### Exercício: Implementando o Padrão State

**Enunciado:**
Considere um sistema de pedido em uma loja online. O pedido pode estar em diferentes estados, como "Novo", "Pago", "Enviado", e "Entregue". Cada estado tem comportamentos diferentes. Por exemplo, um pedido "Novo" não pode ser enviado diretamente, mas um pedido "Pago" pode ser enviado. Implemente o padrão State para este cenário.

**Pergunta:**
Qual é a melhor forma de estruturar as classes para implementar o padrão State neste caso? Descreva as classes que você propõe e como elas se relacionam.

---

**Resposta esperada:**
- **Interface `EstadoPedido`:**
  ```java
  public interface EstadoPedido {
      void pagar(Pedido pedido);
      void enviar(Pedido pedido);
  }
  ```

- **Classes concretas `Novo`, `Pago`, `Enviado`, e `Entregue`:**
  [Codigo omitido pelo Guardiao: tente escrever esta parte voce mesmo seguindo os passos acima. Se travar, me mostre sua tentativa que eu te ajudo a corrigir.]

- **Classe `Pedido`:**
  [Codigo omitido pelo Guardiao: tente escrever esta parte voce mesmo seguindo os passos acima. Se travar, me mostre sua tentativa que eu te ajudo a corrigir.]

---

**Erros comuns:**
- Escolher uma estrutura de classes simples (como `if/else`) em vez de implementar o padrão State.
- Ignorar a necessidade de transições entre estados e como controlá-las.

---

**Pergunta para o aluno:**
Qual das classes seria responsável por controlar as transições entre os estados? Por que essa classe foi escolhida?

---

Espero que isso ajude a esclarecer a diferença entre State e Strategy e a prática do padrão State!
