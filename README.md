# komercio-local-csv

Esta é a minha resolução para um problema proposto no curso de Back-end da Kenzie Academy.

***Objetivo:** Desenvolver uma API (Utilizando Python) que fosse capaz de fazer tratamentos de rotas e gravação de dados em arquivo CSV,
 com a utilização de testes (pytest) para o desenvolvimento.

### Algumas features:
- Rota GET /products - Sem query params
- Rota GET /products - Com query params
- Rota GET /products/<product_id>
- Rota POST /products - Seguir sequência de geração dos ids
- Rota PATCH /products/<product_id> Verificando se produto existe na base e retornando erro se não existir.
- Rota DELETE /products/<product_id> Verificando se produto existe na base e retornando erro se não existir.

### Tecnologias utilizadas:
- `Flask`
- `pytest`
