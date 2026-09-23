# Cadastro de Produtos

Projeto desenvolvido em Java para demonstrar o cadastro e a exibição de produtos usando construtores, sobrecarga e atributo estático.

## Funcionalidades

- Criação de produtos usando o construtor padrão.
- Criação de produtos usando um construtor com nome e preço.
- Exibição dos dados de cada produto.
- Contagem total de produtos cadastrados.

## Estrutura do projeto

```text
src/
└── br/
    └── edu/
        └── produto/
            ├── Principal.java
            └── Produto.java
```

## Requisitos

- Java JDK 8 ou superior.

## Como executar

Na raiz do projeto, compile os arquivos:

```bash
javac -d out src/br/edu/produto/*.java
```

Depois, execute a classe principal:

```bash
java -cp out br.edu.produto.Principal
```

## Exemplo de saída

```text
Produto: Produto sem nome | Preço: R$ 0.0
Produto: Notebook | Preço: R$ 3500.0
Produto: Mouse sem fio | Preço: R$ 89.9
Quantidade total de produtos cadastrados: 3
```