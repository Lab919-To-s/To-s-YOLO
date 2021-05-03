import numpy as np

import os

np.random.seed(3)

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img


optInputPath = '/home/jeongni/First_floor/'


optOutputPath = '/home/jeongni/image_increase/'



optRescale = 1./255


optRotationRange=10


optWidthShiftRange=0.2


optHeightShiftRange=0.2


optShearRange=0.5


optZoomRange=[0.9,2.2]


optHorizontalFlip = True 


optVerticalFlip = True

optFillMode='nearest'


optNbrOfIncreasePerPic = 5


optNbrOfBatchPerPic = 5




train_datagen = ImageDataGenerator(rescale=optRescale, 

                                   rotation_range=optRotationRange,

                                   width_shift_range=optWidthShiftRange,

                                   height_shift_range=optHeightShiftRange,

                                   shear_range=optShearRange,

                                   zoom_range=optZoomRange,

                                   horizontal_flip=optHorizontalFlip,

                                   vertical_flip=optVerticalFlip,

                                   fill_mode=optFillMode)


def checkFoler(path):

    try:

        if not(os.path.isdir(path)):

            os.makedirs(os.path.join(path))

    except OSError as e:

        if e.errno != errno.EEXIST:                        

            raise            



def increaseImage(path ,folder):

    for index in range(0,optNbrOfIncreasePerPic):                                   

        img = load_img(path)

        x = img_to_array(img)

        x = x.reshape((1,) + x.shape)

        i = 0


        checkFoler(optOutputPath+folder)               

        print('index : ' + str(index))

        for batch in train_datagen.flow(x, batch_size=1, save_to_dir=optOutputPath+folder, save_prefix='tri', save_format='jpg'):

            i += 1

            print(folder + " " + str(i))

            if i >= optNbrOfBatchPerPic: 

                break



def generator(dirName):

    checkFoler(optOutputPath)

    try:

        fileNames = os.listdir(dirName)

        for fileName in fileNames:

            fullFileName = os.path.join(dirName, fileName)

            if os.path.isdir(fullFileName):                

                generator(fullFileName)

            else:


                ext = os.path.splitext(fullFileName)[-1]


                folderName = os.path.splitext(fullFileName)[0].split('/')[-2]

                if(ext == '.jpg'):                    

                    increaseImage(fullFileName, folderName)               

                    

    except PermissionError:

        pass



if __name__ == "__main__":

        generator(optInputPath)  
