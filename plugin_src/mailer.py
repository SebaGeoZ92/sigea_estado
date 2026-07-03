"""
mailer.py — Puente entre el plugin y el servidor de correos SIGEA (Railway).

El servidor (dashboard/server.js) expone POST /mail y hace 3 cosas:
  1. Envía el correo real por SMTP (o simula si no hay SMTP configurado).
  2. Si tipo == "entrega", agrega copia automática al supervisor
     (SIGEA_SUPERVISOR_MAIL en Railway) — así no hace falta lógica de CC aquí.
  3. Registra el evento en bitacora.json usando las credenciales de estado.json.

REGLA (config, NO hardcodear): la URL del servidor de mail se lee de
estado.json campo "_mail". Si no está configurada, se cae a simulación
local (bitacora.evento_mail con enviado=False) para no romper el flujo.
"""
import json
from urllib import request as _req, error as _err


def _url_mail():
    """Lee '_mail' desde estado.json vía las credenciales ya configuradas."""
    from . import github_report
    creds = github_report._obtener_credenciales()
    repo, branch, token = creds['repo'], creds['branch'], creds['token']
    url = f"https://api.github.com/repos/{repo}/contents/estado.json?ref={branch}"
    req = _req.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "SIGEA-Plugin")
    import base64
    with _req.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
        estado = json.loads(base64.b64decode(data["content"]).decode())
    return (estado.get("_mail") or "").rstrip("/")


def enviar_mail(destinatario, tipo, recinto, funcionario=""):
    """Envía un correo real vía el servidor SIGEA en Railway.

    destinatario: clave de usuario en estado.json (ej. 'igarrido') o email directo.
    tipo: 'asignacion' | 'entrega' | 'qa_ok' | 'qa_obs' | 'cierre'.

    Si '_mail' no está configurado en estado.json o la llamada falla,
    cae a simulación local (no bloquea el flujo del funcionario).
    Devuelve (ok: bool, msg: str).
    """
    try:
        base = _url_mail()
    except Exception as e:
        base = ""
        _fallback_simulado(recinto, funcionario, destinatario, tipo,
                           f"sin _mail configurado ({e})")
        return False, f"Mail server no configurado: {e}"

    if not base:
        _fallback_simulado(recinto, funcionario, destinatario, tipo,
                           "_mail vacío en estado.json")
        return False, "'_mail' no configurado en estado.json — mail simulado."

    payload = json.dumps({
        "destinatario": destinatario, "tipo": tipo,
        "recinto": recinto, "funcionario": funcionario,
    }).encode()
    try:
        req = _req.Request(f"{base}/mail", data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with _req.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read().decode())
        enviado = resp.get("enviado", False)
        return True, ("Correo enviado." if enviado else "Correo simulado (SMTP no configurado en Railway).")
    except (_err.URLError, _err.HTTPError, Exception) as e:
        # El servidor no registra el evento si la llamada falla — lo hacemos
        # nosotros localmente para no perder el rastro en bitácora.
        _fallback_simulado(recinto, funcionario, destinatario, tipo,
                           f"error de red: {e}")
        return False, f"No se pudo contactar el servidor de mail: {e}"


def _fallback_simulado(recinto, funcionario, destinatario, tipo, motivo):
    from . import bitacora
    asunto = f"[SIGEA] {tipo} — recinto {recinto}"
    bitacora.evento_mail(recinto, funcionario or destinatario, destinatario,
                         asunto, enviado=False)
