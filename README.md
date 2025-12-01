# IDS-ML

**data/**:
    - **data/raw/:** Datasets crudos.
        - **/nslkdd:** Dataset NSL-KDD donde se encuentra el archivo de entrenamiento y el archivo de test.

## Datasets utilizados:
- **nslkdd:** presenta 43 columnas diferentes;
    1. **Duration:** Duración de la conexión.
    2. **protocol_type:** protocolo (tcp/udp)
    3. **service:** Servicio del destino (http / private)
    4. **flag:** Estado de la conexión (p. ej., SF, S0, REJ).
    5. **src_bytes:** Bytes enviados desde el origen hacia el destino
    6. **dst_bytes:** Bytes enviados desde el destino hacia el origen.
    7. **land:** Valor 1 si la IP y el puerto de origen y destino son iguales; 0 en caso contrario.
    8. **wrong_fragment:** Número de fragmentos IP erróneos.
    9. **urgent:** Número de paquetes con la bandera URG activa.
    10. **hot:** Número de indicadores “hot” (por ejemplo, accesos a directorios o al sistema).
    11. **num_failed_logins:** Número de intentos fallidos de inicio de sesión.
    12. **logged_in:** alor 1 si hubo un inicio de sesión exitoso; 0 si no.
    13. **num_compromised:** Número de condiciones comprometidas detectadas.
    14. **root_shell:** Valor 1 si se obtuvo acceso a una shell con privilegios de root.
    15. **su_attempted:** Valor 1 si se intentó obtener acceso como superusuario (su root).
    16. **num_root:** Número de accesos realizados como usuario root.
    17. **num_file_creations:** Número de archivos creados durante la conexión.
    18. **num_shells:** Número de ejecuciones de shell detectadas.
    19. **num_access_files:** Número de accesos a archivos de control.
    20. **num_outbound_cmds:** Número de comandos salientes por FTP (usualmente 0 en NSL-KDD).
    21. **is_host_login:** Valor 1 si el inicio de sesión corresponde a un host.
    22. **is_guest_login:** Valor 1 si el inicio de sesión fue como usuario invitado.
    23. **count:** Número de conexiones al mismo host en los últimos 2 segundos.
    24. **srv_count:** Número de conexiones al mismo servicio en los últimos 2 segundos.
    25. **serror_rate:** Porcentaje de conexiones con errores tipo SYN entre las recientes.
    26. **srv_serror_rate:** Porcentaje de conexiones al mismo servicio con errores SYN.
    27. **rerror_rate:** Porcentaje de conexiones con errores tipo REJ.
    28. **srv_rerror_rate:** Porcentaje de errores REJ en conexiones al mismo servicio.
    29. **same_srv_rate:** Fracción de conexiones al mismo servicio (ventana de 2 segundos).
    30. **diff_srv_rate:** Fracción de conexiones a servicios distintos (ventana de 2 segundos).
    31. **srv_diff_host_rate:** Fracción de conexiones al mismo servicio pero a diferentes hosts (en 2 segundos).
    32. **dst_host_count:** Número de conexiones al mismo host destino (ventana de 100 conexiones).
    33. **dst_host_srv_count:** Número de conexiones al mismo host y servicio (ventana de 100 conexiones).
    34. **dst_host_same_srv_rate:** Porcentaje de conexiones al mismo host que usan el mismo servicio.
    35. **dst_host_diff_srv_rate:** Porcentaje de conexiones al mismo host que utilizan servicios diferentes.
    36. **dst_host_same_src_port_rate:** Porcentaje de conexiones al mismo host que provienen del mismo puerto de origen.
    37. **dst_host_srv_diff_host_rate:** Porcentaje de conexiones al mismo servicio dirigidas a diferentes hosts.
    38. **dst_host_serror_rate:** Porcentaje de conexiones al mismo host que presentan errores SYN.
    39. **dst_host_srv_serror_rate:** Porcentaje de conexiones al mismo host y servicio con errores SYN.
    40. **dst_host_rerror_rate:** Porcentaje de conexiones al mismo host con errores REJ.
    41. **dst_host_srv_rerror_rate:** Porcentaje de conexiones al mismo host y servicio con errores REJ.
    42. **label:** Etiqueta que indica si la conexión es normal o un tipo específico de ataque (por ejemplo, neptune).

    ### Tipos de ataques que registra.
    - **neptune:** Denegación de servicios, el atacante envia una gran cantidad de paquetes TCP SYN a un host.

    - **warezclient:** Ataque de acceso no autorizado, Uso de un cliente FTP para subir archivos ilegales

    - **teardrop:** Denegación de servicios envia fragmentos IP solapados, el sistema se puede crashear.