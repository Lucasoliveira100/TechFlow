# TechFlow Tasks — Sistema Ágil de Gerenciamento de Tarefas

## Objetivo
Sistema básico para criar, listar, editar e excluir tarefas (CRUD), simulando um projeto ágil com Kanban, commits frequentes e CI com GitHub Actions.

## Como executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
-----
## Gestão de Mudanças (Mudança de Escopo)

Durante o desenvolvimento do projeto, foi simulada uma mudança de escopo com o objetivo de tornar o sistema mais aderente ao contexto de uma startup de logística.

A mudança consistiu na criação da seguinte regra de negócio:
- Tarefas com prioridade **crítica** passaram a exigir obrigatoriamente uma **data limite (deadline)**.

### Justificativa da Mudança
No setor de logística, o cumprimento de prazos é essencial para evitar atrasos em entregas e impactos operacionais. Dessa forma, a inclusão do campo *deadline* para tarefas críticas permite melhor priorização e controle das atividades.

### Gestão da Mudança
A alteração de escopo foi:
- Registrada no **Kanban** do GitHub Projects
- Documentada neste **README**
- Validada por meio de **testes automatizados**, garantindo que a regra seja cumprida pelo sistema

