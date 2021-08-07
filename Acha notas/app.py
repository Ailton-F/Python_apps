import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys

opt = Options()
opt.add_argument('window-size=400,800')
opt.add_argument('--headless')
nav = webdriver.Chrome(executable_path=r"chromedriver.exe", options=opt)

mat = int(input('Matrícula: '))
password_ = input('Senha: ')
nav.get('https://suap.ifrn.edu.br/accounts/login/')
nav.find_element_by_id("id_username").send_keys(mat)
nav.find_element_by_id("id_password").send_keys(password_)
nav.find_element_by_class_name("btn.success").send_keys(Keys.RETURN)
nav.get("https://suap.ifrn.edu.br/edu/aluno/{}/?tab=boletim".format(mat))

print()
print()
print()

sleep(1)

fontcode = nav.page_source
site = bs(fontcode, 'html.parser')

notas_data = []

tabela = site.find('table', attrs={'summary': "Boletim do Aluno"})
corpodatabela = tabela.find('tbody')
disciplinas = corpodatabela.findAll('tr')


for boletins in disciplinas:
    materias = boletins.find('td', attrs={'headers': 'th_disciplina'})
    materia_content = materias.text

    try:
        n1n = boletins.find('td', attrs={'headers': 'th_n1n'})
        n1_content = n1n.text
    except:
        n1_content = '--'

    try:
        n2n = boletins.find('td', attrs={'headers': 'th_n2n'})
        n2_content = n2n.text
    except:
        n2_content = '--'
    
    try:
        n3n = boletins.find('td', attrs={'headers': 'th_n3n'})
        n3_content = n3n.text
    except:
        n3_content = '--'
    
    try:
        n4n = boletins.find('td', attrs={'headers': 'th_n4n'})
        n4_content = n4n.text
    except:
        n4_content = '--'

    mdf = boletins.find('td', attrs={'headers': 'th_mfd'})
    mdf_content = mdf.text
    
    situacao = boletins.find('td', attrs={'headers': 'th_situacao'})
    situacao_content = situacao.text

    notas_data.append([materia_content.replace(" ", ""), n1_content, n2_content, n3_content, n4_content,mdf_content, situacao_content])

print(pd.DataFrame(notas_data, columns=['Matéria', 'N1', 'N2', 'N3', 'N4','MDF', 'Situação']))
print()
print()
print('Script desenvolvido por: Ailton Filho')