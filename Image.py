import pytest
import random


class Image:
    GREATER = 0
    EQUAL = 1
    LESS = 2

    def __init__(self, shotID=0, ImageData=[0]):
        # Raise exception for garbage Input from the client
        if None in ImageData or shotID == None:
            raise ValueError("ShotID or ImageData has None value")
        self.shotID = shotID
        self.ImageData = ImageData  # will be a list of integers

    def copy_to_Image_object(self, Image):
        self.shotID = Image.shotID
        self.ImageData = Image.ImageData

    def fill_ImageData_with_value(self, value):
        for i in range(len(self.ImageData)):
            for j in range(len(self.ImageData[i])):
                self.ImageData[i][j] = value

    def compare_pixel_value_with_value(self, value):
        temp = []
        for i in range(len(self.ImageData)):
            for j in range(len(self.ImageData[i])):
                inner_list = []
                if self.ImageData[i][j] == value:
                    inner_list.append(self.EQUAL)
                elif self.ImageData[i][j] > value:
                    inner_list.append(self.GREATER)
                elif self.ImageData[i][j] < value:
                    inner_list.append(self.LESS)
            temp.append(inner_list)
        return temp

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.shotID == other.shotID and self.ImageData == other.ImageData
        return False


class ImageHandler:

    dict = {}
    sorted_list = []
    # we will keep appending the images to the ImageHandler

    def append_Image(self, Image):
        self.dict[Image.shotID] = Image.ImageData

    def get_shot_by_shotID(self, shotID):
        return self.dict[shotID]

    def remove_image_by_shotID(self, shotID):
        del self.dict[shotID]

    def sort_image_by_shotID(self):
        list = []
        for key in sorted(self.dict.keys()):
            list.append(
                (key, self.dict[key])
            )  # append key value pair(shotID,ImageData)
        self.sorted_list = list
        # Can use this prints for understanding the sorting
        # print(list)
        # print(len(list))
        # print(list[1][0])
        return self.sorted_list

    def substract_background_from_images(self, shotID, noise_threshold):
        # calling background substraction algorithm on the list of image values
        # for this example lets consider it is based on some noise_threshold
        temp = self.dict[shotID]
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if temp[i][j] <= noise_threshold:
                    temp[i][j] = 0
        self.dict[shotID] = temp
        return self.dict[shotID]

    def list_of_shotID(self):
        return sorted(self.dict.keys())


# creating helper functions
def create_random_imageData(dimension):
    imagedata = []
    for i in range(0, dimension):
        temp = []
        for j in range(0, dimension):
            temp.append(random.randint(10, 200))
        imagedata.append(temp)
    return imagedata


def create_constant_imageData(dimension, constant):
    imagedata = []
    for i in range(0, dimension):
        temp = []
        for j in range(0, dimension):
            temp.append(constant)
        imagedata.append(temp)
    return imagedata


def print_image_data(Image):
    for i in range(len(Image.ImageData)):
        print(Image.ImageData[i])


# I was using this for testing purpose ..
# You can look at the unit test for better understanding of the code
# if __name__ == "__main__":
#     imagedata = create_random_imageData(10)
#     # image = Image(None,[None]) for value exception
#     image = Image(2, imagedata)
#     # print_image_data(image) # Image creation output
#     image2 = Image()
#     image2.copy_to_Image_object(image)
#     # print_image_data(image2) # Copying of image verification

#     print(image == image2)
#     imageHandler = ImageHandler()
#     # Create a imagedata with pixel values as 100 and shotID 50
#     imagedata = create_constant_imageData(512, 100)
#     image = Image(50, imagedata)
#     imageHandler.append_Image(image)
#     # Create a imagedata with pixel values as 70 and shotID 10
#     imagedata = create_constant_imageData(512, 70)
#     image = Image(10, imagedata)
#     imageHandler.append_Image(image)
#     # Create a imagedata with pixel values as 15 and shotID 20
#     imagedata = create_constant_imageData(512, 20)
#     image = Image(20, imagedata)
#     imageHandler.append_Image(image)

#     # 2 Verify substraction of the
#     # Create a imagedata with pixel values as 7 and shotID 120
#     imagedata = create_constant_imageData(512, 7)
#     image = Image(120, imagedata)

#     imageHandler.append_Image(image)

#     imageHandler.substract_background_from_images(120, 7)

#     # print(imageHandler.sort_image_by_shotID())

