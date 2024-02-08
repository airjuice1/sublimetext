<?php
[$scriptName, $projectName, $mode] = $argv + array_fill(0, 3, null);

$homeDrive = getenv('HOMEDRIVE');
$webappsDir = $homeDrive  . getenv('HOMEPATH') . DIRECTORY_SEPARATOR . 'Documents' . DIRECTORY_SEPARATOR . 'webapps';
$workspacesDir = $homeDrive  . DIRECTORY_SEPARATOR . getenv('HOMEPATH') . DIRECTORY_SEPARATOR . 'Documents' . DIRECTORY_SEPARATOR . 'workspaces';
$extProject = '.sublime-project';
$extWorkspace = '.sublime-workspace';
$projectPath = str_replace('\\', '\\\\', $webappsDir. '\\' . $projectName);

$template1 = <<<EOT
{
	"folders":
	[
		{
			"path": "{$projectPath}"
		},
	],
}
EOT;

function rrmdir($dir) { 
   if (is_dir($dir)) { 
     $objects = scandir($dir);
     foreach ($objects as $object) { 
       if ($object != "." && $object != "..") { 
         if (is_dir($dir. DIRECTORY_SEPARATOR .$object) && !is_link($dir."/".$object))
           rrmdir($dir. DIRECTORY_SEPARATOR .$object);
         else
           unlink($dir. DIRECTORY_SEPARATOR .$object); 
       } 
     }
     rmdir($dir); 
   } 
 }

$help = <<<HEREDOC
====================
php {$scriptName} <project name> <mode>
mode 1 - create project files without webapps directory
mode 2 - delete sublime project files
mode 3 - erease all project files
====================
HEREDOC;

echo $help;

switch ($mode) 
{
	case 1:
		file_put_contents($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extProject, $template1);
	break;

	case 2:
		unlink($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extProject);
		unlink($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extWorkspace);
	break;

	case 3:
		exec("taskkill /IM \"sublime_text.exe\" /F");
		exec("timeout /t 5 /nobreak");
		rrmdir($webappsDir . DIRECTORY_SEPARATOR . $projectName);
		unlink($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extProject);
		unlink($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extWorkspace);
	break;
	
	default:
		mkdir($webappsDir . DIRECTORY_SEPARATOR . $projectName);
		file_put_contents($workspacesDir . DIRECTORY_SEPARATOR . $projectName . $extProject, $template1);
	break;
}
