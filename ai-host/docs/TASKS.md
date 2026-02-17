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

## FASE 3 — Criacao Visual (Pipeline de Assets IA)
> Objetivo: Gerar imagens, animar, criar musica/SFX/voz com IA

### 3.0 MCP Setup
- [ ] **T-300**: Configurar .mcp.json com todos os MCPs do projeto
- [ ] **T-301**: Configurar e testar Stitch MCP (Google Cloud + auth)
- [ ] **T-302**: Configurar e testar remotion-media-mcp (Kie.ai key)
- [ ] **T-303**: Configurar e testar ElevenLabs MCP
- [ ] **T-304**: Configurar e testar OBS MCP (obs-mcp)
- [ ] **T-305**: Configurar e testar @remotion/mcp (docs) + Agent Skills

### 3.1 Geracao de Imagens (Nano Banana Pro)
- [ ] **T-311**: Criar modulo de geracao de imagem com prompts cinematograficos
- [ ] **T-312**: Template de prompt: thumbnail YouTube (close-up, emocao, contraste)
- [ ] **T-313**: Template de prompt: b-roll cinematico (lente, luz, composicao)
- [ ] **T-314**: Template de prompt: graficos/infograficos (texto em imagem, layout)
- [ ] **T-315**: Sistema de referencia visual (manter consistencia entre assets)
- [ ] **T-316**: Gerar em multiplos aspect ratios (16:9, 9:16, 1:1) automaticamente

### 3.2 Animacao de Imagens (Veo 3.1)
- [ ] **T-321**: Criar modulo de animacao (image-to-video)
- [ ] **T-322**: Templates de movimento: dolly in, pan, crane, steady
- [ ] **T-323**: Transicoes cinematograficas entre imagens (match cut, morph)
- [ ] **T-324**: Gerar clips de b-roll animado a partir de imagens estaticas

### 3.3 Audio IA
- [ ] **T-331**: Criar modulo de TTS com ElevenLabs (21 vozes, controle de estilo)
- [ ] **T-332**: Criar modulo de musica com Suno (background, intro, outro)
- [ ] **T-333**: Criar modulo de SFX com ElevenLabs (swoosh, impact, ambient)
- [ ] **T-334**: Gerar legendas com Whisper local

### 3.4 UI/UX com Stitch
- [ ] **T-341**: Extrair Design DNA de referencia visual
- [ ] **T-342**: Gerar tela do Avatar Overlay com Stitch
- [ ] **T-343**: Gerar tela do HUD com Stitch
- [ ] **T-344**: Gerar tela do Painel de Controle com Stitch
- [ ] **T-345**: Converter HTML+Tailwind do Stitch pra componentes React

---

## FASE 4 — Post Engine (Remotion + FFmpeg)
> Objetivo: Edicao automatizada com assets gerados por IA

### 4.1 Remotion Setup
- [ ] **T-401**: Criar projeto Remotion com Agent Skills instalados
- [ ] **T-402**: Criar composicao base 16:9 (video principal)
- [ ] **T-403**: Criar composicao base 9:16 (Shorts/Reels)
- [ ] **T-404**: Criar composicao 2.39:1 (cinematico)

### 4.2 Pipeline de Assets → Video
- [ ] **T-411**: Integrar assets do remotion-media-mcp (public/ → staticFile)
- [ ] **T-412**: Montar timeline com imagens animadas + audio + legendas
- [ ] **T-413**: Aplicar principios de ritmo de edicao (ver CINEMATOGRAPHY.md)
- [ ] **T-414**: J-cuts e L-cuts automaticos nas transicoes de audio

### 4.3 Edicao Automatizada (FFmpeg MCP)
- [ ] **T-421**: Detectar e remover silencios (FFmpeg MCP)
- [ ] **T-422**: Marcar highlights (momentos de energia alta no audio)
- [ ] **T-423**: Gerar cortes de Shorts (< 60s, 9:16, vertical)
- [ ] **T-424**: Capturar melhor frame pra thumbnail
- [ ] **T-425**: Renderizar via Remotion CLI (programmatic render)

---

## FASE 5 — SEO + AEO + Copy + YouTube
> Objetivo: Conteudo nasce otimizado e publicado

### 5.1 SEO Engine
- [ ] **T-501**: Criar modulo SEO (titulo, descricao, tags)
- [ ] **T-502**: Integrar pesquisa de keywords (YouTube suggest API)
- [ ] **T-503**: Gerar 5+ opcoes de titulo com CTR estimado
- [ ] **T-504**: Gerar descricao estruturada com keywords
- [ ] **T-505**: Gerar tags relevantes
- [ ] **T-506**: Gerar capitulos com timestamps

### 5.2 AEO Engine
- [ ] **T-511**: Criar modulo AEO
- [ ] **T-512**: Gerar FAQ estruturado do conteudo
- [ ] **T-513**: Gerar resumo semantico (snippet-ready)

### 5.3 Copy Engine
- [ ] **T-521**: Criar modulo de copywriting
- [ ] **T-522**: Gerar hooks (primeiros 30s)
- [ ] **T-523**: Estrutura de retencao (reset points)
- [ ] **T-524**: CTAs naturais + texto de thumbnail

### 5.4 YouTube Integration
- [ ] **T-531**: Integrar YouTube Data API v3 (OAuth 2.0)
- [ ] **T-532**: Upload de video com metadata otimizada
- [ ] **T-533**: Upload de thumbnail gerada por IA
- [ ] **T-534**: Ler analytics (retencao, CTR, views)

---

## FASE 6 — Memoria e Evolucao
> Objetivo: Sistema aprende com voce

### 6.1 Memory Core
- [ ] **T-601**: Criar sistema de memoria JSON local
- [ ] **T-602**: Salvar historico de broadcasts
- [ ] **T-603**: Salvar roteiros e prompts usados (cinematografia)
- [ ] **T-604**: Salvar metricas por video (retencao, CTR, views)
- [ ] **T-605**: Detectar padroes de estilo visual + verbal

### 6.2 Learning Loop
- [ ] **T-611**: Analisar quais videos/thumbnails performaram melhor
- [ ] **T-612**: Ajustar prompts de imagem baseado em CTR de thumbnails
- [ ] **T-613**: Ajustar copy baseado em retencao real
- [ ] **T-614**: Gerar relatorio semanal de performance
