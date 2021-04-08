import matplotlib.pyplot as plt
import pandas as pd
import argparse
import math 

parser = argparse.ArgumentParser()
parser.add_argument("-xt", type=float, default="575",  help="Xt (MPa)")
parser.add_argument("-yt", type=float, default="575",  help="Yt (MPa)")
parser.add_argument("-xc", type=float, default="600",  help="Xc (MPa)")
parser.add_argument("-yc", type=float, default="600",  help="Yc (MPa)")
parser.add_argument("-s",  type=int, default="100",  help="S (MPa)")
parser.add_argument('-n', type=str, default=None, help='pdf figure name')
args = parser.parse_args()


xt=args.xt
yt=args.yt
xc=args.xc
yc=args.yc
S=args.s
name=args.n
sigma=[]
sigma22=[]
sigma22_2=[]
fig, axs = plt.subplots(3, 1, figsize=(7, 15))


for i in range(S*2*2+1):
    if i==0:
        a=-S
        sigma.append(a)
    else:
        a=-S+i/2
        sigma.append(a)

#ec1 sigma12=0
a=1/(yt*yc)
for sigma11 in sigma:
    b=1/yt-1/yc-math.sqrt(1/(xt*xc*yt*yc))*sigma11
    c=math.pow(sigma11,2)/(xt*xc)+(1/xt-1/xc)*sigma11-1
    sigma22.append([(-b+math.sqrt(math.pow(b,2)-4*a*c))/(2*a),(-b-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)]) 
sigma_plot=pd.DataFrame(data=sigma22,columns=['R','-R'])
axs[0].plot(sigma,sigma_plot['R'], color='green', linewidth=1,label='FFT') 
axs[0].plot(sigma,sigma_plot['-R'], color='blue', linewidth=1,label='FFC')
axs[0].plot([min(sigma),min(sigma)],[min(sigma_plot['R']),min(sigma_plot['-R'])], color='red', linewidth=1,label='FMC')
axs[0].plot([max(sigma),max(sigma)],[max(sigma_plot['R']),max(sigma_plot['-R'])], color='red', linewidth=1,label='FMT')
axs[0].set_title('$\sigma_{22}$ vs $\sigma_{11}$ ($\sigma_{12}=0$)') 

#ec2 sigma11=0
a=1/(yt*yc)
b=(1/yt-1/yc)
for sigma12 in sigma:
    c=math.pow(sigma12/S,2)-1
    sigma22_2.append([(-b+math.sqrt(math.pow(b,2)-4*a*c))/(2*a),(-b-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)])
sigma_plot=pd.DataFrame(data=sigma22_2,columns=['R','-R'])
axs[1].plot(sigma,sigma_plot['R'], color='green', linewidth=1,label='FFT') 
axs[1].plot(sigma,sigma_plot['-R'], color='blue', linewidth=1,label='FFC')
axs[1].plot([min(sigma),min(sigma)],[min(sigma_plot['R']),max(sigma_plot['-R'])], color='red', linewidth=1,label='FMC')
axs[1].plot([max(sigma),max(sigma)],[min(sigma_plot['R']),max(sigma_plot['-R'])], color='red', linewidth=1,label='FMT')
axs[1].set_title('$\sigma_{22}$ vs $\sigma_{12}$ ($\sigma_{11}=0$)') 

#ec3 sigma22=0
sigma11=[]
a=1/(xt*xc)
b=(1/xt-1/xc)
for sigma12 in sigma:
    c=math.pow(sigma12/S,2)-1
    sigma11.append([(-b+math.sqrt(math.pow(b,2)-4*a*c))/(2*a),(-b-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)])
sigma_plot=pd.DataFrame(data=sigma11,columns=['R','-R'])
axs[2].plot(sigma,sigma_plot['R'], color='green', linewidth=1,label='FFT') 
axs[2].plot(sigma,sigma_plot['-R'], color='blue', linewidth=1,label='FFC')
axs[2].plot([min(sigma),min(sigma)],[min(sigma_plot['R']),max(sigma_plot['-R'])], color='red', linewidth=1,label='FMC')
axs[2].plot([max(sigma),max(sigma)],[min(sigma_plot['R']),max(sigma_plot['-R'])], color='red', linewidth=1,label='FMT')
axs[2].set_title('$\sigma_{11}$ vs $\sigma_{12}$ ($\sigma_{22}=0$)') 

for i in range(3):
    axs[i].spines['left'].set_position('zero')
    axs[i].spines['bottom'].set_position('zero')
    axs[i].spines['right'].set_visible(False)
    axs[i].spines['top'].set_visible(False)
    axs[i].xaxis.set_ticks_position('bottom')
    axs[i].yaxis.set_ticks_position('left')
    
del sigma11,a,b,c,sigma22_2,sigma12,i

fig.tight_layout(pad=3.0)
if name!=None:
    fig.savefig('{}.pdf'.format(name))
 
plt.show()

