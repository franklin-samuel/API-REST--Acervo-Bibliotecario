# Biblioteca API 📚

![image](https://github.com/user-attachments/assets/b7b769d6-0e22-4049-88a8-856e637f66a3)

Este projeto é uma API REST desenvolvida com **FastAPI** para gerenciamento de uma biblioteca, permitindo o controle de obras, usuários e empréstimos.

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** – Framework moderno e rápido para APIs RESTful
- **Uvicorn** – Servidor ASGI leve e eficiente
- **UUID** – Para identificação única das entidades
- **Pydantic** – Para validação de dados

## 🧩 Funcionalidades

- Cadastro de obras no acervo
- Remoção e listagem de obras disponíveis
- Registro de usuários
- Empréstimos de obras com controle de datas
- Histórico de empréstimos

## 📌 Organização Interna

- O acervo armazena os livros como um dicionário de `{obra_id: quantidade}`, garantindo desempenho e integridade na manipulação.
- As entidades são identificadas por UUID e possuem controle de criação automática.
- O sistema foi projetado com estrutura simples e modular para facilitar futuras integrações.

## 💡 Arquitetura Orientada a Objetos (POO)

Este projeto foi desenvolvido com base em **Programação Orientada a Objetos (POO)**, visando modularidade, reutilização de código e facilidade de manutenção.

As principais entidades — `Obra`, `Usuário` e `Empréstimo` — herdam de uma classe base comum (`BaseEntity`), que centraliza lógica como geração de ID e controle de data de criação.

**Características principais de POO aplicadas:**

- **Encapsulamento**: os dados e comportamentos estão isolados em classes específicas.
- **Herança**: uso da classe `BaseEntity` como superclasse comum.
- **Polimorfismo**: métodos como `__str__`, `__eq__` e `__hash__` são personalizados.
- **Abstração**: operações complexas estão encapsuladas em métodos do `Acervo`.

Essa estrutura garante que o sistema seja extensível e pronto para futuras integrações.

## 🌐 Futuras Expansões

Pretendemos utilizar essa API como **backend unificado** para as versões:

- **Web** (frontend em Django)
- **Mobile** (aplicativo em React Native)
- **Funcionalidades** (criação de mais endpoints para controle completo)

Assim, este projeto já foi estruturado pensando em escalabilidade e reaproveitamento de código.

## ▶️ Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/API-Rest--Acervo-Bibliotecario.git
cd fastAPI----AcervoBibliotecario

# 2. Crie e ative um ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn main:app --reload

# 5. Acesse a documentação interativa
http://127.0.0.1:8000/docs
```

## 👨‍💻 Desenvolvedores

- [@franklin-samuel](https://github.com/franklin-samuel)
- [@pedrohenrc](https://github.com/pedrohenrc)

