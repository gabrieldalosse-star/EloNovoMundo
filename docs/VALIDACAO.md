# Validação da entrega — 14/10/2026

Executado localmente:

- `npm test`: passou. Abrange ausência de registro, fechamento incompleto, atualização sem duplicidade, correção motivada, datas/horários inválidos, transições, preservação da versão aprovada, cópia e nomes duplicados.
- Testes de métricas: passaram. Abrangem dados ausentes, denominador inválido, percentual acima de 100%, série de escopo ambíguo e soma de contadores.
- `npm run build`: passou. TypeScript do frontend e compilação Vite concluídos.
- `npm --prefix functions run build`: passou. Backend Firebase compilado.

Não executado:

- Deploy nas contas Firebase/GitHub do usuário.
- Login OAuth real, envio de e-mails, IAM, leitura efetiva das métricas do usuário e faturamento.
- Testes de integração com emuladores ou projeto Firebase real.
- SQL executado em Supabase/Neon. Os scripts são uma base inicial a validar em projeto vazio.
- Teste visual/interativo em navegador e aparelho móvel.
- Backup/restauração da infraestrutura real.

Ambiente de compilação local: Node 24. Runtime do backend e CI configurados para Node 22. Os arquivos de lock registram as dependências resolvidas. O teste no runtime de destino continua sendo necessário após a configuração.

A compilação bem-sucedida não equivale a validação institucional. O README e o guia identificam os módulos ausentes e a limitação de documento único do piloto.

## Revisão da identidade visual

Build frontend, testes de domínio/métricas e build do backend repetidos após a integração da marca: passaram. Prancha da marca, capa e splash inspecionadas visualmente como imagens. SVGs exportados para PNG; fontes locais e ilustração WebP incluídas. A inspeção dessas artes não substitui teste interativo da interface em navegador, que permanece pendente.
