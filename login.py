import pyautogui
import random
from flet import *

def main(page):

    user_list = ListView(expand=1, spacing=10, auto_scroll=True)
    chat = ListView(expand=1, spacing=10, auto_scroll=True)

    def enter(e):
        if not user_name.value:
            user_name.error_text = 'Preencha este campo, por favor!'
            page.update()
        elif len(user_name.value) > 18:
            user_name.error_text = 'Preencha com no máximo 18 caracteres!'
            page.update()
        else:
            page.remove(body)
            def send_message_tunnel(msg):
                tipo = msg['tipo']
                if tipo == 'message':
                    text_message = msg['txt']
                    user_message = msg['user']
                    color_message = msg['color']
                    
                    chat.controls.append(
                        Container(
                            content=Text(
                                f'{user_message}: \n{text_message}', color=f'#{color_message}', weight='w700', size=14
                            ),
                            bgcolor='#7fffd4',
                            border_radius=10,
                            padding=padding.only(10,5,0,5)
                        )
                    )
                else:
                    user_message = msg['user']
                    color_message = msg['color']
                    chat.controls.append(Text(f'{user_message} entrou no chat', size=15, weight='w700', italic=True, color='#006400'))
                    user_list.controls.append(
                        Container(
                            content=Text(
                                f'{user_message}', size=14, weight='w700', italic=True, color=f'#{color_message}'
                            ),
                            bgcolor='#7fffd4',
                            border_radius=10,
                            padding=padding.only(10,5,0,5)
                        ),
                    )
                page.update()
            page.pubsub.subscribe(send_message_tunnel)

            def send_message(e):
                if message.value:
                    page.pubsub.send_all({'txt': message.value, 'user': user_name.value, 'color': user_color, 'tipo': 'message'})
                    message.value = ''
                    page.update()
                    pyautogui.PAUSE=0.3
                    pyautogui.press('tab')

            message = TextField(
                hint_text='Digite uma mensagem', 
                border='underline',
                color='#303030',
                on_submit=send_message,
                prefix_icon=icons.MESSAGE,
                width=1400
            )
            
            btn_send = ElevatedButton(
                content=Text(
                    'ENVIAR',
                    color='white',
                    weight='w500',
                ),
                bgcolor='#1e90ff',
                on_click=send_message
            )
            
            campo = Row([message, btn_send])

            user_color = random.randint(100000,999999)
            page.pubsub.send_all({'user': user_name.value, 'color': user_color, 'tipo': 'enter_chat'})
            
            control = Container(
                Container(
                    Stack([
                        Container(
                            content=user_list,
                            width=180,
                            height=800,
                            bgcolor='#32ffffff',
                            padding=padding.only(15,15,15,5)
                        ),
                        Container(
                            Column([
                                Container(
                                    content=chat,
                                    width=1420,
                                    height=720,
                                    padding=padding.only(125,15)
                                ),
                                Container(
                                    content=campo,
                                    padding=padding.only(32,0)
                                ),
                            ]),
                            width=1580,
                            height=800,
                            bgcolor='#32ffffff',
                            margin=margin.only(190,0)
                        ),
                    ]),
                ),
                width=2180,
                height=920,
                alignment=alignment.center,
                gradient=LinearGradient(['#1e90ff', '#32cd32']),
            )
            page.add(control)
            page.update()
           
    user_name = TextField(
        width=280,
        height=40,
        hint_text='User',
        border='underline',
        color='#303030',
        prefix_icon=icons.PERSON_ROUNDED,
        on_submit=enter
    )

    body = Container(
        Container(
            Stack([
                Container(
                    Container(
                        Column([
                            Container(
                                Image(
                                    src='E:/Biblioteca/Documentos/Estudos/Python/Flet/LoginPage/logo.png',
                                    width=80,
                                ), 
                                alignment=alignment.top_center,
                                padding=padding.only(0,30)
                            ),
                            Text(
                                'Estácio Zap',
                                width=360,
                                size=30,
                                weight='w700',
                                text_align='center'
                            ),
                            Text(
                                'Por favor, digite seu nome de usuário',
                                size=16,
                                weight='w500',
                                text_align='center',
                                width=360,
                            ),
                            Container(
                                content=user_name,
                                alignment=alignment.center,
                                padding=padding.only(top=10)
                            ),
                            Container(
                                ElevatedButton(
                                    content=Text(
                                        'ENTRAR',
                                        color='white',
                                        weight='w500',
                                    ),
                                    on_click=enter,
                                    bgcolor='#1e90ff',
                                    width=280
                                ),
                                padding=padding.only(0,15),
                                alignment=alignment.center
                            )
                        ])    
                    ),
                    width=360,
                    height=360,
                    bgcolor='#22ffffff',
                    border_radius=15,
                )
            ]),
            width=360,
            height=360,
            alignment=alignment.center,
            padding=padding.only(bottom=300)
        ),
        width=2180,
        height=1110,
        gradient=LinearGradient(['#1e90ff', '#32cd32'])
    )

    page.window_max_width = 2180
    page.window_max_height = 1110
    page.padding = 0
    page.add(body)
    page.update()

app(target=main, view=WEB_BROWSER, port=8000)
