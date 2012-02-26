import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

ax1 = None
ax2 = None

#### Plot time series (or just about anything) ####
# Function returns reference to the plotted line
# xarr, yarr are the x and y -axis arrays.
#       xarr is optional. if not passed, it uses the index of the yarr points as the x-axis 
# ptype can be "plot" or "scatter"
# cnt - integer between 0 and 11, to choose the line and marker style.
#       this is optional. use if you're using multiple lines in same plot
# color - optional. black by default.
# mfreq - optional. frequency of markers. default is 10 per plot
# axis - optional. 'ax1' or 'ax2'. Use only if using multiple y-axis * currently not supported *
# linewidth - optional. 0.5 by default
#### 

def plot_ts(xarr=None,yarr=None,yerr=None,ptype='plot',cnt=0,color=False,mfreq=0,axis='ax1',linewidth=0.5,markersize=25):
  colors = ['r','b','g','y','k']
  if axis == 'ax2':
    ax = ax2
  else:
    ax = ax1
  ax
  ls = ['-','-.','--',':','-','--','-.',':','-','--','-.',':']
  marker = ['o','*','^','s','d','3','d','o','*','^','1','4']
  if mfreq == 0:
    mfreq = len(yarr)
  markerfreq = len(yarr)/mfreq  
  #print markerfreq
  if ptype == 'plot':
    if xarr == None:
        if color == False:
          p = ax.plot(yarr,color='k',linestyle=ls[cnt],marker=marker[cnt],markevery=markerfreq)[0]
        else:
          p = ax.plot(yarr,color=colors[cnt],linestyle=ls[cnt],linewidth=3)[0]
    else:
        if yerr == None:
          if color == False:
            p = ax.plot(xarr,yarr,color='k',linestyle=ls[cnt],marker=marker[cnt],markevery=markerfreq)[0]
          else:
            p = ax.plot(xarr,yarr,color=colors[cnt],linestyle=ls[cnt],linewidth=3)[0]
        else:
          if color == False:
            p = ax.errorbar(xarr,yarr,yerr=yerr,color='k',linestyle=ls[cnt],marker=marker[cnt])[0]
          else:
            p = ax.errorbar(xarr,yarr,yerr=yerr,colors=color[cnt])[0]
  if ptype == 'scatter':
    marker = ['x','o','d','+']
    if color == False:
      p = ax.scatter(xarr,yarr,marker=marker[cnt],color='k',linewidth=linewidth,s=markersize)
    else:
      p = ax.scatter(xarr,yarr,marker=marker[cnt],color=colors[cnt],linewidth=linewidth,s=markersize)
  return p 

#### To plot CDFs.
#    Same as plot_ts, except xarr is not optional

def plot_cdf(xarr=[],yarr=[],file=None,cnt=0,color=False,axis='ax1'):
  if axis == 'ax2':
    ax = ax2
  else:
    ax = ax1
  ls = ['-','--','-.',':','-','--','-.',':','-','--','-.',':']
  marker = ['o','*','^','1','2','3','4','o','*','^','1','^']
  colors = ['r','b','g','y','k']

  markerfreq = len(yarr)/10  
  if color == False:
    p = ax.plot(xarr,yarr,color='k',linestyle=ls[cnt],marker=marker[cnt],markevery=markerfreq)[0]
  else:
    p = ax.plot(xarr,yarr,color=colors[cnt],linewidth=3,linestyle=ls[cnt])[0]
  del xarr
  del yarr
  return p 

def plot_hist(yarr,width,yerr=None,col=1,cnt=0,color=False):
  htch = ['/','**','..','++','x','o','\\','||','oo','//']
  colors = ['r','b','g','y','k']
  #if width == None:
  #  width = (0.8*ncol)/len(yarr)
  p = []
  y = yarr
  x = np.arange(0,len(y))
  left = np.array(x)*col + cnt*width 
  #print y,cnt,left
  if color == False:
    p = plt.bar(left,y,width,hatch=htch[cnt],color='w',ecolor='k')
  else:
    p = plt.bar(left,y,width,color=colors[cnt])
  if yerr != None:
    yerr = np.array(yerr)/2
    plt.errorbar(left+width/2,np.array(yarr)+np.array(yerr),fmt=None,yerr=yerr,ecolor='k')
    
  return p 

def plot_box(arr,notch=0,sym='+',vert=1,whis=1.5,positions=None,widths=0.75):
  bp = plt.boxplot(arr,notch=notch,sym=sym,vert=vert,whis=whis,positions=positions)
  return bp

#### Add legends, save file
# fn - filename to save the figure
# leg - optional; array of strings in the keybox
# p - optional; array of references to the plot lines, corresponding the leg array
# loc - optional; upper-left by default
# axis - optional; same as in plot_ts * currently not supported *

