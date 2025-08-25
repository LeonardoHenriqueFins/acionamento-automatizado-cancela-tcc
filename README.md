# acionamento-automatizado-cancela-tcc
Projeto de TCC - Acionamento Automatizado de Cancela

# 🚧 Acionamento Automatizado de Cancela 🚧

Projeto de TCC (PIT2) - Faculdade Cotemig  
**Autor:** Leonardo Henrique Fins de Oliveira Santos  

---

## 🎯 Objetivo
Desenvolver um sistema que automatize o acionamento de cancelas em locadoras de veículos.  
O sistema identifica placas veiculares a partir de imagens estáticas, consulta a API da Locavia para verificar autorização e envia comandos a um Arduino para controle físico da cancela.

---

## 🛠 Tecnologias Utilizadas
- **Python** → OCR (EasyOCR, OpenCV), integração com API e servidor Flask  
- **Arduino (C/C++)** → controle físico da cancela via relé/motor  
- **API Locavia** → verificação de clientes autorizados  
- **GitHub** → versionamento do projeto e documentação  

---

## 📂 Estrutura do Projeto
acionamento-automatizado-cancela-tcc/
├── src/ # código fonte (Python, Arduino, etc.)
│ ├── app.py # aplicação principal em Python
│ └── arduino/ # código do Arduino
├── imagens/ # imagens de placas para testes
├── docs/ # documentação (diagramas, relatórios, etc.)
└── README.md # descrição do projeto

---

## 🔄 Fluxo do Sistema
1. Ler uma imagem contendo a placa de um veículo.  
2. Extrair o texto da placa usando OCR.  
3. Consultar a API Locavia para verificar se o veículo está autorizado.  
4. Se autorizado → enviar comando ao Arduino para abrir a cancela.  
5. Se não autorizado → manter cancela fechada (ou emitir alerta).  

---

## ▶️ Como Executar
### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/acionamento-automatizado-cancela-tcc.git
cd acionamento-automatizado-cancela-tcc
