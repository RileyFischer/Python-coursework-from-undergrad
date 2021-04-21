import click
# project: p5
# submitter: Rjfischer
# partner: none

import csv
from zipfile import ZipFile 
from io import TextIOWrapper
import re
import pandas as pd
import socket, struct
import os
from collections import defaultdict
import geopandas
from matplotlib.animation import FuncAnimation
import operator
import json
import matplotlib.pyplot as plt
import math
import geopandas
import time
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row
            
def zip_csv_iter_ips(name):
    with ZipFile(name) as zf:
        with zf.open(name.split(".ZIP")[0]) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row

#funcion from https://stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa
def ip2long(ip):
    """
    Convert an IP string to long
    stackoverflow
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

@click.command()
@click.argument('zip1')
@click.argument('zip2')
@click.argument('mod', type=click.INT)
def sample(zip1, zip2, mod):
    with ZipFile(zip1) as zf:
        with zf.open(zip1.replace(".zip", ".csv")) as f:
            df = pd.read_csv(f)

    stride_list = []
    for i in range(len(df)):
        if i % mod == 0:
            stride_list.append(df.iloc[i])
    
    stride_df = pd.DataFrame(stride_list)
            
    with ZipFile(zip2, "w") as zf:
        with zf.open(zip2.replace(".zip", ".csv"), "w") as f:
            f.write(bytes(stride_df.to_csv(index=False), "utf-8"))


@click.command()
@click.argument('zip1')
@click.argument('zip2')
def country(zip1, zip2):
    reader = zip_csv_iter(zip1)
    header = next(reader)
    header.append('country')
    rows = list(reader)
    for row in rows:
        row.append(ip2long( re.sub(r"[a-z]+$", '000', row[0])))
    
    rows = sorted(rows, key=lambda x: x[-1])

    ips = zip_csv_iter_ips('IP2LOCATION-LITE-DB1.CSV.ZIP')
    ip_ranges = list(ips)

    ip_idx = 0
    for row in rows:
        temp = ip_idx
        for ip in ip_ranges[ip_idx:]:
            if int(ip[0]) <= int(row[-1]) <= int(ip[1]):
                row.pop()
                row.append(ip[3])
                ip_idx = temp
                break
            temp += 1
            
    with ZipFile(zip2, 'w') as zf:
        with zf.open(zip2.replace('.zip', '.csv'), 'w') as f:
            pd.DataFrame(rows, columns=header).to_csv(TextIOWrapper(f), index=False)

def geohour_helper(zipname, hour=None,top_5=False):
    reader = zip_csv_iter(zipname)
    header = next(reader)
    cidx = header.index("country")
    timeidx = header.index("time")
    counts = defaultdict(int)
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world=world[world["continent"]!="Antarctica"]
    w = world
    for row in reader:
        if hour != None:
            if hour != int(row[timeidx].split(":")[0]):
                continue
            counts[row[cidx]] += 1
    names=w.name.tolist()
    if top_5:
        top_five=dict(counts)
        top_five= sorted(counts.items(), key=operator.itemgetter(1),reverse=True)
        remove=[]
        for i in range(len(top_five)):
            if not top_five[i][0] in names:
                remove.append(i)
        remove.reverse()
        for i in remove:
            top_five.pop(i)
        with open('top_5_h{}.json'.format(hour), 'w') as f:
            json.dump(dict(top_five[:5]), f)
    c=[]
    for i in range(len(w)):
        c.append(0)
    w['count']=c
    for country, count in counts.items():
        if not country in names:
            continue
        else:
            w.loc[w['name']==country,'count']=math.sqrt(count)
    return(w)
@click.command()
@click.argument('zipname')
@click.argument('ax')
@click.argument('hour', type= click.INT)
def geohour(zipname, ax=None, hour=None):
    g=geohour_helper(zipname,hour,top_5=True)
    fig, av = plt.subplots(figsize=(20, 10))
    g.plot(ax=av,column="count",legend=True,cmap='OrRd')  
    plt.savefig(ax) 
    plt.close()    

@click.command()
@click.argument('zipname')
@click.argument('ax')
@click.argument('continent')

def geocontinent(zipname, ax=None, continent=None):
    reader = zip_csv_iter(zipname)
    header = next(reader)
    cidx = header.index("country")
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    timeidx = header.index("time")
    continent=continent[0].upper()+continent[1:]
    countries=world[world["continent"]==continent]["name"].tolist()
    counts = defaultdict(int)
    world=world[world["continent"]!="Antarctica"]
    w = world
    for row in reader:
        if  row[cidx] in countries:
            counts[(row[cidx])] += 1    
    names=w.name.tolist()
    c=[]
    for i in range(len(w)):
        c.append(0)
    w['count']=c
    for country, count in counts.items():
        # sometimes country names in IP dataset don't
        # match names in naturalearth_lowres -- skip those
        if country in names:
            w.loc[w['name']==country,'count']=math.sqrt(count)  
    fig, av = plt.subplots(figsize=(20, 10))
    w.plot(ax=av,column="count",legend=True,cmap='OrRd')      
    plt.savefig(ax)
    plt.close(fig)
    
@click.command()
@click.argument('zipname')
@click.argument('htmlname')


def video(zipname, htmlname=None):
    fig, ax = plt.subplots(figsize=(20, 10))
    def make_frame(frame_num):
        ax.clear()
        g=geohour_helper(zipname,frame_num,top_5=False)
        g.plot(ax=ax,column="count",cmap='OrRd')  
    anim=FuncAnimation(fig,make_frame,frames=24)
    with open(htmlname,"w")as f:
        f.write(anim.to_html5_video())
    plt.close(fig)

    
@click.group()
def commands():
    pass

commands.add_command(sample)
commands.add_command(country)
commands.add_command(geohour)
commands.add_command(geocontinent)
commands.add_command(video)

if __name__ == "__main__":
    commands()







