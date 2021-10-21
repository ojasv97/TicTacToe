import pygame
import os

letterX = pygame.image.load(r'res\letterX.png')
letterO = pygame.image.load(r'res\letterO.png')



class Grid:
    def __init__(self):
        self.grid_lines = [((0,200),(600,200)),((0,400),(600,400)),
                            ((200,0),(200,600)),((400,0),(400,600))] 
    
        self.grid = [[0 for x in range(3)] for y in range(3)]

        self.switch_player = True

        self.search_dirs = [(1,1),(-1,-1),(1,-1),(-1,1),(0,-1),(0,1),(1,0),(-1,0)]

        self.game_over = False

    def clear_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                self.set_cell_value(i,j,0)


    def draw(self,surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200,200,200), line[0],line[1], 2)
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x,y) == 'X':
                    surface.blit(letterX ,(x*200, y*200))
                elif self.get_cell_value(x,y) == 'O':
                    surface.blit(letterO, (x*200, y*200))
                
    def print_grid(self):
        for row in self.grid:
            print(row)
    def get_cell_value(self,x,y):
        return self.grid[y][x]
    
    def set_cell_value(self,x,y,value):
        self.grid[y][x] = value

    def get_mouse(self,x,y,player):
        if(self.get_cell_value(x,y)==0):
            self.set_cell_value(x,y,player)
            self.check_grid(x,y,player)
    
    def is_within_bound(self,x,y):
        return x<3 and x>=0 and y<3 and y>=0
    
    def dfs(self,index, x, y, dir_x, dir_y, player, count, vis) -> bool:
        vis[x][y]=1
        count[index]+=1
        if(count[index]==3):
            return True
        next_x = x+dir_x
        next_y = y+dir_y
        if(self.is_within_bound(next_x,next_y) and vis[next_x][next_y]==0 and self.get_cell_value(next_x,next_y)==player):
            ans = self.dfs(index,next_x,next_y,dir_x,dir_y,player,count,vis)
        else:
            return False
        return ans

    def isDraw(self):
        available = 0
        for i in range(3):
            for j in range(3):
                if self.get_cell_value(i,j) == 0:
                    available+=1
        if available==0:
            self.game_over = True
            return True
        return False

    def check_grid(self,x,y,player):
        count = [1 for i in range(len(self.grid)**2)]
        ans = False
        for index,dirs in enumerate(self.search_dirs):
            vis = [[0 for i in range(3)]for j in range(3)]
            vis[x][y]=1
            dx = dirs[0]
            dy = dirs[1]
            next_x = x+dx
            next_y = y+dy
            if(self.is_within_bound(next_x,next_y) and vis[next_x][next_y]==0 and self.get_cell_value(next_x,next_y)==player):
                ans = ans | self.dfs(index,next_x,next_y,dx,dy,player,count,vis)
        for i in range(0,len(self.search_dirs),2):
            if count[i]+count[i+1]-1>=len(self.grid):
                ans = True
        if ans:
            self.game_over = True
            print(str(player)+" won")  
        elif self.isDraw():
            self.game_over = True
            print("Match Draw!")
            ans = True
        return ans

            
