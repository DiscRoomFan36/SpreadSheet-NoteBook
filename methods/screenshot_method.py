from method import Method

from void_capture import get_screenshot_of_window
import image_uploader_test
from image_test import resize_void_stranger_to_native

TEMP_FILE_NAME = "./temp/void.png"
TEMP_SMALL_FILE_NAME = "./temp/void_small.png"

class ScreenShot(Method):

	@property
	def name(self):
		return "ScreenShot"
	
	
	@staticmethod
	def Preform_Method() -> str:

		# TODO: check if the user whats a screenshot of void stranger
		void_stranger = True
		if not void_stranger: raise NotImplementedError("No screenshots other than void stranger")

		# TODO: Maybe remove the files after the file is uploaded
		res = get_screenshot_of_window("Void Stranger", TEMP_FILE_NAME)
		if not res: raise RuntimeError("Cannot Take a picture of Void Stranger")

		resize_void_stranger_to_native(TEMP_FILE_NAME, TEMP_SMALL_FILE_NAME)
		
		folder_id = image_uploader_test.get_folder_id("Void_SpreadSheet_Images")

		file_id = image_uploader_test.upload_file(TEMP_SMALL_FILE_NAME, folder_id)

		image_string = f'=image("https://drive.google.com/uc?export=view&id={file_id}")'

		return image_string
