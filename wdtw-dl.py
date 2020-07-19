from PIL import Image
from html.parser import HTMLParser
import os
import urllib.request

image_root_path = "./images/"
site_url = "https://osricrpg.com/wizardawn/"

def main():
    html_filename = "body.html"
    print("Parse"+html_filename)
    wmhp =  WizardawnMapHTMLParser()
    with open(html_filename,'r') as f:
        while True:
            html_code = f.read()
            if (html_code == ''):
                break
            wmhp.feed(html_code)
    print("Download missing images in folder", image_root_path)
    download_all_images(wmhp.image_data_list)
    print("Produce result")
    assemble_all_images(wmhp.image_data_list)
    print("Done")

class WizardawnMapHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_in_body = False
        self.depth = 0                                   # 0 in body, increasing, only considers div with "z-index"
        self.node_coordinates = [(0,0)]                  # coordinates of depth relative to root, depth 0 is (0,0)
        self.image_data_list = []                                 # contains tuples like (path, realx, realy)
    def handle_starttag(self,tag,attrs):
        if (tag == "body"):
            self.is_in_body = True
            return
        if (not self.is_in_body):
            return
        if (tag == "div"):
            # check if there is z-index
            for attr in attrs:
                for i in range(0, len(attr), 2):
                    if (attr[i] == "style" and attr[i+1].find("z-index") > -1):
                        self.depth += 1
                        topbegin = attr[i+1].find("top:")+4
                        leftbegin = attr[i+1].find("left:")+5
                        topend = attr[i+1].find("px;",topbegin)
                        leftend = attr[i+1].find("px;", leftbegin)
                        y = int(attr[i+1][topbegin:topend])
                        x = int(attr[i+1][leftbegin:leftend])
                        self.node_coordinates.append((x,y))
        if (tag == "img" and self.depth > 0):
            for attr in attrs:
                for i in range(0, len(attr), 2):
                    if (attr[i] == "src"):
                        path = attr[i+1]
                realx = sum([self.node_coordinates[i][0] for i in range(self.depth+1)])
                realy = sum([self.node_coordinates[i][1] for i in range(self.depth+1)])
                self.image_data_list.append((path, realx,realy))
    def handle_endtag(self, tag):
        if (tag == "body"):
            self.is_in_body = False
            return
        if (not self.is_in_body):
            return
        if (tag == "div"):
            if (self.depth > 0):
                self.depth -= 1
                self.node_coordinates.pop()

def download_all_images(image_data_list):
    if not os.path.isdir(image_root_path):
        os.mkdir(image_root_path)
    for image_data in image_data_list:
        path = image_data[0]
        if os.path.isfile(image_root_path+path):
            continue
        # check if folder exist
        index = path.rfind('/')
        os.makedirs(image_root_path+path[:index], exist_ok=True)
        urllib.request.urlretrieve(site_url+path, image_root_path+path)

def assemble_all_images(image_data_list):
    images = dict()
    size = [0,0]
    # Size of result
    for image_data in image_data_list:
        if not image_data[0] in images:
            new_image = Image.open(image_root_path+image_data[0])
            images[image_data[0]] = new_image
        if (size[0] < image_data[1] + new_image.size[0]):
            size[0] = image_data[1] + new_image.size[0]
        if (size[1] < image_data[2] + new_image.size[1]):
            size[1] = image_data[2] + new_image.size[1]
    result = Image.new('RGBA', size, (0,0,0,0))
    print(size)
    for image_data in image_data_list:
        result.alpha_composite(images[image_data[0]], (image_data[1],image_data[2]))
    result.save(image_root_path+"merged.png", 'PNG')

if __name__=="__main__":
    main()
