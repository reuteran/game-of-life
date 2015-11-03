import pyglet
import random
from pyglet import clock
from pyglet import window




class Cell():
    def __init__(self,x,y, length, color=(1.0,1.0,1.0,1.0)):
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.doDraw = False

    def draw(self):
	pyglet.gl.glColor4f(*self.color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, 
        ('v2i', (self.x, self.y,
                 self.x, self.y + self.length,
                 self.x + self.length, self.y + self.length,
                 self.x + self.length, self.y)))


class Grid(pyglet.window.Window):
    def __init__(self, width, height, cell_size=20, fps=10):
        window.Window.__init__(self, width=width, height=height)
        
        if self.width % cell_size != 0 or self.height % cell_size != 0:
            print("FAIL SIZE!")
            self.cell_size = 20
        else:
            self.cell_size = cell_size

        self.rows = self.height/self.cell_size
        self.columns = self.width/self.cell_size
        self.gridcolor = (0.2,0.2,0.2,0.1)
        self.cellcolor = self.gridcolor
        self.cells = self.create_cells()

    def draw_cells(self):
        for row in self.cells:
            for cell in row:
                if cell.doDraw:
                    cell.draw()

    def draw_grid(self):
        self.clear()
        self.draw_cells()
        i = 0 
	pyglet.gl.glColor4f(*self.gridcolor)
        #Vertical lines
        while i < self.width:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i',(i, 0, i, self.height)))
            i = i + self.cell_size

        i = 0
        #Horizontal lines
        while i < self.height:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i',(0, i, self.width, i)))
            i = i + self.cell_size


    def create_cells(self):
        cells = [[0 for x in range(self.columns)] for x in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns): 
                cells[i][j] = Cell(j*self.cell_size ,i * self.cell_size, self.cell_size, self.cellcolor) 
        return cells

    def update_cells(self):
        pass

    def main_loop(self):
        clock.set_fps_limit(self.update_fps)
        while not self.has_exit:
            self.dispatch_events()
            self.update_cells()
            self.draw_grid()
            clock.tick()
            self.flip()


if __name__ == "__main__":
    h = Grid(1200,800,cell_size=10)
    h.main_loop()













