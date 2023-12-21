# Trabalho Final de Fundamento Redes de Computadores 2023/2

## Alunos
| Matrícula  | Aluno                            |
| ---------- | -------------------------------- |
| 20/2015984 | Breno Henrique de Souza          |
| 19/0026588 | Davi Lima da Silva               |
| 21/1030729 | Eric Rabelo Borges               |
| 21/1041043 | Juan Pablo Ricarte de Barros     |
| 20/0021541 | Karla Chaiane da Silva Feliciano |

## Sobre 
Este projeto tem como objetivo proporcionar aos alunos uma compreensão prática da arquitetura de protocolos de camada de aplicação mais recentes, com foco especial no HTTP, HTTPS e WebSocket. A aplicação a ser desenvolvida consiste em um serviço web que oferece um ambiente de encontro para diálogos, onde os clientes podem se conectar, ingressar em salas de chat e interagir em tempo real.

Recursos Principais:

* Autenticação e Registro de Usuários: Os usuários podem se cadastrar e fazer login na plataforma. A autenticação permite a personalização da experiência do usuário e rastreamento de participantes.

* Salas de Chat: Os usuários podem criar e ingressar em diferentes salas de chat, cada uma dedicada a um tópico específico.
Cada sala de chat possui um nome, descrição e lista de participantes atuais.

* Comunicação em Tempo Real com WebSockets: A comunicação entre os participantes é realizada em tempo real por meio do protocolo WebSocket.
Mensagens de chat são entregues instantaneamente aos participantes na sala.

* Recursos de Mensagens: Os usuários podem enviar mensagens de texto formatadas.
Suporte para o envio de emojis, imagens ou outros tipos de mídia.
Controles de Privacidade e Moderação:

* Registro de Atividades e Histórico de Chat: Registro de atividades para salas de chat, permitindo a revisão de mensagens antigas.
Recursos para exportar ou salvar o histórico de chat.

## Video de apresetação

https://www.youtube.com/watch?v=SzvQlCdPtmc

## Screenshots

![image](https://github.com/rabelzx/video-chat-app/assets/79341819/00f36451-6f1e-474a-9db4-063402cfa561)
![image](https://github.com/rabelzx/video-chat-app/assets/79341819/d3f6ca2e-df54-4432-9a8b-b07e79d3825b)
![image](https://github.com/rabelzx/video-chat-app/assets/79341819/f5405e29-ee76-4c14-9673-98620d107f74)

## Instalação 
**Linguagem**: Python e MySQL<br>
**Framework/Bibliotecas**: Flask, Flaskmysqldb e Flasksocketio <br>

Antes de relizar a instalação das dependências do projeto, é necessário ter o mysql instalado e criar uma base de dados com o nome 'video-chat-app'.
Agora para conseguir estabelecer a conexão Http e Https com o banco, será necessário rodar no terminal mysql os seguintes comandos:

```mysql
sudo mysql -u root

mysql> USE mysql;
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> exit;

sudo service mysql restart
``````
Para realizar a instalação do projeto, basta estar na pasta raiz do projeto e rodar o script "setup.sh" no terminal linux, que assim as dependências do projeto serão instaladas. A seguir um passo a passo de como executar:

* Passo 1
    ```
    chmod +x ./setup.sh
    ```
* Passo 2
    ```
    sudo ./setup.sh
    ```

Ao finalizar o script será possivel acessar o projeto com as urls a seguir ou com o comando python app.py

[localhost](localhost) <br>
http://www.projetofrc.com <br>
https://www.projetofrc.com
