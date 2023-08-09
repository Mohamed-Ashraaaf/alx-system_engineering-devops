# Puppet manifest to troubleshoot and fix Apache 500 error using strace

exec { 'strace_apache':
  command     => 'strace -o /tmp/strace_output.txt -f -s 200 -p $(pgrep apache2)',
  path        => ['/usr/bin', '/bin'],
  refreshonly => true,
}

exec { 'fix_apache_issue':
  command     => 'fix_command_here',
  path        => ['/usr/bin', '/bin'],
  refreshonly => true,
  subscribe   => Exec['strace_apache'],
  onlyif      => "test -f /tmp/strace_output.txt",
}

service { 'apache2':
  ensure    => 'running',
  enable    => true,
  subscribe => Exec['fix_apache_issue'],
}
