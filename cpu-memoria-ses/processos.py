import datetime
import time
import psutil
import boto3

# Configurar as credenciais do AWS SES
aws_access_key = 'AKIAYURVOFAAOGIEIMWK'
aws_secret_key = '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'
aws_region = 'us-east-1'  # Substitua pelo seu região da AWS

# ...

def get_disk_usage():
    disk_info = psutil.disk_usage('/')
    disk_total = disk_info.total / (1024 ** 3)  # Converter para gigabytes
    disk_free = disk_info.free / (1024 ** 3)  # Converter para gigabytes
    return disk_total, disk_free

# ...

# Configurar o cliente AWS SES
ses_client = boto3.client('ses', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Variável para controlar o tempo do último envio de e-mail
last_email_time = 0

# Função para obter o tempo de atividade formatado
def get_formatted_uptime():
    uptime = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime_days = uptime.days
    uptime_hours, uptime_remainder = divmod(uptime.seconds, 3600)
    uptime_minutes, _ = divmod(uptime_remainder, 60)
    uptime_formatted = f"{uptime_days} dias, {uptime_hours} horas, {uptime_minutes} minutos"
    return uptime_formatted


# Obter os processos mais intensivos em memória RAM e CPU
processes = list(psutil.process_iter())
try:
    memory_process = max(processes, key=lambda p: p.memory_percent())
except psutil.NoSuchProcess:
    memory_process = None

try:
    cpu_process = max(processes, key=lambda p: p.cpu_percent())
except psutil.NoSuchProcess:
    cpu_process = None

# Loop contínuo para obter e enviar as informações em tempo real
while True:
    # Obter o uso da CPU
    cpu_percent = psutil.cpu_percent()

    # Obter o uso da memória RAM
    memory_info = psutil.virtual_memory()
    memory_used_percent = memory_info.percent

     # Obter o uso da memória RAM
    memory_info = psutil.virtual_memory()
    memory_used_percent = memory_info.percent

       # Obter o espaço total e livre em disco
    disk_total, disk_free = get_disk_usage()


  

  # Verificar se o consumo ultrapassou 70% e se já se passaram 20 minutos desde o último envio de e-mail
    current_time = time.time()
       # Obter o tempo de atividade da máquina
    uptime_formatted = get_formatted_uptime()

    

    if (cpu_percent > 70 or memory_used_percent > 70) and (current_time - last_email_time >= 1200):
        # Construir o corpo do e-mail com as informações
        email_body = f"Uso da CPU: {cpu_percent:.2f} porcento\n"
        email_body += f"Uso de memória RAM: {memory_used_percent:.2f} porcento"
        email_body += f"Tempo de atividade da máquina: {uptime_formatted}"
        email_body += f"Espaço livre em disco: {disk_free:.2f} GB\n"
       

        email_body += "Processo mais intenso em memória RAM:\n"
        email_body += f"PID: {memory_process.pid}\n"
        email_body += f"Nome: {memory_process.name()}\n"
        email_body += f"Uso de memória RAM: {memory_process.memory_percent()} porcento\n\n"
        email_body += "Processo mais intenso em CPU:\n"
        email_body += f"PID: {cpu_process.pid}\n"
        email_body += f"Nome: {cpu_process.name()}\n"
        email_body += f"Uso de CPU: {cpu_process.cpu_percent()} porcento\n"
    

        # Enviar o e-mail
        response = ses_client.send_email(
            Source='maikwilliam4553@gmail.com',
            Destination={
                'ToAddresses': ['seubanbi@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': 'Informações de consumo de CPU e memória'
                },
                'Body': {
                    'Text': {
                        'Data': email_body
                    }
                }
            }
        )
            # Atualizar o tempo do último envio de e-mail
        last_email_time = current_time

    # Aguardar um intervalo de tempo antes de atualizar novamente
    time.sleep(1)