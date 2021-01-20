"""
@author: crisp
@date: 20210119
@describe: to extract words from picture using baidu-api
"""

import os
import easyocr
from pprint import pprint

IMAGES_DIR_PATH = "./images"
RESULT_DIR_PATH = "./results"
TEXT_FILE_APPEND = ".txt"


class WordsExtract(object):
    """
    Used to extract words from images
    """

    def __init__(self, wrap: bool = True):
        """
        :param wrap: default True, no os.linesep behind the line if wrap is False
        """
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.wrap = wrap

    def read_text(self,file_path: str):
        """
        read image and return text extracted from image
        :param file_path:
        :return: list[text1,text2,...]
        """
        return self.reader.readtext(file_path, detail=0)

    def write_text(self, file_name: str, result_list: list):
        """
        write text into file
        :param file_name: file's name
        :param result_list: list of text result
        :return:
        """
        if not os.path.exists(RESULT_DIR_PATH):
            os.mkdir(RESULT_DIR_PATH)
        result_list = filter(lambda res: res.strip() != "" and res.strip() != os.linesep, result_list)
        file_path = RESULT_DIR_PATH+ os.sep + file_name+TEXT_FILE_APPEND
        line_sep = os.linesep if self.wrap else ""
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "a", encoding="utf-8") as f:
            for res in result_list:
                f.write(res+line_sep)

    def run(self,img_dir_path:str = IMAGES_DIR_PATH):
        """
        start read image and write into file
        :param img_dir_path: path of images directory
        :return:
        """
        for maindir,subdir,file_name_list in os.walk(img_dir_path):
            for file_name in file_name_list:
                # join into a full path
                file_path = os.path.join(maindir, file_name)
                file_name = file_name.split(".")[0] if "." in file_name else file_name
                # read text from image
                result_list = self.read_text(file_path)
                # write text into file
                self.write_text(file_name, result_list)
                print(f"Read {file_name} successfully.")


if __name__ == '__main__':
    # reader = easyocr.Reader(['ch_sim','en']) # need to run only once to load model into memory
    # result = reader.readtext('./images/2.png',detail=1)
    # pprint(result)
    extractor = WordsExtract()
    extractor.run()