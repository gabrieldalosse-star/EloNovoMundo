# Plataforma pedagógica: arquitetura, bancos e instalação

Preparado para Gabriel em 14/10/2026. Fontes oficiais consultadas nessa data. Valores em dólar, sem conversão cambial, impostos ou promessa de gratuidade permanente.

## 1. Qual caminho escolher

Minha recomendação para começar é **GitHub + React/Vite + Firebase Authentication + Firestore + Cloud Functions + Firebase Hosting**, pela continuidade com seus aplicativos Firebase. Se a prioridade for cruzar muitos cadastros, gerar relatórios SQL e integrar sistemas administrativos, **Supabase/PostgreSQL** merece ser a escolha inicial. Não é preciso adotar três bancos ao mesmo tempo.

| Opção | Quando faz sentido | Vantagem neste projeto | Atenção |
|---|---|---|---|
| Firebase / Firestore | Aproveitar o ecossistema já usado nos apps | Login e documentos, com biblioteca web integrada | Modelagem sem joins tradicionais; leituras, índices e listeners afetam custo |
| Supabase / PostgreSQL | Relações entre alunos, matrículas, turmas e relatórios | SQL, chaves estrangeiras e segurança por linha | Políticas RLS e operações transacionais precisam ser bem implementadas |
| Neon / PostgreSQL | Controlar o backend e o modelo relacional | PostgreSQL gerenciado com ambientes/branches | Selecionar e configurar os componentes de aplicação e identidade |

Essas três opções são bancos/serviços externos. **GitHub guarda versões do código. GitHub Pages serve arquivos estáticos. Nenhum deles substitui o banco da escola.** O frontend pode ser público e ainda assim exigir autenticação para acessar dados, mas nenhum dado privado deve estar embutido no HTML, JavaScript ou repositório.

