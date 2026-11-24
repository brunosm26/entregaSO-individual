import json
import time
from datetime import datetime, timezone

# Variável global para observar reutilização de ambiente (cold start vs warm start)
contador = 0


def lambda_handler(event, context):
    global contador
    contador += 1

    try:
        pedido = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"erro": "JSON inválido no corpo da requisição"}),
        }

    if "requisicaoId" not in pedido:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"erro": "requisicaoId obrigatório"}),
        }

    # Simula processamento lento para o experimento de Timeout (3s -> 10s)
    if pedido.get("demorar"):
        time.sleep(5)

    guia_entrega = {
        "sistema": "HemoChain",
        "guia": f"GUIA-HC-{pedido['requisicaoId']}",
        "requisicaoId": pedido["requisicaoId"],
        "hospital": pedido.get("hospital", "Hospital não informado"),
        "tipoComponente": pedido.get("tipoComponente", "CONCENTRADO_HEMACIAS"),
        "tipoSanguineo": pedido.get("tipoSanguineo", "O_NEGATIVO"),
        "urgencia": pedido.get("urgencia", "ROTINA"),
        "bolsas": pedido.get("bolsas", []),
        "statusEntrega": "EM_TRANSPORTE",
        "emitidaEm": datetime.now(timezone.utc).isoformat(),
        "invocacaoNesteAmbiente": contador,
    }

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(guia_entrega, ensure_ascii=False),
    }
