
ATTACK_CATEGORY = {
    "back": "dos",
    "land": "dos",
    "neptune": "dos",
    "pod": "dos",
    "smurf": "dos",
    "teardrop": "dos",
    "apache2": "dos",
    "mailbomb": "dos",
    "processtable": "dos",
    "udpstorm": "dos",

    "ipsweep": "probe",
    "nmap": "probe",
    "portsweep": "probe",
    "satan": "probe",
    "mscan": "probe",
    "saint": "probe",

    "buffer_overflow": "u2r",
    "loadmodule": "u2r",
    "perl": "u2r",
    "rootkit": "u2r",
    "ps": "u2r",
    "sqlattack": "u2r",

    "ftp_write": "r2l",
    "guess_passwd": "r2l",
    "imap": "r2l",
    "multihop": "r2l",
    "phf": "r2l",
    "spy": "r2l",
    "warezclient": "r2l",
    "warezmaster": "r2l",
    "xlock": "r2l",
    "xsnoop": "r2l",
    "snmpguess": "r2l",
    "worm": "r2l",
}

STANDARD_PROTOCOL_BY_CATEGORY = {
    "dos": (
        "Ataque de tipo DoS/DDoS. Acciones sugeridas:\n"
        "1) Activar mitigación DoS/DDoS.\n"
        "2) Bloquear rango/IP origen.\n"
        "3) Coordinar con ISP.\n"
        "4) Revisar balanceadores/firewalls.\n"
    ),
    "probe": (
        "Actividad de escaneo/sondeo. Acciones:\n"
        "1) Bloquear IP origen.\n"
        "2) Revisar exposición de puertos.\n"
        "3) Correlacionar con eventos recientes.\n"
        "4) Ajustar reglas IDS/IPS.\n"
    ),
    "r2l": (
        "Intento de acceso remoto no autorizado.\n"
        "1) Bloquear credenciales o IP.\n"
        "2) Revisar logs de autenticación.\n"
        "3) Activar MFA.\n"
        "4) Verificar integridad del sistema.\n"
    ),
    "u2r": (
        "Escalamiento de privilegios detectado.\n"
        "1) Aislar host.\n"
        "2) Revocar credenciales comprometidas.\n"
        "3) Recolectar evidencia (forense).\n"
        "4) Revisar vulnerabilidades.\n"
    ),
}

# Nota: para tráfico normal NO usamos categoría, solo un texto sencillo
STANDARD_PROTOCOL_NORMAL = "Tráfico normal. Continuar monitoreo estándar."


