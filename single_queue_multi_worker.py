from multiprocessing import Process, Manager
import argparse
from pathlib import Path
from rich.console import Console
import cv2
from time import sleep, perf_counter


arg = argparse.ArgumentParser(description="single queueu multi worker")
arg.add_argument('-d', '--dir', default="C:/Users/Talha/Downloads/dummy_images", help='path to the dir having images')
parser = arg.parse_args()


def read_folder(que, lck):
    
    
        while True:
            if que.qsize() > 0:
                    
                with lck:
                    folder = que.get()
                
                if folder == "DONE":
                    break
                else:
                    Console().print(f"taken ---> {folder} folder")  
                    for img in folder.iterdir():
                        img = cv2.imread(img.as_posix())
                        
                        sleep(1)
            else:
                break



def send2queue(f, q):

    for k in f:
        q.put(k)
    q.put("DONE")    



if __name__=='__main__':
    folders = [ k for k in Path(parser.dir).iterdir() if k.is_dir() ]
    m = Manager()
    folder_q = m.Queue()
    lock =  m.Lock()


    Console().rule(title="[color(128)]making a process", style="bold green", characters="+")
    p1 = Process(target=read_folder, args=(folder_q, lock))
    p1.daemon = True
    p1.start()
    
    p2 = Process(target=read_folder, args=(folder_q, lock))
    p2.daemon = True
    p2.start()
    


    t0 = perf_counter()
    send2queue(folders, folder_q)


    p1.join()
    p2.join()
    
    t1 = perf_counter()
    Console().rule(title=f"took {t1-t0} seconds .. . .")