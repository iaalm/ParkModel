import matplotlib.pyplot as plt
from matplotlib import animation
import q
import random

park_tab = [[(1,300,0),(2,400,1)],
        [(0,300,0),(2,300,2),(5,350,3),(10,250,4)],
        [(0,400,1),(1,300,2),(3,300,5),(5,350,6)],
        [(2,300,5),(4,450,7),(5,500,8)],
        [(3,450,7),(6,500,9)],
        [(1,350,3),(2,350,6),(3,500,8),(7,550,10),(9,450,11)],
        [(4,500,9),(7,650,12)],
        [(5,550,10),(6,650,12),(8,400,13)],
        [(7,400,13),(9,450,14)],
        [(5,450,11),(8,450,14),(10,350,15)],
        [(9,350,15),(1,250,4)]
        ]

park_pos= ((70,0,0,0),(65,30,400,33*4),(75,32,30,5),(85,35,50,10),(100,100,30,10),(60,50,100,20),(60,85,50,10),(30,85,30,8),(0,50,30,6),(35,35,20,6),(50,20,50,8))

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
    ax.plot(*list(zip(*(park_pos[x][:2],park_pos[y][:2]))),linewidth=1)

def print_park_lines(ax):
    for i in range(11):
        for j in park_tab[i]:
            print_line(ax,i,j[0])

#an
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
print_park_points(ax)

def find_path(f,t):
    #print('ft:',f,t)
    queue = []
    s = set([f])
    now = []
    while True:
        for i in park_tab[f]:
            if i[0] == t:
                #print(now+[(i[2],i[0])])
                return now+[(i[2],i[0])]
            elif i[0] not in s:
                queue.append(now+[(i[2],i[0])])
                s.add(i[0])
        now = queue.pop(0)
        f = now[-1][1]
    
walk_speed = 20
total_t = 4*60*12
num_p = 0
in_p = [0] * total_t
out_p = 0
now_time = 0

for i in range(4*60*8):
    in_p[i] = int(random.uniform(0,10))

class place:
    def __init__(self,idx):
        self.idx = idx
        self.play = []
        self.queue = []
        self.time = int(park_pos[self.idx][3]/2)
    def enter(self, people):
        if self.idx != 0:
            self.queue.append(people)

    def step(self,time):
        self.time = self.time + time
        if self.time >= park_pos[self.idx][3]:
            for i in self.play: i.go()
            self.play = []
            for _ in range(min(park_pos[self.idx][2],len(self.queue))):
                    self.play.append(self.queue.pop(0))
            self.time = 0
    def draw(self):
        ax.text(park_pos[self.idx][0],park_pos[self.idx][1],str(len(self.play))+','+str(len(self.queue)),color='blue')
places = [place(i) for i in range(11)]

class way:
    def __init__(self,f,t,l):
        self.f = f
        self.t = t
        self.l = l
        self.fq = []
        self.tq = []
    def enter(self,people,t):
        if t == self.t:
            self.tq.append([people,self.l])
        elif t == self.f:
            self.fq.append([people,self.l])
        else:
            print('way error')
    def step(self,time):
        tq = self.tq
        fq = self.fq
        for i in range(len(tq)):
            if i >= len(tq):
                break
            dis = tq[i][1] - tq[i][0].speed * time
            if dis < 0:
                tq[i][0].reach(self.t)
                tq.pop(i)
            else:
                tq[i][1] = dis
        for i in range(len(fq)):
            if i >= len(fq):
                break
            dis = fq[i][1] - fq[i][0].speed * time
            if dis < 0:
                fq[i][0].reach(self.f)
                fq.pop(i)
            else:
                fq[i][1] = dis
    def draw(self):
        print_line(ax,self.f,self.t)
        x = (park_pos[self.f][0]+park_pos[self.t][0])/2
        y = (park_pos[self.f][1]+park_pos[self.t][1])/2
        ax.text(x,y,str(len(self.tq)+len(self.fq)))

ways = [None] * 16
for i in range(11):
    for j in park_tab[i]:
        if not ways[j[2]]:
            ways[j[2]] = way(i,j[0],j[1])
tour_time = [0,0]
class person:
    def __init__(self,speed):
        self.start_time = now_time
        self.pos = (0,0) #0 for place, 1 for way
        self.want = set(range(1,11))
        self.speed = speed
        self.target = []
    def reach(self, idx):
        if idx == 0:
            tour_time[0] = tour_time[0] + now_time - self.start_time
            tour_time[1] = tour_time[1] + 1
            print(now_time - self.start_time)
            global out_p
            out_p = out_p + 1
            return
        if len(self.target) == 0:
            play = len(places[idx].queue)
            wait = park_pos[idx][2] 
            p = play / (play + wait)
            r = random.random()
            if r < p:
                self.pos = (0,idx)
                self.go()
            else:
                self.want.remove(idx)
                self.pos = (0,idx)
                places[idx].enter(self)
        else:
            t = self.target.pop(0)
            self.pos = (1,t[0])
            ways[t[0]].enter(self,t[1])

    def go(self):
        r = park_tab[self.pos[1]].copy()
        random.shuffle(r)
        for idx in r:
            if idx[0] in self.want:
                #print(self.pos[1],'->',idx[0])
                self.pos = (1,idx[0])
                ways[idx[2]].enter(self,idx[0])
                break
        else:
            if len(self.want) > 0:
                tg = self.want.pop()
                self.want.add(tg)
            else:
                tg = 0
            self.target = find_path(self.pos[1],tg)
            t = self.target.pop(0)
            self.pos = (1,t[0])
            ways[t[0]].enter(self,t[1])


class animate:
    def __init__(self):
        self.pos = 0
        ax.clear()

    def __call__(self,i):
        global num_p
        global out_p
        global now_time
        ax.clear()
        t = i * 15
        now_time = t
        for _ in range(in_p[i]):places[0].play.append(person(walk_speed))
        num_p = num_p + in_p[i] - out_p
        print('%02d:%02d:%02d,in:%d,out:%d,num:%d'%(int(t/3600),int(t%3600/60),t%60,in_p[i],out_p,num_p))
        out_p = 0
        #for i in self.people:i.go()
        for i in ways:i.step(1)
        for i in places:i.step(1)
        for i in places:i.draw()
        for i in ways:i.draw()
        

anim = animation.FuncAnimation(fig, animate(),frames=4*60*12, interval=100) 
plt.show()

