OpenREM Release Notes version 0.4.0
***********************************

Headline changes
================================


Specific upgrade instructions
=============================

..      Warning::
        
        This release requires a database migration (instructions below). This requires a choice to be made 
        to allow for backwards migrations at a later date. Please consult the details below.

When South has considered the changes to the schema, you will see the following message::
    
 ? The field 'Observer_context.device_observer_name' does not have a default specified, yet is NOT NULL.
 ? Since you are making this field nullable, you MUST specify a default
 ? value to use for existing rows. Would you like to:
 ?  1. Quit now.
 ?  2. Specify a one-off value to use for existing columns now
 ?  3. Disable the backwards migration by raising an exception; you can edit the migration to fix it later
 ? Please select a choice: 3

As per the final line above, the correct choice is ``3``. The fields that are now
nullable previously weren't. Existing data in those fields will have a value, or those
tables don't exist in the current database. The problem scenario is if after
the migration these tables are used and one of the new nullable fields is left as null,
you will not be able to migrate back to the old database schema without error.
This is not something that you will want to do, so the is ok.
