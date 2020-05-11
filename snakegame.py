import random

import pygame




class cube(object):
    rows =20
    width =500
    def __init__(self, start, dirnx=1,dirny=0,color=(255,0,0)):
        self.pos=start
        self.dirnx=1
        self.dirny=0
        self.color=color




    def move(self,dirnx,dirny):
        self.dirnx=dirnx
        self.dirny=dirny
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)


    def draw(self, surface, eyes=False):
        global rows,width
        dis = self.width//self.rows

        i=self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            center= dis//2
            radius =3
            circlemiddle = (i*dis+center-radius, j*dis+8)
            circlemiddle2 = (i*dis+center-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circlemiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circlemiddle2, radius)


class snake(object):
    body =[]
    turns={}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def reset(self,pos):
        s.head=cube(pos)
        s.body=[]
        s.turns={}
        s.body.append(s.head)
        self.dirnx=1
        self.dirny=0
        


    def addCube(self):
        tail = self.body[-1]
        dirnx = tail.dirnx
        dirny = tail.dirny

        #if you are going right
        if dirnx == 1 and dirny == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            #if you are going left
        elif dirnx == -1 and dirny == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dirnx == 0 and dirny == -1:
            #if you are going up
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
            #if you are going down
        elif dirnx == 0 and dirny == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))

        self.body[-1].dirnx=dirnx
        self.body[-1].dirny=dirny



    def draw(self,surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface,True)
            else:
                c.draw(surface)


    def move(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx=-1
                    self.dirny=0
                    self.turns[self.head.pos[:]] =[self.dirnx,self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    #[:] creates a copy (local version)


        #body has cubes turns has positions dictionary where it has to turn
        for i, c in enumerate(self.body):
            p = c.pos[:] #c is the cube in the body
            # if the cube piece is in the pos where it has to turn
            if p in self.turns:
                turn = self.turns[p] #that positional turn
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #condition for new position encountered
                if c.dirnx==-1 and c.pos[0]<=0:c.pos=(c.rows-1,c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows: c.pos = (0, c.pos[1])
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                elif c.dirny == 1 and c.pos[1] >= c.rows: c.pos = (c.pos[0], 0)
                else: c.move(c.dirnx, c.dirny)






def drawGrid(width,rows,surface):
    sizebetween  = width // rows

    x=0
    y=0
    for i in range(rows):
        x=x + sizebetween
        y=y + sizebetween
        pygame.draw.line(surface,(255,255,255),(x,0),(x,width))
        pygame.draw.line(surface,(255,255,255),(0,y),(width,y))



def redrawWindow(surface):
    global rows,width,s,snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()


def randomsnack(rows,snake):
    position=snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)


        #passing position as z
        if len(list(filter(lambda z:z.pos ==(x,y),position)))>0:
            continue
        else:
            break
    return (x,y)



def main():
    global width,height,rows,s,snack
    pygame.init()
    width= 500
    height= 500
    rows = 20
    win= pygame.display.set_mode((width,height))

    s = snake((255, 0, 0), (10, 10))
    snack =cube(randomsnack(rows,snake),0,0,(0,255,0))
    flag = True
    clock=pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomsnack(rows, snake), 0, 0, (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #if two body cubes occupy same position
                print("score is ",len(s.body))
                s.reset((10,10))



        redrawWindow(win)




        pass


main()