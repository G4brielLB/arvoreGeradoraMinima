from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter.messagebox import showinfo
import random
import grafo_gui as gpg

graphic = gpg.GrafoGui() 
canvas = None

def handlePrim():
    try:
        graphic.prim()
    except Exception as e:
        raise e
    render()

def handleKruskal():
    try:
        graphic.kruskal()
    except Exception as e:
        raise e
    render()
    
def handleZoomOut():
    graphic.zoomOut()
    render()

def handleZoomIn():
    graphic.zoomIn()
    render()

def handlePaintNext():
    graphic.paintNext()
    render()

def handleEraseSelected():
    graphic.eraseSelected()
    render()

def handleReset():
    graphic.reset()
    render()

def handleClick(x,y):
    graphic.handleClick(x,y)

def selectVerticeToDrag(x,y):
    graphic.selectVerticeToDrag(x,y)

def deselectDrag():
    graphic.deselectDrag()

def handleDrag(x,y):
    graphic.handleDrag(x,y)

def handleMotion(offset_x,offset_y):
    graphic.move(offset_x,offset_y)

def handleAtribuatteValueToSelectedEdge(value_buffer):
    try:
        value = int(value_buffer)
        graphic.atribuatteValueToSelectedEdge(value)
    except Exception as e:
        print(e) #passando dado errado ,aí é paia
        raise e

def handleAddEdges(string_edges):
    try:
        edges_str_line = string_edges.split(";")
        edges_str = [edge_line.split(",") for edge_line in edges_str_line]
        edges = []

        for edge_str in edges_str:
            if(len(edge_str) != 3):
                raise Exception("valor inválido")
            new_edge = []
            for char in edge_str:
                new_edge.append(int(char))
            edges.append(new_edge)

        graphic.addEdges(edges)
    except Exception as e:
        print(e) #passando dado errado ,aí é paia
        raise e

def handleRandom(vertices_num, completo):
    vertices = vertices_num

    max_arestas = (vertices) * (vertices-1)

    grafo_str = ""

    if completo == 1:
        arestas_this_time = vertices - 1
        i = 1
        while arestas_this_time > 0:
            v1 = i
            for j in range(i+1,vertices+1):
                v2 = j
                peso = random.randint(1,30)
                grafo_str += str(v1)+","+str(v2)+","+str(peso)+";"
            i+=1
            arestas_this_time -= 1
    else:
        for i in range(random.randint(0,max_arestas)):

            v1 = random.randint(1,vertices)
            v2 = random.randint(1,vertices)
            while v2 == v1:
                v2 = random.randint(1,vertices)
            
            peso = random.randint(1,30)

            grafo_str += str(v1)+","+str(v2)+","+str(peso)+";"
    try:
        handleReset()
        handleAddEdges(grafo_str[0:-1])
    except Exception as e:
        print(e) #passando dado errado ,aí é paia
        raise e

def render():
    graphic.render(canvas)

if __name__ == '__main__':
    shift = False
    space = False
    edge_value_buffer = ""
    dragging = False
    mouse_pos = [0,0]

    def handClick(event):
        if shift:
            handleClick(event.x,event.y)
        elif dragging == False:
            selectVerticeToDrag(event.x,event.y)

        render()
        root.focus()
    
    def handScroll(event):
        if event.delta < 0:
            handleZoomOut()
        else:
            handleZoomIn()

    def handleKeyPress(event):
        global shift
        global space
        global edge_value_buffer

        if (event.keysym) == "Shift_L":
            if shift:
                return
            shift = True

        elif graphic.hasEdgeSelected():
            if(event.keysym == "Return"):
                try:
                    handleAtribuatteValueToSelectedEdge(edge_value_buffer)
                except Exception:
                    showinfo("Aviso", "Valor inválido")
                edge_value_buffer = ""
                render()
                return
            edge_value_buffer += event.char

        if(event.keysym == "Return"):
            handlePaintNext()

        if(event.keysym == "BackSpace"):
            handleEraseSelected()

        if (event.keysym) == "space":
            if space:
                return
            space = True
        root.focus()

    def handleKeyRelease(event):
        global shift
        global space

        if (event.keysym) == "Shift_L":
            if not shift:
                return
            shift = False

        if (event.keysym) == "space":
            if not space:
                return
            space = False
        root.focus()

    def handDrag(event):
        global dragging
        global space
        global mouse_pos

        if not dragging:
            mouse_pos = [event.x,event.y]
        dragging = True

        if space:
            handleMotion(mouse_pos[0] - event.x,mouse_pos[1] - event.y)
            mouse_pos = [event.x,event.y]
        else:
            handleDrag(event.x,event.y)
        render()

    def stopDrag(event):
        global dragging
        dragging = False
        deselectDrag()

    def handPrim():
        try:
            handlePrim()
        except Exception:
            showinfo("Aviso", "Grafo desconectado")

    def handKruskal():
        try:
            handleKruskal()
        except Exception as e:
            showinfo("Aviso", "Grafo desconectado")

    root = Tk()
    root.title("Grafos")

    root.bind('<KeyPress>', handleKeyPress)
    root.bind('<KeyRelease>', handleKeyRelease)

    frm = ttk.Frame(root, padding=10)
    # frm.grid()
    frm.pack()
    inputes = ttk.Frame(frm)
    inputes.pack()

    ttk.Button(inputes, text="Resetar", width=20, command=handleReset).grid(column=2, row=0)

    def inputVertices():
        string_edges = simpledialog.askstring(title="Arestas",prompt="digite arestas aqui (v1,v2,peso):")
        if string_edges == None:
            return
        try:
            handleAddEdges(string_edges)
        except Exception:
            showinfo("Aviso", "Valor inválido")
        render()
        root.focus()

    def inputRandom():
        popupWin = Toplevel()
        popupWin.title("Criar grafo aleatório")

        vertices_num = 0
        completo = 0

        checkVariable = IntVar()
    
        txt = Label(popupWin,width=40,text="digite o número de vértices:")
        txt.pack()
        vertices_str = Entry(popupWin, width=20)
        vertices_str.pack()

        def handFunctionInfo():
            completo = int(checkVariable.get())
            vertices_num = vertices_str.get()
            if vertices_str == None:
                return
            try:
                vertices_num = int(vertices_num)
                handleRandom(vertices_num,completo)
            except Exception:
                showinfo("Aviso", "Valor inválido")
            popupWin.destroy()
            render()
            root.focus()

        checkBox = Checkbutton(popupWin, text="Grafo completo?", variable=checkVariable)
        checkBox.pack()

        btn3 = Button(popupWin, text="Gerar grafo", command=handFunctionInfo)
        btn3.pack()


    canvas = Canvas(frm, width=1000, height=550, background='gray90')
    # canvas.grid(column=0,row=1)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<B1-Motion>", handDrag) #mover
    canvas.bind("<ButtonRelease-1>", stopDrag) #mover
    canvas.bind("<Button-1>", handClick) #click
    canvas.bind("<MouseWheel>", handScroll)
    
    ttk.Button(inputes, text="Prim", width=20, command=handPrim).grid(column=1, row=0)
    ttk.Button(inputes, text="Kruskal", width=20, command=handKruskal).grid(column=0, row=0)

    ttk.Button(inputes, text="Adicionar", width=20, command=inputVertices).grid(column=3, row=0)
    ttk.Button(inputes, text="Grafo Aleatório", width=20, command=inputRandom).grid(column=4, row=0)
    
    root.mainloop()