def legend(leg=None,p=None,fn=None,loc='best',axis='ax1',fs='large',ncol=1,clear=True):
  if axis == 'ax2':
    ax = ax2
  else:
    ax = ax1
  if leg != None and p != None:
    ax.legend(p,leg,loc=loc,prop=dict(size=fs),ncol=ncol)
  if fn != None:
    plt.savefig(fn)
  if clear == True:
    plt.clf()

#### Set figure size, create axes
# l - length of canvas
# h - height
# axes - optional; if you want to move around the axes, see example file
####
 
def figsize(l,h,axes=None):
  fig = plt.figure(num=1,figsize=(l,h))
  global ax1
  global ax2
  if axes != None:
    ax1 = plt.axes(axes)
    #ax2 = plt.twinx()
  if axes == None:
    ax1 = plt.subplot(111)
    #print 'ax2'
    #ax2 = plt.twinx()
    ax1 = plt.subplot(111,axes=axes)

#### Add info to figure
# All parameters are optional
# log - 'logx','logy',logxy'
# xlabel - string
# ylabel - string
# xlim - 2 member int array with xmin, xmax
# ylim - 2 member int array with ymin, ymax
# xticks - array with 1 or 2 arrays as members. If 2 arrays, array 0 is treated
# 		   as the x-axis locations, and array 1 as the xticks text
#		   If single array, it is treated as the xtixks text, and the locations are
#		   the indices of the corresponding array value
# yticks - same as for xticks
# hline - location of horizontal line. single int/float value
# vline - location of vertical line. single int/float value
# title - title of the plot
# axis - Use if multiple axes * Currently not supported
# grid - 'True','False','x', or 'y'. default - true
# fn - if given, it will save and ***clear the current figure***

def figstuff(log=None,xlabel=None,ylabel=None,xlim=None,ylim=None,xticks=None,yticks=None,hline=None,vline=None,title=None,fn=None,axis='ax1',grid=True):
  if axis == 'ax2':
    ax = ax2
  else:
    ax = ax1

  if log in ['logx','logxy']:
    ax.set_xscale('log')
  if log in ['logy','logxy']:
    ax.set_yscale('log')
   
  if xlabel == None:
    xlabel = ''
  if ylabel == None:
    ylabel = ''
  if title == None:
    title = ''

  if xticks != None:
    if len(xticks) == 1:
      #print xticks
      ax.set_xticks(xticks[0])
      ax.set_xticklabels(xticks[0],size='large')
    else:
      ax.set_xticks(xticks[0])
      ax.set_xticklabels(xticks[1],size='large')
  #else:
  #  plt.xticks([])
  if yticks != None:
    if len(yticks) == 1:
      ax.set_yticks(yticks[0])
      ax.set_yticklabels(yticks[0],size='large')
    else:
      ax.set_yticks(yticks[0])
      ax.set_yticklabels(yticks[1],size='large')

  if xlim != None:
    if xlim[0] != None:
      ax.set_xlim(xmin=xlim[0])
    if xlim[1] != None:
      ax.set_xlim(xmax=xlim[1])

  if ylim != None:
    if ylim[0] == None:
      ax.set_ylim(ymax=ylim[1])
    elif ylim[1] == None:
      ax.set_ylim(ymin=ylim[0])
    else:
      ax.set_ylim(ymin=ylim[0],ymax=ylim[1])
    
  if hline != None:
    ax.axhline(y=hline)
  if vline != None:
    ax.axvline(x=vline)

  #ax.ylim(ymin=10,ymax=200)
  ax.set_xlabel(xlabel,size='large')
  ax.set_ylabel(ylabel,size='large')
  if grid == True or grid == False:
    ax.grid(grid)
  if grid == "x":
    ax.xaxis.grid(True)
  if grid == "y":
    ax.yaxis.grid(True)
  plt.title(title)
  if fn != None:
    plt.savefig(fn)
    plt.clf()

#### Annotate plot with text
# x - x values of the points where the arrows end
# y - y values of the points where the arrows end
# xt - x values of the points where the arrows begin
# yt - y values of the points where the arrows begin
# t - the text of the annotation
# All the above are arrays, and should have equal length

def annotate(x,y,xt,yt,t):
  for i in range(0,len(x)):
    ax1.annotate(t[i],(x[i],y[i]),xytext=(xt[i],yt[i]),arrowprops=dict(arrowstyle='->')) 

def text(xarr,yarr,tarr,fontsize=12):
  for i in range(0,len(xarr)):
    ax1.text(xarr[i],yarr[i],tarr[i],fontsize=fontsize,horizontalalignment='center')
