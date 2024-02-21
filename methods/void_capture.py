# program to get a screenshot of void stranger so i can put it all in as spreadsheet for some AUTO-HOTKEY GAMING


# Bad Way of doing this
def get_window_names():
	import gi
	gi.require_version('Gtk', '3.0')
	gi.require_version('Wnck', '3.0')
	from gi.repository import Gtk, Wnck

	Gtk.init([])  # necessary only if not using a Gtk.main() loop
	screen = Wnck.Screen.get_default()
	screen.force_update()  # recommended per Wnck documentation

	# loop all windows
	windows: list[str] = [window.get_name() for window in screen.get_windows()]

	# clean up Wnck (saves resources, check documentation)
	window = None
	screen = None
	Wnck.shutdown()

	return windows
def get_screenshot_of_window(name: str, output = "out.png"):
	import gi
	gi.require_version('Gtk', '3.0')
	gi.require_version('Wnck', '3.0')
	gi.require_version('Gdk', '3.0')
	from gi.repository import Gtk, Wnck, Gdk

	Gtk.init([])  # necessary only if not using a Gtk.main() loop
	screen = Wnck.Screen.get_default()
	screen.force_update()  # recommended per Wnck documentation

	# loop all windows
	found_window = False
	for window in screen.get_windows():
		if window.get_name() == name:
			gdk_window = Gdk.get_default_root_window()
			pb = Gdk.pixbuf_get_from_window(gdk_window, *window.get_geometry())
			pb.savev(output, "png", (), ())
			found_window = True
			break

	# clean up Wnck (saves resources, check documentation)
	window = None
	screen = None
	Wnck.shutdown()

	return found_window


if __name__ == "__main__":
	found = get_screenshot_of_window("Void Stranger", "void.png")
	if not found:
		print("Could Not Find Window")
	# get_screenshot_of_void_stranger("void.png")