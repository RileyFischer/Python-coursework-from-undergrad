# project: p6
# submitter: Rjfischer
# partner: none

import sqlite3
from sklearn.linear_model import LinearRegression
from re import search
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
from zipfile import ZipFile 
from io import TextIOWrapper
import numpy as np

def open(name):
    return Connection(name)

class Connection:
    def __init__(self, name):
        self.db = sqlite3.connect(name+".db")
        self.zf = ZipFile(name+".zip")
        self.samples = self._get_samples()
        self.cities = self._get_cities()
        
    def __enter__(self):
        return(self)
    
    def __exit__(self,type,value,traceback):
        return(self.db.close())

    def close(self):
        self.db.close()
        
    def _color_map(self):
        use_cmap = np.zeros(shape=(256,4))
        use_cmap[:,-1] = 1
        uses = np.array([
            [0, 0.00000000000, 0.00000000000, 0.00000000000],
            [11, 0.27843137255, 0.41960784314, 0.62745098039],
            [12, 0.81960784314, 0.86666666667, 0.97647058824],
            [21, 0.86666666667, 0.78823529412, 0.78823529412],
            [22, 0.84705882353, 0.57647058824, 0.50980392157],
            [23, 0.92941176471, 0.00000000000, 0.00000000000],
            [24, 0.66666666667, 0.00000000000, 0.00000000000],
            [31, 0.69803921569, 0.67843137255, 0.63921568628],
            [41, 0.40784313726, 0.66666666667, 0.38823529412],
            [42, 0.10980392157, 0.38823529412, 0.18823529412],
            [43, 0.70980392157, 0.78823529412, 0.55686274510],
            [51, 0.64705882353, 0.54901960784, 0.18823529412],
            [52, 0.80000000000, 0.72941176471, 0.48627450980],
            [71, 0.88627450980, 0.88627450980, 0.75686274510],
            [72, 0.78823529412, 0.78823529412, 0.46666666667],
            [73, 0.60000000000, 0.75686274510, 0.27843137255],
            [74, 0.46666666667, 0.67843137255, 0.57647058824],
            [81, 0.85882352941, 0.84705882353, 0.23921568628],
            [82, 0.66666666667, 0.43921568628, 0.15686274510],
            [90, 0.72941176471, 0.84705882353, 0.91764705882],
            [95, 0.43921568628, 0.63921568628, 0.72941176471],
        ])
        for row in uses:
            use_cmap[int(row[0]),:-1] = row[1:]
        return ListedColormap(use_cmap)
    
    def _get_samples(self):
        df = pd.read_sql("""
                SELECT * FROM places 
                INNER JOIN images i on places.place_id = i.place_id
        """, self.db)
        return df[df.name.str.contains("samp", regex=True)]
    
    def _get_cities(self):
        df = pd.read_sql("""SELECT * FROM places 
                    INNER JOIN images i on places.place_id = i.place_id""", self.db)
        return df[df.name.str.contains("^((?!samp).)*$", regex=True)]
    
    def _abline(self, slope, intercept):
        """Plot a line from slope and intercept"""
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, '--')
        
    def _find_percent_use(self, use_code):
        """helper function for lat_regression"""
        lat_percent = {}
        for i, r in self.samples.iterrows(): # all samp images
            samp_image = r['image']
            lat = r['lat']
            n = self.image_load(samp_image)
            per = (n == use_code).astype(int).mean() * 100
            lat_percent[lat] = per
            
        data = pd.DataFrame(list(lat_percent.items()), columns=['x', 'y'])
        lr = LinearRegression()
        lr.fit(data[['x']], data['y'])
        slope = lr.coef_[0]
        intercept = lr.intercept_
        return (slope, intercept) , data
    
    def _predict(self, data, year):
        pred = {}
        for d in data:
            for key, val in d.items():
                p = val[0]*year + val[1]
                if key in pred:
                    pred[key] += p
                else:
                    pred[key] = p

        key_max = max(pred, key=pred.get)
        return (key_max, pred[key_max])
        
    def list_images(self):
        df = pd.read_sql("""
                    SELECT image FROM sqlite_master 
                    INNER JOIN images 
                    WHERE tbl_name='images'
                    """, self.db)
        return sorted(df["image"].values.tolist())
    
    def image_year(self, image):
        year = pd.read_sql('SELECT year FROM images WHERE image == "{}"'.format(image), self.db)
        return int(year['year'].values)
    
    def image_name(self, image):
        name = pd.read_sql("""SELECT name FROM images i
                        INNER JOIN places p 
                        WHERE i.place_id == p.place_id and image == '{}'
            """.format(image), self.db)
        return name.iloc[0]['name']
    
    def image_load(self, image):
        n = np.load(self.zf.filename)
        return n[image]
    
    def plot_img(self, image, ax=None):
        year = self.image_year(image)
        city = self.image_name(image)
        city_array = self.image_load(image)
        ax = plt.imshow(city_array, cmap=self._color_map(), vmin=0, vmax=255)
        plt.title(f"{city}: {year}")
        return ax
          
    def lat_regression(self, use_code, ax=None):
        coef, data = self._find_percent_use(use_code)
        if ax is None:
            return coef[0], coef[1]
        else:
            data.plot.scatter(x = "x", y = "y", color="black", ax=ax)
            self._abline(coef[0], coef[1])
            return coef[0], coef[1]
            
    def city_regression(self, list_code, year):
        city_names = list(self.cities['name'].values)
        city_set = set(city_names)
        city_regr_list = []
        for code in list_code:
            city_regr = {}
            for city in city_set:
                temp = {}
                for i, r in self.cities.iterrows():
                    if r['name'] == city:
                        samp_image = r['image']
                        y = r['year']
                        n = self.image_load(samp_image)
                        per = (n == code).astype(int).mean() * 100
                        temp[y] = per

                data = pd.DataFrame(list(temp.items()), columns=['x', 'y'])
                lr = LinearRegression()
                lr.fit(data[['x']], data['y'])
                slope = lr.coef_[0]
                intercept = lr.intercept_
                city_regr[city] = (slope, intercept)
                
            city_regr_list.append(city_regr)
        
        return self._predict(city_regr_list, year)
    
    def city_plot(self,city_name):
        use_codes = {11:'Open Water', 12: 'Perennial Ice/Snow', 
            21: "Developed, Open Space", 22: "Developed, Low Intensity",
            23: "Developed, Medium Intensity", 24: "Developed, High Intensity",
            31: "Barren Land (Rock/Sand/Clay)", 41: "Deciduous Forest",
            42: "Evergreen Forest", 43: "Mixed Forest",
            51: "Dwarf Scrub (Alaska)", 52: "Shrub/Scrub",
            71: "Grassland/Herbaceous", 72: "Sedge/Herbaceous (Alaska)",
            73: "Lichens (Alaska)", 74: "Moss (Alaska)",
            81: "Pasture/Hay", 82: "Cultivated Crops",
            90: "Woody Wetlands", 95: "Emergent Herbaceous Wetlands"
            }
        fig, ax = plt.subplots()
        codes=[]
        rs=[]
        for i,r in self.cities.iterrows():
            if r['name'] == city_name:
                rs.append(r)
        for code in use_codes:
            temp={}
            x_vals=[]
            y_vals=[]
            for r in rs:
                samp_image = r['image']
                y = r['year']
                n = self.image_load(samp_image)
                per = (n == code).astype(int).mean() * 100
                y_vals.append(per)
                x_vals.append(y)
            if(sum(y_vals))==0:
                pass
            else:
                codes.append(code)
                ax.plot(x_vals,y_vals,label=use_codes[code])
        ax.set_ylabel('Percent')   
        ax.set_title(city_name)  
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
        return ax
    def animate(self,city):
        rs=[]
        for i,r in self.cities.iterrows():
            if r['name'] == "kenosha":
                rs.append(r)
        fig,ax=plt.subplots()
        def make_frame(frame_num):
            ax.clear()
            self.plot_img(rs[frame_num]["image"])
        anim=FuncAnimation(fig,make_frame,frames=7)
        plt.close(fig)
        return anim