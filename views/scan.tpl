% rebase('master.tpl', title='Scan document')

<h1>Scanner</h1>

<form action="/scan" method="POST">
	<p>When you press scan the page may take some time to load</p>

	<label for="ppi">PPI:</label>
	<select name="ppi">
		<option value="75">75 ppi</option>
		<option value="100">100 ppi</option>
		<option value="300" selected>300 ppi</option>
		<option value="600">600 ppi</option>
	</select>

	<label for="mode">Mode:</label>
	<select name="mode">
		<option value="Gray">Gray</option>
		<option value="Color">Color</option>
	</select>

	<input type="submit" value="Scan" />
</form>