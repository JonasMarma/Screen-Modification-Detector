import tkinter as tk
import tkinter.scrolledtext as tkst
from pyautogui import screenshot as scrShoot
import time
import threading

import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

resource_path('pause.png')
resource_path('play.png')
resource_path('selec.png')
resource_path('question.png')

selectedArea = None
isRunning = False
changePopActv = False
tutoPop = False
selPop = False
errArea = False

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        

        def switchOn(area):
            if selectedArea == None:
                noAreaError()
            else:
                global isRunning
                isRunning = True
                watch(area)
            updateGUI()

                
        def switchOff():    
            global isRunning
            isRunning = False
            updateGUI()

        def watch(area):
            def callback(area):
                lastPic = scrShoot(region = area)
                while isRunning == True:
                    currPic = scrShoot(region = area)
                    if currPic != lastPic:
                        changePopup()
                    lastPic = currPic
                    if isRunning == False:
                        break
                    time.sleep(1)

            t = threading.Thread(target = callback, args = (area,))
            t.start()


        def changePopup():
            global changePopActv
            
            if changePopActv == False:
                changePopActv = True

                def on_closing():
                    global changePopActv
                    changePopActv = False
                    changePop.destroy()
                                    
                changePop = tk.Toplevel()
                changePop.geometry("230x100")
                changePop.resizable(width = False, height = False)
                changePop.title("Aviso")
                changePop.wm_attributes("-topmost", 1)
                changePop.protocol("WM_DELETE_WINDOW", on_closing)

                okBtn = tk.Button(changePop, text = "Ok", command = on_closing)
                okBtn.pack(side = "bottom")

                message = tk.Message(changePop, text = "Foi detectada uma mudança na área selecionada")
                message.pack(side = "top")
            else:
                pass


        def noAreaError():
            global errArea
            errArea = True
            updateGUI()

            def on_closing():
                global errArea
                errArea = False
                errorScreen.destroy()
                updateGUI()
            
            def closeErr():
                global errArea
                errArea = False
                updateGUI()
                errorScreen.destroy()
                
            errorScreen = tk.Toplevel()
            errorScreen.geometry("150x50")
            errorScreen.resizable(width = False, height = False)
            errorScreen.title("Erro")
            errorScreen.protocol("WM_DELETE_WINDOW", on_closing)

            okBtn = tk.Button(errorScreen, text = "Ok", command = closeErr)
            okBtn.pack(side = "bottom")

            message = tk.Label(errorScreen, text = "Nenhuma área selecionada")
            message.pack(side = "bottom")


        def selectPop():
            global selPop
            selPop = True
            updateGUI()
            def on_closing():
                global selPop
                selPop = False
                boundBox.destroy()
                updateGUI()
                
            def select():
                global selectedArea
                global selPop
                selPop = False
                selectedArea = (boundBox.winfo_x(),
                                boundBox.winfo_y(),
                                boundBox.winfo_width(),
                                boundBox.winfo_height())
                updateGUI()
                boundBox.destroy()
            
            boundBox = tk.Toplevel(bg = "red")
            boundBox.geometry("200x100")
            boundBox.title("Selecionar")
            boundBox.wm_attributes('-alpha',0.6)
            boundBox.protocol("WM_DELETE_WINDOW", on_closing)

            selBtn = tk.Button(boundBox, text = "Ok", command = select)
            selBtn.pack(side = "bottom")
            updateGUI()


        def showTuto():
            global tutoPop
            tutoPop = True
            updateGUI()
            
            def on_closing():
                global tutoPop
                tutoPop = False
                tuto.destroy()
                updateGUI()
                
            def close():
                global tutoPop
                tutoPop = False
                updateGUI()
                tuto.destroy()
            
            tuto = tk.Toplevel()
            tuto.resizable(width = False, height = False)
            tuto.title("Como utilizar?")
            tuto.protocol("WM_DELETE_WINDOW", on_closing)

            editArea = tkst.ScrolledText(master = tuto,
                                         width  = 60,
                                         height = 15)
            editArea.pack()

            editArea.insert(tk.INSERT,
            """Este programa tem por objetivo alertar o usuário por meio de um popup sobre qualquer alteração ocorrendo em uma determinada região da tela.

Para selecionar a região da tela a ser monitorada, clique no botão "Selecionar Àrea". Aparecerá uma janela semitransparente com fundo vermelho que deve ser movida e redimensionada até que a área vermelha cubra a região desejada.

Quando estiver satisfeito com a área selecionada, clique em "OK" na janela transparente. Ela desaparecerá e a região estará pronta para ser monitorada.

Para iniciar o monitoramento, clique no botão "Começar", e para interrompê-lo, clique em "Pausar".

Enquanto o monitoramento está pausado, é possível clicar em "Selecionar Àrea" e selecionar outra região da tela a ser monitorada.
            """)

            okBtn = tk.Button(tuto, text = "Ok", command = close)
            okBtn.pack()

        def updateGUI():
            if isRunning == False:
                self.tutoBtn.config(state = "normal")
                self.selBtn.config(state = "normal")
                self.stopBtn.config(state = "disabled")
                self.startBtn.config(state = "normal")
                
            else:
                self.tutoBtn.config(state = "normal")
                self.selBtn.config(state = "disabled")
                self.stopBtn.config(state = "normal")
                self.startBtn.config(state = "disabled")
                
            if selPop == True or tutoPop == True or errArea == True:
                self.tutoBtn.config(state = "disabled")
                self.selBtn.config(state = "disabled")
                self.startBtn.config(state = "disabled")
                self.stopBtn.config(state = "disabled")


        playImage  = tk.PhotoImage(file = "play.png")
        playImage = playImage.subsample(6,6)
        pauseImage = tk.PhotoImage(file = "pause.png")
        pauseImage = pauseImage.subsample(6,6)
        selecImage = tk.PhotoImage(file = "selec.png")
        selecImage = selecImage.subsample(6,6)
        questionImage = tk.PhotoImage(file = "question.png")
        questionImage = questionImage.subsample(6,6)


        self.label = tk.Label(root, text = "Detector de alterações na tela - v1.0")
        self.label.grid(row=0, column = 0, columnspan = 2)


        self.tutoBtn = tk.Button(text = "Como utilizar", command = showTuto)
        self.tutoBtn.image = questionImage
        self.tutoBtn.config(image = questionImage, compound = "left")
        self.tutoBtn.grid(row = 1, column = 0, columnspan = 2)


        self.selBtn = tk.Button(text = "Selecionar Área", command = selectPop)
        self.selBtn.image = selecImage
        self.selBtn.config(image = selecImage, compound = "left")
        self.selBtn.grid(row = 2, column = 0, columnspan = 2, pady = 5)


        self.startBtn = tk.Button(text = "Começar", command = lambda: switchOn(selectedArea), state = "disabled")
        self.startBtn.image = playImage
        self.startBtn.config(image = playImage, compound = "left")
        self.startBtn.grid(row = 3, column = 0)

        self.stopBtn = tk.Button(text = "Pausar", command = lambda: switchOff(), state = "disabled")
        self.stopBtn.image = pauseImage
        self.stopBtn.config(image = pauseImage, compound = "left")
        self.stopBtn.grid(row = 3, column = 1)


def on_closing():
    print("NOPE")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vigia")
    root.resizable(width = False, height = False)
    MainApplication(root).grid()
    root.mainloop()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    quit()

    
