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

				file_path = os.path.join(project_path, root, file)
				with open(file_path, encoding='utf-8') as f:
					code = _extract_class(f.read())
					if code:
						result[0].append(code[0])
						result[1].append(code[1])
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
			self.view.run_command("insert_classname_at_position", {"text": selected_class})
			self.view.run_command("insert_text_at_position", {"position": position + 2, "text": selected_item})
		else:
			print('class not found')