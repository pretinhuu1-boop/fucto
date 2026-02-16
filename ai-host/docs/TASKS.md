# AI HOST — Task Board

## Como usar este board

Cada task e autocontida. O Claude (ou outro agente) deve:
1. Pegar a proxima task `[ ]` do modulo atual
2. Implementar com codigo completo
3. Explicar decisoes
4. Marcar como `[x]`
5. Nao avancar de fase sem todas as tasks da fase concluidas

**Legenda**: `[ ]` pendente | `[~]` em progresso | `[x]` concluido

---

## FASE 1 — Base Operacional
> Objetivo: Avatar aparece no OBS e backend se comunica

### 1.1 Backend Base
- [ ] **T-101**: Criar projeto Node + Express + WebSocket server (porta 3001)
- [ ] **T-102**: Criar sistema de eventos interno (EventEmitter)
- [ ] **T-103**: Criar rota REST `/api/health` e `/api/status`
- [ ] **T-104**: Criar WebSocket handler para comunicacao com frontend
- [ ] **T-105**: Criar config loader (le .env e config.json)

### 1.2 OBS Setup
- [ ] **T-111**: Integrar `obs-websocket-js` v5 no backend
- [ ] **T-112**: Criar modulo OBS Director (connect, disconnect, status)
- [ ] **T-113**: Criar funcao: listar cenas e fontes
- [ ] **T-114**: Criar funcao: trocar cena
- [ ] **T-115**: Criar funcao: criar cena "AI Host Live" com layout padrao
- [ ] **T-116**: Criar funcao: adicionar Browser Source (avatar + HUD)
- [ ] **T-117**: Documentar setup inicial do OBS (WebSocket server habilitado)

### 1.3 Avatar Frontend
- [ ] **T-121**: Criar projeto React (Vite) para avatar
- [ ] **T-122**: Integrar React Three Fiber
- [ ] **T-123**: Carregar modelo Ready Player Me (.glb)
- [ ] **T-124**: Configurar canvas transparente (alpha: true)
- [ ] **T-125**: Implementar animacao idle (respiracao, olhar)
- [ ] **T-126**: Implementar lip sync basico com visemas
- [ ] **T-127**: Conectar ao backend via WebSocket
- [ ] **T-128**: Testar como Browser Source no OBS (9:16, fundo transparente)

### 1.4 HUD Frontend
- [ ] **T-131**: Criar projeto React (Vite) para HUD overlay
- [ ] **T-132**: Layout: area de noticias (scrolling), teleprompter, alertas
- [ ] **T-133**: Conectar ao backend via WebSocket
- [ ] **T-134**: Receber e exibir mensagens do backend
- [ ] **T-135**: Testar como Browser Source no OBS (fullscreen, transparente)

---

## FASE 2 — Teleprompter Inteligente
> Objetivo: Ele ouve voce e rastreia o roteiro

### 2.1 STT Integration
- [ ] **T-201**: Integrar Google Cloud Speech-to-Text (streaming)
- [ ] **T-202**: Capturar audio do microfone no backend
- [ ] **T-203**: Transcricao em tempo real com resultados parciais
- [ ] **T-204**: Enviar transcricao pro frontend via WebSocket

### 2.2 Script Tracking
- [ ] **T-211**: Criar formato de roteiro estruturado (JSON)
- [ ] **T-212**: Criar endpoint para carregar roteiro
- [ ] **T-213**: Implementar fuzzy matching (transcricao vs roteiro)
- [ ] **T-214**: Detectar posicao atual no roteiro
- [ ] **T-215**: Detectar quando pulou um ponto
- [ ] **T-216**: Detectar quando saiu do assunto
- [ ] **T-217**: Enviar posicao + alertas pro HUD

### 2.3 TTS Integration
- [ ] **T-221**: Integrar Google Cloud Text-to-Speech
- [ ] **T-222**: Gerar audio + visemas para lip sync
- [ ] **T-223**: Avatar falar frases curtas (alertas, dicas)
- [ ] **T-224**: Controle de volume e momento (nao falar durante live critica)

---

## FASE 3 — SEO + AEO + Copy Engine
> Objetivo: Conteudo nasce otimizado

### 3.1 SEO Engine
- [ ] **T-301**: Criar modulo SEO (titulo, descricao, tags)
- [ ] **T-302**: Integrar pesquisa de keywords (YouTube suggest API)
- [ ] **T-303**: Gerar 5+ opcoes de titulo com CTR estimado
- [ ] **T-304**: Gerar descricao estruturada com keywords
- [ ] **T-305**: Gerar tags relevantes
- [ ] **T-306**: Gerar capitulos com timestamps

### 3.2 AEO Engine
- [ ] **T-311**: Criar modulo AEO
- [ ] **T-312**: Gerar FAQ estruturado do conteudo
- [ ] **T-313**: Gerar resumo semantico (snippet-ready)
- [ ] **T-314**: Estruturar para featured snippets

### 3.3 Copy Engine
- [ ] **T-321**: Criar modulo de copywriting
- [ ] **T-322**: Gerar hooks (primeiros 30s)
- [ ] **T-323**: Estrutura de retencao (reset points a cada 2-3min)
- [ ] **T-324**: CTAs naturais
- [ ] **T-325**: Texto de thumbnail

---

## FASE 4 — Post Engine (Remotion)
> Objetivo: Edicao automatizada

### 4.1 Remotion Setup
- [ ] **T-401**: Criar projeto Remotion
- [ ] **T-402**: Pesquisar e documentar API do Remotion
- [ ] **T-403**: Criar composicao base (16:9 e 9:16)

### 4.2 Edicao Automatizada
- [ ] **T-411**: Detectar silencios no audio (ffmpeg)
- [ ] **T-412**: Remover silencios automaticamente
- [ ] **T-413**: Marcar highlights (momentos de energia alta)
- [ ] **T-414**: Gerar cortes de shorts (< 60s, 9:16)
- [ ] **T-415**: Capturar frame para thumbnail
- [ ] **T-416**: Renderizar via Node (programmatic render)

### 4.3 YouTube Integration
- [ ] **T-421**: Integrar YouTube Data API v3 (OAuth 2.0)
- [ ] **T-422**: Funcao: upload de video
- [ ] **T-423**: Funcao: definir metadata (titulo, desc, tags, thumbnail)
- [ ] **T-424**: Funcao: ler analytics de video
- [ ] **T-425**: Funcao: ler analytics do canal

---

## FASE 5 — Memoria e Evolucao
> Objetivo: Sistema aprende com voce

### 5.1 Memory Core
- [ ] **T-501**: Criar sistema de memoria JSON local
- [ ] **T-502**: Salvar historico de broadcasts
- [ ] **T-503**: Salvar roteiros usados
- [ ] **T-504**: Salvar metricas por video (retencao, CTR, views)
- [ ] **T-505**: Detectar padroes de estilo (palavras frequentes, ritmo)

### 5.2 Learning Loop
- [ ] **T-511**: Analisar quais videos performaram melhor
- [ ] **T-512**: Ajustar sugestoes de SEO baseado em historico
- [ ] **T-513**: Ajustar copy baseado em retencao real
- [ ] **T-514**: Gerar relatorio semanal de performance
