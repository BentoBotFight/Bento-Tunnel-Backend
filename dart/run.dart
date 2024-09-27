import 'dart:io';

Future<void> main() async {
  ProcessResult result = await Process.run('ls', ['-l']);
  print(result.stdout);
  print('Exit code: ${result.exitCode}');
}