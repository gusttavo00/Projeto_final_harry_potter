from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'HarryPotterSecretKey'

# Páginas comuns
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/fundador')
def fundador():
    return render_template('fundador.html')

@app.route('/integrantes')
def integrantes():
    return render_template('integrantes.html')

@app.route('/draco')
def draco():
    return render_template('draco.html')

@app.route('/tom')
def tom():
    return render_template('tom.html')

@app.route('/regulus')
def regulus():
    return render_template('regulus.html')


# Jogo 1: Número secreto
@app.route('/jogo_numero', methods=['GET', 'POST'])
def jogo_numero():
    if 'numero_secreto' not in session or request.method == 'GET':
        session['numero_secreto'] = random.randint(1, 10)
        session['tentativas'] = 3
        session['mensagem'] = ("O fundador da Sonserina deixou um enigma para os ambiciosos. "
                               "Ele escondeu um número entre 1 e 10. Você tem 3 chances para provar sua astúcia.")
        
    mensagem = session.get('mensagem')
    tentativas = session.get('tentativas')
    
    if request.method == 'POST':
        try:
            palpite = int(request.form['palpite'])
            session['tentativas'] -= 1
            
            if palpite == session['numero_secreto']:
                session['mensagem'] = f"A ambição o levou à vitória! O número era {session['numero_secreto']}."
            elif palpite < session['numero_secreto']:
                session['mensagem'] = "Seu palpite é frio como as masmorras. Tente um número maior."
            elif palpite > session['numero_secreto']:
                session['mensagem'] = "Seu palpite está alto demais. Tente um número menor."
                
            if session['tentativas'] <= 0 and palpite != session['numero_secreto']:
                session['mensagem'] = f"Game Over. O enigma era {session['numero_secreto']}."
                
        except (ValueError, KeyError):
            session['mensagem'] = "Isso não é um número válido."
    
    return render_template('jogo_numero.html', mensagem=mensagem, tentativas=tentativas)


# Jogo 2: Quiz do Chapéu Seletor
perguntas = [
    {
        "pergunta": "1) O que você mais valoriza?",
        "opcoes": {
            "a": ("Coragem", "Grifinória"),
            "b": ("Ambição", "Sonserina"),
            "c": ("Lealdade", "Lufa-Lufa"),
            "d": ("Inteligência", "Corvinal")
        }
    },
    {
        "pergunta": "2) Qual animal você escolheria como mascote?",
        "opcoes": {
            "a": ("Leão", "Grifinória"),
            "b": ("Cobra", "Sonserina"),
            "c": ("Texugo", "Lufa-Lufa"),
            "d": ("Corvo", "Corvinal")
        }
    },
    {
        "pergunta": "3) Qual qualidade você mais admira em si mesmo?",
        "opcoes": {
            "a": ("Corajoso", "Grifinória"),
            "b": ("Astuto", "Sonserina"),
            "c": ("Trabalhador", "Lufa-Lufa"),
            "d": ("Sábio", "Corvinal")
        }
    },
    {
        "pergunta": "4) Qual feitiço você usaria primeiro?",
        "opcoes": {
            "a": ("Expelliarmus (desarmar inimigos)", "Grifinória"),
            "b": ("Avada Kedavra (poder supremo)", "Sonserina"),
            "c": ("Alohomora (abrir portas)", "Lufa-Lufa"),
            "d": ("Legilimens (ler mentes)", "Corvinal")
        }
    },
    {
        "pergunta": "5) Se tivesse que escolher, preferiria ser lembrado como:",
        "opcoes": {
            "a": ("O Bravo", "Grifinória"),
            "b": ("O Grande", "Sonserina"),
            "c": ("O Bondoso", "Lufa-Lufa"),
            "d": ("O Sábio", "Corvinal")
        }
    }
]

@app.route('/jogo_quiz', methods=['GET', 'POST'])
def jogo_quiz():
    erro = None
    if request.method == 'POST':
        if len(request.form) < len(perguntas):
            erro = "Por favor, responda a todas as perguntas para descobrir sua casa!"
            # CORREÇÃO: Passando 'perguntas_enumeradas' para o template no caso de erro
            return render_template('jogo_quiz.html', perguntas_enumeradas=enumerate(perguntas), erro=erro)
        
        try:
            respostas = request.form
            pontos = {"Grifinória": 0, "Sonserina": 0, "Lufa-Lufa": 0, "Corvinal": 0}

            for i, pergunta in enumerate(perguntas):
                escolha = respostas.get(f"q{i}")
                if escolha and escolha in pergunta["opcoes"]:
                    casa = pergunta["opcoes"][escolha][1]
                    pontos[casa] += 1

            if all(p == 0 for p in pontos.values()):
                resultado = "Nenhuma"
            else:
                resultado = max(pontos, key=pontos.get)

            return redirect(url_for('resultado_quiz', casa=resultado))

        except Exception as e:
            erro = f"Ocorreu um erro ao processar seu quiz. Tente novamente."
            # CORREÇÃO: Passando 'perguntas_enumeradas' aqui também
            return render_template('jogo_quiz.html', perguntas_enumeradas=enumerate(perguntas), erro=erro)

    # CORREÇÃO: Passando 'perguntas_enumeradas' para o template no carregamento inicial da página
    return render_template('jogo_quiz.html', perguntas_enumeradas=enumerate(perguntas), erro=erro)

# Nova rota para exibir o resultado do quiz
@app.route('/resultado_quiz')
def resultado_quiz():
    casa = request.args.get('casa', 'Nenhuma')
    return render_template('resultado_quiz.html', resultado=casa)

# Rota para reiniciar o quiz
@app.route('/reiniciar_quiz')
def reiniciar_quiz():
    return redirect(url_for('jogo_quiz'))

#Executa o servidor 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)