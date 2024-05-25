# Integrantes

- Bernardo do Nascimento Nunes
- Samuel Brum Martins
- Filipe Araújo

# Explicação do Sistema

Este repositório contém um sistema de blog desenvolvido em Django. O sistema oferece uma plataforma completa para criação, edição, visualização e gerenciamento de posts de blog, além de funcionalidades de autenticação de usuários, filtragem por categorias e busca.

## Funcionalidades Principais

O sistema inclui as seguintes funcionalidades:
- Autenticação de Usuários:
  Usuários podem se registrar, fazer login e logout.
  A autenticação é necessária para criar, editar ou deletar posts.

- Filtragem por Categorias:
  Os posts podem ser categorizados, e os usuários podem filtrar posts com base em categorias específicas.

- Gerenciamento de Posts:
  Usuários autenticados podem criar novos posts, editar posts existentes e deletar seus próprios posts.
  Usuários que não estejam logados poderão apenas visualizar os posts.
  
- Funcionalidade de Busca:
  Os usuários podem buscar posts pelo o título. 

# Tecnologias utilizadas

- _Python_ com o framework _Django_
- _SQLite_ para banco de dados
- _unittest_ para criação e execução de testes unitários

# Documentação de referência

- [Django](https://www.djangoproject.com/)
- [Testando com Django](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Testing)

# Execução
- Instalar as Dependências: 
  pip install -r requirements.txt
- Realizar as Migrações do Banco de Dados: 
  python manage.py makemigrations
  python manage.py migrate
- Iniciar o Servidor de Desenvolvimento:
  python manage.py runserver

### Testes de Sistema 

Para executar os testes de unidade:
    python manage.py test
