# BGTDM Discord Bot Community

![discord-image](https://bs-uploads.toptal.io/blackfish-uploads/components/seo/5948054/og_image/optimized/how-to-make-a-discord-bot-7c0fe302b98b05b145682344b3a4ec59.png)

Este projeto foi desenvolvido para facilitar o controle e a gestão de uma comunidade de jogos do GTA SAMP (BGTDM Community). Com este bot, você pode gerenciar eficientemente a entrada e saída de novos usuários, fornecendo mensagens personalizadas de boas-vindas e despedida. Além disso, é possível criar comandos personalizados para interagir com os jogadores e oferecer à alta administração controle total sobre os usuários da comunidade.

## Índice
- [Como realizar a instalação?](#como-realizar-a-instalação)
- [Como criar um usuário para administrador?](#como-criar-um-usuário-para-administrador)
- [Como visualizar os comandos do projeto?](#como-visualizar-os-comandos-do-projeto)

## Como preparar a instalação?

Antes de iniciar a configuração dos containers que realizarão a execução do ambiente de mensagens do bot, é necessário realizar a alteração de configurações padrões como senhas dos ambientes.

1. **Alterando usuário e senha do banco de dados:** 
   - Acesse o arquivo `docker-compose.yaml` e altere o valor da variável de ambiente `POSTGRES_PASSWORD` para a senha que será utilizada no banco de dados.
   - Após alterar o valor da variável do docker-compose, acesse a pasta `endpoints`, copie o arquivo `.env-example` e cole com o nome de `.env` personalizando as chaves conforme necessidade (Altere a chave `DB_PASSWORD`) com o mesmo valor alterado no `docker-compose.yaml`.

2. **Alterando usuário e para chamada da API:** 
   - Na pasta `discord-bot`, copie o arquivo `.env-example` colando na mesma pasta com o nome `.env` e substitua as chaves `API_USERNAME` e `API_PASSWORD` pelo usuário e senha do administrador explicado abaixo.

## Como instalar o Docker e o Docker Compose?

Para testar os sistemas desenvolvidos é necessário que seja feita a instalação do Docker e o Docker Compose.

Abaixo, encontram-se links de instalação para facilitar o preparo do ambiente.

- [Como realizar a instalação do Docker](https://docs.docker.com/get-docker/)
- [Como realizar a instalação do Docker Compose](https://docs.docker.com/compose/install/)

## Executando os containers e criando o usuário administrador:

Para iniciar os containers e executar o sistema, utilize o seguinte comando:

```bash
docker-compose up -d && docker exec -it discord_django python manage.py createsuperuser
```

## Tecnologias utilizadas
1. [Python]()
2. [VueJs]()
3. [Docker]()