Referências: [Firestore](https://firebase.google.com/docs/firestore), [Supabase Database](https://supabase.com/docs/guides/database/overview), [Neon Console](https://neon.com/docs/get-started/signing-up), [GitHub Pages](https://docs.github.com/en/pages).

## 2. Arquitetura proposta para uso institucional

O navegador recebe apenas a interface e as configurações públicas. O login emite identidade; o backend verifica vínculo ativo, escola, função, turma e expiração antes de executar operações. Os arquivos ficam em armazenamento próprio para documentos. Métricas são consultadas por uma função administrativa, sem expor credenciais do Google Cloud.

| Camada | Escolha Firebase | Alternativa PostgreSQL |
|---|---|---|
| Código | Repositório GitHub privado | Mesmo modelo |
| Interface | React + Vite + TypeScript | Mesmo modelo |
| Hospedagem | Firebase Hosting | Serviço de frontend escolhido pela escola |
| Login | Firebase Authentication | Supabase Auth ou provedor configurado no backend |
| API e regras de negócio | Cloud Functions | API/Edge Functions/serviço próprio |
| Dados estruturados | Firestore | PostgreSQL Supabase ou Neon |
| Anexos | Drive ou Cloud Storage | Storage do provedor ou Drive |
| IA | Backend → OpenAI API | Mesmo princípio |
| Consumo | Backend → Cloud Monitoring | Backend → consultas SQL e métricas do provedor |

### Entidades e relações

- `schools`: identidade e configurações da escola.
- `users`: identidade estável vinculada ao provedor de autenticação.
- `memberships`: usuário, escola, função, segmentos, turmas e vigência.
- `classes`: turma, segmento, ano letivo e disciplinas.
- `students`: cadastro estável, separado das matrículas anuais.
- `enrollments`: aluno + turma + início + fim. Transferir não apaga o passado.
- `plans`: autoria, turma, data, estado e versão corrente.
- `planVersions`: snapshots imutáveis de cada envio/revisão/aprovação.
- `planComments`: comentário, autor, campo e versão.
- `lessons`: turma, data, horário e plano vinculado; conteúdo realizado separado do planejado.
- `attendance`: aula + matrícula + marcação. Ausente de registro não é falta.
- `attendanceCorrections`: valor anterior, novo valor, motivo e responsável.
- `messages` / `acknowledgements`: comunicado e ciência explícita por destinatário.
- `documents`: referência do arquivo, proprietário e escopo de acesso.
- `integrationEvents`: identificador idempotente, origem, destino, tentativa e resultado.
- `auditEvents`: alterações relevantes, sem armazenar tokens e senhas.
- `infraSnapshots`: métricas e instante da coleta, sem nomes de alunos.

No Firestore, a organização recomendada é `schools/{schoolId}/classes/{classId}`, e coleções equivalentes para as demais entidades. IDs de frequência e aula devem ser determinísticos quando representarem a mesma ocorrência. Aprovar plano, concluir chamada e corrigir registro exigem transações.

**O piloto incluído não usa essa modelagem institucional completa.** Ele guarda o ambiente de cada administrador em `pilotWorkspaces/{uid}`, com controle de revisão e teto de 700.000 bytes. É uma implementação para validar interação e regras. Migrar para coleções/tabelas por entidade é obrigatório antes de escalar para a escola.

### Matriz de acesso planejada

| Perfil | Pode atuar | Não recebe automaticamente |
|---|---|---|
| Administrador | Usuários, configurações e infraestrutura | Conteúdo sensível sem concessão pedagógica específica |
| Direção | Indicadores e escopos institucionais autorizados | Poder de editar toda chamada ou aprovar tudo |
| Coordenação | Professores/segmentos vinculados, revisão de planos | Outras escolas ou segmentos |
| Professor | Turmas e aulas atribuídas | Turmas de colegas e painel financeiro |
| Secretaria | Cadastros e frequência conforme concessão | Devolutivas confidenciais e configurações técnicas |
| Substituto | Aulas e período determinados | Acesso após expirar o vínculo |

No pacote atual, o backend libera **somente administradores autorizados**. Os outros perfis não estão implementados nem liberados. Esconder um botão não protege uma API; os testes precisam tentar a chamada diretamente.

## 3. Tela separada: Infraestrutura e consumo

Acesse esse item no menu do piloto. Ela contém:

1. Tamanho dos dados e índices do Firestore em MiB/GiB.
2. Porcentagem do limite interno definido pela escola.
3. Comparação informativa com a referência de 1 GiB da franquia elegível.
4. Leituras, gravações e exclusões observadas nas últimas 24 horas móveis.
5. Armazenamento de backups e PITR, quando houver amostras.
6. Fonte da métrica, projeto, banco e horário da medição/coleta.
7. Configuração do limite interno por administrador e registro de auditoria.
8. Aviso visual a partir de 80%; acima de 100%, indicação de limite interno excedido.

**Exemplo ilustrativo, não consumo real da sua escola:** 256 MiB de dados e índices para referência de 1 GiB = `256 ÷ 1.024 × 100 = 25%`.

O limite de 1 GiB pode significar referência de franquia, e um limite de 5 GiB pode ser uma escolha administrativa. Nenhum deles deve ser rotulado como a capacidade total do Firestore no plano pago. A barra não interrompe gravações nem impede cobranças.

O coletor consulta `firestore.googleapis.com/storage/data_and_index_storage_bytes`. Backups e PITR têm métricas separadas. Leituras usam `document/read_ops_count`; gravações, `document/write_ops_count`; exclusões, `document/delete_ops_count`. O filtro restringe a base selecionada. Se vários aplicativos compartilham essa base, o total inclui todos eles. Separação por app exige projetos/bases distintos ou contabilidade da aplicação.

O backend retorna `null` quando não recebe dado verificável. Não há varredura dos alunos para calcular tamanho. O cache dura até 3 minutos; uma medição de armazenamento com mais de 15 minutos é sinalizada como antiga. As 24 horas móveis **não são a janela diária da franquia**; por isso o pacote não calcula “% da cota diária de leituras” usando esse período.

Ainda não implementado: custo do mês via exportação de faturamento, gráfico histórico persistente, consumo de Drive/Cloud Storage, limites de IA, notificações externas e teste de restauração. O painel informa essas ausências. Tamanho de backup não prova que ele pode ser restaurado.

Fontes: [métricas Firestore](https://docs.cloud.google.com/monitoring/api/metrics_gcp_d_h#firestore), [monitoramento e diferenças do faturamento](https://firebase.google.com/docs/firestore/monitor-usage), [recursos monitorados](https://docs.cloud.google.com/monitoring/api/resources#tag_firestore.googleapis.com/Database).

## 4. Preparar o computador e o GitHub

### 4.1 Testar sem contratar serviços

1. Instale Node.js 22 e Git. O runtime configurado das Cloud Functions é Node 22.
2. Extraia o ZIP para uma pasta, por exemplo `Documentos/elo-pedagogico`.
3. Abra a pasta no VS Code e selecione Terminal → Novo terminal.
4. Execute `npm ci`. Aguarde a instalação terminar.
5. Execute `npm test` para verificar as regras do piloto e os cálculos.
6. Execute `npm run dev` e abra o endereço informado, normalmente `http://localhost:5173`.
7. Sem `.env`, o sistema mostra o modo local. Use somente nomes fictícios. Atualizar a página conserva os dados neste navegador, mas outro computador não os verá.
8. Abra **Infraestrutura e consumo**: os dados aparecerão indisponíveis até conectar Firebase. Isso é esperado.

### 4.2 Guardar no GitHub

1. No GitHub, selecione New repository.
2. Dê o nome `elo-pedagogico` e escolha **Private** para começar.
3. Crie o repositório vazio. Não inicialize um README remoto se vai enviar a pasta completa.
4. Na pasta local, execute:

```bash
git init
git add .
git commit -m "Estrutura inicial da plataforma pedagogica"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/elo-pedagogico.git
git push -u origin main
```

5. Substitua `SEU-USUARIO` pelo seu nome real do GitHub. Autentique pelo mecanismo normal do Git/GitHub; não coloque token na URL.
6. Confirme que `.env`, `node_modules`, contas de serviço e senhas não foram enviados. O `.gitignore` já exclui esses caminhos comuns.
7. A aba Actions executará testes e compilação. Falha deve ser corrigida antes do deploy.
8. Não envie apenas o ZIP para a raiz esperando que o aplicativo rode. O repositório precisa conter os arquivos extraídos, incluindo `package.json`, `src`, `functions` e `.github`.

O workflow `pages-demo.yml` é manual e **publica somente a demonstração sem Firebase**. Para acioná-lo, seria necessário configurar Pages → Source: GitHub Actions e executar o workflow. Ele não foi executado nesta entrega. Para o sistema institucional, prefira a hospedagem apropriada ao backend escolhido. GitHub Pages tem restrições para negócios online e SaaS comercial; avalie os termos antes de usar.

Fontes: [build e deploy Vite](https://vite.dev/guide/static-deploy.html), [restrições do Pages](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/github-pages-limits).

## 5. Caminho A — Firebase, passo a passo

### 5.1 Criar um ambiente isolado

1. Acesse [Firebase Console](https://console.firebase.google.com/).
2. Crie um projeto exclusivo de teste, por exemplo `escola-pedagogico-dev`. Não reutilize o banco de outro app nesta primeira configuração.
3. Registre o ID exato gerado; nome exibido e ID podem ser diferentes.
4. Analytics é opcional para este piloto.
5. Em Configurações do projeto → Seus aplicativos, registre um aplicativo Web.
6. Copie `apiKey`, `authDomain`, `projectId` e `appId` do objeto de configuração.
7. Na pasta do projeto, copie `.env.example` para `.env` e preencha os quatro campos `VITE_FIREBASE_*` correspondentes. Esses campos web identificam o projeto, não concedem privilégios administrativos. Regras e backend continuam necessários.
8. Use `VITE_FUNCTIONS_REGION=southamerica-east1` se mantiver a região padrão do pacote. Frontend e funções precisam concordar.

### 5.2 Criar o banco e o login

1. Em Firestore Database, crie a base **Standard**, modo nativo, ID `(default)`.
2. Escolha a região com cuidado; considere latência, preço e requisitos da escola. O exemplo das funções usa São Paulo. Não há promessa de franquias regionais para outros produtos.
3. Selecione regras restritas/produção, não regras públicas de teste.
4. Em Authentication → Sign-in method, habilite Google e Email/Password.
5. Informe o e-mail de suporte exigido pelo provedor Google.
6. Em Authentication → Settings → Authorized domains, inclua o domínio de hospedagem. Para desenvolvimento, verifique se `localhost` está autorizado; adicione-o apenas no projeto de teste se necessário.
7. Para e-mail/senha, crie o usuário de teste na área Users. Não existe cadastro público no frontend do pacote.
8. Configure/valide os modelos de recuperação e verificação de e-mail. O frontend oferece recuperação e envio da verificação.

Referências: [registrar app web](https://firebase.google.com/docs/web/setup), [login Google](https://firebase.google.com/docs/auth/web/google-signin), [domínios e fluxos de e-mail](https://firebase.google.com/docs/auth/web/email-link-auth).

### 5.3 Ativar backend e publicar

Cloud Functions exige configuração de faturamento compatível com implantação. Este pacote usa Blaze para o backend; franquias não dispensam o vínculo de faturamento. Configure orçamento antes de implantar. **Alerta de orçamento não é teto rígido de despesa.**

1. No projeto de teste, habilite o plano Blaze se ainda não estiver habilitado e configure avisos de orçamento no Google Cloud Billing.
2. Instale as ferramentas:

```bash
npm install -g firebase-tools
firebase login
firebase use --add
npm ci --prefix functions
```

3. Selecione o projeto de teste e dê a ele o alias `dev`. O comando cria `.firebaserc` com o vínculo.
4. Copie `functions/.env.example` para `functions/.env.SEUIDDOPROJETO`. Substitua `SEUIDDOPROJETO` pelo ID exato, sem colchetes.
5. Mantenha `FIRESTORE_DATABASE_ID=(default)` e `STORAGE_BUDGET_BYTES=1073741824` inicialmente. O segundo valor é referência interna, ajustável pela tela.
6. Compile e publique as regras e funções:

```bash
npm --prefix functions run build
firebase deploy --only firestore,functions --project dev
```

7. O comando utiliza a identidade da sua sessão de deploy. O servidor usa a conta de execução, sem chave administrativa embutida no frontend.
8. Compile a interface após preencher o `.env` e publique:

```bash
npm run build
firebase deploy --only hosting --project dev
```

9. Abra a URL que o Firebase retornar e confirme o domínio na lista de autorizados do Authentication.
10. Se alterar o `.env` da interface, faça novo build e deploy. O Vite incorpora as variáveis públicas na compilação.

Não copie as regras deste pacote sobre o banco de um sistema existente: elas negam todo acesso direto do cliente. No projeto novo, isso é intencional; o backend valida todas as operações e usa o Admin SDK. Em uma migração, as regras precisam ser integradas e testadas, não substituídas cegamente.

Fontes: [primeiras funções](https://firebase.google.com/docs/functions/get-started), [runtimes e configuração](https://firebase.google.com/docs/functions/manage-functions).

### 5.4 Autorizar o primeiro administrador

1. Entre no aplicativo com sua conta Google ou com e-mail/senha já criado.
2. O primeiro acesso pode dizer “sem autorização”; o UID será exibido. Isso confirma apenas a identidade.
3. No Firestore Console, crie a coleção `systemMembers`.
4. Crie um documento cujo ID seja **exatamente o UID** do usuário.
5. Adicione `role` como string `admin` e `active` como boolean `true`.
6. Se o login for e-mail/senha, clique para enviar verificação, confirme o e-mail e volte ao app.
7. Clique em **Verificar autorização novamente**. O backend confere a autorização no Firestore a cada operação.
8. Para revogar, mude `active` para boolean `false`. Isso não apaga o histórico. O próximo pedido será negado, embora informação já carregada no navegador não possa ser recolhida retroativamente.
9. Não crie esse documento por um botão que o próprio usuário possa acionar livremente. Só o operador autorizado do projeto deve promovê-lo.

### 5.5 Ligar as métricas reais

1. Abra Google Cloud Console no MESMO projeto.
2. Em APIs e serviços → Biblioteca, habilite **Cloud Monitoring API**.
3. Localize a função `getInfrastructure` em Cloud Run/Cloud Functions e identifique a conta de serviço de execução nas configurações.
4. Em IAM, conceda a essa conta a função **Monitoring Viewer** (`roles/monitoring.viewer`) no projeto monitorado. Não é necessário conceder Owner.
5. Garanta que a conta de execução tem acesso aos documentos internos usados pelo backend. Para um projeto com conta dedicada, conceda os privilégios de dados necessários; a implantação pode exigir permissões adicionais do operador, diferentes das permissões de execução.
6. Faça uma alteração fictícia no piloto para gerar operações e aguarde a emissão das métricas.
7. Abra **Infraestrutura e consumo** e clique em Atualizar. Confira o projeto, banco e horário.
8. Compare armazenamento e operações com o console oficial. Uma ausência de amostra pode ser atraso, serviço ainda sem dados ou configuração faltando; não conclua que o uso é zero.
9. Ajuste o limite interno na própria tela. Por exemplo, 2 GiB = `2 × 1.073.741.824 = 2.147.483.648 bytes`.
10. Para erros, consulte os logs da função. Verifique IAM, Monitoring API, ID de projeto e filtro `database_id` antes de alterar código.

O pacote não foi conectado à sua conta Firebase nesta conversa. As funções foram preparadas para implantação, mas o teste integrado depende desses passos e das suas permissões.

### 5.6 Testes antes de liberar a escola

- Conta não autorizada deve conseguir autenticar a identidade e continuar sem acesso aos dados.
- Usuário sem e-mail verificado deve receber negativa.
- Remover `active` deve negar o próximo pedido.
- Duas abas alterando a mesma revisão devem gerar conflito, não perda silenciosa.
- Concluir chamada sem todos os registros deve falhar.
- Repetir turma/data/horário deve atualizar a ocorrência, não criar outra.
- Plano aprovado deve permanecer preservado; alterações partem de cópia.
- Tela de infraestrutura não deve retornar métricas a não administradores, mesmo via chamada direta.
- Antes de incluir professores: implementar papéis/escopos, testar banco por entidade, backup e restauração, anexos privados e dispositivos móveis.

## 6. Caminho B — Supabase/PostgreSQL, passo a passo

Este caminho é alternativo. Os arquivos SQL ajudam a construir o banco, mas a interface Firebase do pacote não passa a usar Supabase só por executá-los. É preciso escrever o adaptador de dados e autenticação correspondente.

1. Acesse [Supabase](https://supabase.com/) e crie uma organização/projeto de teste.
2. Escolha região e uma senha forte para o banco. Guarde a senha fora do GitHub.
3. Aguarde o provisionamento e abra **SQL Editor**.
4. Em projeto novo e vazio, execute `sql/01_nucleo_postgres.sql`. Ele cria escolas, membros, turmas, alunos, matrículas, planos, versões, aulas, frequências e auditoria. Habilita RLS e não cria liberação pública.
5. Execute `sql/02_supabase_admin_piloto.sql`. Ele permite somente administradores ativos da própria escola. Usuários não podem editar seus privilégios nem escrever diretamente versões e auditoria.
6. Em Authentication, crie/convidе seu usuário administrativo e copie o UUID do usuário.
7. No SQL Editor, crie sua escola e anote o ID retornado:

```sql
insert into public.schools(name)
values ('Escola de teste')
returning id;
```

8. Crie o vínculo usando os valores reais, substituindo os textos ilustrativos:

```sql
insert into public.members(school_id,user_id,role,active)
values ('UUID-DA-ESCOLA','UUID-DO-USUARIO','admin',true);
```

9. Configure Site URL e URLs de redirecionamento em Authentication para o domínio do seu app. Ative Google se desejar e configure as credenciais OAuth no painel do provedor.
10. Obtenha a URL do projeto e a chave **publishable** nas configurações de API. A chave publicável pode ir no frontend com RLS adequada. Chaves secretas e a antiga `service_role` ficam exclusivamente no backend.
11. No projeto de interface que usará Supabase, instale `@supabase/supabase-js` e inicialize `createClient(URL, PUBLISHABLE_KEY)`. Faça login antes das consultas. Substitua `src/data.ts` e `src/firebase.ts` por adaptadores Supabase; este passo exige desenvolvimento, não simples troca de variável.
12. Faça uma consulta real de `classes` como administrador. Crie um usuário comum sem vínculo e confirme que ele não recebe linhas nem consegue inserir.
13. Teste duas escolas diferentes para evitar vazamento entre instituições. Só depois adicione políticas por turma para docentes e segmento para coordenação.
14. Para aprovar planos ou fechar chamadas, use função transacional/API: validar estado, gravar versão/correção e auditoria juntos. O SQL inicial não implementa todo esse fluxo; não o trate como sistema institucional pronto.
15. Abra `sql/03_monitoramento_postgres.sql` no SQL Editor para consultar tamanho total e por tabela. No app, exponha esse resultado somente por endpoint administrativo autenticado.
16. Para uploads, crie bucket privado e políticas equivalentes às da escola/turma. Não use arquivos públicos para registros escolares.
17. Configure backup conforme o plano e restaure em projeto de teste. A restauração precisa ser validada por contagem, vínculos e amostragem de documentos.

A consulta `pg_database_size(current_database())` mede o banco atual. Disco contratado, WAL, arquivos temporários, backups e Storage de anexos são medidas diferentes. Use o painel oficial para comparar consumo faturável. Não subtraia arquivos de alunos ou invente percentual do disco usando apenas tabelas visíveis.

Fontes: [React + Supabase](https://supabase.com/docs/guides/getting-started/quickstarts/reactjs), [Auth](https://supabase.com/docs/guides/auth/quickstarts/react), [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [tamanho do banco e disco](https://supabase.com/docs/guides/platform/database-size).

## 7. Caminho C — Neon/PostgreSQL, passo a passo

Escolha este caminho se quiser separar o banco do backend com mais liberdade. Este guia usa uma API própria como fronteira de acesso; não depende de um recurso de autenticação específico do Neon.

1. Crie a conta no [Neon Console](https://console.neon.tech/) e um projeto de teste.
2. Escolha região, versão de PostgreSQL e nome da base, conforme as opções do painel.
3. Mantenha ambientes de desenvolvimento e produção separados. Uma branch pode facilitar testes, mas não substitui uma política completa de backup.
4. Abra o SQL Editor na branch de desenvolvimento e execute `sql/01_nucleo_postgres.sql`.
5. **Não execute o arquivo 02 do Supabase**: ele depende de `auth.uid()` e do papel `authenticated`, específicos daquela integração.
6. Na opção Connect, obtenha a conexão apropriada. Para um backend serverless, avalie a conexão com pooling recomendada pelo console.
7. Salve `DATABASE_URL` exclusivamente nas variáveis secretas do backend. Nunca use prefixo `VITE_` para essa URL. Não coloque senha ou URL completa em arquivos do GitHub.
8. Construa a API em serviço com execução de código (por exemplo, Cloud Run ou outro backend contratado). GitHub Pages não executa esse servidor.
9. Configure identidade com um provedor. A API valida o token, resolve o usuário e consulta `members` para conferir escola, função e acesso ativo antes da operação.
10. Separe a credencial de migração da credencial de execução. Não entregue ao backend público uma conexão com o proprietário de todas as tabelas como se RLS o limitasse automaticamente. Proprietários e papéis com BYPASSRLS podem contornar RLS; use papel limitado e políticas validadas ou autorização explícita rigorosa na API.
11. Implemente transações para frequência, aprovação e auditoria; use as restrições únicas e chaves estrangeiras do schema como segunda proteção.
12. Execute `sql/03_monitoramento_postgres.sql` via consulta de administração. A interface recebe somente bytes, limites e percentuais, nunca credenciais.
13. Teste pool, conexões simultâneas e retorno após inatividade. Limites de computação também importam, não só gigabytes.
14. Configure backup/exportação e faça restauração em destino isolado. Use as instruções oficiais de `pg_dump`/`pg_restore`, sem colar senha em logs ou capturas de tela.
15. Somente depois de testar autorização e restauração, configure o frontend para sua API e faça deploy.

Fontes: [console Neon](https://neon.com/docs/get-started/signing-up), [migração PostgreSQL](https://neon.com/migration), [backup e exportação](https://github.com/neondatabase/website/blob/main/content/docs/manage/backup-pg-dump.md).

## 8. Custos e dimensionamento sem adivinhar o tamanho da escola

| Serviço | Referência consultada | Como interpretar |
|---|---|---|
| Firestore | Franquia de 1 GiB; 50.000 leituras/dia; 20.000 escritas/dia; uma base gratuita por projeto | Não inclui automaticamente Functions, backup, IA, anexos ou todos os tipos de operação |
| Supabase Free | 500 MB de banco por projeto | Útil para teste; não comparar diretamente com todos os itens de disco de planos pagos |
| Supabase Pro | A partir de US$ 25/mês; 8 GB de disco por projeto nas condições do plano | Projetos adicionais, compute e excedentes podem aumentar o total |
| Neon Free | Página consultada informa 1 GB de armazenamento por projeto e 100 CU-h/mês por projeto | Computação, retenção, tráfego e outros recursos têm condições próprias |
| Neon pago | Cobrança por uso | Não tratar “gasto típico” divulgado como mensalidade fixa |

Fontes: [Firestore](https://cloud.google.com/firestore/pricing), [Firebase](https://firebase.google.com/pricing), [Supabase](https://supabase.com/pricing), [Neon](https://neon.com/pricing).

**Hipótese de simulação:** 50 profissionais × 400 leituras/dia = 20.000 leituras/dia. 50 × 80 escritas/dia = 4.000 escritas/dia. Essas operações isoladas caberiam nas franquias citadas, nas condições de elegibilidade. Não significam custo total zero.

Para estimar armazenamento, a escola deve fornecer quantidade de alunos, turmas, aulas/dia, dias letivos, anos de retenção, tamanho médio real de registros e anexos. Medir uma amostra do banco é mais confiável que atribuir “1 KB por aluno”: índices, nomes de campos, histórico e estruturas internas também ocupam espaço.

Total mensal = banco + funções/API + hospedagem + arquivos + backups + tráfego + IA + eventuais licenças. O custo exato permanece não confirmado sem volumes, região e planos escolhidos.

## 9. Drive, seus outros apps e login único

Confirme primeiro se você paga **Google One pessoal** ou **Google Workspace**. Meu Drive usa propriedade individual; uma pasta compartilhada não transfere automaticamente propriedade nem cota. Drives compartilhados elegíveis permitem propriedade organizacional, o que ajuda na saída de funcionários.

O sistema deve registrar proprietário, ID do arquivo, permissões e política de saída. Remover alguém da plataforma não remove por si só um compartilhamento direto do Drive. Essa revogação precisa fazer parte do processo.

Drive é para documentos, não para hospedar o Firestore. Cloud Storage exige plano Blaze nas condições atuais; tem regras e cobrança próprias. Uso padrão da Drive API não tem custo adicional segundo a documentação consultada, mas há previsão de cobrança por excesso de cotas em 2026; reconfirme ao implantar.

| Integração | O que entrega | Trabalho necessário |
|---|---|---|
| Atalho | Abre outro app | URL configurada |
| Identidade compartilhada | Mesmo identificador de usuário | Provedor e mapeamento de IDs |
| Login único | Navegação autenticada adequada entre apps | Fluxo de sessão por domínio, redirecionamentos autorizados e revogação |
| Dados compartilhados | Cadastros e ações sincronizados | API autenticada, sistema fonte, idempotência, retentativas e logs |

Compartilhar o projeto Firebase não mantém automaticamente a sessão entre domínios diferentes. Não passe tokens nas URLs. Prefira centralizar identidade, manter cada app com escopos explícitos e decidir quem é responsável por aluno, turma, matrícula e frequência.

Fontes: [drives compartilhados](https://developers.google.com/workspace/drive/api/guides/about-shareddrives), [Drive API](https://developers.google.com/workspace/drive/api/guides/limits), [Cloud Storage](https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024).

## 10. O que falta para concluir a etapa institucional

O pacote entrega código inicial, fluxos demonstrativos e a tela de infraestrutura configurável. Não foram criados projetos ou bancos nas suas contas externas, nem enviado código ao seu GitHub.

Antes do uso real: definir segmentos e volumes; migrar o piloto para entidades separadas; implementar matrículas/transferências e papéis completos; convites, anexos e comentários por campo; autosave com conflitos; prazos e aulas previstas; privacidade/retenção com a escola; backup e restauração testados; revisão visual no celular; teste de API sem acesso indevido. IA, Drive e integrações são etapas posteriores.

Para decidir a próxima implantação, informe: tipo da conta Google, quantidade aproximada de professores/alunos, segmentos, nome do sistema escolar existente e tecnologia/domínios dos apps próprios. Não envie senhas nem contas de serviço.

## 15. Identidade ELO Novo Mundo

Esta revisão inclui a identidade **Educação, Ligação e Organização**, aplicada à tela de entrada e ao painel. Abra `COMECE_POR_AQUI.html` para visualizar as artes. Os arquivos prontos ficam em `public/brand/`, e o guia de aplicação em `docs/IDENTIDADE_VISUAL.md`. A galeria também está disponível no menu do app. A atualização visual não altera os requisitos de implantação, permissões ou as limitações do piloto descritas acima.
