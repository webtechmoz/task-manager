from manage_sql import SQLITE
from datetime import datetime
from tabulate import tabulate
import os

class Usuario:
    def __init__(
        self,
        username: str
    ):
        self.username = username
        self.__db = SQLITE(
            database='usuarios',
            path='usuarios'
        )
        self.__db.create_table(
            tablename='usuarios',
            columns=[
                self.__db.Column(
                    name='nome',
                    column_type=self.__db.Column_types.text
                ),
                self.__db.Column(
                    name='username',
                    column_type=self.__db.Column_types.text
                )
            ]
        )
    
    def criar_usuario(self, nome: str):
        self.__db.insert_data(
            tablename='usuarios',
            insert_query=[
                self.__db.ColumnData(
                    column='nome',
                    value=nome
                ),
                self.__db.ColumnData(
                    column='username',
                    value=self.username
                )
            ]
        )
    
    def ver_usuario(self):
        usuario = self.__db.select_data(
            tablename='usuarios',
            columns=['nome', 'username'],
            condition=self.__db.filter_by(
                column='username'
            ).EQUAL(
                value=self.username
            )
        )

        return usuario

class Tarefa:
    def __init__(
        self,
        username: str
    ):
        self.username = username
        self.__db = SQLITE(
            database='tarefas',
            path='tarefas'
        )
        self.__db.create_table(
            tablename='tarefas',
            columns=[
                self.__db.Column(
                    name='username',
                    column_type=self.__db.Column_types.text
                ),
                self.__db.Column(
                    name='tarefa',
                    column_type=self.__db.Column_types.text
                ),
                self.__db.Column(
                    name='criado_em',
                    column_type=self.__db.Column_types.text
                ),
                self.__db.Column(
                    name='prazo',
                    column_type=self.__db.Column_types.text
                ),
                self.__db.Column(
                    name='status',
                    column_type=self.__db.Column_types.text
                )
            ]
        )
    
    def ver_tarefas(self, status: str):
        tarefas = self.__db.select_data(
            tablename='tarefas',
            columns=['id','username', 'tarefa', 'criado_em', 'prazo', 'status'],
            condition=self.__db.filter_by(
                column='status'
            ).EQUAL(
                value=status
            ).AND.filterby(
                column='username'
            ).EQUAL(
                value=self.username
            )
        )

        return tarefas
    
    def criar_tarefa(self, tarefa: str, data: str):

        horario_actual = self.horario_actual()

        self.__db.insert_data(
            tablename='tarefas',
            insert_query=[
                self.__db.ColumnData(
                    column='username',
                    value=self.username
                ),
                self.__db.ColumnData(
                    column='tarefa',
                    value=tarefa
                ),
                self.__db.ColumnData(
                    column='criado_em',
                    value=horario_actual
                ),
                self.__db.ColumnData(
                    column='prazo',
                    value=data
                ),
                self.__db.ColumnData(
                    column='status',
                    value='Pendente' if horario_actual < data else 'Vencida'
                )
            ]
        )
    
    def editar_tarefa(self, coluna: str, valor: str, id: int):

        tarefa = self.__db.select_data(
            tablename='tarefas',
            columns=['criado_em', 'status'],
            condition=self.__db.filter_by(
                column='id'
            ).EQUAL(
                value=id
            )
        )

        if coluna == 'prazo' and tarefa[0][0] < valor and tarefa[0][1] != 'Concluida':
            self.__db.update_data(
                tablename='tarefas',
                edit_query=[
                    self.__db.ColumnData(
                        column='status',
                        value='Pendente'
                    )
                ],
                condition=self.__db.filter_by(
                    column='id'
                ).EQUAL(
                    value=id
                )
            )
        
        elif coluna == 'prazo' and tarefa[0][0] > valor and tarefa[0][1] != 'Concluida':
            self.__db.update_data(
                tablename='tarefas',
                edit_query=[
                    self.__db.ColumnData(
                        column='status',
                        value='Vencida'
                    )
                ],
                condition=self.__db.filter_by(
                    column='id'
                ).EQUAL(
                    value=id
                )
            )

        self.__db.update_data(
            tablename='tarefas',
            edit_query=[
                self.__db.ColumnData(
                    column=coluna,
                    value=valor
                )
            ],
            condition=self.__db.filter_by(
                column='id'
            ).EQUAL(
                value=id
            )
        )
    
    def horario_actual(self) -> str:

        now = datetime.now()

        date = now.strftime('%d/%m/%Y')
        hour = now.strftime('%H:%M')

        return f'{date} {hour}'

