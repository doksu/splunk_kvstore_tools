# splunk_kvstore_tools

The kvstore_migration.py script is designed to automatically migrate all the contents of all a Splunk server's KV Store Collections to another server. This is useful when migrating to a new search head, especially in complex cases such as migrating an existing Enterprise Security deployment into a SHC. The script is currently rudimentary and so variables are hardcoded for the time being. Please change the variables at the top of the script before usage, where those starting with 's' are for the source server, and those starting with 'd' are for the destination server.
