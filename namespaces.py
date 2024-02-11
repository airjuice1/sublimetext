import sublime
import sublime_plugin

class NamespacesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		namespace = self.view.substr(self.view.find("namespace.*", 0))
		classname = self.view.substr(self.view.find("class.*", 0)).split()
		# use		  = self.view.substr(self.view.find("use.*", 0))

		if namespace:
			namespace = namespace.replace("namespace", "use").replace(";", "")
			try:
				classname = classname[1]
			except:
				classname = ""
				print("classname not found")

			if bool(classname):
				namespace = namespace + "\\" + classname + ";"
			else:
				namespace = namespace + ";"

			sublime.set_clipboard(namespace)

		print(namespace)

		#self.view.insert(edit, 0, "Hello, World!")