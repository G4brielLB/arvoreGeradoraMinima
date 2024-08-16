import math
import random

import algorithms

def getDistanceOf(x,y,x2,y2):
    dist = math.sqrt( (x2 - x)**2 + (y2 - y)**2 )
    return dist

def create_circle(x, y, r, canvas, fill='white'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill=fill,outline="")

class GrafoGui():
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.vertices_selecteds = []
        self.vertice_to_drag = None
        self.edge_selected = None
        self.vertices_id = 1
        self.next_index = 0
        self.to_paint = []
        self.zoom = 1
        self.total_pounds = 0
        self.has_pound = False

    def reset(self):
        self.vertices.clear()
        self.edges.clear()
        self.vertices_selecteds.clear()
        self.vertice_to_drag = None
        self.edge_selected = None
        self.vertices_id = 1
        self.next_index = 0
        self.to_paint.clear()
        self.total_pounds = 0
        self.has_pound = False

    def addVertice(self, vertice_x, vertice_y, vertice_id):
        try:
            existent_vertice = self.getVertice(vertice_id)
            self.addVertice(int(vertice_x/self.zoom), int(vertice_y/self.zoom), existent_vertice.id + 1)
        except Exception:
            new_vertice = Vertice(int(vertice_x/self.zoom),int(vertice_y/self.zoom),vertice_id,self.next_index)
            self.vertices_id += 1
            self.next_index += 1
            self.vertices.append(new_vertice)

    def appendVertice(self, vertice):
        self.vertices.append(vertice)

    def getVertice(self,vertice_id):
        for vertice in self.vertices:
            if vertice.id == vertice_id:
                return vertice
        raise Exception("nenhum vertice encontrado")

    def handleClick(self, click_x, click_y):
        for vertice in self.vertices:
            if getDistanceOf(click_x,click_y,vertice.rend_x,vertice.rend_y) < (vertice.radius + 5):
                vertice.handleSelect()

                if vertice.selected:
                    self.vertices_selecteds.append(vertice)
                elif vertice in self.vertices_selecteds:
                    self.vertices_selecteds.remove(vertice)
        
                self.checkSelecteds()
                return

        self.addVertice(click_x,click_y,self.vertices_id)

    def selectVerticeToDrag(self,x,y):
        for vertice in self.vertices:
            if getDistanceOf(x,y,vertice.rend_x,vertice.rend_y) < (vertice.radius + 10):
                self.vertice_to_drag = vertice
                return

    def deselectDrag(self):
        self.vertice_to_drag = None

    def handleDrag(self,click_x, click_y):
        try:
            self.vertice_to_drag.move(int(click_x/self.zoom),int(click_y/self.zoom))
        except Exception:
            pass

    def checkSelecteds(self):
        if len(self.vertices_selecteds) == 2:
            for edge in self.edges:
                if edge.vertices[0] == self.vertices_selecteds[0] and edge.vertices[1] == self.vertices_selecteds[1] or edge.vertices[0] == self.vertices_selecteds[1] and edge.vertices[1] == self.vertices_selecteds[0]:
                    self.selectEdge(edge)
                    self.unselectAll()
                    return

            new_edge = self.addEdge(self.vertices_selecteds[0],self.vertices_selecteds[1])
            self.selectEdge(new_edge)
            self.unselectAll()

    def addEdge(self, vertice_1, vertice_2):
        edge = self.getEdge(vertice_1,vertice_2)
        if edge != None:
            return edge
        new_edge = Edge(vertice_1,vertice_2)
        self.edges.append(new_edge)
        return new_edge

    def addEdges(self, edge_list):
        for edge in edge_list:
            from_vertice = None
            to_vertice = None

            try:
                from_vertice = self.getVertice(edge[0])
            except Exception:
                self.addVertice(random.randint(0,1000),random.randint(0,550),edge[0]) #canvas size
                from_vertice = self.getVertice(edge[0])
            try:
                to_vertice = self.getVertice(edge[1])
            except Exception:
                self.addVertice(random.randint(0,1000),random.randint(0,550),edge[1]) #canvas size
                to_vertice = self.getVertice(edge[1])

            existent_edge = self.getEdge(edge[0],edge[1])
            
            if existent_edge != None:
                existent_edge.setPound(edge[2])
                continue

            new_edge = self.addEdge(from_vertice,to_vertice)
            new_edge.setPound(edge[2])  #edge[2] = pound

    def selectEdge(self, edge):
        if self.edge_selected != None:
            self.edge_selected.handleSelect()
        edge.handleSelect()
        self.edge_selected = edge

    def atribuatteValueToSelectedEdge(self, value):
        self.edge_selected.setPound(value)
        self.edge_selected.handleSelect()
        self.edge_selected = None

    def hasEdgeSelected(self):
        return self.edge_selected != None

    def unselectAll(self):
        for vertice in self.vertices_selecteds:
            vertice.handleSelect()

        self.vertices_selecteds.clear()

    def move(self, offset_x, offset_y):
        for vertice in self.vertices:
            vertice.x -= offset_x
            vertice.y -= offset_y

    def render(self, canvas):
        canvas.delete("all")
        
        if self.has_pound:
            canvas.create_text(30,30,fill="black",font="Times 30 bold", text=str(self.total_pounds))

        for vertice in self.vertices:
            vertice.resize(self.zoom)
        for edge in self.edges:
            edge.render(canvas)
        for vertice in self.vertices:
            vertice.render(canvas)

    def getGraphSchemma(self):
        graph = [[] for _ in range(len(self.vertices))]
        for edge in self.edges:
            graph[edge.vertices[0].index].append((edge.vertices[1].index,edge.pound))
            graph[edge.vertices[1].index].append((edge.vertices[0].index,edge.pound))
        return graph

    def eraseSelected(self):
        if len(self.vertices_selecteds) == 0:
            return
        
        selected = self.vertices_selecteds[0]

        edges_ = []

        for edge in self.edges:
            if edge.vertices[0] != selected and edge.vertices[1] != selected:
                edges_.append(edge)

        self.edges = edges_

        self.vertices.remove(selected)
        self.vertices_selecteds.clear()

        for new_i in range(len(self.vertices)):
            self.vertices[new_i].index = new_i

        self.next_index = len(self.vertices)

    def getEdge(self, vertice_1, vertice_2):
        for edge in self.edges:
            if edge.vertices[0].id == vertice_1 and edge.vertices[1].id == vertice_2 or edge.vertices[0].id == vertice_2 and edge.vertices[1].id == vertice_1:
                return edge
        return None

    def getEdgeByIndex(self, vertice_1, vertice_2):
        for edge in self.edges:
            if edge.vertices[0].index == vertice_1 and edge.vertices[1].index == vertice_2 or edge.vertices[0].index == vertice_2 and edge.vertices[1].index == vertice_1:
                return edge
        return None

    def prim(self): 
        self.unpaintAll()
        try:
            edges_to_paint = algorithms.Prim(self.getGraphSchemma())
        except Exception as e:
            print(e)
            raise e
        for edge_to_paint in edges_to_paint:
            edge = self.getEdgeByIndex(edge_to_paint[0],edge_to_paint[1])
            if edge != None:
                self.to_paint.append(edge)
        self.has_pound = True

    def kruskal(self):
        self.unpaintAll()
        try:
            edges_to_paint = algorithms.Kruskal(self.getGraphSchemma())
        except Exception as e:
            raise e
        for edge_to_paint in edges_to_paint:
            edge = self.getEdgeByIndex(edge_to_paint[0],edge_to_paint[1])
            if edge != None:
                self.to_paint.append(edge)
        self.has_pound = True

    def paintNext(self):
        if len(self.to_paint) == 0:
            self.unpaintAll()
            return

        if self.to_paint[0].painted == True:
            self.to_paint.pop(0)
            self.paintNext()
            return

        self.to_paint[0].paint() #paint next edge
        self.total_pounds += self.to_paint[0].pound
        self.to_paint.pop(0)

    def unpaintAll(self):
        self.has_pound = False
        self.total_pounds = 0
        self.to_paint = []
        for edge in self.edges:
            edge.unpaint()

    def zoomIn(self):
        self.zoom += 0.01
    
    def zoomOut(self):
        if self.zoom - 0.1 >= 0.5:
            self.zoom -= 0.01

