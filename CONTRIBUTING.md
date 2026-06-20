# 🤝 Guia de Contribuição - Clean Taggy

Primeiramente, obrigado por se interessar em contribuir para o **Clean Taggy**! Este documento visa orientar novos desenvolvedores sobre como configurar o ambiente de desenvolvimento local e submeter alterações para o projeto.

---

## 💻 1. Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
- **Python** (versão 3.10 ou superior)
- **Git**
- **XAMPP** (ou qualquer servidor MySQL/MariaDB rodando localmente).

---

## ⚙️ 2. Configurando o Ambiente Local

Siga os passos abaixo para rodar o projeto na sua máquina de forma isolada e segura:

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/clean-taggy.git
cd clean-taggy
```

### Passo 2: Acessar a pasta do Backend
Todos os arquivos de configuração do Django estão na pasta `Back-end`.
```bash
cd Back-end
```

### Passo 3: Criar e Ativar o Ambiente Virtual (Virtualenv)
O ambiente virtual isola as bibliotecas deste projeto das demais existentes no seu computador.
- **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **No Linux/Mac:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Passo 4: Instalar as Dependências
Com o ambiente ativado (você verá `(venv)` no terminal), instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### Passo 5: Configurar o Banco de Dados
Com o banco MySQL rodando, aplique as migrações para gerar as tabelas do sistema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 6: Popular o Banco de Dados (Seed)
Para facilitar o desenvolvimento, possuímos um script que preenche o banco com usuários fictícios, transações, catálogo de metas e dados de comunidade.
```bash
python popular_banco.py
```
*(Após rodar o script, você poderá testar o sistema com o usuário **`gabriel_teste`** e a senha **`senha123`**).*

### Passo 7: Rodar o Servidor
```bash
python manage.py runserver
```
Acesse a aplicação no navegador via: `http://127.0.0.1:8000/`.

---

## 🛠️ 3. Padrões de Commit

Para manter o histórico do repositório organizado e fácil de ler, adotamos a convenção **Conventional Commits**.

Exemplos de como suas mensagens de commit devem ser estruturadas:
- `feat(funcionalidade): adiciona nova tela de login` (Novas features)
- `fix(dashboard): corrige calculo do mes atual zerado` (Correções de bugs)
- `docs(readme): atualiza instrucoes de instalacao` (Ajustes em documentações)
- `style(ui): melhora responsividade no menu mobile` (Alterações visuais)

---

## 🔄 4. Fluxo de Trabalho (Workflow)

Para enviar o seu código, siga este fluxo rigorosamente:

1. **Crie uma nova Branch** a partir da `main` com um nome descritivo. Ex:
   ```bash
   git checkout -b feature/minha-nova-funcionalidade
   ```
2. **Desenvolva e teste** suas alterações localmente.
3. **Adicione os arquivos** modificados e crie o commit:
   ```bash
   git add .
   git commit -m "feat(modulo): sua mensagem descritiva"
   ```
4. **Envie a branch para o repositório remoto**:
   ```bash
   git push origin feature/minha-nova-funcionalidade
   ```
5. **Abra um Pull Request (PR)** detalhando o que foi feito, as melhorias alcançadas e marque um colega de equipe para revisar o código.

---

### Ficou com dúvidas?
Sinta-se à vontade para buscar ajuda com a equipe no Jira, via Slack ou abrindo uma *Issue* detalhando seu bloqueio.

**Bom código! 🚀**
