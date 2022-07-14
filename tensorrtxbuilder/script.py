import os
import subprocess

#used for in conjunction with the below PATHs
DIR_CURRENT = os.path.abspath(os.getcwd()) # you should be in the dir with the script.py
#used for generation of .wts from .pt
PATH_GENFILE = "/yolov5_v6_genfile/" 
#used for creating compiled yolo executable with .wts
PATH_YOLOV5 = "/yolov5/"
PATH_YOLOV5_BUILD = "/yolov5/build/"
#used for inferencing with compiled yolo and .engine
PATH_YOLOV5INF = "/yolov5_inferenceonly/"
PATH_YOLOV5INF_BUILD = "/yolov5_inferenceonly/build/"

FILE_GENWTS = "gen_wts.py"
FILE_WTS = "atasv3.wts"
FILE_YOLOV5 = "yolov5"
FILE_ENGINE = "atasv3.engine"

CMD_MKBUILDFD = ["mkdir", "build"]
CMD_CPWTS = ["cp", DIR_CURRENT+PATH_GENFILE+FILE_WTS, DIR_CURRENT+PATH_YOLOV5INF_BUILD]
CMD_CMAKE = ["cmake", ".."]
CMD_MAKE = ["make"]
CMD_CRENGINE = ["sudo", "-S", "./"+FILE_YOLOV5, "-s", FILE_WTS, FILE_ENGINE, "s6"]
CMD_CPENGEXE = ["cp", FILE_YOLOV5, FILE_ENGINE, DIR_CURRENT+PATH_YOLOV5INF]

USER_PASS = str.encode("amarisjetson\n")

#Script requires at least python 3 for the input
print("Starting tensorrtxbuilder...")
print("This script only works for s-sized models of yolov5 version 6")
print("Please ensure that your model is placed inside of yolov5_v6_genfile folder\n")

modelName = input("Enter Model name: ").strip()
PATH_MODEL = PATH_GENFILE + modelName

print("\nSearching for your model...")

if (os.path.exists(DIR_CURRENT + PATH_MODEL)):
    print(modelName + " model found!\n")
else:
    print(modelName + " cannot be found, exiting...")
    exit()


# GENERATING .WTS FILE FROM MODEL
try:
    print("Attempting to generate the " + FILE_WTS + "... please wait...")

    if(os.path.exists(DIR_CURRENT + PATH_GENFILE + FILE_WTS)):
        print(FILE_WTS + " have been found, generation stopped\n")
    else:
        CMD_GENWTS= ["python", FILE_GENWTS, "-w", modelName, "-o", FILE_WTS]
        output = subprocess.run(CMD_GENWTS, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_GENFILE)
        if output.returncode == 0:
            print(FILE_WTS + " file generation successful!\n")
        else:
            print(FILE_WTS + " file generation error!\n")
            print("printing full output...")
            print(output)
            print("exiting...")
            exit()
except Exception as e:
    print(e)
    print("exiting...")
    exit()


# CREATING BUILD FOLDER IN YOLOV5_INFERENCEONLY FOLDER 
try:
    print("Attempting to create /build folder in /yolov5_inferenceonly folder... please wait...")
    if(os.path.exists(DIR_CURRENT + PATH_YOLOV5INF)):
        print(PATH_YOLOV5INF + " folder already exists, creation stopped\n")
    else:
        output = subprocess.run(CMD_MKBUILDFD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5INF)
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


# COPYING .WTS FILE OVER TO BUILD FOLDER IN /yolov5_inferenceonly
try:
    print("Copying " + FILE_WTS + " over to yolov5_inferenceonly/build...")
    output = subprocess.run(CMD_CPWTS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(output.returncode == 0):
        print(FILE_WTS + " have been copied over to yolov5_inferenceonly/build successfully!\n")
    else:
        print("copying " + FILE_WTS + " over to yolov5_inferenceonly/build error!")
        print("printing full output...")
        print(output)
        print("exiting...")
        exit()
except Exception as e:
    print(e)


# GENERATING MAKEFILES WITH CMAKE (of yolov5_inferenceonly)
try:
    print("Attempting to CMAKE required Buildfiles in yolov5/build folder... please wait...")
    output = subprocess.run(CMD_CMAKE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5INF)
    if(output.returncode == 0):
        print(output.stdout)
        print("Buildfiles created successfully!\n")
    else:
        print("CMAKE build error!")
        print("printing full output...")
        print(output)
        print("exiting...")
        exit()
except Exception as e:
    print(e)


# GENERATING YOLOV5 COMPILED EXE WITH MAKE
try:
    print("Attempting to Makefile to generate compiled yolo exe in yolov5_inferenceonly/build folder... please wait...")
    output = subprocess.run(CMD_MAKE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5INF)
    if(output.returncode == 0):
        print(output.stdout)
        print("Makefile compiled yolov5 exe sucessfully!\n")
    else:
        print("Makefile error!")
        print("printing full output...")
        print(output)
        print("exiting...")
        exit()
except Exception as e:
    print(e)


# GENERATING .ENGINE FILE FROM COMPILED YOLOV5 EXE AND .WTS
try:
    print("Attempting to create .engine file from " + FILE_WTS + " & " + FILE_YOLOV5 + " compiled exe... please wait...")
    pipe = subprocess.Popen(CMD_CRENGINE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5INF_BUILD)

    print("getting sudo access...")
    pipe.stdin.write(USER_PASS)
    pipeout, pipeerr = pipe.communicate()

    
    if(pipe.returncode == 0):
        print(FILE_ENGINE + " file created successfully!\n")
    else:
        print(FILE_ENGINE + " file generation error!")
        print("printing stderr...")
        print(pipeerr)
        print("printing stdout...")
        print(pipeout)
        print("exiting...")
        exit()
except Exception as e:
    print(e)


# COPYING FILES OVER TO /YOLOV5_INFERENCE ONLY FOLDER
# try:
#     print("Attempting to copy " + FILE_ENGINE + " and " + FILE_YOLOV5 + " over to /yolov5_inferenceonly")
#     output = subprocess.run(CMD_CPENGEXE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=DIR_CURRENT+PATH_YOLOV5_BUILD)
#     if(output.returncode == 0):
#         print(FILE_ENGINE + " and " + FILE_YOLOV5 + " have been copied over to /yolov5_inferenceonly sucessfully!\n")
#     else:
#         print("copying " + FILE_ENGINE + " and " + FILE_YOLOV5 + " over to /yolov5_inferenceonly error!")
#         print("printing full output...")
#         print(output)
#         print("exiting...")
#         exit()
# except Exception as e:
#     print(e)

print("Script executed successfully. Exiting...")