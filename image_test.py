from PIL import Image

VOID_STRANGER_RESOLUTION = (224, 144)
def resize_image_to_native(image):
	assert (image.width % VOID_STRANGER_RESOLUTION[0], image.height % VOID_STRANGER_RESOLUTION[1]) == (0, 0)
	return image.resize(VOID_STRANGER_RESOLUTION, Image.NEAREST)

def resize_void_stranger_to_native(file_path: str, output_path = "out.png"):
	"""Makes a screenshot of void stranger into its native resolution.
	Requires the image to be linearly scaled"""
	image = Image.open(file_path)
	resize_image_to_native(image)
	image.save(output_path)



if __name__ == "__main__":
	resize_void_stranger_to_native("void.png", "void2.png")