class Main:
    def __init__(
        self
    ):
        self.iniciar()
    
    def iniciar(self, username: str = None):
        """Inicio do programa"""
        self.clean_system

        if username:
            texto = f'Bem vindo {username}\n\n1. Criar Tarefa\n2. Editar Tarefa\n3. Ver Tarefas\n0. Sair: '
            
            while True:
                
                opcao = input(texto)

                if opcao in ['0','1','2','3']:
                    self.clean_system

                    if opcao == '0':
                        exit()
                    
                    elif opcao == '1':
                        self.criar_tarefa(username=username)
                    
                    elif opcao == '2':
                        self.tarefa_a_editar(username=username)
                    
                    elif opcao == '3':
                        self.clean_system
                        texto = 'Selecione uma das opções\n\n1. Tarefas Pendentes\n2. Tarefas Concluidas\n3. Tarefas Vencidas\n0. Voltar: '

                        while True:
                            opcao = input(texto)

                            if opcao in ['0', '1', '2', '3']:
                                self.clean_system

                                if opcao == '0':
                                    return self.iniciar(username=username)

                                elif opcao == '1':
                                    self.ver_tarefas(username=username, status='Pendente')
                                
                                elif opcao == '2':
                                    self.ver_tarefas(username=username, status='Concluida')
                                
                                elif opcao == '3':
                                    self.ver_tarefas(username=username, status='Vencida')
                            
                            break
                    
                    break

                else:
                    self.clean_system
                    print('Opção inválida, tente de novo\n')
        
        else:
            self.criar_usuario()
    
    def criar_usuario(self):

        while True:
            username = input('Digite seu username (0. Sair): ')

            if username == '':
                self.clean_system
                print('Username vazio inadimissível\n')
            
            elif username == '0':
                self.clean_system
                exit()
            
            else:
                ver_usuario = Usuario(username=username).ver_usuario()

                if len(ver_usuario) > 0:
                    return self.iniciar(username)

                break

        while True:
            nome = input('Digite seu nome (0. Sair): ')

            if nome == '':
                self.clean_system
                print('Nome vazio inadimissível\n')
            
            elif nome == '0':
                self.clean_system
                exit()
            
            else:
                break
        
        Usuario(username=username).criar_usuario(nome=nome)

        return self.iniciar(username)

    def criar_tarefa(self, username: str):
        while True:
            tarefa = input('Qual tarefa?: ')

            if tarefa == '0':
                self.clean_system
                return self.iniciar(username=username)
            
            elif tarefa == '':
                self.clean_system
                print('Tarefa vazia inadimisível\n')
            
            else:
                break
        
        while True:
            data = input('Em que dia? (dd/mm/yyyy): ')

            if data == '':
                self.clean_system
                print('Data vazia inadimisível\n')
            
            elif data == '0':
                self.clean_system
                return self.iniciar(username=username)

            else:
                break
        
        while True:
            hora = input('A que horas? (HH:MM): ')

            if hora == '':
                self.clean_system
                print('Hora vazia inadimisível\n')
            
            elif hora == '0':
                self.clean_system
                return self.iniciar(username=username)

            else:
                break
        
        self.clean_system
        Tarefa(username=username).criar_tarefa(tarefa=tarefa, data=f'{data} {hora}')

        return self.iniciar(username=username)
    
    def tarefa_a_editar(self, username: str):

        db = SQLITE(
            database='tarefas',
            path='tarefas'
        )

        header = ['id', 'username', 'tarefa', 'criado_em', 'prazo', 'status']
        tarefas = db.select_data(
            tablename='tarefas',
            columns=['id', 'username', 'tarefa', 'criado_em', 'prazo', 'status'],
            condition=db.filter_by(
                column='username'
            ).EQUAL(
                value=username
            ).AND.filterby(
                column='status'
            ).NOT_EQUAL(
                value='Concluida'
            )
        )

        while True:
            print(f'{tabulate(tarefas, header, tablefmt='grid')}\n')

            tarefa_id = [id[0] for id in tarefas]

            opcao = input('Escolha a tarefa a editar: ')
            
            if opcao == '':
                self.clean_system
                print('Id vazio inadimissível\n')
            
            elif opcao == '0':
                self.clean_system
                self.iniciar(username=username)
            
            elif int(opcao) in tarefa_id:
                self.clean_system
                return self.editar_tarefa(username=username, id=int(opcao))

            else:
                self.clean_system
                print('Opção incorrecta, tente de novo\n')
    
    def editar_tarefa(self, username: str, id: int):
        while True:
            texto = 'O que pretende editar?\n\n1. Tarefa\n2. Prazo\n3. Status: '

            opcao = input(texto)

            if opcao == '':
                self.clean_system
                print('Coluna vazia inadimissível\n')
            
            elif opcao == '0':
                self.clean_system
                return self.iniciar(username=username)

            elif opcao in ['1', '2', '3']:
                break

            else:
                self.clean_system()
                print('Opção inválida, tente novamente\n')
        
        if opcao == '1':
            self.clean_system
            tarefa = input('Nova Tarefa: ')

            Tarefa(username).editar_tarefa(coluna='tarefa', valor=tarefa, id=id)
        
        elif opcao == '2':
            self.clean_system
            data = input('Nova data (dd/mm/yyyy): ')
            hora = input('Nova data (HH:MM): ')
            Tarefa(username).editar_tarefa(coluna='prazo', valor=f'{data} {hora}', id=id)
        
        elif opcao == '3':
            db = SQLITE(
                database='tarefas',
                path='tarefas'
            )

            tarefa = db.select_data(
                tablename='tarefas',
                columns=['status'],
                condition=db.filter_by(
                    column='id'
                ).EQUAL(
                    value=id
                )
            )

            if tarefa[0][0] == 'Vencida':
                self.clean_system
                print('Não pode editar o status de uma tarefa vencida\n')

                return self.tarefa_a_editar(username=username)

            self.clean_system

            while True:
                i = input('Escolha a opção:\n\n1. Concluida\n0. Voltar: ')

                if i in ['0', '1']:
                    if i == '0':
                        return self.iniciar(username=username)

                    else:
                        break

            status = ['Concluida']
            Tarefa(username).editar_tarefa(coluna='status', valor=status[int(i) - 1], id=id)

        return self.iniciar(username=username)

    def ver_tarefas(self, username: str, status: str):

        tarefas = Tarefa(username=username).ver_tarefas(status=status)
        header = ['ID', 'Username', 'Tarefa', 'Criado Em', 'Prazo', 'Status']
        
        while True:
            print(tabulate(tarefas, headers=header, tablefmt='grid'))
            opcao = input('\n0. Voltar: ')

            if opcao == '0':
                self.clean_system
                return self.iniciar(username=username)

            else:
                self.clean_system
                exit()

    @property
    def clean_system(self):
        os.system('cls')

if __name__ == '__main__':
    Main()