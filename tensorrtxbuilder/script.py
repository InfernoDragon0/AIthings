import os
import subprocess

#used for in conjunction with the below PATHs
DIR_CURRENT = os.path.abspath(os.getcwd())
#used for generation of .wts from .pt
PATH_GENFILE = "/yolov5_v6_genfile/" 
#used for creating compiled yolo executable with .wts
PATH_YOLOV5 = "/yolov5/"
#used for inferencing with compiled yolo and .engine
PATH_YOLOV5INF = "/yolov5_inferenceonly/"

FILE_GENWTS = "gen_wts.py"
FILE_WTS = "atasv3.wts"

modelName = "" # to be filled input by user later
CMD_GENWTS = ["python", FILE_GENWTS, "-w", modelName, "-o", FILE_WTS]


#Script requires at least python 3 for the input
print("Starting tensorrtxbuilder...")
print("This script only works for s-sized models of yolov5 version 6")
print("Please ensure that your model is placed inside of yolov5_v6_genfile folder\n")

modelName = input("Enter Model name: ").strip()
PATH_MODEL = PATH_GENFILE + modelName

print("\nSearching for your model...\n")

if (os.path.exists(DIR_CURRENT + PATH_MODEL)):
    print("model found")
else:
    print("model/directory cannot be found, exiting...")
    exit()


# GENERATING .WTS FILE FROM MODEL
try:
    print("Attempting to generate the .wts file... please wait...")
    
    output = subprocess.run(CMD_GENWTS, capture_output=True, text=True, cwd=DIR_CURRENT+PATH_GENFILE)
    print(output.stdout)

except Exception as e:
    print(e)
    exit()

# GENERATING YOLO EXECUTABLE WITH CMAKE

