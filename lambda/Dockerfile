 
# BASE IMAGE OFICIAL PARA AWS LAMBDA
 
FROM public.ecr.aws/lambda/python:3.11

 
# Instalar dependencias del sistema (si tu modelo lo requiere)
 
# Si no necesitas dependencias del sistema, puedes eliminar RUN apt-get
RUN yum install -y \
    tar \
    gzip \
    && yum clean all

# Copiar requerimientos
COPY lambda/requirements.txt ./

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt


# Copiar código ML + modelo + handler de Lambda

COPY src/ ./src/
COPY models/ ./models/
COPY lambda/lambda_function.py ./lambda_function.py

 
# Definir punto de entrada del handler Lambda
 
CMD ["lambda_function.lambda_handler"]
