import matplotlib.pyplot as plt
from matplotlib import animation
import q
import random

park_tab = [[(1,300,1),(2,400,2)],
        [(0,300,1),(2,300,3),(5,350,4),(10,250,5)],
        [(0,400,2),(1,300,3),(3,300,6),(5,350,7)],
        [(2,300,6),(4,450,8),(5,500,9)],
        [(3,450,8),(6,500,10)],
        [(1,350,4),(2,350,7),(3,500,9),(7,550,11),(9,450,12)],
        [(4,500,10),(7,650,13)],
        [(5,550,11),(6,650,13),(8,400,14)],
        [(7,400,14),(9,450,15)],
        [(5,450,12),(8,450,15),(10,350,16)],
        [(9,350,16),(1,250,5)]
        ]

park_pos= ((70,0),(65,30),(75,32),(85,35),(100,100),(60,50),(60,85),(30,85),(0,50),(35,35),(50,20))

tab = [ [0] * 11 for _ in range(11)]
for i in range(11):
    for j in park_tab[i]:
        tab[i][j[0]] = j[1:]
'''
for i in range(11):
    for j in range(11):
        if tab[i][j] != tab[j][i]:
            print('error')
            break
        print(tab[i][j],end="\t")
    print('')
'''

def print_park_points(ax):
    pos = list(zip(*park_pos))
    ax.scatter(pos[0],pos[1])
def print_line(ax,x,y):
    ax.plot(*list(zip(*(park_pos[x],park_pos[y]))),linewidth=1)

def print_park_lines(ax):
    for i in range(11):
        for j in park_tab[i]:
            print_line(ax,i,j[0])

#an
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
print_park_points(ax)
class animate:
    def __init__(self):
        self.pos = 0
        self.tab = set([0])
        ax.clear()
        print_park_points(ax)

    def __call__(self,i):
        p = park_tab[self.pos]
        pos = random.choice(p)[0]
        print_line(ax,self.pos,pos)
        self.pos = pos


anim = animation.FuncAnimation(fig, animate(),frames=200, interval=200) 
plt.show()

