import grid
import random
import sys
import pyglet
from pyglet import clock


class GameOfLife(grid.Grid):
    def __init__(self,width,height,cell_size=20,fps=10):
        super(GameOfLife, self).__init__(width,height,cell_size,fps)
        self.init_run = True
        self.update_run = False
        self.init_fps = 100
        self.update_fps = fps
        self.cellcolor = (0.5, 0.5, 0.5, 0.2)

    def countAliveNeighbours(self,cells,i,j):
        neighbours = self.getNeighbours(cells,i,j)
        aliveNeighbours = 0
        for cell in neighbours:
            if cell.doDraw:
                aliveNeighbours +=1
        return aliveNeighbours
        
    def getNeighbours(self,cells,i,j):
        neighbours = []

        #left
        if j != 0:
            neighbours.append(cells[i][j-1])
        #top left
        if j != 0 and i != 0:
            neighbours.append(cells[i-1][j-1])

        #top
        if i != 0:
            neighbours.append(cells[i-1][j])

        #top right
        if i !=0 and j < self.columns-1:
            neighbours.append(cells[i-1][j+1])

        #right
        if j < self.columns-1:
            neighbours.append(cells[i][j+1])

        #bottom right
        if i < self.rows-1 and j < self.columns-1:
            neighbours.append(cells[i+1][j+1])

        #bottom
        if i < self.rows-1:
            neighbours.append(cells[i+1][j])

        #bottom left
        if i < self.rows-1 and j !=0:
            neighbours.append(cells[i+1][j-1])
        return neighbours


    def update_cells(self):
        new_cells = self.create_cells()
        for i in range(0,len(self.cells)):
            for j in range(0,len(self.cells[i])):
                aliveNeighbours = self.countAliveNeighbours(self.cells,i,j)
                #Initially all cells in new_cells are dead (doDraw = False)
                #If a cell has exactly 2 alive neighbours and was alive before,
                #it stays alive.
                if aliveNeighbours == 2:
                    new_cells[i][j].doDraw = self.cells[i][j].doDraw
                #If a cell has exactly 3 alive neighbours it is alive no matter what
                if aliveNeighbours == 3:
                    new_cells[i][j].doDraw = True
        self.cells = new_cells
    

    def main_loop(self):
        clock.set_fps_limit(self.init_fps)
        while not self.has_exit:
            self.dispatch_events()
            if self.update_run:
                self.update_cells()
            self.draw_grid()
            clock.tick()
            self.flip()
            
        

    def on_mouse_drag(self,x,y,dx,dy,button,modifiers):
        if button & pyglet.window.mouse.LEFT and self.init_run:
            self.activateCell(x,y)
    def on_mouse_press(self,x,y,button,modifiers):
        if button & pyglet.window.mouse.LEFT and self.init_run:
            self.activateCell(x,y)

    def activateCell(self,x,y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return
        #find column:
        col = x // self.cell_size
        row = y // self.cell_size
        self.cells[row][col].doDraw = not self.cells[row][col].doDraw
        
    def on_key_press(self,symbol,modifiers):
        if symbol == pyglet.window.key.SPACE:
            if modifiers & pyglet.window.key.MOD_CTRL:
                #Reset if ctrl+space is pressed
                self.cells = self.create_cells()
                self.switch_to_init()
            else:
                if self.init_run:
                    self.switch_to_update()
                else:
                    self.switch_to_init()
                


    def switch_to_init(self):
        self.update_run = False
        self.init_run = True
        clock.set_fps_limit(self.init_fps)

    def switch_to_update(self):
        self.update_run = True
        self.init_run = False
        clock.set_fps_limit(self.update_fps)

        
            
            


if __name__=="__main__":

    size = int(sys.argv[1])
    frames = int(sys.argv[2])
    h = GameOfLife(1200,800,cell_size=size,fps=frames)
    h.main_loop()
