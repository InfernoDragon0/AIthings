import os
import subprocess

#used for in conjunction with the below PATHs
DIR_CURRENT = os.path.abspath(os.getcwd()) # you should be in the dir with the script.py
#used for generation of .wts from .pt
PATH_GENFILE = "/yolov5_v6_genfile/" 
#used for creating compiled yolo executable with .wts
PATH_YOLOV5 = "/yolov5/"
#used for inferencing with compiled yolo and .engine
PATH_YOLOV5INF = "/yolov5_inferenceonly/"

FILE_GENWTS = "gen_wts.py"
FILE_WTS = "atasv3.wts"

CMD_MKBUILDFD = ["mkdir", "build"]

#Script requires at least python 3 for the input
print("Starting tensorrtxbuilder...")
print("This script only works for s-sized models of yolov5 version 6")
print("Please ensure that your model is placed inside of yolov5_v6_genfile folder\n")

modelName = input("Enter Model name: ").strip()
PATH_MODEL = PATH_GENFILE + modelName

print("\nSearching for your model...")

if (os.path.exists(DIR_CURRENT + PATH_MODEL)):
    print("model found!\n")
else:
    print("model/directory cannot be found, exiting...")
    exit()


# GENERATING .WTS FILE FROM MODEL
try:
    print("Attempting to generate the .wts file... please wait...")

    if(os.path.exists(DIR_CURRENT + PATH_GENFILE + FILE_WTS)):
        print(FILE_WTS + " have been found, generation stopped")
    else:
        CMD_GENWTS= ["python", FILE_GENWTS, "-w", modelName, "-o", FILE_WTS]
        output = subprocess.run(CMD_GENWTS, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_GENFILE)
        if output.returncode == 0:
            print(".wts file generation successful!\n")
        else:
            print(".wts file generation error!\n")
            print("printing full output...")
            print(output)
            print("exiting...")
            exit()

except Exception as e:
    print(e)
    print("exiting...")
    exit()

# CREATING BUILD FOLDER IN YOLOV5 FOLDER 
try:
    print("Creating /build folder in yolov5 folder...")
    output = subprocess.run(CMD_MKBUILDFD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5)
    if (output.returncode == 0):
        print("build folder created successfully!\n")
    else:
            print("build folder creation error!")
            print("printing full output...")
            print(output)
            print("exiting...")
            exit()
except Exception as e:
    print(e)

# COPYING .WTS FILE OVER TO BUILD FOLDER IN YOLOV5

# GENERATING YOLO EXECUTABLE WITH CMAKE

