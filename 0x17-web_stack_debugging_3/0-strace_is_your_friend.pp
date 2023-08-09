# Puppet manifest to troubleshoot and fix Apache 500 error using strace
exec {'replace':
  provider => shell,
  command  => 'sed -i "s/phpp/php/g" /var/www/html/wp-settings.php'
}
