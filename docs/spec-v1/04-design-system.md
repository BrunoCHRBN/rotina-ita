# 04 --- Design system v1.0

## 1. Direção de arte

Editorial acadêmico contemporâneo: - marfim como fundo principal; -
tinta escura para texto; - títulos serifados; - corpo funcional sem
serifa; - terracota como acento restrito; - divisores finos e grade
consistente; - densidade equilibrada; - sem gradientes decorativos,
glassmorphism ou excesso de cards.

A interface deve parecer um instrumento de planejamento editorialmente
desenhado, não um template genérico de dashboard.

## 2. Tokens de cor --- tema claro

``` css
:root {
  --color-canvas: #F7F5F0;
  --color-surface: #FFFFFF;
  --color-surface-muted: #F0EEE8;
  --color-ink: #222522;
  --color-ink-muted: #686B65;
  --color-border: #DEDDD5;
  --color-accent: #A84635;
  --color-accent-hover: #873829;
  --color-accent-soft: #F3E5E0;
  --color-success: #356B50;
  --color-warning: #8A5B19;
  --color-danger: #A13D36;
  --color-info: #3D6178;
  --color-focus: #315E91;
}
```

Os tokens semânticos de status devem ser verificados para contraste
antes da publicação. Não usar a cor como único indicador: sempre
combinar com texto, ícone ou rótulo.

## 3. Tipografia

-   Títulos: Source Serif 4 ou alternativa serifada equivalente.
-   Interface e corpo: Inter ou alternativa sans-serif equivalente.
-   Dados numéricos: usar números tabulares onde isso melhorar
    alinhamento.
-   Evitar mais de duas famílias tipográficas principais.
-   Escala sugerida: 12, 14, 16, 18, 24, 32, 40 px.
-   Texto principal geralmente entre 14 e 16 px; não reduzir para
    encaixar conteúdo excessivo.

Fontes devem ter fallback local e carregamento eficiente. Não depender
de uma fonte remota para renderizar conteúdo crítico.

## 4. Espaçamento e geometria

-   Unidade-base: 4 px.
-   Espaçamentos frequentes: 4, 8, 12, 16, 24, 32, 40, 48 px.
-   Bordas: 1 px.
-   Raio pequeno para controles; médio para painéis; evitar pílulas em
    todos os elementos.
-   Sombras mínimas, apenas quando indicarem elevação real.
-   Layout desktop com navegação lateral discreta e área principal
    ampla.
-   Mobile com navegação compacta e prioridade à agenda do dia.

## 5. Componentes P0

### Navegação

-   App shell.
-   Navegação lateral desktop.
-   Navegação compacta mobile.
-   Cabeçalho de página com título, data e ações contextuais.

### Planejamento

-   Timeline diária.
-   Grade semanal.
-   Bloco de sessão.
-   Bloco de compromisso.
-   Indicador de sessão protegida.
-   Estado de tarefa não alocada.
-   Resumo de carga planejada.
-   Diff de replanejamento.

### Formulários

-   Input, select, textarea, checkbox, radio e switch acessíveis.
-   Seletor de data e horário com validação.
-   Campos de duração e limites com unidades explícitas.
-   Mensagens de erro próximas ao campo.

### Execução

-   Ação iniciar sessão.
-   Estado em andamento.
-   Ação concluir/interromper.
-   Formulário de resultado e tempo real.
-   Confirmação para ações destrutivas ou irreversíveis.

### Feedback

-   Empty states com próximo passo.
-   Skeletons para carregamento real.
-   Erros recuperáveis.
-   Aviso de conflitos.
-   Aviso de capacidade insuficiente.
-   Confirmação de salvamento.

## 6. Estados obrigatórios dos componentes

Cada componente interativo deve considerar: - default; - hover; -
focus-visible; - active; - disabled; - loading, quando aplicável; -
error; - empty; - responsive.

Não criar botões ou controles decorativos sem ação real.

## 7. Layouts

### Hoje

-   Cabeçalho com data e contexto.
-   Próxima sessão em destaque moderado.
-   Progresso planejado versus concluído.
-   Agenda cronológica.
-   Revisões e tarefas não alocadas em áreas secundárias.
-   Ações rápidas para iniciar, concluir e reagendar.

### Semana

-   Grade por dia e horário.
-   Navegação entre semanas.
-   Indicadores discretos de capacidade e conflito.
-   Tarefas não alocadas visíveis fora da grade.
-   Alternativa acessível em lista para telas pequenas.

### Minha rotina

-   Disponibilidade recorrente.
-   Compromissos e exceções.
-   Limites diários/semanais.
-   Preferências por disciplina.
-   Políticas de autonomia da IA.

### Evolução

-   Tempo planejado versus realizado.
-   Distribuição por disciplina.
-   Pendências e revisões.
-   Sem previsões de aprovação não validadas.

## 8. Regras anti-AI-slop

-   Não usar gradientes roxos ou fundos decorativos por padrão.
-   Não converter toda seção em um card.
-   Não usar glassmorphism.
-   Não usar emojis como ícones de interface.
-   Não adicionar gráficos sem decisão associada.
-   Não usar animações de entrada em todos os elementos.
-   Não usar slogans genéricos em lugar de informação útil.
-   Não inventar métricas para preencher espaço.
-   Não exibir chatbot como centro visual da aplicação.
-   Não sacrificar legibilidade para parecer minimalista.
-   Não criar um componente novo para cada tela se o padrão semântico
    for o mesmo.
-   Não usar cor como único canal de informação.

## 9. Acessibilidade

-   WCAG AA como alvo para contraste.
-   Navegação completa por teclado.
-   Foco visível.
-   Rótulos programáticos e mensagens de erro associadas.
-   Alvos de toque adequados.
-   Respeitar preferência por movimento reduzido.
-   Alternativa em lista para calendário visual.
-   Não comunicar estado apenas por cor.

## 10. Tema escuro futuro

O MVP é claro. Todos os componentes devem consumir tokens semânticos,
não cores literais espalhadas. O tema escuro será adicionado
posteriormente com tokens equivalentes; não inverter cores
automaticamente.
