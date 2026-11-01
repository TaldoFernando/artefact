# 02 store information

Actual local model transcript. Model: `qwen3:8b`.

**Customer:** What is the store address and regular opening hours?

**Mel:** The Empório da Música is located at **Rua 14 de Maio, 3200 — Centro, Campo Grande - MS, 79202-333**. 

Our regular hours of operation are:
- **Monday to Friday:** 09:00 to 18:00
- **Saturday:** 09:00 to 13:00
- **Sunday and Holidays:** Closed

Note that during special events like Black Friday or the Store Anniversary, the hours may be extended. Any changes will be communicated in advance through our social media and WhatsApp support.

Policy evidence: store_policies.pdf, pp. 2, 6, 7.

<details><summary>Tool evidence</summary>

```json
[
  {
    "tool": "search_policies",
    "arguments": {
      "query": "store address and regular opening hours"
    },
    "result": {
      "source": "store_policies.pdf, v2.1 June 2025",
      "passages": [
        {
          "page": 2,
          "text": "Empório  da  Música  Manual  de  Políticas  e  Procedimentos\n \n1.  Sobre  a  Empório  da  Música  \nA  Empório  da  Música  é  uma  loja  especializada  em  instrumentos  musicais,  fundada  em  2008  em  \nCampo\n \nGrande,\n \nMato\n \nGrosso\n \ndo\n \nSul.\n \nCom\n \nmais\n \nde\n \n15\n \nanos\n \nde\n \natuação\n \nno\n \nmercado,\n \nsomos\n \nreferência\n \nregional\n \nna\n \nvenda\n \nde\n \ninstrumentos\n \npara\n \nmúsicos\n \niniciantes,\n \nintermediários\n \ne\n \nprofissionais.\n Nosso  catálogo  abrange  mais  de  300  instrumentos  de  marcas  nacionais  e  internacionais,  incluindo  \nguitarras,\n \nbaixos,\n \nviolões,\n \nbaterias,\n \nteclados,\n \ninstrumentos\n \nde\n \nsopro,\n \ncordas\n \norquestrais\n \ne\n \nukuleles.\n \nTrabalhamos\n \nexclusivamente\n \ncom\n \ninstrumentos\n \nmusicais\n \n—\n \nnão\n \ncomercializamos\n \nacessórios\n \ncomo\n \ncordas,\n \npalhetas,\n \ncabos,\n \ncases,\n \npedais\n \nou\n \namplificadores.\n \n1.1  Missão  Democratizar  o  acesso  a  instrumentos  musicais  de  qualidade  na  região  Centro-Oeste,  oferecendo  \natendimento\n \nespecializado\n \ne\n \npreços\n \ncompetitivos,\n \ncontribuindo\n \npara\n \no\n \ndesenvolvimento\n \ncultural\n \ne\n \nmusical\n \nda\n \ncomunidade.\n \n1.2  Dados  da  Empresa  \nCampo Informação \nRazão  Social  Empório  da  Música  Instrumentos  Musicais  Ltda.  \nNome  Fantasia  Empório  da  Música  \nCNPJ  12.345.678/0001-90  \nEndereço  Rua  14  de  Maio,  3200  —  Centro,  Campo  Grande  -  MS,  79202-333  \nTelefone  /  WhatsApp  (67)  3341 - 4444  \nE-mail  contato@empóriodamusica.com.br  \nFundação  2008  \n \n2.  Horário  de  Funcionamento  \nO  atendimento  presencial  na  loja  segue  os  horários  abaixo.  O  atendimento  via  WhatsApp  segue  o  \nmesmo\n \nhorário,\n \ncom\n \nrespostas\n \nautomáticas\n \nfora\n \ndo\n \nexpediente.\n \nDia Horário \nSegunda  a  Sexta-feira  09:00  às  18:00  \nSábado  09:00  às  13:00  \nDomingo  e  Feriados  Fechado   Em  datas  especiais  (Black  Friday,  Aniversário  da  Loja,  Natal),  o  horário  pode  ser  estendido.  \nAlterações\n \nserão\n \ncomunicadas\n \ncom\n \nantecedência\n \nnas\n \nredes\n \nsociais\n \ne\n \nno\n \natendimento\n \nvia\n \nWhatsApp.\n \n \nPágina  2\n "
        },
        {
          "page": 6,
          "text": "Empório  da  Música  Manual  de  Políticas  e  Procedimentos\n \n6.  Promoções  e  Descontos  \n6.1  Tipos  de  Promoção  A  Empório  da  Música  realiza  promoções  periódicas  ao  longo  do  ano.  As  principais  campanhas  \nincluem:\n •  Aniversário  da  Loja  (Agosto):  descontos  de  10%  a  25%  em  itens  selecionados.  •  Black  Friday  (Novembro):  descontos  de  15%  a  30%  em  todo  o  catálogo.  •  Volta  às  Aulas  (Fevereiro):  descontos  especiais  em  instrumentos  para  estudantes.  •  Queima  de  Estoque:  promoções  pontuais  para  renovação  de  catálogo.  •  Semana  do  Músico:  promoções  na  semana  do  Dia  do  Músico  (22  de  novembro).  \n6.2  Regras  de  Promoções  Cumulatividade:  promoções  não  são  cumulativas.  O  desconto  de  PIX  (5%)  não  se  aplica  sobre  \npreços\n \njá\n \npromocionais.\n Estoque:  promoções  estão  sujeitas  à  disponibilidade  de  estoque.  Produtos  esgotados  durante  a  \npromoção\n \nnão\n \ngeram\n \ndireito\n \na\n \nrain\n \ncheck\n \n(reserva\n \nde\n \npreço).\n Comunicação:  preços  promocionais  devem  sempre  ser  apresentados  junto  ao  preço  original  e  o  \npercentual\n \nde\n \ndesconto,\n \npara\n \ntotal\n \ntransparência\n \nao\n \ncliente.\n \n \n7.  Atendimento  via  WhatsApp  \nO  canal  de  WhatsApp  (67)  3321-4500  é  o  principal  meio  de  atendimento  remoto  da  Empório  da  \nMúsica.\n \nO\n \natendimento\n \npode\n \nser\n \nrealizado\n \npor\n \natendentes\n \nhumanos\n \nou\n \npelo\n \nassistente\n \nvirtual.\n \n \n7.1  Diretrizes  de  Atendimento  Tom  de  voz:  informal  mas  profissional.  O  cliente  deve  se  sentir  acolhido,  como  se  estivesse  \nconversando\n \ncom\n \num\n \namigo\n \nque\n \nentende\n \nde\n \nmúsica.\n \nEvitar\n \nlinguagem\n \nexcessivamente\n \nformal\n \nou\n \nrobotizada.\n Tempo  de  resposta:  máximo  de  5  minutos  durante  o  horário  de  funcionamento.  Fora  do  expediente,  \no\n \nassistente\n \nvirtual\n \ndeve\n \ninformar\n \no\n \nhorário\n \nde\n \nretorno.\n Informações  precisas:  nunca  fornecer  informações  sobre  preços,  estoque  ou  prazos  sem  consultar  \no\n \nsistema.\n \nInformações\n \nincorretas\n \ngeram\n \nfrustração\n \ne\n \npodem\n \nconfigurar\n \npropaganda\n \nenganosa.\n Escopo:  o  atendente  deve  informar  que  a  loja  trabalha  exclusivamente  com  instrumentos  musicais.  \nPedidos\n \nde\n \nacessórios\n \n(cordas,\n \ncabos,\n \npalhetas,\n \npedais,\n \namplificadores,\n \ncases)\n \ndevem\n \nser\n \neducadamente\n \nredirecionados.\n \nSugerir\n \nlojas\n \nparceiras\n \nquando\n \npossível.\n \n7.2  Fluxo  de  Atendimento  Padrão  1.  Saudação:  cumprimentar  o  cliente  pelo  nome  (se  disponível)  e  perguntar  como  pode  ajudar.  2.  Entendimento:  identificar  a  necessidade  do  cliente  (busca  de  produto,  dúvida,  rastreamento,  \nreclamação).\n \nPágina  6\n "
        },
        {
          "page": 7,
          "text": "Empório  da  Música  Manual  de  Políticas  e  Procedimentos\n \n3.  Consulta:  buscar  no  sistema  as  informações  relevantes  (produto,  estoque,  promoção,  \npedido).\n 4.  Resposta:  apresentar  as  opções  de  forma  clara  e  objetiva,  com  preços  e  condições.  5.  Fechamento:  confirmar  se  o  cliente  precisa  de  mais  alguma  coisa  e  encerrar  com  \ncordialidade.\n \n7.3  Situações  Especiais  Produto  fora  de  estoque:  informar  que  o  produto  está  temporariamente  indisponível  e  sugerir  \nalternativas\n \nsemelhantes\n \nque\n \nestejam\n \ndisponíveis.\n \nNunca\n \nconfirmar\n \ndisponibilidade\n \nsem\n \nverificar\n \no\n \nestoque\n \natual.\n Produto  descontinuado:  informar  que  o  produto  não  faz  mais  parte  do  catálogo  e  oferecer  modelos  \nequivalentes\n \nou\n \nsucessores.\n Promoção  expirada:  caso  o  cliente  pergunte  sobre  uma  promoção,  verificar  se  ela  encontra-se  ativa  \nno\n \nsistema.\n \nSe\n \na\n \npromoção\n \nestiver\n \nvencida,\n \ninformar\n \ncom\n \ntransparência\n \ne\n \napresentar\n \no\n \npreço\n \natual.\n \nNunca\n \nprometer\n \num\n \ndesconto\n \nque\n \nnão\n \nestá\n \nmais\n \nvigente.\n Reclamação:  ouvir  o  cliente  com  empatia,  registrar  a  reclamação  e  encaminhar  para  o  responsável.  \nPrazo\n \nde\n \nretorno:\n \n24\n \nhoras\n \núteis.\n \n \n8.  Garantia  \n8.1  Garantia  Legal  Conforme  o  Código  de  Defesa  do  Consumidor,  todos  os  produtos  possuem  garantia  legal  de  90  \n(noventa)\n \ndias\n \ncontra\n \ndefeitos\n \nde\n \nfabricação,\n \ncontados\n \na\n \npartir\n \nda\n \ndata\n \nde\n \nrecebimento\n \npelo\n \ncliente.\n \n8.2  Garantia  do  Fabricante  Além  da  garantia  legal,  a  maioria  dos  fabricantes  oferece  garantia  própria  que  pode  variar  de  6  \nmeses\n \na\n \n2\n \nanos.\n \nOs\n \nprazos\n \ne\n \ncondições\n \nespecíficos\n \nestão\n \ndetalhados\n \nno\n \ncertificado\n \nde\n \ngarantia\n \nque\n \nacompanha\n \ncada\n \nproduto.\n \n8.3  O  que  Não  Cobre  a  Garantia  •  Desgaste  natural  de  peças  (trastes,  cordas,  feltros,  palhetas  de  sopro).  •  Danos  por  mau  uso,  queda,  exposição  a  condições  climáticas  extremas.  •  Modificações  ou  reparos  realizados  por  terceiros  não  autorizados.  •  Danos  estéticos  que  não  afetem  a  funcionalidade  do  instrumento.  \n \n9.  Privacidade  e  Proteção  de  Dados  \nA  Empório  da  Música  está  em  conformidade  com  a  Lei  Geral  de  Proteção  de  Dados  (LGPD  —  Lei  nº  \n13.709/2018).\n \nOs\n \ndados\n \npessoais\n \ncoletados\n \ndurante\n \no\n \natendimento\n \n(nome,\n \ntelefone,\n \ne-mail,\n \nendereço)\n \nsão\n \nutilizados\n \nexclusivamente\n \npara:\n \nPágina  7\n "
        }
      ],
      "warning": "Internal policies may conflict. Do not adjudicate legal rights; escalate unclear cases."
    }
  }
]
```

</details>
