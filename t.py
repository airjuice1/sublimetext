import os

app_path = os.path.join(os.path.expanduser('~'), "Documents", "webapps", "app1", "app")
# cfg_path = os.path.join(os.path.expanduser('~'), "Documents", "webapps", "app1", "config")
dba_path = os.path.join(os.path.expanduser('~'), "Documents", "webapps", "app1", "database")

for root, dirs, files in os.walk(app_path):
	for name in files:
		if name == '.gitignore':
			break
		file_name = os.path.join(root, name)

		print(open(file_name).read())


# for root, dirs, files in os.walk(cfg_path):
#    print(dirs)

# for root, dirs, files in os.walk(dba_path):
#    print(dirs)