# SeguranÃ§a e publicaÃ§Ã£o

O projeto nÃ£o requer credenciais, tokens, senhas ou serviÃ§os externos para execuÃ§Ã£o local.

Antes de publicar:

1. confirme que `data/raw/` continua ignorado pelo Git;
2. nÃ£o adicione `.streamlit/secrets.toml`, arquivos `.env` ou ambientes virtuais;
3. execute `git status --ignored` e revise arquivos nÃ£o rastreados;
4. execute os testes, o lint e uma verificaÃ§Ã£o de segredos do provedor Git escolhido;
5. confirme que nenhuma captura de tela contÃ©m caminho local, dados pessoais ou sessÃµes abertas.

Relatos de vulnerabilidade devem ser enviados de forma privada ao mantenedor do repositÃ³rio, sem
incluir credenciais ou documentos financeiros nÃ£o pÃºblicos.
