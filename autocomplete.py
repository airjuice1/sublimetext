import sublime
import sublime_plugin
import os
import re

def _read_files(pathes, project_path):
	except_files = ['.gitignore', 'database.sqlite']
	result = [[],[]]
	for path in pathes:
		for root, dirs, files in os.walk(path):
			for file in files:

				if file in except_files:
					continue

				if not file.endswith('.php'):
					continue

				file_path = os.path.join(project_path, root, file)
				with open(file_path, encoding='utf-8') as f:
					code = _extract_class(f.read())
					if code:
						result[0].append(code[0])
						result[1].append(code[1])
						# result[1].append(file_path)
	return result

def _extract_class(text):
	patten_namespace = r'namespace\s+(.*?);'
	patten_class = r'class\s+(.*?)\s+extends'
	matches_namespace = re.findall(patten_namespace, text)
	matches_class = re.findall(patten_class, text)
	if matches_namespace and matches_class:
		return [matches_namespace[0] + '\\' + matches_class[0], matches_class[0]]

def _find_postion_in_text(text):

	result = False

	pattern = r';([^;]*?)\s*(?:class|Route)'
	matches = re.search(pattern, text)

	if matches:
		result = matches.start()

	return result

def _check_class(text, class_name):
	if text.find(class_name) == -1:
		return False
	return True

class DefaultLaravelClassesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.namespaces = []
		self.classes = []

		file_contained_namespaces = os.path.join(sublime.packages_path(), 'User', 'laravelnamespaces.txt')
		file_contained_class_names = os.path.join(sublime.packages_path(), 'User', 'laravelclasses.txt')

		if not os.path.isfile(file_contained_namespaces) or not os.path.isfile(file_contained_class_names):
			print('file not found')
			return
		
		with open(file_contained_namespaces, 'r') as f:
			lines = f.readlines()
		for l in lines:
			self.namespaces.append(l)

		with open(file_contained_class_names, 'r') as f:
			lines = f.readlines()
		for l in lines:
			self.classes.append(l)

		self.view.window().show_quick_panel(self.namespaces, self.on_done)

	def on_done(self, index):
		if index == -1:
			return

		text = self.view.substr(sublime.Region(0, self.view.size()))

		position = _find_postion_in_text(text)
		selected_item = 'use ' + self.namespaces[index].strip() + ';\n'
		selected_class = self.classes[index]

		if position:
			if not _check_class(text, 'use ' + self.namespaces[index].strip() + ';'):
				self.view.run_command("insert_text_at_position", {"position": position + 2, "text": selected_item})
			self.view.run_command("insert_snippet", {"contents": selected_class})
		else:
			print('class not found')



class MakeLaravelClassesFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		prj_path = sublime.active_window().folders()[0]
		ven_path = os.path.join(prj_path, "vendor\\laravel\\framework\\src\\Illuminate")
		self.elements = _read_files([ven_path], prj_path)

		file_contained_namespaces = os.path.join(sublime.packages_path(), 'User', 'laravelnamespaces.txt')
		file_contained_class_names = os.path.join(sublime.packages_path(), 'User', 'laravelclasses.txt')

		fcn = open(file_contained_namespaces, 'a')
		fcn.truncate(0)
		fccn = open(file_contained_class_names, 'a')
		fccn.truncate(0)

		for namespace in self.elements[0]:
			fcn.write(namespace + "\n")
		for class_name in self.elements[1]:
			fccn.write(class_name + "\n")

class InsertTextAtPositionCommand(sublime_plugin.TextCommand):
	def run(self, edit, position, text):
		self.view.insert(edit, position, text)

class SimpleLaravelAutoCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		prj_path = sublime.active_window().folders()[0]
		app_path = os.path.join(prj_path, "app")
		dba_path = os.path.join(prj_path, "database")

		self.elements = _read_files([app_path, dba_path], prj_path)
		self.view.window().show_quick_panel(self.elements[0], self.on_done)

	def on_done(self, index):
		if index == -1:
			return

		text = self.view.substr(sublime.Region(0, self.view.size()))

		position = _find_postion_in_text(text)
		selected_item = 'use ' + self.elements[0][index] + ';\n'
		selected_class = self.elements[1][index]
		# sublime.set_clipboard('use ' + selected_item + ';\n')


		if position:
			if not _check_class(text, 'use ' + self.elements[0][index] + ';'):
				self.view.run_command("insert_text_at_position", {"position": position + 2, "text": selected_item})
			self.view.run_command("insert_snippet", {"contents": selected_class})
		else:
			print('class not found')