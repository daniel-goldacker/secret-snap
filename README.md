# secret-snap

O **secret-snap** é uma aplicação Flask que permite codificar e decodificar mensagens secretas dentro de imagens. Utilizando técnicas de esteganografia, a aplicação permite que mensagens sejam ocultas em imagens PNG e recuperadas posteriormente.

## Funcionalidades

- **Codificar Mensagem**: Envia uma imagem e uma mensagem para a API e recebe uma imagem com a mensagem codificada.
- **Decodificar Mensagem**: Envia uma imagem com uma mensagem codificada para a API e recebe a mensagem oculta.


## Instalação

Para rodar o projeto, siga os seguintes passos:

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/usuario/secret-snap.git
    cd secret-snap
    ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate   # No Windows use: venv\\Scripts\\activate
    ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Inicie a aplicação**:
    ```bash
    python app.py
    ```

5. **Acesse a documentação Swagger**:
    Abra seu navegador e vá para `http://localhost:5000/swagger` para visualizar e testar a API.

## Uso da API

### Codificar Mensagem

**Endpoint**: `/encode`  
**Método**: `POST`

**Parâmetros**:

- `file` (arquivo): Imagem PNG para codificação.
- `message` (string): Mensagem a ser codificada na imagem.

**Resposta**: Imagem PNG com a mensagem codificada.

### Decodificar Mensagem

**Endpoint**: `/decode`  
**Método**: `POST`

**Parâmetros**:

- `file` (arquivo): Imagem PNG com a mensagem codificada.

**Resposta**: Mensagem oculta na imagem.

