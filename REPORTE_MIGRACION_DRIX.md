# REPORTE PARA EL DIRECTOR — Migración SIGEA a cuenta institucional

Fecha: 2026-07-03 (actualizado — migración confirmada y verificada)
De: Seba (smardones) — asistido por Claude Code
Para: Director DR Araucanía

═══════════════════════════════════════════════════════════════
ECOSISTEMA — LINKS DE REFERENCIA (para documentación)
═══════════════════════════════════════════════════════════════
OJO: el usuario GitHub institucional es "direccionregionalix-star"
(con sufijo "-star" — "direccionregionalix" a secas ya estaba tomado
por otra cuenta). Cualquier documentación futura debe usar el nombre
completo con sufijo.

SIGEA (este sistema — plugin + dashboard + mail):
  - Repo código:     github.com/direccionregionalix-star/sigea_estado
  - estado.json:     raw.githubusercontent.com/direccionregionalix-star/sigea_estado/main/estado.json
  - plugins.xml:      raw.githubusercontent.com/direccionregionalix-star/sigea_estado/main/plugins.xml
  - Dashboard web:    https://web-production-17ce60.up.railway.app
  - Proyecto Railway: nombre auto-generado por Railway (revisar en el
    dashboard de Railway cuál service corresponde — se creó como
    proyecto nuevo y separado del resto).

SIGE (geocodificador v4.2 "Dratini" — herramienta de terreno, repo distinto):
  - Proyecto Railway: "skillful-flow" → sigeraildrix-production.up.railway.app
  - Repo: SIGE_RAIL_DRIX (no gestionado por Claude Code en esta sesión)

Otros proyectos Railway de la cuenta institucional (confirmar detalle
con Seba al documentar — no se tocaron en esta migración):
  - Bot Telegram de captura de recintos — 2 instancias (pruebas + producción)
  - Web visor de levantamientos del bot
  - Blog personal
  (nombres Railway: "site", "resplendent-enthusiasm", "loyal-perfection",
  "soothing-respect" — falta mapear cada uno a su función exacta)

Repo personal DEPRECADO (ya no es producción, se mantiene como historial):
  - github.com/SebaGeoZ92/sigea_estado

═══════════════════════════════════════════════════════════════
CONTEXTO — POR QUÉ MIGRAMOS
═══════════════════════════════════════════════════════════════
Desde el Sprint 1, producción de SIGEA vivía en mi cuenta personal
(SebaGeoZ92/sigea_estado en GitHub) por una limitación técnica: el
conector de Claude Code no llegaba a la cuenta institucional DRIX. Esto
era deuda explícita, documentada, y de riesgo bajo mientras estado.json
no llevara datos sensibles (nunca los llevó — solo metadata y conteos).

Esta semana resolvimos esa deuda: todo el sistema SIGEA (plugin QGIS +
dashboard + servidor de correo) ahora corre bajo la cuenta institucional
direccionregionalix, con su propio Railway pagado.

═══════════════════════════════════════════════════════════════
QUÉ SE HIZO
═══════════════════════════════════════════════════════════════

1. MIGRACIÓN DEL REPOSITORIO
   - Repo importado completo (código + historial) de SebaGeoZ92/sigea_estado
     a direccionregionalix-star/sigea_estado. Público, igual que antes.
     (Nota: el usuario GitHub institucional quedó con sufijo "-star"
     porque "direccionregionalix" ya estaba tomado — hubo que corregir
     todas las URLs una vez detectado.)
   - Token de escritura nuevo generado en la cuenta institucional
     (fine-grained, acotado solo a este repo, permiso Contents R/W).
   - estado.json actualizado con el nuevo repo destino (_r) y token
     ofuscado (_t) — mecanismo configurable, nunca hardcodeado en código.

2. INFRAESTRUCTURA — RAILWAY
   - Confirmamos que el Railway institucional ya corría 5 proyectos
     (bot Telegram x2, visor de levantamientos, SIGE, blog personal).
     SIGEA no comparte proyecto con ninguno — evita mezclar variables
     de entorno y logs de sistemas distintos.
   - Proyecto nuevo creado solo para SIGEA:
     https://web-production-17ce60.up.railway.app
   - Sirve el dashboard de estado + el servidor de notificaciones por
     correo (antes esa pieza existía en código pero nunca se había
     desplegado — los mails llevaban meses en modo simulación).

3. DISTRIBUCIÓN DEL PLUGIN
   - plugins.xml y el zip del plugin (v2.1.0) ahora se sirven directo
     desde GitHub raw institucional. Se dio de baja la dependencia de
     Netlify personal (sigeadmin.netlify.app) que existía desde antes
     del Sprint 1.