STANDARD_PROTOCOL_BY_ATTACK = {
    "back": (
        "Ataque DoS tipo back (HTTP). "
        "Acciones: limitar conexiones al servidor web, bloquear IP origen en firewall y revisar logs de aplicación."
    ),
    "land": (
        "Ataque DoS land (paquetes con misma IP origen/destino). "
        "Acciones: filtrar paquetes inválidos en firewall/IDS y actualizar firmware de routers/firewalls."
    ),
    "neptune": (
        "SYN flood detectado (neptune). "
        "Acciones: activar limitación de conexiones SYN, usar SYN cookies y bloquear/limitar IP origen."
    ),
    "pod": (
        "Ping of Death (pod) detectado. "
        "Acciones: filtrar paquetes ICMP fragmentados/anómalos y mantener sistemas actualizados."
    ),
    "smurf": (
        "Ataque Smurf detectado (ICMP broadcast). "
        "Acciones: deshabilitar directed broadcast en routers y filtrar ICMP hacia direcciones broadcast."
    ),
    "teardrop": (
        "Ataque de fragmentación teardrop detectado. "
        "Acciones: actualizar sistemas, filtrar fragmentos anómalos y revisar configuraciones de red."
    ),
    "apache2": (
        "Ataque DoS contra servidor web (apache2). "
        "Acciones: activar rate limiting, limitar workers/procesos en el servidor web y bloquear IPs agresivas."
    ),
    "mailbomb": (
        "Ataque DoS por correo masivo (mailbomb). "
        "Acciones: limitar tasa de correos entrantes, usar listas negras y coordinar con el proveedor de correo."
    ),
    "processtable": (
        "Ataque DoS a tabla de procesos (processtable). "
        "Acciones: limitar procesos/ conexiones por usuario/IP y revisar servicios expuestos."
    ),
    "udpstorm": (
        "Ataque DoS basado en UDP (udpstorm). "
        "Acciones: filtrar tráfico UDP anómalo, aplicar rate limiting y coordinar con ISP para filtrado upstream."
    ),

    "ipsweep": (
        "Escaneo de direcciones IP (ipsweep). "
        "Acciones: bloquear IP origen, revisar exposición de redes internas y reforzar reglas IDS/IPS."
    ),
    "nmap": (
        "Escaneo de puertos/servicios con nmap. "
        "Acciones: bloquear IP origen, limitar respuestas a escaneos y minimizar superficie de ataque."
    ),
    "portsweep": (
        "Barrido de puertos (portsweep). "
        "Acciones: bloquear IP origen y revisar qué puertos innecesarios están abiertos."
    ),
    "satan": (
        "Escaneo de vulnerabilidades (satan). "
        "Acciones: revisar servicios detectados, aplicar parches y endurecer configuraciones."
    ),
    "mscan": (
        "Escaneo masivo de vulnerabilidades (mscan). "
        "Acciones: bloquear IP, revisar logs y aplicar parches pendientes en servicios expuestos."
    ),
    "saint": (
        "Escaneo de seguridad (saint). "
        "Acciones: bloquear origen, revisar superficie de exposición y ajustar controles de acceso."
    ),

    "buffer_overflow": (
        "Intento de explotación por buffer overflow. "
        "Acciones: aislar host, revisar binarios/vulnerabilidades conocidas y aplicar parches de seguridad."
    ),
    "loadmodule": (
        "Intento de carga de módulo malicioso (loadmodule). "
        "Acciones: aislar host, revisar procesos y módulos cargados, y ejecutar análisis forense."
    ),
    "perl": (
        "Uso de scripts Perl para escalamiento (perl). "
        "Acciones: revisar scripts ejecutados, limitar intérpretes en producción y aislar el sistema sospechoso."
    ),
    "rootkit": (
        "Posible instalación de rootkit. "
        "Acciones: aislar inmediatamente el host, tomar imagen forense y planear reinstalación limpia."
    ),
    "ps": (
        "Abuso del comando ps para reconocimiento y posible U2R. "
        "Acciones: revisar comandos ejecutados, cuentas involucradas y limitar accesos a herramientas administrativas."
    ),
    "sqlattack": (
        "Intento de ataque SQL (sqlattack). "
        "Acciones: revisar logs de base de datos y aplicación, aplicar validación de entrada y usar parametrización."
    ),

    "ftp_write": (
        "Intento de escritura remota vía FTP (ftp_write). "
        "Acciones: deshabilitar FTP inseguro, revisar archivos subidos y limitar accesos anónimos."
    ),
    "guess_passwd": (
        "Ataque de fuerza bruta a contraseñas (guess_passwd). "
        "Acciones: bloquear o retardar intentos, habilitar MFA y revisar cuentas bloqueadas."
    ),
    "imap": (
        "Intento de explotación de servicio IMAP. "
        "Acciones: revisar logs de correo, actualizar servidor IMAP y reforzar autenticación."
    ),
    "multihop": (
        "Acceso remoto usando saltos intermedios (multihop). "
        "Acciones: revisar túneles/encadenamientos, limitar forwardings y auditar conexiones entrantes/salientes."
    ),
    "phf": (
        "Explotación de vulnerabilidad CGI (phf). "
        "Acciones: deshabilitar scripts inseguros, actualizar servidor web y revisar accesos al CGI."
    ),
    "spy": (
        "Actividad de espionaje/monitorización remota (spy). "
        "Acciones: revisar procesos y conexiones, buscar herramientas de espionaje y aislar el sistema si se confirma."
    ),
    "warezclient": (
        "Uso no autorizado de recursos para intercambio de archivos (warezclient). "
        "Acciones: identificar usuario/host, cortar sesión y aplicar política disciplinaria si aplica."
    ),
    "warezmaster": (
        "Servidor de distribución warez detectado (warezmaster). "
        "Acciones: aislar el servidor, eliminar contenido ilícito y revisar posibles fugas de datos."
    ),
    "xlock": (
        "Intento de bloqueo/uso indebido de estación (xlock). "
        "Acciones: revisar sesiones locales, políticas de bloqueo de pantalla y accesos físicos."
    ),
    "xsnoop": (
        "Intento de espionaje de sesiones X (xsnoop). "
        "Acciones: forzar cifrado de sesiones, revisar usuarios conectados y restringir acceso remoto gráfico."
    ),
    "snmpguess": (
        "Intento de adivinar cadenas SNMP (snmpguess). "
        "Acciones: cambiar comunidades por valores robustos, limitar SNMP por IP y usar SNMPv3."
    ),
    "worm": (
        "Actividad tipo worm detectada. "
        "Acciones: aislar host, escanear red en busca de propagación y aplicar parches en todos los nodos afectados."
    ),
}

CLASS_NORMAL = "normal"


def classify_attack_state(pred_label: str, probabilities: dict) -> dict:


    p_attack = float(probabilities.get(pred_label, 0.0))


    if pred_label == CLASS_NORMAL:

        if p_attack >= 0.7:
            return {
                "state": "NORMAL",
                "attack_probability": p_attack,
                "category": None,
                "protocol": (
                    f"{STANDARD_PROTOCOL_NORMAL}\n"
                    "Confianza alta del modelo en que el tráfico es legítimo."
                ),
            }

        elif 0.3 <= p_attack < 0.7:
            return {
                "state": "FALSO_POSITIVO",
                "attack_probability": p_attack,
                "category": None,
                "protocol": (
                    "El modelo indica 'normal' pero con probabilidad moderada (0.3–0.7). "
                    "Posible falso positivo o sesión atípica. Revisar si es necesario."
                ),
            }

        else:  # p_attack < 0.3
            return {
                "state": "CRITICO",
                "attack_probability": p_attack,
                "category": None,
                "protocol": (
                    "El modelo predice 'normal' con probabilidad muy baja (<0.3). "
                    "Tráfico altamente sospechoso: ESCALAR inmediatamente al equipo de seguridad."
                ),
            }



    category = ATTACK_CATEGORY.get(pred_label)

    base_protocol = STANDARD_PROTOCOL_BY_ATTACK.get(
        pred_label,
        "Protocolo específico no definido para este ataque."
    )

    category_protocol = STANDARD_PROTOCOL_BY_CATEGORY.get(
        category,
        "Protocolo genérico de respuesta a incidentes."
    )

    final_protocol = (
        f"{base_protocol}\n\n"
        "[Protocolo estándar por categoría:]\n"
        f"{category_protocol}"
    )

    if p_attack < 0.3:
        state = "NORMAL"
    elif 0.3 <= p_attack < 0.7:
        state = "FALSO_POSITIVO"
    elif 0.7 <= p_attack < 0.9:
        state = "CONOCIDO"
    else:
        state = "CRITICO"

    return {
        "state": state,
        "attack_probability": p_attack,
        "category": category,
        "protocol": final_protocol,
    }
