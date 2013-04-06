A simple unintrusive django db field for html content, with wysiwyg
editing in django admin that does not take over all of the admin or
makes all other fields wysiwyg editable.

Use like any TextField in your models, but pass through the safe
filter in templates like this: {{ somemodel.somefield|safe }}
