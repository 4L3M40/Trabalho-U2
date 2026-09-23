package br.edu.produto;

public class Produto {

    // Atributos de instância
    private final String nome;
    private final double preco;

    // Atributo estático (compartilhado entre todos os objetos)
    private static int quantidadeTotal = 0;

    // Construtor padrão (sem parâmetros)
    public Produto() {
        this.nome = "Produto sem nome";
        this.preco = 0.0;
        quantidadeTotal++; // incrementa o total a cada objeto criado
    }

    // Construtor com parâmetros (sobrecarga do construtor padrão)
    public Produto(String nome, double preco) {
        this.nome = nome;
        this.preco = preco;
        quantidadeTotal++; // incrementa o total a cada objeto criado
    }

    // Método de instância para exibir os dados do produto
    public void exibirDados() {
        System.out.println("Produto: " + nome + " | Preço: R$ " + preco);
    }

    // Método estático para exibir a quantidade total de produtos cadastrados
    public static void exibirQuantidadeTotal() {
        System.out.println("Quantidade total de produtos cadastrados: " + quantidadeTotal);
    }
}
