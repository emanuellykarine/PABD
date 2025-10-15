# API Kanban - Exemplos para Swagger

## Configuração do Banco
- **Nome do banco**: `kanban`
- **Senha**: `postgres`

---

#### **Usuários** (`/usuarios/`)
```json
{
  "nome": "Emanuelly Karine",
  "cpf": "12345678901"
}
```

```json
{
  "nome": "João Silva",
  "cpf": "98765432100"
}
```

```json
{
  "nome": "Maria Santos",
  "cpf": "11122233344"
}
```

#### **Etiquetas** (`/etiquetas/`)
```json
{
  "nome": "Backend",
  "cor": "laranja"
}
```

```json
{
  "nome": "Frontend",
  "cor": "verde"
}
```

```json
{
  "nome": "Urgente",
  "cor": "vermelho"
}
```

```json
{
  "nome": "Bug",
  "cor": "rosa"
}
```

#### **Projetos** (`/projetos/`)
```json
{
  "nome": "Sistema de Vendas Online",
  "descricao": "Desenvolvimento do novo sistema de vendas online com carrinho de compras e pagamento",
  "proprietario": 1
}
```

```json
{
  "nome": "App Mobile Delivery",
  "descricao": "Aplicativo mobile para delivery de comida com geolocalização",
  "proprietario": 2,
  "membros": [1, 2, 3]
}
```

#### **Colunas** (`/colunas/`)
```json
{
  "titulo": "A Fazer",
  "ordem": 1,
  "projeto": 1
}
```

```json
{
  "titulo": "Em Progresso",
  "ordem": 2,
  "projeto": 1
}
```

```json
{
  "titulo": "Em Revisão",
  "ordem": 3,
  "projeto": 1
}
```

```json
{
  "titulo": "Concluído",
  "ordem": 4,
  "projeto": 1
}
```

#### **Tarefas** (`/tarefas/`)
```json
{
  "titulo": "Implementar autenticação JWT",
  "descricao": "Adicionar sistema de autenticação usando JWT com refresh token",
  "coluna": 1,
  "responsavel": 1,
  "criador": 1,
  "prioridade": "alta",
  "tags": [1, 3]
}
```

```json
{
  "titulo": "Criar tela de login",
  "descricao": "Desenvolver interface de login responsiva com validação",
  "coluna": 1,
  "responsavel": 2,
  "criador": 1,
  "prioridade": "média",
  "tags": [2]
}
```

```json
{
  "titulo": "Configurar banco de dados",
  "descricao": "Configurar PostgreSQL e criar migrations iniciais",
  "coluna": 2,
  "responsavel": 1,
  "criador": 1,
  "prioridade": "alta",
  "tags": [1]
}
```

```json
{
  "titulo": "Corrigir bug no carrinho",
  "descricao": "Resolver problema de cálculo incorreto no total do carrinho",
  "coluna": 2,
  "responsavel": 3,
  "criador": 2,
  "prioridade": "alta",
  "tags": [4, 3]
}
```

#### **Comentários** (`/comentarios/`)
```json
{
  "tarefa": 1,
  "autor": 1,
  "texto": "Já comecei a implementação. Usando a biblioteca PyJWT."
}
```

```json
{
  "tarefa": 1,
  "autor": 2,
  "texto": "Lembrar de implementar o refresh token para maior segurança."
}
```

```json
{
  "tarefa": 2,
  "autor": 2,
  "texto": "Vou usar React com styled-components para esta tela."
}
```

## Filtrar tarefa 
GET /api/tarefas/?prioridade=alta&coluna=2

## Atribuir responsável
POST /api/tarefas/1/atribuir/
{
  "user_id": 3
}

## Adicionai membro
POST /api/projetos/1/add_membro/
{
  "user_id": 4
}

## Ver minhas tarefas
GET /api/projetos/1/minhas_tarefas/?user_id=3
