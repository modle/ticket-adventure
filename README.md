# Execution
```
git clone git@git.ent.tds.net:usrodt/tickets-adventure.git
cd tickets-adventure
python3 main.py
```

# Save File
A file `tickets.json` will be created at the project root. This is the poor man's datastore.

# Commands
These commands can be entered at the prompt `Choose your path: `

<dl>
    <dt><code>0</code></dt>
    <dd>Exit the application.</dd>
    <br>
    <dt><code>1</code></dt>
    <dd>The magic command. 1 will list all ACTIVE tickets by default.
    <ul>
        <li>The 1 command will take options, such as [open, closed, blocked, contains somestring, anystring]</li>
        <li>More on ticket filtering below</li>
    </ul>
    </dd>
    <br>
    <dt><code>2</code></dt>
    <dd>Add a new ticket. At any point during the add ticket script, type <code>cancel</code> to exit add ticket mode without saving the new ticket</dd>
    <br>
    <dt><code>3</code></dt>
    <dd>Print a ticket summary</dd>
    <br>
    <dt><code>!12345</code></dt>
    <dd>(where 12345 is the value in the id field). Enter Ticket Details Mode (TDM, because ACRONYMS YEA!).
        <br>
        This opens up additional commands and changes existing command behavior.</dd>
    <br>
    <dt><code>status</code> or <code>s</code></dt>
    <dd>Show a list of preset statuses. In TDM, print the current ticket's status</dd>
    <br>
    <dt><code>info</code> or <code>i</code></dt>
    <dd>In TDM, print ticket details</dd>
    <br>
    <dt><code>fields</code></dt>
    <dd>Shows a list of available fields</dd>
    <br>
    <dt><code>edit</code></dt>
    <dd>In TDM, show a list of editable fields, with optional field name or id.
        <ul>
            <li>If a nonexistent option is supplied, <code>edit</code> will not execute.</li>
            <li>If no option is supplied, the user will be prompted for a field number or name.</li>
            <li>If a valid field number or name is supplied, vim will open.</li>
        </ul>
        Exiting vim will prompt the user to confirm the field value change.
        <ul>
            <li>Certain fields will be appendable, while others will simply be overwritten.</li>
            <li>Appendable fields will be timestamped.</li>
            <li>Most field changes will be noted in the notes field.</li>
        </ul>
    </dd>
    <br>
    <dt><code>fieldname</code></dt>
    <dd>
        Enter a field name to see the value of the field for the current ticket in TDM
        <br>
        Certain fields can be edited using the field name command by supplying an option.
        <br>
        For example, with <code>notes</code>, which is an appendable field: <code>notes a new note</code> will append <code>timestamp: a new note</code> to the notes entry
        <br>
        Another example, with <code>category</code>, which is NOT an appendable field: <code>category a category</code> will set the value of <code>category</code> to <code>a category</code>
    </dd>
    <br>
    <dt><code>properties</code> or <code>prop</code> or <code>links</code></dt>
    <dd>This will print everything in the application.properties file.
        <br>
        This is helpful for having quick access to links
    </dd>
</dl>

# Ticket Filtering
<dl>
    <dt>The option `contains` can be applied to the the `1` command to string match against the status of a ticket.</dt>
    <dd>For example, if a ticket has the status `pending: investigate` the command `1 contains invest` can be used to show all tickets with a status containing `invest`.</dd>
    <br>
    <dt>The `1` command can also be used to filter all tickets by matching the entered option against the beginning of the string.</dt>
    <dd>For example, the command `1 priority` will show all tickets with a status which begins with `priority`</dd>
</dl>
