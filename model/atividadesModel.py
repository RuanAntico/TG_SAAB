import random

def gerar_pergunta_soma():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    resultado = num1 + num2
    
    pergunta_texto = f"{num1} + {num2} = ??"
    
    return {
        "texto": pergunta_texto,
        "resposta": str(resultado) 
    }

def gerar_pergunta_subtracao():
 
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    
    if num2 > num1:
        num1, num2 = num2, num1 
        
    resultado = num1 - num2
    pergunta_texto = f"{num1} - {num2} = ??"
    
    return {
        "texto": pergunta_texto,
        "resposta": str(resultado)
    }

def gerar_opcoes(resposta_correta):

    opcoes = [resposta_correta]
    resposta_int = int(resposta_correta)


    while len(opcoes) < 4:
        desvio = random.randint(-3, 3) 
        if desvio == 0: continue 

        opcao_falsa = resposta_int + desvio
        
        if opcao_falsa >= 0 and str(opcao_falsa) not in opcoes:
            opcoes.append(str(opcao_falsa))

    random.shuffle(opcoes)
    return opcoes

def gerar_pergunta_forma_geometrica():
    formas = ["Círculo", "Quadrado", "Triângulo", "Retângulo"]

    forma_correta = random.choice(formas)
    nomes_errados = [f for f in formas if f != forma_correta]

    opcoes = random.sample(nomes_errados, 3)
    opcoes.append(forma_correta)
    random.shuffle(opcoes)

    return {
        "texto": "Qual é essa forma geométrica?",
        "forma": forma_correta,  # nome que o front vai usar pra desenhar
        "resposta": forma_correta,
        "opcoes": opcoes
    }
    
    