# 1 Image creation test
def test_if_image_is_create():
    imagedata = create_constant_imageData(512, 100)
    image = Image(1, imagedata)
    assert image.ImageData == imagedata


# 2 Image copy test
def test_if_image_copy_works():
    imagedata = create_random_imageData(10)
    image = Image(1, imagedata)
    image2 = Image()
    image2.copy_to_Image_object(image)

    assert image2.ImageData == image.ImageData


# 3 Setting pixel values
# @pytest.mark.parametrize("pixel_value", "10",)
def test_setting_pixel():
    pixel_value = 20  # you can change this value to check for different value if pytest parameterized does not work
    imagedata = create_random_imageData(512)
    image = Image(1, imagedata)
    print_image_data(image)
    image.fill_ImageData_with_value(pixel_value)

    compare = image.compare_pixel_value_with_value(pixel_value)

    for i in range(len(compare)):
        for j in range(len(compare[i])):
            if compare[i][j] != 1:  # 1 for equal
                assert False

    assert True


# 4 for value comparison
def test_value_comparison():
    pixel_value = 20  # you can change this value to check for different value if pytest parameterized does not work
    imagedata = create_random_imageData(512)
    image = Image(1, imagedata)
    print_image_data(image)
    image.fill_ImageData_with_value(pixel_value)

    compare = image.compare_pixel_value_with_value(pixel_value + 10)

    for i in range(len(compare)):
        for j in range(len(compare[i])):
            if compare[i][j] != 2:  # 2 for less
                assert False

    assert True


# 5 for resilient to garbage input from clients
def test_for_invalid_value():
    with pytest.raises(ValueError) as exc:
        image = Image(None, [None])
    assert "ShotID or ImageData has None value" == str(exc.value)


# Unit test for ImageHandler

# 1 test if image handler has stored shotID of 50,10,15 with dimension (512,512) and value 100,70,20, respectively


def test_imageHandler_store():
    shotID = [50, 10, 20]
    imageHandler = ImageHandler()
    # Create a imagedata with pixel values as 100 and shotID 50
    imagedata = create_constant_imageData(512, 100)
    image = Image(shotID[0], imagedata)
    imageHandler.append_Image(image)
    # Create a imagedata with pixel values as 70 and shotID 10
    imagedata = create_constant_imageData(512, 70)
    image = Image(shotID[1], imagedata)
    imageHandler.append_Image(image)
    # Create a imagedata with pixel values as 15 and shotID 20
    imagedata = create_constant_imageData(512, 20)
    image = Image(shotID[2], imagedata)
    imageHandler.append_Image(image)

    assert sorted(imageHandler.dict.keys()) == sorted(shotID)
    # we need to sort because order does not matter in dictionary


# 2 test background subsrtaction with pixel value 7
def test_background_substraction():
    imageHandler = ImageHandler()
    # Create a imagedata with pixel values as 7 and shotID 120
    imagedata = create_constant_imageData(512, 7)
    image = Image(120, imagedata)

    imageHandler.append_Image(image)
    # def substract_background_from_images(self,shotID,noise_threshold):
    image_data = imageHandler.substract_background_from_images(120, 7)
    # so the image_data should be all Zero
    for i in range(len(image_data)):
        for j in range(len(image_data[0])):
            if image_data[i][j] != 0:
                assert False

    assert True


# 3 test sorting of all Image IDs
def test_sorting_all_images_by_shotID():
    shotID = [50, 10, 20, 120]
    imageHandler = ImageHandler()
    # Create a imagedata with pixel values as 100 and shotID 50
    imagedata = create_constant_imageData(10, 100)
    image = Image(shotID[0], imagedata)
    imageHandler.append_Image(image)
    # Create a imagedata with pixel values as 70 and shotID 10
    imagedata = create_constant_imageData(10, 70)
    image = Image(shotID[1], imagedata)
    imageHandler.append_Image(image)
    # Create a imagedata with pixel values as 15 and shotID 20
    imagedata = create_constant_imageData(10, 20)
    image = Image(shotID[2], imagedata)
    imageHandler.append_Image(image)
    # Create a imagedata with pixel values as 7 and shotID 120
    imagedata = create_constant_imageData(10, 7)
    image = Image(shotID[3], imagedata)
    imageHandler.append_Image(image)

    imageHandler.sort_image_by_shotID()

    shotID = sorted(shotID)  # sorting the shotID
    j = 0
    for i in range(len(imageHandler.sorted_list)):
        if imageHandler.sorted_list[i][0] == shotID[j]:
            j += 1
        else:
            assert False
    assert True