class Vertice():
    def __init__(self,x,y,vertice_id,index):
        self.x = x
        self.y = y
        self.rend_x = x
        self.rend_y = y
        self.id = vertice_id
        self.radius = 10
        self.selected = False
        self.index = index

    def render(self,canvas):
        if self.selected:
            create_circle(self.rend_x,self.rend_y,self.radius + 2,canvas,'black')
            create_circle(self.rend_x,self.rend_y,self.radius,canvas,'#01ff1c')
        else:
            create_circle(self.rend_x,self.rend_y,self.radius,canvas,'#00ffff')
        canvas.create_text(self.rend_x,self.rend_y,fill="black",font="Times 10 bold", text=str(self.id))

    def resize(self,zoom):
        self.rend_x = self.x * zoom
        self.rend_y = self.y * zoom


    def handleSelect(self):
        if self.selected:
            self.deselect()
        else:
            self.select()

    def move(self,to_x,to_y):
        self.x = to_x
        self.y = to_y

    def select(self):
        # print(self.id)
        self.selected = True

    def deselect(self):
        self.selected = False

class Edge():
    def __init__(self,vertice_from,vertice_to):
        self.vertices = [vertice_from,vertice_to]
        self.pound = 0
        self.selected = False
        self.painted = False

    def render(self, canvas):
        v_from = self.vertices[0]
        v_to = self.vertices[1]
        
        if self.selected:
            canvas.create_line(v_from.rend_x,v_from.rend_y,v_to.rend_x,v_to.rend_y, fill="red",width = 5)
        elif self.painted:
            canvas.create_line(v_from.rend_x,v_from.rend_y,v_to.rend_x,v_to.rend_y, fill="black",width = 10)
            canvas.create_line(v_from.rend_x,v_from.rend_y,v_to.rend_x,v_to.rend_y, fill="#00ffa1",width = 5)
        else:
            canvas.create_line(v_from.rend_x,v_from.rend_y,v_to.rend_x,v_to.rend_y, fill="black",width = 5)

        center_x = v_from.rend_x + (v_to.rend_x - v_from.rend_x)/2
        center_y =v_from.rend_y + (v_to.rend_y - v_from.rend_y)/2 - 20 # -20 = offset 
        canvas.create_text(center_x+1,center_y+1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x-1,center_y+1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x,center_y-1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x-1,center_y,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x+1,center_y,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x-1,center_y+1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x+1,center_y+1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x-1,center_y+1,fill="black",font="Times 18 bold", text=str(self.pound))
        canvas.create_text(center_x,center_y,fill="white",font="Times 16 ", text=str(self.pound))
    
    def setPound(self,value):
        if(value >= 0):
            self.pound = value
    
    def handleSelect(self):
        if self.selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def paint(self):
        self.painted = True
    
    def unpaint(self):
        self.painted = False