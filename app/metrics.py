import time
from typing import Optional

# Importar psutil/pynvml de forma defensiva para permitir execução
# em máquinas sem NVidia / sem as bibliotecas instaladas.
try:
    import psutil
except Exception:
    psutil = None

try:
    import pynvml
except Exception:
    pynvml = None


# Medidor de performance para CPU, GPU e memória
class MedidorPerformance:
    def __init__(self):
        self.medidas_cpu = []
        self.medidas_gpu = []
        self.medidas_mem = []
        self.start_time = time.time()

        # Inicializa NVML (NVIDIA) apenas se disponível
        self.gpu_handle: Optional[object] = None
        if pynvml is not None:
            try:
                pynvml.nvmlInit()
                self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            except Exception:
                self.gpu_handle = None

    # Medir uso atual
    def medir(self):
        # CPU e memória (se psutil disponível)
        if psutil is not None:
            try:
                self.medidas_cpu.append(psutil.cpu_percent(interval=None))
                self.medidas_mem.append(psutil.virtual_memory().percent)
            except Exception:
                # Em caso de falha na medição, registrar zeros para manter contagem
                self.medidas_cpu.append(0)
                self.medidas_mem.append(0)
        else:
            # Bibliotecas de medição não disponíveis
            self.medidas_cpu.append(0)
            self.medidas_mem.append(0)

        # GPU (se houver NVIDIA)
        if self.gpu_handle:
            try:
                util = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
                self.medidas_gpu.append(getattr(util, "gpu", 0))
            except Exception:
                # Não falhar por causa da GPU
                self.medidas_gpu.append(0)

    # Finalizar e calcular médias
    def finalizar(self):
        total_time = time.time() - self.start_time
        avg_cpu = (
            sum(self.medidas_cpu) / len(self.medidas_cpu) if self.medidas_cpu else 0
        )
        avg_mem = (
            sum(self.medidas_mem) / len(self.medidas_mem) if self.medidas_mem else 0
        )
        avg_gpu = (
            sum(self.medidas_gpu) / len(self.medidas_gpu) if self.medidas_gpu else 0
        )
        return {
            "tempo_total_segundos": round(total_time, 2),
            "cpu_media_percent": round(avg_cpu, 2),
            "memoria_media_percent": round(avg_mem, 2),
            "gpu_media_percent": (
                round(avg_gpu, 2) if self.medidas_gpu else "Sem GPU NVIDIA."
            ),
            "amostras_coletadas": len(self.medidas_cpu),
        }


# Dependência para FastAPI
def get_medidor():
    # Criar nova instância do medidor
    return MedidorPerformance()
