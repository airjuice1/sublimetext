import sublime
import sublime_plugin
import os
import re

class SimpleLaravelAutoCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		project_path = sublime.active_window().folders()[0]
		app_path = os.path.join(project_path, "app")
		dba_path = os.path.join(project_path, "database")

		self.classes = dict(self.read_path(app_path, project_path))
		self.classes.update(self.read_path(dba_path, project_path))

		# for code_string in classes:
			# self.view.insert(edit, 0, code_string + "\n")

	def read_path(object, path, project_path):
		except_files = ['.gitignore', 'database.sqlite']
		result = dict()
		for root, dirs, files in os.walk(path):
			for file in files:

				# print(file)

				if file in except_files:
					continue

				file_path = os.path.join(project_path, root, file)
				with open(file_path, encoding='utf-8') as f:
					code = object.namespaces(f.read())
					if code:
						result.update([(code[1], code[1])])
		return result

	def namespaces(object, text):
		patten_namespace = r'namespace\s+(.*?);'
		patten_class = r'class\s+(.*?)\s+extends'
		matches_namespace = re.findall(patten_namespace, text)
		matches_class = re.findall(patten_class, text)
		if matches_namespace and matches_class:
			return [matches_class[0], matches_namespace[0] + '\\' + matches_class[0]]

	def input(self, args):
		return EntityInputHandler(self.classes)

class EntityInputHandler(sublime_plugin.ListInputHandler):
	def __init__(self, classes):
		self.classes = classes

	def list_items(self):
		return sorted(self.classes.keys())

	def confirm(self, value):
		print(self.window.active_view())
		new_view = self.window.new_file()
		# new_view.set_name("App Files Content")
		# new_view.insert(sublime.Edit(new_view), 0, value)
		sublime.set_clipboard(value)

	# def preview(self, value):
		# return "Character: {}".format(self.classes.get(value))
		# return "Character: {}".format(html5.get(value))