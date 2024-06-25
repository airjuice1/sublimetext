import sublime
import sublime_plugin
import os
import re
import json

class SimpleLaravelAutoCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		project_path = sublime.active_window().folders()[0]
		app_path = os.path.join(project_path, "app")
		dba_path = os.path.join(project_path, "database")

		self.classes = self.read_path(dba_path, project_path) + self.read_path(app_path, project_path)

		# for code_string in classes:
			# self.view.insert(edit, 0, code_string + "\n")

	def read_path(object, path, project_path):
		except_files = ['.gitignore', 'database.sqlite']
		result = []
		for root, dirs, files in os.walk(path):
			for file in files:

				print(file)

				if file in except_files:
					continue

				file_path = os.path.join(project_path, root, file)
				with open(file_path, encoding='utf-8') as f:
					code = object.namespaces(f.read())
					if code:
						result.append(code)
		return result

	def namespaces(object, text):
		result = {}
		patten_namespace = r'namespace\s+(.*?);'
		patten_class = r'class\s+(.*?)\s+extends'
		matches_namespace = re.findall(patten_namespace, text)
		matches_class = re.findall(patten_class, text)
		if matches_namespace and matches_class:
			result[matches_class[0]] = matches_namespace[0] + '\\' + matches_class[0]
			return json.dumps(result)

	def input(self, args):
		return EntityInputHandler(self.classes)

class EntityInputHandler(sublime_plugin.ListInputHandler):
	def __init__(self, classes):
		self.classes = classes

	def list_items(self):
		print(sorted(self.classes))
		return sorted(self.classes)


	def preview(self, value):
		# return "Character: {}".format(self.classes.get(value))
		return