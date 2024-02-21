from method import Method

from utils.void_capture import get_screenshot_of_window
from utils.image_uploader import get_folder_id, upload_file

VOID_STRANGER_RESOLUTION = (224, 144)
def resize_void_stranger_to_native(file_path: str, output_path = "out.png"):
	"""Makes a screenshot of void stranger into its native resolution.
	Requires the image to be linearly scaled"""
	from PIL import Image
	
	image = Image.open(file_path)

	assert (image.width % VOID_STRANGER_RESOLUTION[0], image.height % VOID_STRANGER_RESOLUTION[1]) == (0, 0)
	image = image.resize(VOID_STRANGER_RESOLUTION, Image.NEAREST)

	image.save(output_path)

TEMP_FILE_NAME = "./temp/void.png"
TEMP_SMALL_FILE_NAME = "./temp/void_small.png"

class ScreenShot(Method):
	@property
	def name(self):
		return "ScreenShot"
	
	def Preform_Method(self, name: str, description: str, method: str, *args, **kwargs) -> str:
		screenshot_type = args[0]

		if screenshot_type != "Void Stranger": raise NotImplementedError("No screenshots other than void stranger")

		# TODO: Maybe remove the files after the file is uploaded
		res = get_screenshot_of_window("Void Stranger", TEMP_FILE_NAME)
		if not res: raise RuntimeError("Cannot Take a picture of Void Stranger")
		resize_void_stranger_to_native(TEMP_FILE_NAME, TEMP_SMALL_FILE_NAME)
		
		folder_id = get_folder_id("Void_SpreadSheet_Images")
		file_id = upload_file(TEMP_SMALL_FILE_NAME, folder_id)
		image_string = f'=image("https://drive.google.com/uc?export=view&id={file_id}")'

		return image_string
