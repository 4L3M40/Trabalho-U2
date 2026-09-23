package br.edu.produto;

public class Principal {

    public static void main(String[] args) throws java.io.UnsupportedEncodingException {

        System.setOut(new java.io.PrintStream(System.out, true, "UTF-8"));

        // Criando objetos usando o construtor padrão
        Produto produto1 = new Produto();

        // Criando objetos usando o construtor com parâmetros (sobrecarga)
        Produto produto2 = new Produto("Notebook", 3500.00);
        Produto produto3 = new Produto("Mouse sem fio", 89.90);

        // Exibindo os dados de cada produto
        produto1.exibirDados();
        produto2.exibirDados();
        produto3.exibirDados();

        // Exibindo a quantidade total de produtos cadastrados via método estático
        Produto.exibirQuantidadeTotal();
    }
}
