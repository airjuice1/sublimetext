<?php
/*
0 - delete empty snippets
1 - create snippet file;
*/

function createSnippet($name, $template)
{
	file_put_contents($name, $template);
}

$template = <<<EOT
<snippet>
	<content><![CDATA[
Hello
]]></content>
	<!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
	<!-- <tabTrigger>hello</tabTrigger> -->
	<!-- Optional: Set a scope to limit where the snippet will trigger -->
	<!-- <scope>source.python</scope> -->
</snippet>
EOT;

$dir = getcwd() . DIRECTORY_SEPARATOR . 'snippets';
$ext = '.sublime-snippet';
$cmd = $argv[1] ?? null;
$prm = $argv[2] ?? null;
$rng = $argv[3] ?? 1;
$msg = "\n\n\n\n\n\nWrong parametrs\n\n\n\n\n\n";
$spc = "\n\n\n\n\n\n\n\n\n\n\n\n";
$options = [
	'laravel',
	'php',
	'js',
	'react',
	'mysql',
	'git',
];
$snippet_number = 1;

(is_dir($dir)) || mkdir($dir);

echo $spc;
echo "==================\n";
echo "Create snippet for\n";
foreach ($options as $key => $value) echo $key + 1 . " " . $value . "\n";
echo "==================\n";
echo "example\n";
echo "php .\index.php 1 1 - create 1 snippet for laravel with max number in over filename\n";
echo "php .\index.php 6 1 - create 1 snippet for git with max number in over filename\n";
echo "php .\index.php 1 1 10 - create 10 snippets for laravel start from max number in over filename\n";
echo "==================\n";

!($cmd < 0 || $cmd > 1) || exit($msg);

switch ($cmd)
{
	case 0:

		$files = array_filter(scandir($dir), fn ($i) => strpos($i, $ext));

		foreach ($files as $key => $value) 
		{
			$fullpath = $dir . DIRECTORY_SEPARATOR . $value;

			if (crc32($template) == crc32(file_get_contents($fullpath)))
			{
				unlink($fullpath);
				echo "File " . $fullpath . " deleted\n";
			}
		}
		
	break;

	case 1:

		!($cmd == 1 && $prm > count($options) || $prm <= 0 || $rng > 10) || exit($msg);

		for ($i = 0; $i < $rng ; $i++) 
		{
			$files = array_values(array_map(fn ($i) => (int) filter_var(explode('.', $i)[0], FILTER_SANITIZE_NUMBER_INT)
				, array_filter(array_filter(scandir($dir), fn ($i) => strpos($i, $ext)), fn ($i) => strpos($i, $options[$prm-1])!== false)));

			if ($files) $snippet_number = max($files) + 1;

			$name = $dir . DIRECTORY_SEPARATOR . $options[$prm-1] . $snippet_number . $ext;
			createSnippet($name, $template);
			echo "File " . $name . " created\n";
		}

		
	break;
	
	default:
	break;
}