import json
import threading
from http.client import HTTPConnection

import pytest

from agente.web import criar_servidor, nome_do_agente
from test_basico import LLMFalso, sistema_falso


@pytest.fixture
def servidor():
    srv = criar_servidor(lambda: sistema_falso(LLMFalso(rotulo="exemplo")), porta=0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield srv.server_address[1]
    srv.shutdown()
    srv.server_close()


def requisitar(porta, metodo, caminho, corpo=None):
    conexao = HTTPConnection("127.0.0.1", porta, timeout=5)
    conexao.request(metodo, caminho, body=None if corpo is None else json.dumps(corpo),
                    headers={"Content-Type": "application/json"})
    r = conexao.getresponse()
    return r.status, r.read().decode("utf-8")


def test_pagina_e_servida(servidor):
    status, html = requisitar(servidor, "GET", "/")
    assert status == 200 and "Tutor do Padrão State" in html


def test_mensagem_informa_agente(servidor):
    status, corpo = requisitar(servidor, "POST", "/api/mensagem", {"sessao": "a", "texto": "Me de um exemplo"})
    dados = json.loads(corpo)
    assert status == 200
    assert dados["texto"] == "resposta do Exemplificador" and dados["agente"] == "Exemplificador"


def test_entrada_vazia_e_json_invalido(servidor):
    _, corpo = requisitar(servidor, "POST", "/api/mensagem", {"sessao": "a", "texto": "  "})
    assert "nao digitou" in json.loads(corpo)["texto"]
    assert requisitar(servidor, "POST", "/api/mensagem", {"texto": "oi"})[0] == 400


def test_nova_conversa_gera_sessao(servidor):
    status, corpo = requisitar(servidor, "POST", "/api/nova", {"sessao": "a"})
    assert status == 200 and json.loads(corpo)["sessao"]


def test_nome_do_agente():
    assert nome_do_agente("avaliacao") == "Inquiridor"
    assert nome_do_agente("padrao_inventado") == "Guardião · recusa"
    assert nome_do_agente(None) is None
