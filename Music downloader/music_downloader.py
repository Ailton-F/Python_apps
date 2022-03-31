import PySimpleGUI as sg
import youtube_dl as yt

sg.theme('Default')
musics = []

#======================PÁGINA PRINCIPAL======================
def pg1():
    layout = [
        [sg.Text('BAIXAR MÚSICAS', text_color='blue')],
        [sg.Text('\n')],
        [sg.Button('Única', key='-ONE-', size=(15, 1)), sg.Button('Várias', key='-MANY-', size=(15, 1))]
    ]

    return sg.Window('Tela Inicial', layout, size=(400,150), element_justification='c', finalize=True)

#======================PÁGINA DE DOWNLOAD ÚNICO======================
def pag_unica():
    layout = [
        [sg.Text('DOWNLOAD ÚNICO', text_color='blue')],
        [sg.Text('\n')],
        [sg.Text('Link: ', size=5),sg.InputText(size=100, key='-URL-')],
        [sg.Text('\n')],
        [sg.Button('Baixar', key='-DU-'), sg.Button('Voltar')]
    ]

    return sg.Window('Download', layout, size=(400,200), element_justification='c', finalize=True)

#======================PÁGINA DE VÁRIOS DOWNLOADS======================
def pag_varias():
    layout = [
        [sg.Text('VÁRIOS DOWNLOADS', text_color='blue')],
        [sg.Text('\n')],
        [sg.Text('Link: ', size=5), sg.InputText(size=100, key='-URL-')],
        [sg.Text('\n')],
        [sg.Button('Adicionar'), sg.Button('Baixar', key='-DV-'), sg.Button('Voltar')]
    ]

    return sg.Window('Download', layout, size=(400,200), element_justification='c', finalize=True)

#======================PROCESSO DE DOWNLOAD======================
def run():
    #======================PÁGINAS======================
    pagina_principal = pg1()
    pu = pag_unica()
    pu.hide()
    pv = pag_varias()
    pv.hide()

    #======================LOOP======================
    while True:

        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event is None:
            break

        if event == 'Voltar':
            pu.hide()
            pv.hide()
            pagina_principal.un_hide()        

        #CONDIÇÕES DA PÁGINA DE DOWNLOAD UNICO
        if event == '-ONE-':
                pagina_principal.hide()
                pu.un_hide()

        if event == '-DU-':
            try:
                video_url = values['-URL-']
                video_info = yt.YoutubeDL().extract_info(
                url = video_url,download=False
                )

                filename = f"{video_info['title']}.mp3"
                options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':filename,
                }
                ydl = yt.YoutubeDL(options) 
                sg.popup(ydl.download([video_info['webpage_url']]))
                sg.popup(f"Download complete... {filename}")
            except:
                sg.popup('Falha ao realizar o download do link {}')

        #CONDIÇÕES DA PÁGINA DE DOWNLOAD UNICO
        if event == '-MANY-':
            pagina_principal.hide()
            pv.un_hide()

        if event == 'Adicionar':
            musics.append(values['-URL-'])
            sg.popup(f'Músicas adicionadas: {musics}')

        if event == '-DV-':
                musics.clear()
                for i in range(len(musics)):
                    try:
                        video_url = musics[i]
                        video_info = yt.YoutubeDL().extract_info(
                        url = video_url,download=False
                        )

                        filename = f"{video_info['title']}.mp3"
                        options={
                        'format':'bestaudio/best',
                        'keepvideo':False,
                        'outtmpl':filename,
                        }
                        ydl = yt.YoutubeDL(options) 
                        ydl.download([video_info['webpage_url']])
                    except:
                        sg.popup('Falha ao realizar o download do link {}')

if __name__=='__main__':
    run()