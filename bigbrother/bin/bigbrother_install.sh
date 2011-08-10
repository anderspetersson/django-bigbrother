#!/bin/bash
echo 'Please enter URL to your project. For example: http://www.yoururl.com'
read URL

(crontab -l; echo "59   23  *    *   * wget $URL/bigbrother/update/") | crontab
echo "Installed cronjob: 59   23  *    *   * wget $URL/bigbrother/update/"