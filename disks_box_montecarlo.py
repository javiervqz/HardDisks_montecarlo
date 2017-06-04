import random, os, pylab, math, sys, time


output_dir = "movie_montecarlo_direct"

img = 0
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def snapshot(pos, colors):
    global img
    pylab.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)#where to put all subplot (axis in this case)
    pylab.gcf().set_size_inches(6,6) #set canvas' dimension
    pylab.axis([0, 1, 0, 1]) #from x - (0,1) and y - (0,1)
    #setup and specific figure (axis(gca), with marks from 0-1 on x and y) "more available setup"
    pylab.setp(pylab.gca(), xticks=[0, 1], yticks = [0,1])
    for (x, y), c in zip (pos, colors):
        circle = pylab.Circle((x, y), radius = sigma, fc = c)
        pylab.gca().add_patch(circle)
    pylab.savefig(os.path.join(output_dir, 'mc%d.png' % img), transparent=False)
    pylab.close()
    img += 1
def place(sigma, N, condition):
    while condition == True:
        position = [(random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))]
        for k in range (1, N):
            a = (random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))
            min_dis = min(math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2) for b in position)
            if min_dis < 2.0*sigma:
                condition = True
                break
            else:
                position.append(a)
                condition = False
    return position

N = int(raw_input("How many disks? \n"))


eta = 0.1
sigma = math.sqrt(eta/(float(N)*math.pi))
colors = ['r']*(N - N/2) + ['b']*(N - N/2)
runs = 100
print sigma
for run  in range(runs):
    condition = True
    position = place(sigma, N, condition)
    snapshot(position, colors)
    print "Calculating...", 100*run/float(runs)
    sys.stdout.write("\033[F") # Cursor up one line
print "\n"
print "animating..."
os.system("convert -delay 9 -dispose Background +page " + str(output_dir) + "/*.png -loop 0 " + str(output_dir) + "/animation.gif")
os.chdir(output_dir)
os.system("eog animation.gif")
print "Done."
