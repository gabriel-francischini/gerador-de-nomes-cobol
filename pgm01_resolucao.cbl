       identification division.
       program-id. pgm01_resolucao.


       environment division.
       input-output section.
       file-control.
           select ARQUIVO-ENTRADA assign to disk
               organization is line sequential.
           select RELATORIO-SAIDA assign to disk.

       data division.
       working-storage section.
      * file section.
      * fd ARQUIVO-ENTRADA
      *     label record are standard
      *value of file-id is "ENTRADA.DAT".


       01 cliente.
           02 rg-do-cliente pic 9(10).
           02 nome-do-cliente pic x(30).
           02 estado pic x(02).
           02 cidade pic x(30).


       working-storage section.
       77 fim-de-arquivo pic x(03) value "nao".
       77 numero-da-linha pic 9(02) value 25.
       77 numero-da-pagina pic 9(02) values zeroes.

       01 carimbo-do-numero-da-pagina.
           02 filler pic x(70) values spaces.
           02 filler pic x(05) value "PAG. ".
           02 carimbo-numero-da-pagina pic ZZ9.
           02 filler pic x(02) value spaces.

       01 carimbo-do-titulo.
           02 filler pic x(29) value spaces.
           02 filler pic x(21) value "RELATORIO DE CLIENTES".
           02 filler pic x(30) value spaces.

       01 carimbo-do-cabecalho.

       01 carimbo-do-rg-e-nome.
       02 filler pic x(10).
