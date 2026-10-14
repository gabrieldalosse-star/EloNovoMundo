# ELO Novo Mundo — Educação, Ligação e Organização

Para conhecer as artes, extraia o ZIP e abra **COMECE_POR_AQUI.html** no navegador. Para instalar, comece pelo **[GUIA_COMPLETO.md](GUIA_COMPLETO.md)**. Ele contém os passos de Firebase, Supabase e Neon, custos, modelo de dados, permissões e monitoramento.

## O que este pacote é

Um projeto React/Vite para guardar no GitHub, com um piloto dos fluxos pedagógicos e uma tela separada **Infraestrutura e consumo**. Há um backend Firebase configurável. Não é a versão institucional completa e não deve receber dados reais de alunos.

- Sem `.env`: demonstração com dados fictícios em `localStorage`, limitada ao navegador.
- Com `.env` + backend implantado: login Firebase, autorização de administrador e salvamento transacional no Firestore.
- Infraestrutura: integração programada com métricas oficiais do Cloud Monitoring, após ativar API, conta de execução e permissões. Sem configuração ou amostra: indisponível, nunca zero inventado.
- Supabase/Neon: guias e SQL inicial. Não há adaptadores desses bancos instalados no frontend.

## Testar no computador

Instale Node.js 22, abra um terminal nesta pasta e execute:

```bash
npm ci
npm test
npm run dev
```

Abra a URL que o terminal informar. Sem Firebase configurado, clique em **Entrar na demonstração** na tela de boas-vindas. Para compilar:

```bash
npm run build
npm ci --prefix functions
npm --prefix functions run build
```

## Pastas

| Caminho | Finalidade |
|---|---|
| `src/Platform.tsx` | Interface e fluxos demonstrativos |
| `src/Infra.tsx` | Tela de infraestrutura e consumo |
| `src/firebase.ts` | Inicialização do Firebase e autenticação |
| `src/data.ts` | Persistência local demonstrativa ou backend configurado |
| `functions/src/index.ts` | Autorização, transações e coleta das métricas |
| `functions/src/domain.ts` | Regras de planos e chamadas do piloto |
| `functions/src/metrics-utils.ts` | Cálculos sem inventar valores ausentes |
| `firestore.rules` | Negação de todo acesso direto do cliente; operações via backend |
| `sql/` | Base relacional inicial e monitoramento PostgreSQL |
| `.github/workflows/ci.yml` | Testes e compilação a cada push |
| `.github/workflows/pages-demo.yml` | Publicação MANUAL de demonstração local, sem Firebase |
| `docs/VALIDACAO.md` | Verificações realizadas e pendentes |

A hospedagem institucional recomendada para a opção Firebase é Firebase Hosting. GitHub guarda o código; banco e funções são serviços externos. O workflow do Pages é opcional, para a demonstração, e publica um site acessível ao público quando executado.

## Limitações importantes

O piloto salva o estado de cada administrador em um documento, com teto de 700.000 bytes UTF-8. Essa escolha é apenas para validação; a arquitetura institucional usa coleções por entidade descritas no guia. Não escalar esse documento único para a escola.

Google/e-mail têm implementação configurável; convites e perfis de professores, segregação por turma, IA, Drive, anexos, backup/restauração e PWA completa permanecem pendentes. A tela de métricas não é uma ferramenta de bloqueio de despesas.

## Identidade visual incluída

- Logos vetoriais SVG e PNG, versões colorida, clara e monocromática.
- Ícones de aplicativo, favicon, capa horizontal, splash vertical e padrão gráfico.
- Ilustração de boas-vindas em PNG e WebP, aplicada à interface.
- Fonte Manrope local com licença OFL e tokens de cores.
- Galeria **Identidade visual** dentro do aplicativo.

Arquivos prontos em `public/brand/`. Orientações, referências e procedência em [docs/IDENTIDADE_VISUAL.md](docs/IDENTIDADE_VISUAL.md). A splash é uma arte disponível; este pacote não instala um aplicativo nativo nem configura PWA.
