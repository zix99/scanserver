% rebase('master.tpl', title='Scan document')

<h1>Scanner</h1>

<form action="/scan" method="POST">
	<p>When you press scan the page may take some time to load</p>

	<label for="ppi">PPI:</label>
	<select name="ppi">
		<option value="75">75 ppi</option>
		<option value="100">100 ppi</option>
		<option value="150">150 ppi</option>
		<option value="300" selected>300 ppi</option>
		<option value="600">600 ppi</option>
	</select>

	<label for="mode">Mode:</label>
	<select name="mode">
		<option value="Gray">Gray</option>
		<option value="Color" selected>Color</option>
	</select>

	<input type="submit" value="Scan" />
</form>

% if defined('err'):
<pre style="color: red">
{{err}}
</pre>
% end

<h2>Images</h2>
<a href="/pdf">Create PDF</a> | <a href="/deleteall" onclick="return confirm('Are you sure you wish to delete ALL files??? There is no undo!')"">Delete all</a><br />
<table border="1" cellpadding="4" cellspacing="0">
	<tr>
		<th>Name</th>
		<th>Size</th>
		<th>Date</th>
		<th>Actions</th>
	</tr>
	% for f in files:
	<tr>
		<td><a href="/scans/{{f['name']}}">{{f['name']}}</a></td>
		<td>{{f['size']/1024}} KB</td>
		<td>{{f['ts']}}</td>
		<td><a href="/scans/{{f['name']}}/delete" onclick="return confirm('Are you sure you wish to delete {{f['name']}}?')">Delete</a></td>
	</tr>
	% end
</table>

% if defined('image'):
	<h3>Scan</h3>
	<img src="/scans/{{image}}" />
% end