# ELO Novo Mundo — guia de identidade

Atualização: 14/10/2026. Nome: **ELO Novo Mundo**. Significado: **Educação, Ligação e Organização**. Assinatura: “Um novo mundo de conexões.”

## Conceito
Três curvas conectadas representam educação, vínculo e organização. O azul sustenta a interface, o verde identifica colaboração e o amarelo destaca momentos de descoberta. A marca do app é própria; o logotipo institucional foi preservado como assinatura da escola.

## Cores e tipografia
| Uso | Cor |
|---|---|
| Base institucional digital | #102A56 |
| Ação principal | #2165DB |
| Colaboração | #16A075 |
| Destaque | #F2C64D |
| Acento | #EF8956 |
| Texto | #162D50 |
| Fundo | #F4F7FC |

Paleta proposta para o produto, não uma reprodução certificada do manual oficial da escola. Use Manrope, incluída localmente em `public/fonts`, com licença OFL. As letras dos SVGs foram convertidas em contornos. Amarelo e verde não devem substituir texto escuro pequeno em fundo claro; estados sempre combinam texto e cor.

## Aplicação
- Use `elo-horizontal.svg` em superfícies claras e `elo-horizontal-claro.svg` em azul-marinho.
- Reserve ao redor da marca pelo menos metade da altura do símbolo. Não estique, gire ou altere as cores.
- Largura recomendada mínima do conjunto: 150 px. Abaixo disso, use o símbolo isolado.
- Ícones PNG: 32, 64, 180, 192 e 512 px. Variante maskable disponível em 512 px.
- Capa: `elo-banner.svg/png`. Abertura vertical: `elo-splash.svg/png`. Essas peças podem ser adaptadas pelo código-fonte vetorial.
- Hero: `elo-conexoes-hero.webp` para web; PNG para edição/apresentações. Mantenha texto como HTML, nunca incorporado à imagem.
- A prancha `elo-prancha-identidade.png` reúne as principais aplicações.

## Referências e procedência
O perfil fornecido foi https://www.instagram.com/colegionovomundococ/ . A consulta ao Instagram foi limitada pelo serviço; não foi feita uma auditoria completa do feed. As referências institucionais verificáveis vieram do site https://colegionovomundosp.com.br/historia/ e de sua página inicial, consultados em 14/10/2026.

Logotipo original da escola, preservado sem redesenho: https://colegionovomundosp.com.br/wp-content/uploads/2022/05/novomundo-1024x1024.png . Guardado como `colegio-novo-mundo-original.png`; o recorte de espaço vazio na interface é apenas de apresentação. O nome, a escola e a referência COC não representam endosso externo deste aplicativo.

O símbolo ELO e as composições vetoriais foram produzidos para esta proposta. Fonte Manrope obtida do repositório Google Fonts, diretório `ofl/manrope`, com licença incluída. Código gerador dos vetores: `brand-source/build_brand.py` (Python + fontTools). A marca proposta não passou por pesquisa de registro no INPI.

A arte de boas-vindas foi gerada com OpenAI imagegen. Direção utilizada: ilustração editorial 3D sofisticada para colaboração escolar; fundo azul-marinho #102A56; três curvas interligadas em azul #2165DB, verde #16A075 e amarelo #F2C64D, pequeno detalhe coral, esfera translúcida, cerâmica fosca, luz suave, composição à direita e espaço livre à esquerda; sem letras, logos ou interface. O arquivo WebP é uma compressão do PNG, sem alteração visual deliberada.

## Integração
`src/Brand.tsx` centraliza os caminhos com o BASE_URL do Vite. A identidade está aplicada à entrada, navegação, painel e galeria. A tela de infraestrutura e os guias Firebase/Supabase/Neon permanecem no pacote. O app segue como piloto, com a configuração real de infraestrutura descrita no guia técnico.