4. CORREO REAL (nueva funcionalidad, no solo migración)
   - Se conectó por primera vez el envío real de correo: el plugin ahora
     sí llama al servidor cuando un funcionario entrega un recinto.
   - Se agregó copia automática a smardones@servel.cl en cada entrega,
     para poder hacer QA sin esperar aviso manual — pedido tuyo de este
     sprint.
   - Variables SMTP configuradas en Railway (Gmail con contraseña de
     aplicación).

5. COMUNICACIÓN A FUNCIONARIOS
   - Mensaje enviado por Teams a igarrido, mespinozan, jmedina,
     pfigueroa con las 2 acciones que deben hacer en su QGIS: cambiar
     la URL del estado online y el repositorio de plugins, para quedar
     sobre la v2.1.0 y el repo institucional.

═══════════════════════════════════════════════════════════════
ESTADO ACTUAL — CHECKLIST
═══════════════════════════════════════════════════════════════
[x] Repo migrado e importado completo
[x] Token institucional generado y estado.json actualizado
[x] Proyecto Railway propio para SIGEA, separado de SIGE y otros
[x] Variables de entorno configuradas (repo, estado, mails, SMTP)
[x] plugins.xml y zip v2.1.0 servidos desde repo institucional
[x] Código de envío de correo real + copia automática al supervisor
[x] Mensaje a funcionarios enviado con instrucciones de reconexión
[x] Bug detectado y corregido: el usuario GitHub real es
    "direccionregionalix-star" (no "direccionregionalix"), causaba
    404 en dashboard, config QGIS y repositorio de plugins. Todas las
    URLs corregidas y verificadas (estado.json, plugins.xml, zip → 200 OK).

[ ] VERIFICACIÓN END-TO-END — pendiente, es el siguiente paso crítico:
    - [x] estado.json, plugins.xml y el zip cargan bien (verificado hoy).
    - [ ] Confirmar visualmente que el dashboard muestra los datos
      (colega ya lo vio cargar antes del fix del "-star"; falta
      confirmar post-fix).
    - [ ] Confirmar que el correo real efectivamente llega (probar con
      una entrega de prueba y revisar logs de Railway).
    - [ ] Confirmar que cada funcionario reconectó su QGIS con las URLs
      corregidas (con "-star").
    - [ ] Probar la pestaña "Entregas SIGE" del modo admin con un xlsx real.

[ ] CIERRE DE LA CUENTA VIEJA — pendiente, no bloquea nada:
    - Revocar el token personal de SebaGeoZ92 (ya no se usa para nada).
    - Decidir si SebaGeoZ92/sigea_estado se archiva o se deja inactivo.

[ ] INTEGRACIÓN SIGE ↔ SIGEA — pendiente, requiere tu decisión:
    - El admin de SIGEA espera que las entregas de funcionarios que
      trabajan en SIGE web (ej. pfigueroa) aparezcan como archivos
      {recinto}_ENTREGA.xlsx en una carpeta OneDrive específica
      (dev_007/funcionarios/{usuario}/).
    - No he podido confirmar si el SIGE que corre hoy en Railway
      (proyecto "skillful-flow") efectivamente exporta a esa ruta.
    - Necesito acceso al repo de SIGE (SIGE_RAIL_DRIX) para revisarlo,
      o que me indiques cómo exporta hoy sus entregas.

═══════════════════════════════════════════════════════════════
RIESGOS Y DECISIONES QUE NECESITAN TU VISTO BUENO
═══════════════════════════════════════════════════════════════
1. El mail real recién se activó — hasta que verifiquemos que llega
   correctamente, seguimos operando con la copia manual de siempre
   como respaldo (avisar por Teams cuando alguien entrega).

2. La integración SIGE↔SIGEA (punto pendiente arriba) es la única
   pieza de este sprint que no puedo cerrar sin más información tuya
   o acceso al otro repo. Si prefieres, puedo trabajar directamente
   con quien mantenga SIGE para coordinar el formato de exportación.

3. El repo personal SebaGeoZ92/sigea_estado queda con historial público
   de un proceso electoral (aunque sin datos sensibles). Sugiero
   archivarlo formalmente una vez confirmada la migración, para dejar
   un solo repo de referencia activo.

═══════════════════════════════════════════════════════════════
PRÓXIMO PASO PROPUESTO
═══════════════════════════════════════════════════════════════
Con tu autorización, esta semana cerramos la verificación end-to-end
(punto pendiente #1) y coordinamos la integración SIGE↔SIGEA (pendiente
#3), que es la pieza que falta para que el flujo completo — SIGE web →
QA → central.gpkg — funcione sin intervención manual.
