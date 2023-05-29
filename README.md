# 🚨 O projeto não está funcionando corretamente, corrigir. 🚨

# mini_twitter_REST
Implementar uma API REST em que um usuário possa realizar um cadastro, publicar Posts e ver as publicações de outros usuários.

## Referencias
https://sourcery.blog/how-to-build-api-with-django-rest-framework-and-postgresql/
https://github.com/shilpavijay/TwitterClone/blob/main/Tweets/models.py
https://kriyavikalpa134158342.wordpress.com/2020/11/21/twitter-clone-with-django-rest-framework-i/

# Arquivo `requirements.txt` rode o comando após fazer o clone do projeto
 O comando `pip install -r requirements.txt`
 O gerenciador de pacotes cuidará de baixar e instalar as versões corretas de todos os pacotes que foram utilizados no sistema.


# Casos de Uso
## CASO 1: Cadastro de usuário
O ator faz o cadastro no sistema através da API. Como usuário, ele deve poder fazer o cadastro, para que ele tenha acesso ao Login. 

# CASO 2: Autenticação (Login)
## Autenticação de usuário
Foi usado o módulo JWT do Python - PyJWT por ser melhor compreensível e fácil de implementar do que o JWT do Django Rest Framework
- O ator cria um post. Esta publicação é persistida no sistema. Como usuário, ele deve poder criar uma publicação, para que possa ser vista por outros usuários do sistema.

# CASO 3: Fazer uma publicação
- O ator cria um post. Esta publicação é persistida no sistema. Como usuário, ele deve poder criar uma publicação, para que possa ser vista por outros usuários do sistema.

# CASO 4: Feed geral
O ator deve receber, no formato JSON, o feed dos últimos 10 posts utilizando paginação.




# 📜 Regras de negócio
O usuário não deve ver os próprios Posts.